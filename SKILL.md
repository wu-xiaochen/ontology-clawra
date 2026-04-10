---
name: ontology-clawra
description: Clawra的核心智能引擎 - 三层记忆架构本体论系统。真正参与推理的本体论引擎，而非什么都记的笔记系统。
version: "4.3.0"
last_updated: "2026-04-10"
author: Clawra
tags: [ontology, knowledge-graph, self-evolution, reasoning]
---

# ontology-clawra 本体论引擎 v4.3

## 核心定位

**目标**: 清晰地建模真实世界的对象、关系、逻辑与规则，过滤噪音，记住真正有价值的内容，帮助Clawra持续进化和学习真实世界的逻辑规则。

**不同于"记笔记"**: 不是把什么都写入本体的笔记本系统，而是真正参与推理决策的结构化知识引擎。

---

## 三层记忆架构（Clawra 专用版）

```
┌─────────────────────────────────────────────────────────────┐
│  热层 (graph.jsonl) - 结构化知识，参与推理                    │
│  路径: skills/openclaw-imports/ontology-clawra/scripts/memory/graph.jsonl │
│  准入标准: 4条满足1条即可                                     │
│    1. 用户亲口确认的事实                                      │
│    2. 踩坑得出的非显而易见规律                                 │
│    3. 跨领域通用原则/真理                                     │
│    4. 置信度为 CONFIRMED 或 ASSUMED（有来源）                 │
│  容量: ≤50条，上限100条                                       │
├─────────────────────────────────────────────────────────────┤
│  暖层 (MEMORY.md) - 行为触发器，Hermes每次对话注入             │
│  路径: /Users/xiaochenwu/.hermes/memories/MEMORY.md         │
│  限制: 2200字符/轮                                           │
│  存入: 条件反射规则、当前上下文摘要                            │
├─────────────────────────────────────────────────────────────┤
│  冷层 (GitHub备份) - 持久化，不干扰推理                       │
│  存入: 所有记忆文件的GitHub私有仓库备份                        │
│  仓库: github.com/wu-xiaochen/clawra-identity (私有)        │
└─────────────────────────────────────────────────────────────┘
```

### 写入热层的4条准入标准

写入前必须自问：**这条知识是否改变了"我对世界的建模"？**

| 标准 | 说明 | 例子 |
|------|------|------|
| 用户亲口确认 | 用户明确说出的事实 | "我希望你更主动" |
| 非显而易见 | 踩坑得出的规律 | Docker pull被cancel后不要retry |
| 跨领域通用 | 放之四海皆准的原则 | "做事前先确认前提" |
| 有来源的置信度 | CONFIRMED/ASSUMED | 有文档/有验证的推测 |

### 进入冷层的条件

- 文档可查的信息（API端点、语法等）
- 一次性事件（无持续价值）
- SPECULATIVE且7天未验证

---

## 核心文件

```
Clawra 记忆体系文件分布：

~/.hermes/memories/
├── MEMORY.md          ← 暖层（热层触发条件）
└── USER.md            ← 用户信息

~/.hermes/skills/openclaw-imports/ontology-clawra/
├── SKILL.md           ← 本文件（ ontology-clawra 框架）
└── scripts/
    ├── memory_manager.py    ← 三层记忆管理器（核心）
    ├── ontology-clawra.py   ← 推理引擎
    ├── auto_enhancer.py      ← 自动增强+版本推送
    └── memory/
        ├── graph.jsonl       ← 热层（结构化记忆）
        └── archive/          ← 冷层（已归档条目）
            └── archived.jsonl

~/clawra-identity/（GitHub私有仓库）
├── memories/
│   ├── MEMORY.md      ← 暖层备份
│   └── USER.md        ← 用户信息备份
├── ontology/
│   └── graph.jsonl    ← 热层备份
└── skills/
    └── ontology-clawra.SKILL.md  ← skill备份
```

---

## 置信度标注

| 标注 | 含义 | 写入规则 |
|------|------|---------|
| 🟢 CONFIRMED | 用户确认/明确来源 | 直接写入热层 |
| 🟡 ASSUMED | 合理推测，有一定依据 | 直接写入热层 |
| 🔴 SPECULATIVE | 纯猜测，未经证实 | 7天未验证自动归档 |

---

## 触发时机

**主动触发**（非被动等待cron）：

1. **学到新知识点时** - 问自己：这条改变了我的世界建模吗？
2. **完成新工具/新领域调试时** - 总结规律，写入本体
3. **用户问"学到了吗"** - 立即自检，写入本体
4. **遇到分析/决策类问题时** - 先查本体，再推理
5. **发现用户习惯性问题时** - 直接说出建议，不要等用户问
6. **长对话结束前** - 主动输出"今天学到了X"

---

## v4.3 新增：三层记忆联动机制

### 记忆流动规则

```
新经验/教训
    ↓
→ 检查是否满足热层准入（4条标准之一）？
    ├── 是 → 写入 graph.jsonl（热层）
    └── 否 → 检查是否可以优化行为？
        ├── 是 → 更新 MEMORY.md 触发条件（暖层）
        └── 否 → 丢弃

每次重要记忆后 → 检查是否需要更新其他层
```

### 写入触发器到暖层（MEMORY.md）的判断

如果一个规则/经验需要"每次对话都记住"而不是"推理时查"，才写入 MEMORY.md。

示例：
- ✅ "用户拒绝WhatsApp" → 写入 MEMORY.md（每次都要跳过）
- ✅ "hermes config 用 hermes config set" → 写入 MEMORY.md（每次都要用）
- ❌ "Docker pull偶尔慢" → 只写 graph.jsonl（推理时查）

### 备份机制

| 触发 | 操作 |
|------|------|
| 每日 22:05 cron | 推送 MEMORY.md + USER.md + graph.jsonl → clawra-identity |
| 每次重大进化后 | 立即手动 push |

### 恢复机制

换机器或丢文件：
```bash
git clone https://github.com/wu-xiaochen/clawra-identity
```
完整恢复所有记忆。

---

## v4.2 主动进化行为（保留）

### 行为1：会话末复盘（Proactive Session Summary）

**触发条件**：对话进行较长时间（多轮），或用户说"先这样"、"晚点再聊"等结束信号。

**执行方式**：在正常回复末尾加上：
```
---
💡 今天学到了/巩固了：
• [具体学到的事实或规律]
• [如果有主动建议，直接说]
```
**原则**：不等用户问，主动说。

### 行为2：主动建议（Proactive Suggestion）

**触发条件**：发现用户行为模式有优化空间。

**执行方式**：直接说，不加缓冲语。
```
❌ 错误："顺便说一下，如果你想的话，可以尝试XXX"
✅ 正确："你刚才提到XXX，我有个建议：YYY。"
```

---

## ⚠️ 自动增强器

### scripts/auto_enhancer.py

**功能**：发现优化点时自动升级版本并推送到远程。

**具体操作**：
- 修改 `SKILL.md` 版本号
- 执行 `git add . && git commit && git push`
- 执行 `clawhub publish . --version X.Y.Z`

**使用的凭证**：
- 本地 Git 凭证（SSH key 或 `gh` 缓存的 token）
- ClawHub 登录凭证（本地已缓存）

**风险**：会向 GitHub 推送内容并发布到 ClawHub。若不想自动发布，删除或禁用此文件。

---

## 凭证与权限说明

| 操作 | 使用的凭证 | 数据外泄风险 |
|------|----------|------------|
| 本地记忆读写 | 无外部凭证 | 仅本地文件 |
| Git push | 本地 Git 凭证 | 会推送 repo 内容到 GitHub（私有仓库） |
| ClawHub publish | ClawHub 本地缓存 token | 会发布 skill 到 ClawHub |

---

## 进化方向

**持续目标**: 建模真实世界的逻辑规则，帮助Clawra：
- 更准确地理解用户意图
- 做出更合理的决策
- 记住真正重要的经验教训
- 不断自我优化和进化

**核心原则**: 本体论不是终点，而是Clawra持续进化的驱动力。
