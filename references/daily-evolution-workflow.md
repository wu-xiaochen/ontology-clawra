# Daily Evolution Cron Job Workflow
## Standard Steps (2026-06-08 更新)

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

## Key Learnings from 2026-06-08 Session
- `skill_view(name='ontology-clawra')` 因 3 份副本歧义失败，需用 `openclaw-imports/ontology-clawra`
- graph.jsonl 当前 22 条，格式混合（旧条目有线号前缀，新条目纯 JSON），每天自检时稳定处理
- 今天 ontology-clawra 自动升级了两次（v4.8.107→v4.8.108），自评 5/5

## Key Learnings from 2026-05-16 Session
- session_search returns limited preview content, full session logs needed for detailed analysis
- Personal session data provides valuable context for empathetic support
- Model configuration verification is critical after provider switches