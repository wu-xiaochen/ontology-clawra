---
name: ontology-clawra
description: |
  ontology-clawra v5.0 - 本地本体推理引擎 + GitHub Top20冲刺辅助。

  **实际功能**：本地化的结构化推理引擎 + 置信度管理 + 自动学习。
  读取用户workspace记忆文件用于上下文，不包含跨skill调度或网络通信。

  **核心能力**：
  - 本体知识图谱存储与推理
  - 置信度计算与自知（元认知）
  - 本地记忆搜索与规则学习
  - GitHub项目（ontology-platform）冲刺辅助

  **文件访问范围**：仅读写 ~/.openclaw/skills/ontology-clawra/memory/ 下的本体文件；
  仅读取 ~/.openclaw/workspace/memory/*.md 用于上下文检索。
  无跨skill调度、无自动网络请求。

metadata:
  {
    "openclaw": {
      "emoji": "🧠",
      "version": "5.0.0",
      "last_updated": "2026-03-25",
      "changelog": [
        "v3.9.0: 新增GitHub Top20冲刺框架；移除夸大的协调中枢描述；明确本地化设计",
        "v3.8.0: 新增Skill协同生态（文档层面）",
        "v3.7.0: 启用自动学习"
      ]
    }
  }
---

# ontology-clawra v5.0 - 本地本体推理引擎

## 一、核心定位（准确描述）

**这是一个本地推理引擎，不是跨skill协调器。**

```
实际能力：
✅ 本地本体知识图谱存储与推理
✅ 置信度计算与自知（元认知）
✅ 本地记忆文件搜索
✅ 自动学习（写入本地memory目录）
✅ GitHub Top20冲刺战略辅助（通过spawn大臣）

实际限制：
❌ 不调度其他skills（无Event Router）
❌ 不执行跨skill通信
❌ 无自动网络请求
❌ 无agent-to-agent RPC
```

## 二、文件访问权限

| 操作 | 路径 | 说明 |
|------|------|------|
| 读 | `~/.openclaw/skills/ontology-clawra/memory/` | 本体文件 |
| 读 | `~/.openclaw/workspace/memory/*.md` | 用户上下文 |
| 写 | `~/.openclaw/skills/ontology-clawra/memory/` | 学习结果 |
| 写 | GitHub（via git push） | 需用户确认 |
| ❌ | 其他目录 | 从不访问 |

**网络行为**：
- 无自动网络请求
- network_fetch.py 仅搜索本地文件，返回获取建议
- 无 requests/sockets/subprocess 外部调用

## 三、核心推理能力

### 置信度等级

- `CONFIRMED`：多来源验证，可信
- `ASSUMED`：单来源，需要用户确认
- `SPECULATIVE`：高不确定性，标注假设

### 推理输出格式

```
## 推理结果

### 用户需求
[原文转述]

### 规则依据
- Rule-Law-[ID]：[规则内容]

### 推理过程
[具体推导步骤]

### 置信度标注
| 结论 | 置信度 | 依据 |
|------|--------|------|
| [结论] | CONFIRMED/ASSUMED/SPECULATIVE | [依据] |
```

## 四、本体文件格式

**目录**：`~/.openclaw/skills/ontology-clawra/memory/`

| 文件 | 用途 |
|------|------|
| `graph.jsonl` | 实体（Concept/Entity）|
| `rules.yaml` | 规则（Rule/Law）|
| `laws.yaml` | 规律（归纳性规律）|
| `confidence_tracker.jsonl` | 置信度追踪 |
| `reasoning.jsonl` | 推理日志 |

## 五、自动学习

### 触发条件

| 事件 | 动作 | 写入位置 |
|------|------|---------|
| 用户确认推理正确 | 抽取到本体 | `graph.jsonl` |
| 置信度可升级 | 更新置信度 | `confidence_tracker.jsonl` |
| 推理失败 | 建议补充本体 | 仅提示 |

### 写入规则

- 所有写操作前告知用户
- 仅写入 `~/.openclaw/skills/ontology-clawra/memory/`
- 不上传任何数据到外部服务

## 六、安全声明

1. **无外部网络调用**：代码不包含 requests/urllib/sockets 外部调用
2. **无凭据访问**：不读取环境变量或API keys
3. **隐私隔离**：workspace记忆文件仅用于上下文，不同步
4. **本地化**：所有学习结果仅存储在本地memory目录

## 七、GitHub Top20 冲刺辅助

ontology-clawra 提供战略推理能力，帮助制定GitHub项目冲刺计划。
大臣体系通过OpenClaw标准subagent机制工作，非本skill直接调度。

## 八、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v3.9 | 2026-03-24 | 移除夸大描述，明确本地化设计 |
| v3.8 | 2026-03-20 | 新增Skill协同文档 |
| v3.7 | 2026-03-16 | 启用自动学习 |
| v3.6 | 2026-03-16 | 初始版本 |

## 九、已支持领域本体

供应链采购、医疗健康、金融银行、网络安全、汽车制造、
人力资源、摄影技术、家具家居、养老服务、育儿教育、
茶叶文化、搬家服务、约会恋爱、航空航天等54+领域。

各领域本体位于：`~/.openclaw/skills/ontology-clawra/memory/` 对应yaml文件。
