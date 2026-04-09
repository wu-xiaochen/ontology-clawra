# ontology-clawra 版本变更记录

## v3.1 (2026-03-16) - 科学推理方法论增强版

### 新增功能
- ✅ `network_fetch.py` - 网络获取模块，本地无数据时自动搜索
- ✅ `typical_scenarios.py` - 典型场景库，内置常见场景默认值
- ✅ `interactive_confirm.py` - 渐进式交互确认，每次只问1-2个核心问题
- ✅ `confidence_tracker.py` - 置信度追踪，记录并自动调整推理可信度
- ✅ `main.py` - 整合所有模块的主推理引擎

### 方法论升级
- 5步流程 → 7步流程（新增：网络获取、渐进交互）
- 支持典型场景快速匹配
- 支持置信度自动追踪
- 支持用户反馈闭环

### 测试验证
- ✅ typical_scenarios.py 测试通过
- ✅ confidence_tracker.py 测试通过
- ✅ main.py 推理引擎测试通过
- ✅ 调压箱选型场景测试通过

---

## v3.0 (2026-03-16) - 初始版本

### 核心改进
- 嵌入科学推理方法论（5步流程）
- 添加置信度标注（CONFIRMED/ASSUMED/SPECULATIVE/UNKNOWN）
- 支持交互式本体构建
- 更新HEARTBEAT.md定期优化任务

### 架构
- 四大支柱：Objects、Links、Functions、Actions
- 存储结构：8个文件（含新增extraction_log, confidence_tracker）

---

## v2.0 (历史版本)

- Palantir本体论基础架构
- 无方法论支持
- 静态本体定义
