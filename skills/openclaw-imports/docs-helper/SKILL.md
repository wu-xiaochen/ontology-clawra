---
name: docs-helper
description: OpenClaw官方文档助手。当需要进行任何配置时，先查询官方文档确保正确操作。
metadata:
  {
    "openclaw": {
      "emoji": "📖",
      "description": "配置前先查文档，确保正确操作"
    }
  }
---

# Docs Helper - 文档查询助手

当需要进行任何配置或操作时，使用此技能查询官方文档。

## 官方文档资源

| 来源 | 地址 |
|------|------|
| 官方文档 | https://docs.openclaw.ai/ |
| GitHub | https://github.com/openclaw/openclaw |
| 配置参考 | https://docs.openclaw.ai/gateway/configuration-reference |
| 配置示例 | https://docs.openclaw.ai/gateway/configuration-examples |

## 查询步骤

1. **确定查询主题** - 例如：model providers, agents, skills, channels等
2. **使用 Tavily 搜索** - `tavily-search` 技能
3. **参考配置示例** - 查找类似配置作为参考
4. **验证配置** - 使用 `openclaw doctor` 检查

## 常用配置查询

- **模型配置**: docs.openclaw.ai/gateway/configuration-reference
- **技能配置**: docs.openclaw.ai/skills/overview
- **渠道配置**: docs.openclaw.ai/channels/overview

## 使用场景

当需要：
- 添加新的 model provider
- 配置新的 skill
- 设置 channel
- 修改 agent 配置
- 任何配置相关的操作

**都应先使用此技能查询文档！**
