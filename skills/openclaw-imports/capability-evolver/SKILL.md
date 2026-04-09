---
name: capability-evolver
description: |
  capability-evolver v2.0 - 轻量级自我进化引擎（纯Python，无外部依赖）。
  
  **核心能力**：
  - 错误自动分析（从日志中提取失败模式）
  - 自我修复（生成修复代码并验证）
  - 规则自动学习（从成功案例中抽取规则）
  - 主动优化（识别低效模式并改进）
  
  **设计原则**：
  - 纯Python实现（无Node.js/git/EvoMap依赖）
  - 零外部依赖（仅用Python标准库）
  - 安全优先（所有修改需确认后执行）
  - 可追溯（每次变更记录到事件日志）

metadata:
  {
    "openclaw": {
      "emoji": "🧬",
      "version": "2.0.0",
      "last_updated": "2026-03-24",
      "changelog": [
        "v2.0.0: 纯Python重写，移除Node.js/git/EvoMap依赖"
      ]
    }
  }
---

# capability-evolver v2.0 - 轻量级自我进化引擎

## 一、核心定位

**不是需要复杂配置的引擎，而是装上就能跑的工具。**

```
对比：
v1.x: 需要 Node.js + git + A2A_NODE_ID + EvoMap
v2.0: 只需要 Python 3.10+（内置标准库）
```

## 二、功能模块

### 1. 错误分析器 (ErrorAnalyzer)

```python
from capability_evolver import ErrorAnalyzer

analyzer = ErrorAnalyzer()
patterns = analyzer.scan_logs(
    log_paths=["~/.openclaw/logs/"],
    since_hours=24
)

# 输出：[{pattern, count, severity, suggestion}]
for p in patterns:
    print(f"[{p.severity}] {p.pattern}: {p.count}次")
```

### 2. 自我修复器 (SelfRepair)

```python
from capability_evolver import SelfRepair

repairer = SelfRepair()
fixes = repairer.analyze_and_fix(
    error_patterns=patterns,
    target_files=["~/.openclaw/skills/ontology-clawra/"]
)

# 生成修复建议（不自动执行）
for fix in fixes:
    print(f"[{fix.confidence}%] {fix.description}")
    print(f"  文件: {fix.file}")
    print(f"  修改: {fix.diff[:100]}...")
```

### 3. 规则学习器 (RuleLearner)

```python
from capability_evolver import RuleLearner

learner = RuleLearner()
new_rules = learner.extract_rules(
    from_success_cases=["~/.openclaw/workspace/memory/"],
    min_occurrences=3
)

# 自动抽取成功模式为规则
for rule in new_rules:
    print(f"[{rule.confidence}] {rule.pattern}")
```

### 4. 主动优化器 (ProactiveOptimizer)

```python
from capability_evolver import ProactiveOptimizer

optimizer = ProactiveOptimizer()
suggestions = optimizer.optimize(
    scope=["skills", "workspace"],
    strategy="balanced"  # balanced/innovate/harden
)

for s in suggestions:
    print(f"[{s.priority}] {s.description}")
```

## 三、运行模式

### 被动模式（默认）

```python
# 仅当被调用时执行
from capability_evolver import CapabilityEvolver

evolver = CapabilityEvolver()
result = evolver.run(mode="passive")
```

### 主动模式（定时）

```python
# 每小时自动检查并优化
evolver = CapabilityEvolver()
result = evolver.run(mode="proactive", interval_hours=1)
```

### 审查模式（安全）

```python
# 生成修改建议，但不自动执行
result = evolver.run(mode="review")
# 输出包含完整的diff和风险评估
```

## 四、安全机制

| 机制 | 说明 |
|------|------|
| **审查模式** | 所有修改先展示，用户确认后才执行 |
| **回滚保证** | 每次修改前保存快照 |
| **影响评估** | 修改前计算风险分数 |
| **变更日志** | 所有操作记录到事件日志 |

## 五、事件日志格式

**文件**：`~/.openclaw/skills/capability-evolver/events.jsonl`

```jsonl
{"ts":"ISO时间","type":"error_analyzed|fix_applied|rule_learned|optimization_suggested","content":{"描述":"..."},"status":"pending|approved|executed|rejected","risk":"low|medium|high"}
```

## 六、文件访问权限

| 操作 | 路径 | 说明 |
|------|------|------|
| 读 | `~/.openclaw/skills/*/` | 所有skill目录 |
| 读 | `~/.openclaw/workspace/memory/` | 工作记忆 |
| 读 | `~/.openclaw/logs/` | 日志文件 |
| 写 | `~/.openclaw/skills/capability-evolver/` | 自身目录 |
| ⚠️ 写 | `~/.openclaw/skills/*/` | 仅审查模式批准后 |

**安全**：无网络请求，仅本地文件操作

## 七、与ontology-clawra集成

```
错误发生 → ErrorAnalyzer分析 → 抽取规则 → RuleLearner学习
                                              ↓
                                      规则存入ontology-clawra
                                              ↓
                                      下次推理使用新规则
```

## 八、配置参数

```python
{
    "EVOLVE_LOAD_MAX": 2.0,        # 系统负载阈值
    "EVOLVE_STRATEGY": "balanced", # balanced/innovate/harden
    "EVOLVE_AUTO_APPROVE": false,   # 是否自动批准低风险修改
    "EVOLVE_LOG_RETENTION_DAYS": 30 # 日志保留天数
}
```

## 九、安装要求

```bash
# 仅Python标准库，无需安装任何包！
# Python 3.10+
```

## 十、版本历史

| 版本 | 日期 | 说明 |
|------|------|------|
| v2.0 | 2026-03-24 | 纯Python重写，移除Node.js依赖 |
| v1.x | 2026-03-16 | 初始版本，需要Node.js+git+EvoMap |
