#!/bin/bash
# 同步工作区规范到运营仓库
cd /home/hatch/workspace/shanhai-squad-ops
cp /home/hatch/workspace/ip/shanhai-squad-bible.md ip/ 2>/dev/null
cp /home/hatch/workspace/ip/voice-bible.md ip/ 2>/dev/null
cp /home/hatch/workspace/custom-skills/local-guoxue-kids-video/SKILL.md skill/ 2>/dev/null
cp /home/hatch/workspace/covers/COVER-STYLE.md covers/ 2>/dev/null
cp /home/hatch/workspace/covers/make_cover.py covers/ 2>/dev/null
cp /home/hatch/workspace/series-plan-guoxue.md docs/ 2>/dev/null
git add -A
if ! git diff --cached --quiet; then
  git -c user.name="Muse" -c user.email="muse@local" commit -m "Sync: $(date '+%Y-%m-%d %H:%M')"
  echo "Committed changes"
else
  echo "No changes"
fi
