# 仓库同步策略

## 架构

```
工作区文件 → [实时监控] → 本地仓库提交 → [每日22:00] → GitHub推送
```

## 实时同步（文件监控）

**监控脚本**：`watch-and-sync.sh`（后台运行，30秒轮询）

**监控文件**：
- `custom-skills/local-guoxue-kids-video/SKILL.md` → `skill/SKILL.md`
- `ip/shanhai-squad-bible.md` → `ip/`
- `ip/voice-bible.md` → `ip/`
- `covers/COVER-STYLE.md` → `covers/`
- `covers/make_cover.py` → `covers/`
- `series-plan-guoxue.md` → `docs/`

**触发**：任一文件 mtime 变化 → 自动执行 `sync.sh` → git commit

**日志**：`watcher.log`

## 定时推送（GitHub）

**任务**：每日 22:00（北京时间），cron `daily-github-sync-2200`

**脚本**：`auto-push.sh`
1. 执行 `sync.sh`（确保本地最新）
2. 从 `~/.config/shanhai-squad-ops/github_token` 读取 Token（600权限）
3. 推送到 `https://github.com/lwpk110/shanhai-squad-ops.git`

**Token 管理**：
- 位置：`~/.config/shanhai-squad-ops/github_token`
- 权限：600（仅所有者可读）
- 不硬编码在脚本中，不提交到仓库

## 新账号接手

1. `git clone https://github.com/lwpk110/shanhai-squad-ops.git`
2. 阅读 `README.md` 了解运营策略
3. 阅读本文件了解同步机制
4. 启动监控：`nohup ./watch-and-sync.sh > watcher.log 2>&1 &`
5. 配置 Token：按上述路径存放 GitHub PAT（需 `repo` 权限）
6. 创建每日 22:00 的 cron 任务执行 `auto-push.sh`

## 手动操作

```bash
# 手动同步
./sync.sh

# 手动推送
./auto-push.sh

# 查看监控日志
tail -f watcher.log
```
