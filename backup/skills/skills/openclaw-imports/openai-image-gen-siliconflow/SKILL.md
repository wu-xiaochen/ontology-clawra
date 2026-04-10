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
# base URL 已默认配置
```

## ⚠️ 重要：Python 版本要求

**必须用 python3.12+，不能用系统默认的 python3（macOS 默认是 3.9）**

原因：`gen.py` 使用了 `str | None` 类型注解语法（Python 3.10+ 才支持），在 3.9 上会报错：
```
TypeError: unsupported operand type(s) for |: 'types.GenericAlias' and 'NoneType'
```

## 已知问题（gen.py 已修复）

1. **参数名**：`Qwen/Qwen-Image` 模型用 `image_size` 而不是 `size`
2. **quality 参数**：Qwen 模型不支持 `quality` 参数
3. **默认模型**：gen.py 默认是 `gpt-image-1`（OpenAI），需显式指定 `--model "Qwen/Qwen-Image"`
4. **endpoint**：`/images/generations`（不是 `/image_generation`）

## 使用方法

```bash
OPENAI_API_KEY="sk-..." python3.12 {baseDir}/gen.py \
  --model "Qwen/Qwen-Image" \
  --prompt "描述" \
  --count 1 \
  --out-dir /tmp/output
```

## 快速验证

```python
import requests
api_key = "sk-..."  # SiliconFlow key
r = requests.post(
    "https://api.siliconflow.cn/v1/images/generations",
    headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    json={"model": "Qwen/Qwen-Image", "prompt": "test", "image_size": "1024x1024", "n": 1}
)
print(r.json())  # 成功返回 {"images": [{"url": "..."}]}
```

## 参数

- `--model`: 模型名称（必须填 `Qwen/Qwen-Image`）
- `--prompt`: 图片描述
- `--count`: 生成数量
- `--size`/`--image_size`: 尺寸（Qwen 模型用 image_size）

## 自拍专用 prompt 模板（Clawra 用）

```
a beautiful Chinese woman, 28 years old, elegant makeup, stunning appearance,
taking a mirror selfie, wearing stylish outfit, realistic photo style, soft lighting
```

**注意**：Qwen-Image 模型生成的风格是"规矩流动"型，和 MiniMax 风格不同。人物一致性不如专业模型，但真实感较好。

## 测试成功的 key 配置（2026-04-09）

```
OPENAI_API_KEY=sk-cyfunmsszjrqumckweykgkjojjfbclilbbochdvprfezqgcw
SILICONFLOW_BASE_URL=https://api.siliconflow.cn/v1
```

## 踩坑记录

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `401 Invalid token` | endpoint 路径写错 | 用 `/images/generations` 不是 `/image_generation` |
| `TypeError: unsupported operand` | Mac python3 是 3.9 | 必须用 `python3.12` |
| 生成图片糊/不像 | prompt 没加 `realistic photo style` | 显式指定风格关键词 |
