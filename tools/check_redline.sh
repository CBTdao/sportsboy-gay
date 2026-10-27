#!/bin/sh
# check_redline.sh — SportsBoy 红线提交卡点
# 拦截公开站点(*.html)上出现的内部机器语言（获客/变现/留存/闭环…），防止"内部信息上站"
# 用法：被 .git/hooks/pre-commit 自动调用；或手动 bash check_redline.sh [file ...]
# 返回 0=放行，1=拦截

BANNED='获客|变现|留存|闭环|IP飞轮|北极星|转化漏斗|私域|矩阵运营|资产沉淀|成本结构壁垒|一鱼多吃|内容即获客|全AI流水线|全 AI 流水线|流量单向|用户生命周期|增长黑客|冷启动|LTV|ARPU'

if [ $# -gt 0 ]; then
  FILES="$@"
else
  FILES=$(git diff --cached --name-only --diff-filter=ACM -- '*.html' 2>/dev/null)
fi

if [ -z "$FILES" ]; then
  exit 0
fi

HIT=0
for f in $FILES; do
  case "$f" in
    *.html) ;;
    *) continue ;;
  esac
  if [ -f "$f" ]; then
    matches=$(grep -nE "$BANNED" "$f" 2>/dev/null)
    if [ -n "$matches" ]; then
      echo "RED-LINE BLOCK: 公开站点出现内部机器语言 -> $f"
      printf '%s\n' "$matches" | sed 's/^/    /'
      HIT=1
    fi
  fi
done

if [ "$HIT" -eq 1 ]; then
  echo ""
  echo "[红线] 内部信息不上站。卡点默认拦截；确需保留请先与团队确认。"
  echo "      绕过（不推荐）：git commit --no-verify"
  exit 1
fi

exit 0
