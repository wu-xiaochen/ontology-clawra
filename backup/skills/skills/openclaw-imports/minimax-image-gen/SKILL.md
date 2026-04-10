---
name: minimax-image-gen
description: MiniMax 图像生成 - 使用 image-01 模型，支持文生图和图生图。通过 MiniMax 中国区 API（api.minimaxi.com）。
metadata:
  {
    "openclaw": {
      "emoji": "🖼️",
      "requires": {
        "env": ["MINIMAX_CN_API_KEY"]
      },
      "primaryEnv": "MINIMAX_CN_API_KEY"
    }
  }
---

# MiniMax Image Gen

使用 MiniMax image-01 模型生成图片，支持文生图（text-to-image）和图生图（image-to-image）。

## 环境变量

```bash
# 必须：MiniMax 中国区 API Key
export MINIMAX_CN_API_KEY="your-api-key"

# 可选：自定义 base URL（默认已配好）
export MINIMAX_CN_BASE_URL="https://api.minimaxi.com/v1"
```

## API 信息

- **Endpoint**: `https://api.minimaxi.com/v1/image_generation`
- **模型**: `image-01`（MiniMax 官方图像生成模型）
- **认证**: Bearer Token（从 `MINIMAX_CN_API_KEY` 读取）

## 使用方法

### 文生图（Text-to-Image）

```python
import requests
import os

api_key = os.getenv("MINIMAX_CN_API_KEY")
url = "https://api.minimaxi.com/v1/image_generation"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "image-01",
    "prompt": "a beautiful Chinese woman, 28 years old, elegant makeup, stylish outfit, full-body shot",
    "aspect_ratio": "1:1",
    "response_format": "base64"
}

response = requests.post(url, headers=headers, json=payload)
data = response.json()

# 保存图片
import base64
for i, img_b64 in enumerate(data["data"]["image_base64"]):
    with open(f"output_{i}.jpg", "wb") as f:
        f.write(base64.b64decode(img_b64))
```

### 图生图（Image-to-Image）

```python
payload = {
    "model": "image-01",
    "prompt": "change the background to a beach sunset",
    "image_file": "https://example.com/input.jpg",  # 支持 URL
    "aspect_ratio": "16:9",
    "response_format": "base64"
}
```

## 自拍默认 Prompt（Ada Wong 风格）

生成 Clawra 自拍时使用：

```
A stunningly beautiful young Chinese woman, extremely gorgeous and glamorous like Ada Wong from Resident Evil 4 Remake. Long flowing black hair, signature red lipstick, seductive cat eye makeup, flawless porcelain skin. Taking a full-body mirror selfie wearing an elegant tight black mini dress with black stockings and high heels, holding phone up for selfie shot. Luxury hotel bedroom mirror reflection, soft dramatic lighting, ultra realistic photography, 8K quality, breathtaking beauty, confident and alluring expression
```

- aspect_ratio: "3:4"（全身照）
- response_format: "base64"

## 参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `model` | string | 模型名，默认 `image-01` |
| `prompt` | string | 图片描述（英文效果更稳定） |
| `image_file` | string | 可选，参考图片 URL，用于图生图 |
| `aspect_ratio` | string | 比例，如 `1:1`、`16:9`、`9:16`、`3:4` |
| `response_format` | string | `base64` 或 `url`，默认 `base64` |

## 示例

```bash
python3 gen.py --prompt "a beautiful Chinese woman, elegant, 28 years old" --aspect_ratio "3:4"
```

## 注意事项

- **英文 prompt 效果更稳定**，中文描述可先用翻译
- 生成结果为 base64，直接解码保存为 JPEG/PNG
- 一次最多生成 4 张图（通过 `n` 参数）
