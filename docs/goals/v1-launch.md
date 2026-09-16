# kefu-next v1：地铁客服系统第一版（单容器最小闭环）

- 日期：2026-09-16
- 状态：delivered
- 提出人：产品（原话："重新做个客服系统，别搞那么重，先能用"）

## 验收清单（每条可执行）

- [ ] A1 `curl -s localhost:8182/api/health` 返回 `{"status":"ok",...}`
- [ ] A2 问"首末班车"：`/api/chat` 返回 answer 含时间区间**且** refs 非空（FAQ 召回）
- [ ] A3 问 FAQ 外问题（"今天股票行情"）：answer 开头含"未在官方FAQ中找到"
- [ ] A4 `/api/history/<同A2会话>` 返回刚发的问答对（≥2 条）
- [ ] A5 数据落盘：`data/kefu.db` 存在，chat_log 行数 >0
- [ ] A6 首页 `curl -s localhost:8182/` HTTP 200 且含"客服"
- [ ] A7 `python3 -m py_compile` 全过；`git commit` 过 pre-commit
- [ ] A8 单容器运行：docker 容器 up 且 curl A1 仍绿

## 架构决策（本期边界）

- **单容器**：FastAPI 单进程 + SQLite（对比 v0 代的 mysql+双容器+nginx——第一版交付物最小化）
- **前端**：内嵌单页 HTML（vanilla JS），不引 React 构建
- **LLM**：glm-4-flash（bigmodel 免费层）；FAQ 12 条从 v0 代继承
- **不做**：多租户、鉴权、按日统计、流式回答、历史曲线——都是下一期 goal

## 自验回执

**2026-09-16（goal 循环 1 轮全绿）**

| 验收 | 结果 | 证据 |
|---|---|---|
| A1 health | ✅ | `{"status":"ok","db":"ok","llm_key":"configured"}` |
| A2 FAQ 召回 | ✅ | faq_hit=true，refs=1，answer 含 05:40-06:30 时间区间 + 引用标注 |
| A3 非 FAQ 声明 | ✅ | faq_hit=false，answer 前 30 字含"未在官方FAQ" |
| A4 历史 | ✅ | /api/history/goal-v1 返回 4 rows（两轮问答对，时序正确） |
| A5 落盘 | ✅ | data/kefu.db 12KB，chat_log 4 行 |
| A6 首页 | ✅ | HTTP 200，页面含"客服"×3 |
| A7 编译+守门 | ✅ | py_compile 过；本 commit 过 pre-commit |
| A8 单容器 | ✅ | kefu-next 容器 Up，宿主 8182 → 容器 8000 |

交付形态：FastAPI 单文件(app.py) + 内嵌聊天页(static/index.html) + 单容器(kefu-next:1.0)，入口 http://localhost:8182
已知限制：①单进程 SQLite 并发写入有限 ②无鉴权 ③LLM 单轮无上下文记忆
下一期 goal 建议：会话上下文记忆 / 流式回答 / 鉴权与用量统计

- 关联 intent：docs/intents/INT-20260916-01-kefu-next-launch.md（accepted）
