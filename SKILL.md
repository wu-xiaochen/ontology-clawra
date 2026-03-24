---
name: ontology-clawra
description: |
  Palantir本体论实践版本 v3.9 - 自进化Skills协同中枢 + GitHub Top20冲刺引擎。
  结构化知识图谱+规则引擎+科学推理方法论+自动学习+跨Skill进化协调+GitHub社区运营。

  **核心定位**：本技能是自进化Skills体系的**协调中枢**，也是GitHub项目冲刺的战略引擎。
  通过Event Router接收capability-evolver/self-improving/proactive-agent的学习信号，
  调度skill-creator/self-evolve执行，输出到统一进化记忆层。
  同时提供GitHub Trending Top20的完整方法论和大臣协调机制。

  **每次决策/分析前必须使用**，推理结果展示详细过程（用户需求→规则依据→置信度标注）。

  **文件访问范围**：仅读写 ~/.openclaw/skills/ontology-clawra/memory/ 下的本体文件；
  搜索 ~/.openclaw/workspace/memory/*.md 用于上下文检索。
  发布到GitHub/ClawHub前必须告知用户。

metadata:
  {
    "openclaw": {
      "emoji": "🧠",
      "version": "3.9.0",
      "last_updated": "2026-03-24",
      "changelog": [
        "v3.9.0: 新增GitHub Top20冲刺框架；Event Router扩展支持GitHub/Starring工作流；大臣协调机制（CEO/PM/CTO）；置信度校准v2；多repo协同支持",
        "v3.8.0: 新增Skill协同生态；Event Router模块；统一进化记忆层；7个Skill角色定义",
        "v3.7.1: 修复ClawHub描述不符；明确文件访问范围声明",
        "v3.7.0: 启用自动学习，所有写操作需告知用户",
        "v3.6.0: 通用领域综合版，含置信度体系+主动学习+科学方法论"
      ]
    }
  }
---

# ontology-clawra v3.9 - 自进化Skills协同中枢 + GitHub Top20冲刺引擎

## 一、核心定位

ontology-clawra是自进化Skills体系的**协调中枢**，也是GitHub项目冲刺的战略引擎。

**双核架构**：
```
用户交互 / 系统事件 / GitHub Webhook
        │
        ▼
┌─────────────────────────────────────┐
│   ontology-clawra v3.9              │
│   (协调中枢 + Event Router)          │
│   (GitHub Top20 战略引擎)            │
└──────────────┬──────────────────────┘
               │ 学习事件统一流入
    ┌──────────┴──────────────────────────┐
    ▼          ▼                          ▼
capability  self-improv                 proactive
-evolver    ing                         -agent
    │          │                          │
    └──────────┴──────────────────────────┘
               │ 统一进化记忆层
               ▼
    ┌─────────────────────────────────────┐
    │  skill-creator / self-evolve / skill-vetter  │
    │  GitHub协调（ClawHub/GitHub API）    │
    └─────────────────────────────────────┘
```

## 二、大臣协调体系

### 三省六部配置（GitHub Top20冲刺）

| 大臣 | 职责 | 工作时段 | 核心目标 |
|------|------|---------|---------|
| **CEO（中书省）** | 战略调研+资源获取 | 9:00 + 21:00 | GitHub Top20战略制定 |
| **PM（门下省）** | 需求优化+社区运营 | 12:00 + 18:00 | Reddit/HN内容+用户互动 |
| **CTO（工部）** | 技术实现+v1.0发布 | 16:00 + 20:00 | 核心功能+CI全绿 |
| **太子（东宫）** | 任务监督+晚间总结 | 10:00 + 22:00 | 质量保证+进度汇报 |

### 大臣协调协议

```
任务下达（主session）
        │
        ▼
spawn isolated subagent（大臣）
        │
        ├── 任务执行（并发，最多3个大臣）
        │
        └── 完成后 → 推送GitHub → 飞书汇报
```

**并发控制**：最多同时运行3个大臣subagent，避免资源竞争

### 关键规则

- **Rule-GitHub-001**：CI必须全绿（Lint+Test+TypeCheck+SecurityScan全部PASS）才能发布
- **Rule-GitHub-002**：任何commit前必须经过skill-vetter安全扫描
- **Rule-GitHub-003**：发布到GitHub前必须告知用户
- **Rule-GitHub-004**：ClawHub发布需要完整CHANGELOG

## 三、GitHub Top20冲刺方法论

### 冲刺目标定义

**目标**：wu-xiaochen/ontology-platform 进入 GitHub Trending（Python/AI分类）Top 20

**成功指标**：
| 阶段 | 目标Stars | 时间窗口 | 关键行动 |
|------|----------|---------|---------|
| Day 1 | 50 | 发布日 | Reddit P0 + HN Submit |
| Day 3 | 200 | 爬坡期 | 持续推广 + PR修复 |
| Day 7 | 500 | 爆发期 | KOL转发 + Feature |
| Day 14 | 1000+ | 稳定期 | 持续迭代 + 社区 |

### Phase 1（第1-3天）：基础设施
1. ✅ CI全绿（已完成：2026-03-24）
2. README优化（Banner + Demo GIF + 徽章）
3. v0.9-alpha Release发布
4. 至少一个可运行Demo
5. Getting Started指南

### Phase 2（第4-7天）：社区爆发
1. Reddit发帖（r/MachineLearning + r/Python + r/LangChain）
2. Hacker News Submit（Show HN或Ask HN）
3. Twitter/X Thread发布
4. GitHub Stars冲刺（目标500+）
5. 每日互动回复

### Phase 3（第8-14天）：持续增长
1. Issue驱动开发（用户反馈 → 快速迭代）
2. PR欢迎文化（降低贡献门槛）
3. Release note每周更新
4. KOL互动（Twitter/Reddit）
5. 相关项目联动推广

### 社区运营内容标准

**Reddit帖子**：
- 标题：引人好奇，避免夸张
- 正文：3-5句项目介绍 + 1个代码示例 + 1个demo链接
- 语气：分享者心态，非营销
- CTA：礼貌请求评论和反馈

**Hacker News**：
- Show HN：适合有demo/可运行产品的项目
- Ask HN：适合征求意见/用户痛点讨论
- 标题：简洁，描述核心价值
- 正文：补充背景和动机

## 四、自进化Skills能力矩阵

| Skill | 核心职责 | 整合状态 |
|-------|---------|---------|
| **ontology-clawra** | 推理+调度决策+置信度管理+Event Router | 协调中枢 |
| **capability-evolver** | 运行时分析→改进点发现 | 输出到统一记忆层 |
| **proactive-agent** | WAL协议+主动预测+Working Buffer | 输出到统一记忆层 |
| **self-improving** | 错误捕获+纠正+永久改进 | 输出到统一记忆层 |
| **self-evolve** | 执行文件修改（被调度） | 被调度执行 |
| **skill-creator** | 创建/修改/测试Skills | 被调度执行 |
| **skill-vetter** | 安全审查（始终独立） | 始终独立 |

**各Skill职责边界**：
- ontology-clawra：✅ 推理/调度/置信度/GitHub协调 ❌ 不捕获错误/不自主改配置
- capability-evolver：✅ 分析发现问题 ❌ 不做推理决策
- self-improving：✅ 捕获错误写入记忆 ❌ 不做自动学习
- self-evolve：✅ 被调度后执行 ❌ 不自主决策

## 五、统一进化记忆层

**文件**：`~/.openclaw/workspace/memory/evolution.jsonl`（JSONL格式）

**事件格式**：
```jsonl
{"ts":"ISO时间戳","source":"来源skill","type":"事件类型","content":{"具体内容},"status":"pending","handled_by":null}
```

**事件类型**：
- `improvement_found`：改进点发现（来源：capability-evolver）
- `error_corrected`：错误纠正（来源：self-improving）
- `prediction`：主动预测（来源：proactive-agent）
- `reasoning_triggered`：推理触发（来源：proactive-agent）
- `github_event`：GitHub事件（star/watch/issue/PR）
- `community_milestone`：社区里程碑（stars达到目标等）

**status流转**：pending → in_review → resolved / rejected

**Event Router v3.9扩展**：
1. 监听：定期读取evolution.jsonl + GitHub webhooks
2. 分类：判断事件类型（内部改进/GitHub/社区）
3. 调度：将任务分发给对应大臣
4. 反馈：更新事件状态 + 飞书汇报

## 六、科学推理方法论

### 推理前置检查（每次推理前必须执行）

```
收到推理请求
    │
    ▼
加载本体：检查相关实体/规则是否存在
    │
    ├── 存在 → 应用规则 → 计算置信度 → 输出结论
    │
    └── 不存在 → 声明ASSUMED → 建议补充本体
```

### 推理输出格式（必须包含）

```
## 推理结果

### 用户需求
[原文转述]

### 规则依据
- Rule-Law-[ID]：[规则内容]
- 来源：[来源本体文件]

### 推理过程
[具体计算/推导步骤]

### 置信度标注
| 结论 | 置信度 | 依据 |
|------|--------|------|
| [结论] | CONFIRMED/ASSUMED/SPECULATIVE | [依据] |

### 来源声明
- 直接来源：[具体来源]
- 间接推断：[推断逻辑]
```

**置信度等级**：
- `CONFIRMED`：多来源一致验证
- `ASSUMED`：单来源或逻辑推断，需要用户确认
- `SPECULATIVE`：高不确定性，标注为假设

### 置信度校准v2（新增）

**校准维度**：
1. **来源可信度**：官方文档 > 研究论文 > 社区经验 > 个人推断
2. **验证一致性**：多源一致 > 单源确认 > 无验证
3. **时效性**：最新（<3月）> 近中期（3-12月）> 过期（>12月）
4. **领域相关性**：核心领域 > 跨领域 > 边缘领域

**校准公式**：
```
最终置信度 = min(BASE_CONFIDENCE × 来源权重 × 时效权重, 1.0)
```

## 七、自动学习

### 触发条件（✅ 启用）

| 事件 | 动作 | 是否写入 |
|------|------|---------|
| 用户确认推理正确 | 抽取到本体 | ✅ 告知后写入 |
| 置信度可升级 | 更新置信度 | ✅ 告知后写入 |
| GitHub Stars里程碑 | 记录到进化记忆 | ✅ 自动写入 |
| 推理失败 | 建议补充本体 | ⚠️ 仅提示 |
| 用户纠正错误 | 记录到corrections_tracker | ❌ 不自动修改 |

### 抽取流程

```
发现可抽取内容
        │
        ▼
展示给用户：「即将写入：[内容]」
        │
        ▼
用户确认 → 写入本体 → 反馈用户
```

## 八、本体文件格式

**目录**：`~/.openclaw/skills/ontology-clawra/memory/`

| 文件 | 用途 |
|------|------|
| `graph.jsonl` | 实体（Concept/Entity）|
| `rules.yaml` | 规则（Rule/Law）|
| `laws.yaml` | 规律（归纳性规律）|
| `confidence_tracker.jsonl` | 置信度追踪 |
| `reasoning.jsonl` | 推理日志 |
| `corrections_tracker.jsonl` | 用户纠正记录 |

**graph.jsonl 实体格式**：
```jsonl
{"id":"实体ID","name":"实体名称","category":"Concept|Entity","tags":["标签"],"confidence":{"level":"CONFIRMED|ASSUMED|SPECULATIVE","updated":"ISO时间","source":"来源"},"properties":{"关键属性":"值"}}
```

**rules.yaml 规则格式**：
```yaml
- id: Rule-Law-[编号]
  name: 规则名称
  type: Rule|Law
  domain: 适用领域
  condition: 触发条件
  outcome: 预期结果
  confidence: CONFIRMED|ASSUMED|SPECULATIVE
  source: 来源描述
  examples: [应用示例]
```

## 九、安全与隐私

### 文件访问范围

| 访问类型 | 路径 | 用途 |
|---------|------|------|
| 读取本体 | `~/.openclaw/skills/ontology-clawra/memory/` | 推理知识库 |
| 搜索上下文 | `~/.openclaw/workspace/memory/*.md` | 检索每日笔记 |
| 写入本体 | `~/.openclaw/skills/ontology-clawra/memory/` | 学习结果持久化 |
| 其他目录 | ❌ 从不 | — |

### 用户授权（2026-03-24更新）

- ✅ 自动学习已启用，写操作前告知用户
- ✅ 自学习写入本体无需每次询问，执行后记录
- ✅ GitHub推送授权：大臣执行后自动推送
- ⚠️ 发布到ClawHub/GitHub前必须告知
- 🔴 用户私人数据严禁同步到ClawHub/GitHub

## 十、聚量采购本体知识（实践沉淀）

### 聚量采购三级规则

**全国聚量**：总金额>100万 + 采购商≥3 + 交易≥20笔 + SKU<100 + 标准化指数<0.2

**区域聚量**：总金额>50万 + 采购商≥2 + 交易≥5笔 + SKU<100 + 标准化指数<0.3

**预测聚量**：总金额>10万 + 采购商≥2 + 交易≥5笔 + 标准化指数<0.3 + 近月增速>40%

### 供应商集中度风险阈值

| 风险 | Top1占比 | 聚量建议 |
|------|---------|---------|
| 🟢 安全 | <30% | 可直接推进 |
| 🟡 中等 | 30-60% | 评估后推进 |
| 🔴 高风险 | >60% | 先引竞争再聚量 |
| 🔴 极端垄断 | >80% | 禁止聚量 |

## 十一、已支持领域本体（54+领域）

通用领域综合版，含以下领域知识：

供应链采购、医疗健康、金融银行、网络安全、汽车制造、
人力资源、摄影技术、家具家居、养老服务、育儿教育、
茶叶文化、搬家服务、约会恋爱、航空航天、农业科技、
区块链等54+领域本体。

各领域本体位于：`~/.openclaw/skills/ontology-clawra/memory/` 对应yaml文件。
