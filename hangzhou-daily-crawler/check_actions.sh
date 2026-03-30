#!/usr/bin/env bash
# 检查 Metrolist GitHub Actions 状态，失败时发送通知

cd /root/.openclaw/workspace/Metrolist

# 获取最近5次运行
RUNS=$(gh run list --branch feat/netease-lyrics-provider --limit 5 --json status,conclusion,workflowName,createdAt,displayTitle,url 2>/dev/null)

if [ -z "$RUNS" ]; then
    exit 0
fi

# 检查是否有失败
FAILURES=$(echo "$RUNS" | jq -r '.[] | select(.conclusion=="failure" or .conclusion=="cancellation")' 2>/dev/null)

if [ -n "$FAILURES" ]; then
    # 构建消息
    MSG="🚨 **Metrolist 构建失败**\n分支: feat/netease-lyrics-provider\n\n失败工作流:\n"
    COUNT=0
    echo "$FAILURES" | while read -r item; do
        STATUS=$(echo "$item" | jq -r '.conclusion')
        NAME=$(echo "$item" | jq -r '.workflowName')
        TITLE=$(echo "$item" | jq -r '.displayTitle // "N/A"')
        TIME=$(echo "$item" | jq -r '.createdAt')
        URL=$(echo "$item" | jq -r '.url')
        ICON="❌"
        [ "$STATUS" = "cancellation" ] && ICON="⚠️"
        MSG="$MSG$ICON **$NAME**\n标题: $TITLE\n时间: $TIME\n$URL\n\n"
        COUNT=$((COUNT + 1))
    done
    
    MSG="$MSG查看: https://github.com/grill-glitch/Metrolist/actions"
    
    # 发送到 OpenClaw 主会话（通过 webhook 或消息工具）
    # 临时写入文件，供心跳检查时读取
    echo "$MSG" > /tmp/gh_actions_failure_msg.txt
fi
