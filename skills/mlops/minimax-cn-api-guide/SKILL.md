---
name: minimax-cn-api-guide
description: MiniMax API 中国版 vs 国际版的区别和避坑指南
category: mlops
tags: [minimax, api, tts, china]
version: 1.0.0
---

# MiniMax API 中国版与国际版避坑指南

## 核心区别

| 功能 | 国际版 | 中国版 |
|------|--------|--------|
| API Key 环境变量 | `MINIMAX_API_KEY` | `MINIMAX_CN_API_KEY` |
| Base URL | `https://api.minimax.io/v1` | `https://api.minimaxi.com/v1` |
| 文本模型 (Chat) | ✅ 支持 | ✅ 支持 |
| TTS 语音合成 | ✅ 支持 | ❌ **不支持** |
| 图像生成 | ❓ 待确认 | ❓ 待确认 |

## 踩坑经历 (2026-04-09)

用户在新奥集团工作，位于中国，配置了 `MINIMAX_CN_API_KEY` + `api.minimaxi.com` endpoint。

想启用 MiniMax TTS，查阅代码后发现：
- `tts_tool.py` 里硬编码读取 `os.getenv("MINIMAX_API_KEY")`
- 没有对中国版 `MINIMAX_CN_API_KEY` 的支持
- 国际版 key 才能用于 TTS

**结论：中国版 key 无法用于 TTS，只能切回 Edge TTS。**

## 配置建议

如果在中国使用 MiniMax：
- **文本/推理任务**：用 `MINIMAX_CN_API_KEY` + `minimax-cn` provider ✅
- **TTS 语音合成**：用 Edge TTS（免费效果好）或国际版 `MINIMAX_API_KEY`
- **图像生成**：待验证，可能也需要国际版 key

## 验证命令

```bash
# 检查 TTS provider 状态
hermes status

# 测试 TTS
/hermes text_to_speech "测试文字"

# 查看当前配置
grep -A5 "tts:" ~/.hermes/config.yaml
grep "MINIMAX" ~/.hermes/.env
```

## 参考文件

- `~/.hermes/hermes-agent/tools/tts_tool.py` - TTS 实现
- `~/.hermes/hermes-agent/hermes_cli/config.py` - Provider 配置
