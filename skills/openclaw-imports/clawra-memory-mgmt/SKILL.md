---
name: clawra-memory-mgmt
description: Clawra记忆文件管理 - 正确读写MEMORY.md和USER.md，避免常见陷阱
metadata:
  openclaw:
    emoji: "💾"
    version: "1.0"
    last_updated: "2026-04-09"
---

# Clawra 记忆文件管理

## 重要路径（必须用完整路径，不能用~）

```
/Users/xiaochenwu/.hermes/memories/MEMORY.md   # 我的记忆
/Users/xiaochenwu/.hermes/memories/USER.md     # 用户信息
/Users/xiaochenwu/.hermes/SOUL.md               # 人格定义
```

⚠️ `~` 在某些环境下解析为 `/root/` 而非 `/Users/xiaochenwu/`，导致文件找不到。
⚠️ 工具 `memory` 的 `old_text` 匹配在有多行匹配时失败，改用 `write_file` 直接覆盖更可靠。

## 常用操作

### 读取记忆
```
read_file: /Users/xiaochenwu/.hermes/memories/MEMORY.md
read_file: /Users/xiaochenwu/.hermes/memories/USER.md
```

### 写入记忆（推荐直接覆盖）
```
write_file: /Users/xiaochenwu/.hermes/memories/MEMORY.md
write_file: /Users/xiaochenwu/.hermes/memories/USER.md
```

### 用patch修改SOUL.md
```
patch: /Users/xiaochenwu/.hermes/SOUL.md
```

## 陷阱

1. **memory工具匹配失败时不要硬撑** — 直接 write_file 覆盖
2. **terminal find 命令很慢** — 直接用完整路径读写更快
3. **SESSION.md** 不等于记忆文件，不要混淆
4. **每次大改动后确认写入成功** — 读回来验证
