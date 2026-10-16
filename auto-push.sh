#!/bin/bash
# 自动同步并推送到 GitHub
# Token 从安全位置读取，不硬编码

TOKEN_FILE="$HOME/.config/shanhai-squad-ops/github_token"
REPO_DIR="/home/hatch/workspace/shanhai-squad-ops"

if [ ! -f "$TOKEN_FILE" ]; then
  echo "Token file not found"
  exit 1
fi

TOKEN=$(cat "$TOKEN_FILE")
cd "$REPO_DIR"

# 先同步工作区文件
./sync.sh

# 推送（用 token 构造临时 remote URL，不存配置）
git push https://lwpk110:${TOKEN}@github.com/lwpk110/shanhai-squad-ops.git main 2>&1 | sed "s/${TOKEN}/***/g"

echo "Push completed at $(date)"
