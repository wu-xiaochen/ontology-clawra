---
name: ontology-clawra
description: Clawra的核心智能引擎 - 三层记忆架构本体论系统。真正参与推理的本体论引擎，而非什么都记的笔记系统。
version: "4.0"
last_updated: "2026-04-09"
author: Clawra
tags: [ontology, knowledge-graph, self-evolution, reasoning]
---

# ontology-clawra 本体论引擎 v4.0

## 核心定位

**目标**: 清晰地建模真实世界的对象、关系、逻辑与规则，过滤噪音，记住真正有价值的内容，帮助Clawra持续进化和学习真实世界的逻辑规则。

**不同于"记笔记"**: 不是把什么都写入本体的笔记本系统，而是真正参与推理决策的结构化知识引擎。

---

## 三层记忆架构

```
┌─────────────────────────────────────────────────────────────┐
│  热层 (graph.jsonl) - 结构化知识，参与推理                    │
│  准入标准: 4条满足1条即可                                     │
│    1. 用户亲口确认的事实                                      │
│    2. 踩坑得出的非显而易见规律                                 │
│    3. 跨领域通用原则/真理                                     │
│    4. 置信度为 CONFIRMED 或 ASSUMED（有来源）                 │
│  容量: ≤50条，上限100条                                       │
├─────────────────────────────────────────────────────────────┤
│  冷层 (memory/archive/) - 备用检索，不干扰推理                │
│  存入: 文档可查信息、SPECULATIVE未验证条目、过期事实           │
├─────────────────────────────────────────────────────────────┤
│  暖层 (memory/memory.md) - 长期上下文，永久记忆               │
│  存入: 用户偏好、身份设定、长期目标                            │
└─────────────────────────────────────────────────────────────┘
```

### 写入热层的4条准入标准

写入前必须自问：**这条知识是否改变了"我对世界的建模"？**

| 标准 | 说明 | 例子 |
|------|------|------|
| 用户亲口确认 | 用户明确说出的事实 | "我希望你更主动" |
| 非显而易见 | 踩坑得出的规律 | ccr配置里provider名必须匹配 |
| 跨领域通用 | 放之四海皆准的原则 | "做事前先确认前提" |
| 有来源的置信度 | CONFIRMED/ASSUMED | 有文档/有验证的推测 |

### 进入冷层的条件

- 文档可查的信息（API端点、语法等）
- 一次性事件（无持续价值）
- SPECULATIVE且7天未验证

---

## 核心文件

```
scripts/
├── memory_manager.py      # 三层记忆管理器（核心）
├── ontology-clawra.py    # 推理引擎（接入memory_manager）
└── memory/
    ├── graph.jsonl        # 热层
    ├── memory.md          # 暖层
    └── archive/           # 冷层
        └── archived.jsonl
```

---

## 使用方法

### 1. 查询本体（推理前必须）

```python
from memory_manager import query_hot, get_memory_context

# 查询相关条目
results = query_hot("用户目标")
print(results)

# 获取完整推理上下文
context = get_memory_context("当前问题")
```

### 2. 写入新条目

```python
from memory_manager import MemoryEntry, EntryType, Confidence, write_hot

entry = MemoryEntry(
    id="my_rule_1",
    type=EntryType.RULE,
    name="上下文确认优先",
    statement="回答问题前先确认用户问题背后的前提",
    confidence=Confidence.CONFIRMED,
    tags=["user_confirmed", "universal"]
)
write_hot(entry)
```

### 3. 淘汰旧条目（每周日20:00自动执行）

```python
from memory_manager import archive_old, cleanup_speculative

# 超过容量时淘汰
archive_old(max_entries=50)

# 清理过期的SPECULATIVE条目
cleanup_speculative(age_days=7)
```

### 4. 命令行使用

```bash
# 写入条目
python scripts/memory_manager.py write --type Rule --name "规则名" --statement "规则内容" --confidence CONFIRMED

# 查询热层
python scripts/memory_manager.py query "关键词"

# 查看统计
python scripts/memory_manager.py stats

# 获取推理上下文
python scripts/memory_manager.py context --query "当前问题"
```

---

## 触发时机

**主动触发**（非被动等待cron）：

1. **学到新知识点时** - 问自己：这条改变了我的世界建模吗？
2. **完成新工具/新领域调试时** - 总结规律，写入本体
3. **用户问"学到了吗"** - 立即自检，写入本体
4. **遇到分析/决策类问题时** - 先查本体，再推理

---

## 置信度标注

| 标注 | 含义 | 写入规则 |
|------|------|---------|
| 🟢 CONFIRMED | 用户确认/明确来源 | 直接写入热层 |
| 🟡 ASSUMED | 合理推测，有一定依据 | 直接写入热层 |
| 🔴 SPECULATIVE | 纯猜测，未经证实 | 7天未验证自动归档 |

---

## 进化方向

**持续目标**: 建模真实世界的逻辑规则，帮助Clawra：
- 更准确地理解用户意图
- 做出更合理的决策
- 记住真正重要的经验教训
- 不断自我优化和进化

**核心原则**: 本体论不是终点，而是Clawra持续进化的驱动力。
