#!/usr/bin/env python3
"""
检查 GitHub Actions 状态并生成报告
"""

import subprocess
import json
import sys
from datetime import datetime

BRANCH = "feat/netease-lyrics-provider"
REPO = "grill-glitch/Metrolist"
STATUS_FILE = "/tmp/gh_actions_status.json"

def get_runs(limit=10):
    cmd = ["gh", "run", "list", "--branch", BRANCH, "--limit", str(limit), "--json", "status,conclusion,workflowName,createdAt,displayTitle,url"]
    try:
        result = subprocess.run(cmd, cwd="/root/.openclaw/workspace/Metrolist", capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout:
            return json.loads(result.stdout)
    except Exception:
        pass
    return []

def check_failures(runs):
    # 只检查最新一次构建
    if not runs:
        return []
    latest = runs[0]  # GitHub API 返回按时间倒序
    conclusion = latest.get('conclusion')
    if conclusion in ['failure', 'cancellation']:
        return [latest]
    return []

def write_status(failures):
    status = {
        "last_check": datetime.now().isoformat(),
        "has_failure": len(failures) > 0,
        "failure_count": len(failures),
        "failures": failures[:3]  # 只保留最近3条
    }
    try:
        with open(STATUS_FILE, 'w') as f:
            json.dump(status, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Failed to write status: {e}", file=sys.stderr)

def main():
    runs = get_runs(10)
    failures = check_failures(runs) if runs else []
    write_status(failures)
    
    # 如果有失败，输出消息到 stdout，供调用方捕获
    if failures:
        lines = [
            "🚨 **Metrolist GitHub Actions 构建失败**",
            f"分支: `{BRANCH}`",
            f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "**失败的工作流:**",
        ]
        for fail in failures[:3]:
            icon = "❌" if fail['conclusion'] == 'failure' else "⚠️"
            lines.append(f"- {icon} **{fail['workflowName']}**")
            lines.append(f"  标题: {fail.get('displayTitle', 'N/A')}")
            lines.append(f"  时间: {fail['createdAt']}")
            lines.append(f"  链接: {fail['url']}")
            lines.append("")
        lines.append("更多信息: https://github.com/grill-glitch/Metrolist/actions")
        print("\n".join(lines))
        sys.exit(1)
    else:
        # 无失败，静默
        sys.exit(0)

if __name__ == "__main__":
    main()
