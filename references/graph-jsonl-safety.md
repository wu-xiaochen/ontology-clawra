# graph.jsonl 安全编辑须知

## ⚠️ 核心问题

graph.jsonl 文件存在**混合格式**，不同历史时期的条目格式不同：

| 时段 | 格式 | 示例 |
|------|------|------|
| 早期 (v3.0 ~ v4.8.100) | `LINE_NO\|SHORT_NO\|{json}` | `1\|     1\|{"type":"lesson"...}` |
| 中期 (v4.8.101 ~ v4.8.103) | 纯 JSON，一行一条 | `{"type":"insight","content":"..."}` |
| 新格式 (v4.8.104+) | 纯 JSON，一行一条 | `{"type":"learning","date":"..."}` |

这意味着**不能假设每一行都可以 `json.loads()` 直接解析**。

## 🚨 危险操作：execute_code + read_file + write_file

**这是本系统最危险的 graph.jsonl 编辑模式。** 2026-06-07 发生过真实事故：

```
事故链：
1. read_file() 输出带行号前缀（"    12|    12|{json}"）
2. 脚本尝试解析 "{" 位置 → 遇到早期条目的行内前缀 → 解析失败
3. 被误判为"0 条目" → write_file 覆盖整个文件
4. 所有历史数据丢失
5. 需从 git commit 恢复
```

**教训**：`read_file` 的输出格式与文件原始格式不同。早期条目的 `LINE_NO|` 前缀和 read_file 的 `LINE_NO|CONTENT` 输出前缀叠加，无法可靠区分。

## ✅ 安全编辑方法（优先级排序）

### 方法 1：cat >> 追加（最安全，推荐）

追加新条目到文件末尾（不读入文件，纯追加）：

```bash
cat >> ~/.hermes/skills/openclaw-imports/ontology-clawra/scripts/memory/graph.jsonl << 'EOF'
{"type": "insight", "confidence": "CONFIRMED", ...}
EOF
```

**优势**：不读取、不修改现有内容，不会丢失数据。

### 方法 2：patch 替换（安全，用于修正某一行）

注意：由于每行可能有行号前缀，`patch` 的 `old_string` 必须包含完整行内容。

### 方法 3：memory_manager.py 脚本（最规范，优先使用）

```bash
cd ~/.hermes/skills/openclaw-imports/ontology-clawra
python scripts/memory_manager.py --add '{"type": "insight", ...}'
```

优先用这个，如果知道其接口的话。

### 方法 4：terminal + cat 读取原始内容

```bash
cat ~/.hermes/skills/openclaw-imports/ontology-clawra/scripts/memory/graph.jsonl
```

**不要用** `read_file()` 读取 graph.jsonl 的 JSON 内容——它的输出格式会误导解析。

## 🛡️ 恢复方案

graph.jsonl 是 git 版本控制的（在 `ontology-clawra` 仓库中）。恢复方式：

```bash
cd ~/.hermes/skills/openclaw-imports/ontology-clawra
git show <commit-hash>:scripts/memory/graph.jsonl > scripts/memory/graph.jsonl
git checkout HEAD~1 -- scripts/memory/graph.jsonl
```

## 📅 事故记录

| 日期 | 事故 | 恢复方式 | 损失 |
|------|------|---------|------|
| 2026-06-07 | execute_code 误 write_file 覆盖 | `git show 60fb707` 恢复 | 无（已恢复） |