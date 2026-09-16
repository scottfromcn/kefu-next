---
name: local-check
description: 提交前本地自测：按改动范围跑受影响的检查（python 编译/pytest、前端 tsc+build、密钥扫描），失败自己先修。写完代码准备提交/提 PR 前必须跑。
---

# local-check · 本地自测与提交检查

提交前的机器守门（对应 agent-sdlc 清单步骤 18-19）。改动完成后、`git commit` 前跑本 skill。

## 流程

1. **圈定影响面**：`git status` + `git diff --name-only` 列出改动文件，按类型分组：
   - `backend/**/*.py` → 后端检查
   - `frontend/src/**` → 前端检查
   - `docs/**` → 文档检查（轻）
   - `deploy/**` → compose 配置检查（`docker compose config -q`）
2. **按组执行**：
   - 后端：`python3 -m py_compile $(git ls-files '*.py' | grep -v venv)`；如有测试再 `pytest backend/tests -q`
   - 前端：`cd frontend && npm run build`（含 tsc 类型检查）
   - 全部：密钥扫描——diff 里不得出现密钥前缀、私钥文件头、明文口令赋值等模式，具体规则以 `.githooks/pre-commit` 为准（grep 自己的 diff）
3. **失败自己修**：编译/类型/构建失败，直接修到过，不允许跳过或注释绕过（发现绕过测试意图直接停手上报）
4. **产出回执**：

```
local-check ✅
  backend: py_compile 32 files OK
  frontend: tsc+build OK (38 modules)
  secrets: clean
  未覆盖：无自动化测试（v1），验收依赖 docs/ 验收清单
```

## 硬规则

- 检查失败时禁止 `git commit`（.githooks/pre-commit 会再拦一次，别赌）
- `--no-verify` 只允许在纯文档改动时用，且要在 worklog 里注明原因
- 环境起不来（依赖装不上等）不等于通过——如实报告并停
