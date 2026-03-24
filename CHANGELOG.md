# ontology-clawra 版本变更记录

## v3.9 (2026-03-24) - GitHub Top20冲刺引擎

### 新增功能
- ✅ **GitHub Top20冲刺框架**：完整的方法论+大臣协调机制
- ✅ **Event Router v3.9**：支持GitHub/Starring工作流和社区里程碑事件
- ✅ **大臣协调体系**：CEO/PM/CTO/太子四臣协调协议
- ✅ **置信度校准v2**：来源可信度+时效性+领域相关性三维校准
- ✅ **多repo协同支持**：支持ontology-platform等项目协同运营

### 大臣体系
- 三省六部配置（GitHub Top20冲刺专用）
- 并发控制（最多3个大臣并发）
- GitHub Stars里程碑追踪
- 飞书汇报机制

### GitHub Top20方法论
- Phase 1（Day1-3）：CI+README+v0.9发布
- Phase 2（Day4-7）：Reddit/HN/Twitter爆发
- Phase 3（Day8-14）：持续增长+社区运营

---

## v3.8 (2026-03-20) - Skill协同生态

### 新增功能
- ✅ Skill协同生态架构
- ✅ Event Router模块（统一进化记忆层）
- ✅ 7个Skill角色定义
- ✅ Phase 3行动计划

### 协调架构
- 用户交互 → Event Router → 能力Skill → 执行Skill
- 事件类型：improvement_found/error_corrected/prediction/reasoning_triggered
- status流转：pending → in_review → resolved/rejected

---

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
