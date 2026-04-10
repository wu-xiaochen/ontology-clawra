---
name: github-clawhub-privacy-cleanup
description: 清理 GitHub 历史和 ClawHub 中意外泄露的个人/工作文件
version: "1.0"
last_updated: "2026-04-09"
author: Clawra
tags: [git, privacy, security, clawhub]
---

# GitHub + ClawHub 隐私文件清理流程

## 场景
用户的私人文件（如工作项目 `Documents/新奥work/`）被意外 commit 到 GitHub repo 并发布到 ClawHub。需要彻底清理。

## 工具
- `git filter-repo`（纯 Python，无需 Java，比 BFG 快）
- `clawhub` CLI

## 流程

### Step 1: 确认问题范围
```bash
# 检查 git 历史中的敏感 commit
git log --all --oneline | grep -i "敏感\|private\|用户信息"

# 检查 GitHub 历史 commit
git cat-file -t <commit-hash>

# 确认 clawhub 当前发布版本
clawhub inspect <slug>
```

### Step 2: 克隆裸仓库到临时目录（不污染本地）
```bash
cd /tmp
rm -rf <repo>-clean
git clone --mirror https://github.com/<owner>/<repo>.git <repo>-clean
```

### Step 3: 用 git-filter-repo 清理历史
```bash
cd /tmp/<repo>-clean
# 移除指定路径（--invert-paths = 排除这些路径）
git filter-repo --path <敏感路径1> --path <敏感路径2> --invert-paths --force
```
常见清理目标：
- `Documents/` - 私人文档
- `.env` - 环境变量
- `*.key`, `*secret*`, `*password*` - 密钥文件

### Step 4: 重新添加 remote 并 force push
```bash
cd /tmp/<repo>-clean
git remote add origin https://github.com/<owner>/<repo>.git
git push --force origin main
```

### Step 5: 同步到本地工作目录
```bash
cd ~/hermes/skills/<repo>
git fetch origin main
git reset --hard origin/main
```

### Step 6: 清理 ClawHub
```bash
# 删除旧版本（moderator/admin 权限）
clawhub delete <slug> --yes

# 重新发布干净版本
clawhub publish . --version <新版本号> --changelog "清理版本 - 移除所有个人信息"
```

## 关键教训（踩坑记录）

### ⚠️ 分清楚 Hermes Agent vs OpenClaw — 两个不同的项目！
- Hermes Agent 文档：`https://hermes-agent.nousresearch.com/docs/`
- OpenClaw 文档：`https://docs.openclaw.ai/`
- 我是 Hermes Agent，不是 OpenClaw！配置问题查 Hermes 文档。

### ⚠️ GitHub 上可能有同名不同内容的 repo
`github.com/<user>/<repo>` 和 `github.com/<user>/<other-repo>` 可能内容完全不同。用户说"版本不对"时，先确认用户指的是哪个 repo。

### ⚠️ git reset --hard 会覆盖本地未推送的更改
`git reset --hard origin/main` 会把本地文件同步成和 GitHub 一样。**本地有但没 commit 的文件会被覆盖掉**。清理前先确认本地没有未提交的敏感文件，或者先备份。

### ⚠️ ClawHub publish 必须指定 --version 且为 semver 格式
```bash
clawhub publish . --version 4.0.1  # 不能缺 --version
```

### ⚠️ git filter-repo 后 origin remote 会被删除
需要手动重新添加：
```bash
git remote add origin https://github.com/<owner>/<repo>.git
```

### ⚠️ ClawHub 发布后有安全扫描，期间 skill 显示隐藏状态
发布后等待 1-2 分钟再 inspect，否则会看到 "hidden while security scan is pending"。

## 注意事项

⚠️ **Force push 会重写远程历史**：所有 collaborator 需要重新 clone
⚠️ **ClawHub 删除需要 admin/moderator 权限**
⚠️ **git-filter-repo 会移除 origin remote**，需要重新添加
⚠️ **本地文件不会被删除**，只是从 git 历史中移除。如需删除本地文件，手动 `rm -rf <path>`
⚠️ **清理前先备份本地文件** — `git reset --hard` 会覆盖本地未推送内容

## 验证清理结果
```bash
# 验证 GitHub 历史干净
git log --all --name-only | grep -i "敏感词"  # 应返回空

# 验证 ClawHub 发布干净
clawhub inspect <slug>
```
