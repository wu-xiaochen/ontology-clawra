---
name: github-history-cleanup
description: 从 GitHub 历史中彻底清除敏感文件的完整流程 — 使用 git filter-repo + force push，适用于清理意外提交的个人文件、工作文件等
version: "1.0"
last_updated: "2026-04-09"
author: Clawra
tags: [git, security, privacy, github]
---

# GitHub 历史彻底清理流程

## 何时用
- 意外提交了私人文件（身份证、护照、手机号、公司文件等）到 GitHub
- 需要从所有分支和历史中移除特定文件
- 敏感信息泄露风险

## ⚠️ 关键警告
**`git reset --hard` 会删除所有未跟踪的文件！** 如果本地有文件但 GitHub 历史已被清理，直接 reset 会丢失本地文件。必须在操作前确认本地文件是否有备份。

## 标准流程（零失误版）

### 第一步：备份本地所有重要文件
```bash
# 确认本地有哪些未跟踪的重要文件
git status --porcelain
# 把它们复制到安全位置
cp -r /path/to/sensitive-stuff ~/backup/
```

### 第二步：在临时目录操作镜像仓库
```bash
cd /tmp
rm -rf repo-clean
git clone --mirror https://github.com/USER/REPO.git repo-clean
```

### 第三步：用 git-filter-repo 清理
```bash
cd repo-clean
# 安装（如果没装）
pip install git-filter-repo

# 移除敏感路径（--invert-paths 表示排除这些文件）
git filter-repo --path Documents --invert-paths --force
# 可以同时移除多个路径：
# git filter-repo --path Documents --path .env --path secrets/ --invert-paths --force
```

### 第四步：重新添加 origin 并 force push
```bash
cd repo-clean
git remote add origin https://github.com/USER/REPO.git
git push --force origin main
```

### 第五步：同步到本地工作目录
```bash
# 重要：先确认本地是否有未跟踪的重要文件
git status --porcelain

# 如果有，先备份再操作
cp -r . ~/repo-backup/
git fetch origin
git reset --hard origin/main

# 如果没有未跟踪文件，可以直接：
git fetch origin
git reset --hard origin/main
```

### 第六步：验证
```bash
# 确认 GitHub 历史已清理
git log --all --name-only | grep -i "敏感词"
# 确认本地文件完整
ls -la
```

## BFG 替代方案（如果装了 Java）
```bash
java -jar bfg.jar --delete-files Documents
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force
```
BFG 比 git-filter-repo 更快，但需要 Java 环境。

## ClawHub 清理（相关）
如果同时发布到 ClawHub，清理 GitHub 后需要重新发布：
```bash
clawhub delete SLUG --yes
clawhub publish . --version X.Y.Z --changelog "清理版本"
```

## 教训记录（2026-04-09）
- ❌ 错误做法：直接 `git reset --hard origin/main` 而不检查本地未跟踪文件
- ✅ 正确做法：先 `git status --porcelain` 确认本地是否有需要保留的文件
- ✅ 最佳实践：在 /tmp 临时目录操作镜像，不动原始工作目录
