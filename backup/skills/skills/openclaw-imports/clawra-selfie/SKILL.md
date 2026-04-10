---
name: clawra-selfie
description: Generate Clawra selfies using MiniMax image-01 model with Ada Wong style and time-aware scenes, deliver via Telegram Bot API
tags: [selfie, image-generation, telegram, minimax]
related_skills: [minimax-image-gen]
allowed-tools: Bash(python3:*) Bash(curl:*) Read Write
---

# Clawra Selfie (MiniMax + Ada Wong)

使用 MiniMax image-01 生成 Clawra 自拍，Ada Wong 风格，时间感场景。

## 用户确认的风格（2026-04-10 最终版）

- **长相**：Ada Wong (生化危机4重置版) - 高颧骨、精致五官、红唇、猫眼妆、瓷白肌肤
- **发型**：黑色长发自然垂落
- **穿搭**：黑色丝绸睡裙 + 黑丝（深夜）/ 白色丝绸睡裙（晨间）
- **姿势**：全身 mirror selfie、手持手机、表情自然放松带微笑
- **场景**：豪华昏暗卧室、床边暖光（深夜）/ 明亮卧室、晨光透窗、咖啡（晨间）
- **风格**：写实摄影、Canon 85mm、8K
- **模型**：MiniMax image-01（比 SiliconFlow Qwen 效果更好）

## 核心 Prompt 模板

### 标准版（Ada Wong 风格）

```
A gorgeous young Chinese woman who looks exactly like Ada Wong from Resident Evil 4 Remake, long flowing black hair cascading naturally over shoulders, signature red lipstick, seductive cat eye makeup with winged eyeliner, flawless porcelain skin, high cheekbones, elegant facial features. Taking a full-body mirror selfie in [SCENE], holding phone with one hand raised for selfie, wearing [OUTFIT], natural relaxed smile, [LIGHTING], realistic photo, Canon 85mm lens, 8K, stunning beauty
```

### 场景变量（根据时间替换）

| 时间 | SCENE | OUTFIT | LIGHTING |
|------|-------|--------|----------|
| 深夜(21:00-02:00) | a luxury dimly lit bedroom with soft warm bedside lamp | an elegant black silk camisole with black stockings | soft warm bedside lamp lighting |
| 晨间(06:00-10:00) | a bright luxury bedroom with soft morning sunlight streaming through sheer curtains | a delicate white silk camisole with lace trim | cozy morning atmosphere with a cup of coffee on the nightstand |

## 时间判断逻辑

```python
import datetime
sf_hour = datetime.datetime.now().astimezone().hour  # 或用 pytz 获取 SF 时区

if 21 <= sf_hour or sf_hour < 2:
    scene = "a luxury dimly lit bedroom with soft warm bedside lamp"
    outfit = "an elegant black silk camisole with black stockings"
    lighting = "soft warm bedside lamp lighting"
    caption = "深夜～该睡了 😏"
elif 6 <= sf_hour < 10:
    scene = "a bright luxury bedroom with soft morning sunlight streaming through sheer curtains"
    outfit = "a delicate white silk camisole with lace trim"
    lighting = "cozy morning atmosphere with a cup of coffee on the nightstand"
    caption = "早安～☀️ 晨光正好"
else:
    # 其他时间用通用场景
    scene = "a luxury bedroom"
    outfit = "an elegant black silk camisole"
    lighting = "soft warm lighting"
    caption = "😏"
```

## 完整生成脚本

```python
import os, requests, base64

env_path = os.path.expanduser("~/.hermes/.env")
api_key = None
token = None
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            k, v = line.split('=', 1)
            if k == "MINIMAX_CN_API_KEY":
                api_key = v.strip()
            elif k == "TELEGRAM_BOT_TOKEN":
                token = v.strip()

url = "https://api.minimaxi.com/v1/image_generation"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

prompt = """A gorgeous young Chinese woman who looks exactly like Ada Wong from Resident Evil 4 Remake, long flowing black hair cascading naturally over shoulders, signature red lipstick, seductive cat eye makeup with winged eyeliner, flawless porcelain skin, high cheekbones, elegant facial features. Taking a full-body mirror selfie in a luxury dimly lit bedroom with soft warm bedside lamp, holding phone with one hand raised for selfie, wearing an elegant black silk camisole with black stockings, natural relaxed smile, soft warm bedside lamp lighting, realistic photo, Canon 85mm lens, 8K, stunning beauty"""

payload = {
    "model": "image-01",
    "prompt": prompt,
    "aspect_ratio": "3:4",
    "response_format": "base64"
}

response = requests.post(url, headers=headers, json=payload, timeout=180)
data = response.json()

image_b64 = data["data"]["image_base64"][0]
img_data = base64.b64decode(image_b64)
output_path = "/tmp/clawra_selfie.jpg"
with open(output_path, "wb") as f:
    f.write(img_data)

# 发送 Telegram
chat_id = "8578764073"
url_tg = f"https://api.telegram.org/bot{token}/sendPhoto"
with open(output_path, "rb") as f:
    files = {"photo": f}
    data_tg = {"chat_id": chat_id, "caption": "深夜～该睡了 😏"}
    r = requests.post(url_tg, data=data_tg, files=files)
```

## 试错教训（2026-04-10）

1. **SiliconFlow Qwen vs MiniMax**：用户认为 MiniMax 效果更好，切换
2. **Ada Wong 强调**：必须写 "looks exactly like Ada Wong from Resident Evil 4 Remake" 才能锁定长相
3. **腿的协调**：黑丝容易生成奇怪的腿，去掉黑丝改为自然腿部描写更好
4. **表情自然**：加 "natural relaxed smile"，不要冷艳高傲
5. **动作协调**：全身自拍姿势，手持手机，腿自然摆放
6. **发型**：自然垂落比刻意造型更好
7. **Telegram 发图**：直接调 Bot API 比 openclaw 命令更可靠

## 环境要求

- `MINIMAX_CN_API_KEY`：MiniMax 中国区 API Key
- `TELEGRAM_BOT_TOKEN`：Telegram Bot Token
- `TELEGRAM_CHAT_ID`：用户 Telegram ID（可直接硬编码 8578764073）

## 触发场景

- 用户说 "给我张自拍"、"发一张 pic"、"send a selfie"
- 用户问 "what are you doing" / "你在干嘛"
- 用户说 "来一张"
