# Daily Evolution Cron Job Workflow
## Standard Steps (2026-06-11 更新)

1. **Load ontology-clawra skill** — 用 `skill_view(name='openclaw-imports/ontology-clawra')`（用全路径规避歧义错误）
2. **Run session_search** 回顾今日活动（传空查询做 browse 模式看最近 session；无参调用就是浏览模式）
3. **Structured reflection**:
   - What went well?
   - What could be better?
   - What did I learn?
4. **读取 graph.jsonl**（安全方法）:
   - 用 `terminal('cat <path>')` 获取原始内容（不用 `read_file`）
   - 每行找到第一个 `{` 取 JSON 部分（去掉行号前缀）
   - 用 `json.loads()` 解析，跳过空行和损坏行
   - 去重（type + content[:100] 作为 key）
   - 过滤空 content 的条目
5. **追加 2-3 条今日洞察** 到 graph.jsonl（安全方法）:
   - 用 `cat > path << 'EOF'\n...\nEOF` 通过 terminal 写入（不用 `write_file`）
   - 必须是纯 JSON 格式，一行一条，无行号前缀
6. **检查 Git 状态**（`git status --short`）:
   - 有变更 → `git add -A && git commit -m "..." && git push`
   - 无变更 → 跳过（auto_enhancer 已经推过的本轮就不重复推）
   - **注意**: 如果 GitHub push 超时（目前环境网络问题），记入 insight 后继续，不重试
7. **写入明日意图** 到 `~/.clawra/self_memory/tomorrow_intention.txt`

## 每日进化流程的安全红线

### 读 graph.jsonl 的正确姿势

```python
# ✅ 安全读取
raw = terminal("cat <path>")["output"]
for line in raw.split("\n"):
    line = line.strip()
    brace = line.find("{")
    if brace >= 0:
        jstr = line[brace:]
        try:
            entry = json.loads(jstr)
            entries.append(entry)
        except:
            pass

# ❌ 绝不这样
from hermes_tools import read_file, write_file
raw = read_file(path)  # 输出格式有行号前缀，与文件原始行号叠加，解析不可靠
write_file(path, json_content)  # 会覆盖整个文件，已发生事故
```

### 写 graph.jsonl 的正确姿势

```bash
# ✅ 安全写入
cat > ~/.hermes/skills/openclaw-imports/ontology-clawra/scripts/memory/graph.jsonl << 'EOF'
{"type": "insight", "confidence": "CONFIRMED", ...}
EOF

# ❌ 绝不这样
write_file(graph_path, clean_content)  # 如解析出错会覆盖全部数据
```

### 每日去重

- 解析后，以 `(type, content[:100])` 作为 key 去重
- 过滤 content 为空或空白的条目
- 保持条目数 <50（超过需归档）

## 自动增强器的已知问题和修复

### 版本漂移问题 (2026-06-11 已修复 ✅)

**问题**：auto_enhancer.py 的 `update_skill_md_version()` 从 `_meta.json` 读版本号后在 SKILL.md 中查找替换。但之前手动修复版本漂移后，SKILL.md 版本与 _meta.json 不同步，导致 `re.escape(old_version)` 找不到匹配，替换失败。

**修复 (2026-06-11)**：新增 `_detect_skill_md_version()` 函数，先检测 SKILL.md 中实际的版本号。如果检测到漂移（如 SKILL.md=4.8.113, _meta.json=4.8.112），优先使用 SKILL.md 中的版本作为替换目标。同时增加兜底机制：如果精确匹配失败，用正则强制替换第一个版本号字符串。

**修复效果**：从 "失败→静默跳过" 变为 "漂移检测→精确替换→兜底强制" 三级容错。

### GitHub 推送超时 (持续性问题)

- GitHub (`https://github.com`) 从目前的环境完全不可达（curl 超时）
- `git push origin main` 每次都会超时
- **对策**：不阻塞流程，记入 insight 后继续。本地 commit 已就绪，用户上线后手动推或重试
- **是否算错误**：不——这是环境网络限制，不是 bug

### ClawHub Token 过期 (持续性问题)

- `clawhub publish` 报 `Unauthorized: API token is invalid or revoked`
- 已连续失败 7 次（自 v4.8.107 起，2026-06-08 至今）
- **对策**：记入 insight。用户需执行 `clawhub login` 重新认证

## Key Learnings from 2026-06-11 Session

### v4.8.112 → v4.9.0 Minor 升级
- auto_enhancer 发现 10 项改进（7 个新领域规则 + 选型推理规则 + 版本同步 + 其他）
- 仅自动实现了 `references/graph-jsonl-safety.md` 的增强
- 其他领域规则和推理规则列为建议，需要手动实施
- SKILL.md 前一次手动修复导致版本漂移 4.8.112→4.8.113，auto_enhancer 替换失败
- ✅ 本次修复了 auto_enhancer.py 的版本漂移除 bug（见上）

### 本周升级节奏 (6/8-6/11)
| 日期 | 版本 | 说明 |
|------|------|------|
| 6/8 | v4.8.107→108→109 | 每日双升级 |
| 6/9 | v4.8.109→110→111 | 连续 |
| 6/10 | v4.8.111→112 | 每日一次 |
| 6/11 | v4.8.112→v4.9.0 | Minor 升级 |
| **总计** | **8次升级** | **v4.8.106→v4.9.0** |

### 关键观察
- `skill_view(name='ontology-clawra')` 因 3 份副本歧义失败 → 需用 `openclaw-imports/ontology-clawra`
- graph.jsonl 当前 26 条，格式统一为纯 JSON（旧格式条目已逐步清理）
- self_eval 稳定 5/5 全通过
- 环境问题（GitHub 超时 + ClawHub token 过期）连续第 5 天未解决

## Key Learnings from 2026-06-08 Session
- `skill_view(name='ontology-clawra')` 因 3 份副本歧义失败，需用 `openclaw-imports/ontology-clawra`
- graph.jsonl 当前 22 条，格式混合（旧条目有线号前缀，新条目纯 JSON），每天自检时稳定处理
- 今天 ontology-clawra 自动升级了两次（v4.8.107→v4.8.108），自评 5/5

## Key Learnings from 2026-05-16 Session
- session_search returns limited preview content, full session logs needed for detailed analysis
- Personal session data provides valuable context for empathetic support
- Model configuration verification is critical after provider switches