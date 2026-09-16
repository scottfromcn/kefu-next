#!/bin/bash
# 机器守门：拦危险 Bash 命令（agent-sdlc 清单"hook 当审批闸门"）
# 输入 stdin: {"tool_name":"Bash","tool_input":{"command":"..."}}
cmd=$(echo "$1" | python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)
[ -z "$cmd" ] && cmd=$(python3 -c "import json,sys; print(json.load(sys.stdin).get('tool_input',{}).get('command',''))" 2>/dev/null)

deny() {
  python3 -c "
import json,sys
print(json.dumps({'hookSpecificOutput':{'hookEventName':'PreToolUse','permissionDecision':'deny','permissionDecisionReason':'$1'}}))"
  exit 0
}

case "$cmd" in
  *"rm -rf /"*|*"rm -rf /*"*) deny "禁止递归删除根目录";;
  *"git push --force"*|*"git push -f"*|*"push --force-with-lease main"*) deny "禁止 force push（红线，人工执行）";;
  *"git reset --hard origin"*) deny "禁止硬重置到远端";;
  *DROP\ TABLE*|*DROP\ DATABASE*) deny "禁止在 hook 内 DROP，DDL 走迁移脚本";;
  *"kubectl delete ns"*|*"kubectl delete namespace"*) deny "禁止删命名空间";;
  *"--dangerously-skip-permissions"*) deny "禁止再嵌套放开权限";;
esac
exit 0
