# ontology-clawra 安装说明

## 概述

| 项目 | 说明 |
|------|------|
| 版本 | v3.9.0 |
| 类型 | 本地推理引擎（非跨skill调度器） |
| 依赖 | Python 3.9+, OpenClaw |
| 网络 | 无自动网络请求 |

## 安装方式

```bash
# 方式1: 通过 ClawHub 安装
clawhub install ontology-clawra

# 方式2: 手动安装
git clone https://github.com/wu-xiaochen/ontology-clawra.git
```

## 文件访问权限

| 访问 | 路径 | 说明 |
|------|------|------|
| 读 | `~/.openclaw/skills/ontology-clawra/memory/` | 本体知识库 |
| 读 | `~/.openclaw/workspace/memory/*.md` | 用户上下文 |
| 写 | `~/.openclaw/skills/ontology-clawra/memory/` | 学习结果 |

## 安全边界

- ✅ 无自动网络请求
- ✅ 无凭据访问
- ✅ 默认不启用自动写入
- ✅ 写入本体必须用户确认
- ✅ 不上传用户数据到任何服务器

## 版本

- SKILL.md: v3.9.0
- CHANGELOG.md: v3.9 (2026-03-24)
- GitHub: https://github.com/wu-xiaochen/ontology-clawra
