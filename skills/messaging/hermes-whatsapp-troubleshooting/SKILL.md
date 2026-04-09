---
name: hermes-whatsapp-troubleshooting
description: Hermes Agent WhatsApp integration troubleshooting — common issues and fixes
---

# Hermes Agent — WhatsApp 疑难排查

## 触发条件
当你遇到 Hermes Agent WhatsApp 配置完成但不回复消息时使用。

## 常见问题及解决方案

### 问题1：aprovals.mode: manual 导致消息被阻断
**症状：** Gateway 显示 connected，但 "Channel directory built: 0 target(s)"，消息无回复。
**原因：** `approvals.mode: manual` 要求所有消息手动审批，直接丢弃。
**解决：**
```yaml
# 编辑 ~/.hermes/config.yaml
approvals:
  mode: auto  # 从 manual 改为 auto
```
```bash
hermes gateway restart
```

### 问题2：给自己发消息无法测试
**症状：** 自发自收没有回应。
**原因：** WhatsApp 不把自发自收的消息路由给 bot。
**解决：** 让别人给你发消息，或用另一个 WhatsApp 账号测试。

### 问题3：Channel directory 始终 0 target(s)
**症状：** WhatsApp connected 但 channel count 为 0。
**原因：** approvals 阻挡，或 allowed_users 未配置。
**解决：** 确认 `whatsapp.allowed_users` 包含你的手机号（国际格式，无+号）：
```yaml
whatsapp:
  allowed_users:
    - "8613912345678"
```

### 问题4：WhatsApp Bridge 不断断开重连
**症状：** 日志显示 "[Whatsapp] Disconnected" 然后立即重连。
**原因：** 正常现象，只要最终显示 "whatsapp connected" 即可。

## 验证步骤
1. `hermes gateway status` 确认服务运行
2. `tail ~/.hermes/logs/gateway.log` 确认 "whatsapp connected"
3. 确认 `Channel directory built: N target(s)` N > 0
4. 发送测试消息，确认收到回复
