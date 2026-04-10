#!/bin/bash
# Hermes 个人配置每日备份脚本
# 备份到 wu-xiaochen/ontology-clawra/backup/

set -e

HERMES_DIR="$HOME/.hermes"
BACKUP_DIR="$HOME/ontology-clawra/backup"
GIT_DIR="$HOME/ontology-clawra"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 需要备份的文件/目录
BACKUP_ITEMS=(
    "config.yaml"
    ".env"
    "memories"
    "skills"
    "cron"
    "hooks"
    "channel_directory.json"
    "gateway_state.json"
    "gateway_voice_mode.json"
    "SOUL.md"
)

cd "$GIT_DIR"

# 切换到 HTTPS + token URL（兼容 CI/新机器）
GITHUB_TOKEN=$(grep "GITHUB_TOKEN" "$HERMES_DIR/.env" 2>/dev/null | cut -d= -f2)
if [ -n "$GITHUB_TOKEN" ]; then
    git remote set-url origin "https://xiaochenwu:${GITHUB_TOKEN}@github.com/wu-xiaochen/ontology-clawra.git" 2>/dev/null || true
fi

# 同步 backup 目录
for item in "${BACKUP_ITEMS[@]}"; do
    if [ -e "$HERMES_DIR/$item" ]; then
        rsync -a --delete "$HERMES_DIR/$item" "$BACKUP_DIR/$item" 2>/dev/null || true
    fi
done

# 提交
cd "$GIT_DIR"
git add backup/
git commit -m "backup: daily config snapshot $TIMESTAMP" 2>/dev/null || true
git push origin master 2>/dev/null || true

echo "[$TIMESTAMP] Backup done"
