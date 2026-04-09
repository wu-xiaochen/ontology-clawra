---
name: openai-image-gen-siliconflow
description: Generate images via SiliconFlow API (OpenAI compatible). Uses Qwen/Qwen-Image model.
metadata:
  {
    "openclaw": {
      "emoji": "🖼️",
      "requires": {
        "env": ["OPENAI_API_KEY"]
      },
      "primaryEnv": "OPENAI_API_KEY"
    }
  }
---

# OpenAI Image Gen (SiliconFlow)

使用 SiliconFlow API 生成图片，支持 Qwen/Qwen-Image 模型。

## 环境变量

```bash
export OPENAI_API_KEY="your-siliconflow-api-key"
# 可选: 自定义 base URL
export OPENAI_BASE_URL="https://api.siliconflow.cn/v1"
```

## 使用方法

```bash
python3 {baseDir}/gen.py --model "Qwen/Qwen-Image" --prompt "描述" --count 1
```

## 参数

- `--model`: 模型名称 (默认: Qwen/Qwen-Image)
- `--prompt`: 图片描述
- `--count`: 生成数量 (默认: 1)
- `--size`: 图片尺寸 (如 1024x1024)

## 示例

```bash
python3 {baseDir}/gen.py --model "Qwen/Qwen-Image" --prompt "一只可爱的猫" --count 1
```
