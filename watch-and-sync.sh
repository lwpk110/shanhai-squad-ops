#!/bin/bash
# 实时监控规范文件，变更立即同步提交
# 监控：SKILL.md、IP圣经、声音圣经、封面系统、系列方案

WATCH_FILES=(
  "/home/hatch/workspace/custom-skills/local-guoxue-kids-video/SKILL.md"
  "/home/hatch/workspace/ip/shanhai-squad-bible.md"
  "/home/hatch/workspace/ip/voice-bible.md"
  "/home/hatch/workspace/covers/COVER-STYLE.md"
  "/home/hatch/workspace/covers/make_cover.py"
  "/home/hatch/workspace/series-plan-guoxue.md"
)

declare -A LAST_MTIME
for f in "${WATCH_FILES[@]}"; do
  [ -f "$f" ] && LAST_MTIME["$f"]=$(stat -c %Y "$f" 2>/dev/null || echo 0)
done

echo "Watching ${#WATCH_FILES[@]} files for changes..."

while true; do
  sleep 30
  CHANGED=0
  for f in "${WATCH_FILES[@]}"; do
    [ -f "$f" ] || continue
    MTIME=$(stat -c %Y "$f" 2>/dev/null || echo 0)
    if [ "$MTIME" != "${LAST_MTIME[$f]}" ]; then
      echo "[$(date '+%H:%M:%S')] Changed: $f"
      LAST_MTIME["$f"]=$MTIME
      CHANGED=1
    fi
  done
  if [ $CHANGED -eq 1 ]; then
    /home/hatch/workspace/shanhai-squad-ops/sync.sh
  fi
done
