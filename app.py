"""kefu-next v1：地铁客服系统第一版——单文件 FastAPI + SQLite + 内嵌聊天页。

组织配置（.claude/skills、.githooks）继承自 sz-mtr-service-agent，流程走 Goal 模式
（docs/goals/v1-launch.md）。
"""

import json
import logging
import os
import sqlite3
import time
from pathlib import Path

import httpx
import jieba
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("kefu-next")

DB_PATH = Path(os.environ.get("KEFU_DB", "data/kefu.db"))
STATIC_DIR = Path(os.environ.get("KEFU_STATIC", "static"))
ZHIPU_KEY = os.environ.get("ZHIPU_API_KEY", "")
ZHIPU_MODEL = os.environ.get("ZHIPU_CHAT_MODEL", "glm-4-flash")
ZHIPU_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

# —— FAQ（继承自 v0 代苏州轨道交通 12 条）——
FAQS = [
    {"q": "首末班车是什么时间？", "a": "各线路首班车一般在 05:40-06:30 之间，末班车在 22:30-23:30 之间，具体以\"苏e行\"App或官网时刻表为准。"},
    {"q": "票价怎么算？", "a": "起步价 2 元可乘 6 公里，之后按里程递增，全程最高 8 元。可使用苏e行App乘车码、单程票或交通卡。"},
    {"q": "丢失物品怎么找回？", "a": "可拨打服务热线 0512-69899000 登记失物，或到任意车站客服中心登记。贵重物品建议同时报警。"},
    {"q": "有哪些无障碍设施和服务？", "a": "车站提供无障碍电梯、无障碍卫生间、盲道，列车与站台间配轮椅渡板。可拨打 0512-69899000 预约爱心接力服务。"},
    {"q": "怎么换乘？", "a": "站内按导向标识换乘即可，换乘不需重新购票，计费按进出站全程计算。换乘通道一般有电梯。"},
    {"q": "有哪些便民服务？", "a": "各站客服中心提供便民雨伞、应急药箱、手机充电、针线包、热水等，部分大站设有母婴室。"},
    {"q": "乘车码怎么用？", "a": "下载\"苏e行\"App注册后生成乘车码，进出站各扫码一次，费用自动扣除。支持支付宝/微信渠道。"},
    {"q": "有什么优惠政策？", "a": "70 周岁以上老人、残疾人、现役军人等按规定免费或优惠乘车，具体携带证件至车站客服中心办理或咨询。"},
    {"q": "哪些物品禁止携带？", "a": "易燃易爆品、管制刀具、超量酒精等禁止携带；充电宝不超过 20000mAh 可携带。详细目录见官网或咨询车站。"},
    {"q": "线路有哪些？", "a": "目前运营 1-8 号线及支线，覆盖园区、新区、古城等主要区域，线网图可下载\"苏e行\"App查看。"},
    {"q": "大客流时会怎样？", "a": "节假日或大型活动期间部分车站会采取限流、封站或越站措施，请留意站内广播与官方公告，预留出行时间。"},
    {"q": "服务热线是多少？", "a": "苏州轨道交通服务热线 0512-69899000，服务时间 06:00-23:00，也可通过\"苏e行\"App在线客服咨询。"},
]
for item in FAQS:
    item["kw"] = set(w for w in jieba.lcut(item["q"] + item["a"]) if len(w) >= 2)

PUNCT = set("，。；：！？、（）\n ")


def match_faq(question: str, top: int = 3) -> list[dict]:
    words = [w for w in jieba.lcut(question) if len(w) >= 2 and w not in PUNCT]
    if not words:
        return []
    scored = []
    for item in FAQS:
        hit = sum(1 for w in words if w in item["kw"])
        if hit:
            scored.append((hit, item))
    scored.sort(key=lambda x: -x[0])
    return [i for _, i in scored[:top]]


# —— 存储 ——
def db() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS chat_log (id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "session_id TEXT NOT NULL, role TEXT NOT NULL, content TEXT NOT NULL, "
        "created_at REAL NOT NULL)"
    )
    return conn


def append_log(session_id: str, role: str, content: str) -> None:
    try:
        with db() as conn:
            conn.execute(
                "INSERT INTO chat_log(session_id, role, content, created_at) VALUES (?,?,?,?)",
                (session_id, role, content, time.time()),
            )
    except Exception as exc:  # noqa: BLE001 落库失败不阻断回答
        logger.warning("chat_log write failed: %s", exc)


# —— LLM ——
async def answer(message: str, refs: list[dict]) -> str:
    if not ZHIPU_KEY:
        raise HTTPException(status_code=502, detail="ZHIPU_API_KEY 未配置")
    if refs:
        context = "\n".join(f"[FAQ{i+1}] {r['q']}\n{r['a']}" for i, r in enumerate(refs))
        system = (
            "你是苏州轨道交通官方客服。仅依据下面的 FAQ 资料回答，"
            "回答末尾标注\"参考来源：官方FAQ《题名》\"：\n" + context
        )
    else:
        system = "你是苏州轨道交通官方客服。未在官方FAQ中找到直接相关内容，回答开头先说明\"未在官方FAQ中找到\"，再基于常识简要回答并建议拨打 0512-69899000。"
    body = {
        "model": ZHIPU_MODEL,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": message}],
        "temperature": 0.3,
        "max_tokens": 500,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(ZHIPU_URL, json=body,
                              headers={"Authorization": f"Bearer {ZHIPU_KEY}"})
    data = r.json()
    if "choices" not in data:
        raise HTTPException(status_code=502, detail=f"LLM 调用失败: {json.dumps(data, ensure_ascii=False)[:200]}")
    return data["choices"][0]["message"]["content"].strip()


# —— API ——
app = FastAPI(title="kefu-next", version="1.0.0")


class ChatIn(BaseModel):
    session_id: str = Field(min_length=1, max_length=64)
    message: str = Field(min_length=1, max_length=2000)


@app.get("/api/health")
def health() -> dict:
    db_ok = DB_PATH.parent.mkdir(parents=True, exist_ok=True) is None
    try:
        with db() as conn:
            conn.execute("SELECT 1 FROM chat_log LIMIT 1")
    except Exception:
        db_ok = False
    return {"status": "ok" if db_ok else "degraded",
            "db": "ok" if db_ok else "error",
            "llm_key": "configured" if ZHIPU_KEY else "missing"}


@app.post("/api/chat")
async def chat(req: ChatIn) -> dict:
    refs = match_faq(req.message)
    append_log(req.session_id, "user", req.message)
    text = await answer(req.message, refs)
    append_log(req.session_id, "assistant", text)
    return {"answer": text, "faq_hit": bool(refs),
            "refs": [{"question": r["q"], "answer": r["a"]} for r in refs]}


@app.get("/api/history/{session_id}")
def history(session_id: str) -> dict:
    with db() as conn:
        rows = conn.execute(
            "SELECT role, content, created_at FROM chat_log WHERE session_id=? "
            "ORDER BY id DESC LIMIT 50", (session_id,)
        ).fetchall()
    rows.reverse()
    return {"session_id": session_id,
            "messages": [{"role": r, "content": c, "created_at": t} for r, c, t in rows]}


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")
