# ngrok 内网穿透设置指南

## 📥 第一步：下载 ngrok

1. 访问 https://ngrok.com/download
2. 下载 **Windows 64-bit** 版本
3. 解压到任意文件夹（建议：`C:\ngrok\`）

---

## 🔑 第二步：注册并获取 Token

1. 访问 https://ngrok.com/
2. 点击 **Sign up** 注册账号（免费）
3. 登录后，访问 https://dashboard.ngrok.com/get-started/your-authtoken
4. 复制你的 **Authtoken**（类似：`2abc123def456ghi789jkl0mn`）

---

## ⚙️ 第三步：配置 ngrok

打开命令行，切换到 ngrok 所在目录：

```bash
cd C:\ngrok

# 配置 authtoken（只需执行一次）
ngrok.exe config add-authtoken <粘贴你的token>
```

---

## 🚀 第四步：启动程序和 ngrok

### 终端 1：启动定时点击助手

```bash
cd "C:\learning materials\vibe coding\mini-program-scheduled-tasks"
python app.py
```

看到提示：
```
* Running on http://0.0.0.0:5000
```

### 终端 2：启动 ngrok

```bash
cd C:\ngrok
ngrok.exe http 5000
```

---

## 🌐 第五步：获取公网地址

ngrok 启动后会显示：

```
ngrok                                                                           

Session Status                online
Account                       你的账号 (Plan: Free)
Version                       3.x.x
Region                        United States (us)
Latency                       50ms
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123xyz.ngrok-free.app -> http://localhost:5000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**关键信息**：
- **公网地址**: `https://abc123xyz.ngrok-free.app`
- **本地监控**: `http://127.0.0.1:4040`（可以查看访问日志）

---

## 📱 第六步：分享给朋友

把 **公网地址** 发给朋友：

```
https://abc123xyz.ngrok-free.app
```

朋友在任何地方（手机、电脑）打开这个地址，就能访问你的程序了！

---

## ⚠️ 注意事项

### 免费版限制
- ✅ 每次启动域名会变（需要重新发给朋友）
- ✅ 有访问速度限制
- ✅ 每分钟请求数有限制
- ✅ 会显示 ngrok 的提示页面（点击"Visit Site"继续）

### 安全提示
- 🔒 使用 HTTPS 加密连接
- 🔒 不要把地址公开发在网上
- 🔒 只分享给信任的朋友

### 保持运行
- 💻 你的电脑必须一直运行
- 💻 `python app.py` 和 `ngrok` 都要保持运行
- 💻 关闭任意一个，朋友就无法访问

---

## 🔄 升级到付费版（可选）

如果需要固定域名，可以升级到 ngrok 付费版：

**Personal Plan ($10/月)**:
- ✅ 固定域名（域名不会变）
- ✅ 更快的速度
- ✅ 更多请求限制
- ✅ 去除 ngrok 提示页面

---

## 🐛 常见问题

### Q: 启动 ngrok 报错 "authtoken not configured"
**A**: 执行 `ngrok config add-authtoken <你的token>`

### Q: 朋友访问显示 "Tunnel not found"
**A**: 检查：
1. `python app.py` 是否在运行
2. `ngrok http 5000` 是否在运行
3. 端口是否是 5000

### Q: 访问很慢或超时
**A**: 
- 免费版有速度限制
- 尝试重启 ngrok
- 考虑升级付费版

### Q: 每次重启域名都变，太麻烦
**A**: 
- 升级到付费版获得固定域名
- 或使用 frp + 自己的域名

### Q: 想要固定域名但不想付费
**A**: 使用 frp 方案（需要自己有服务器或使用免费 frp 服务）

---

## 📊 方案对比

| 方案 | 优点 | 缺点 | 费用 |
|------|------|------|------|
| **ngrok 免费版** | 超简单，5分钟搞定 | 域名每次变 | 免费 |
| **ngrok 付费版** | 固定域名，速度快 | 需要付费 | $10/月 |
| **frp 免费服务** | 完全免费 | 配置复杂，服务不稳定 | 免费 |
| **frp + 自己服务器** | 完全可控 | 需要服务器 | 服务器费用 |

---

## 🎯 推荐方案

**如果只是偶尔用**：ngrok 免费版  
**如果经常用**：ngrok 付费版（$10/月）  
**如果预算有限且愿意折腾**：frp 免费服务

---

## 📚 相关文档

- ngrok 官网: https://ngrok.com/
- ngrok 文档: https://ngrok.com/docs
- 本项目 Web 指南: `WEB_GUIDE.md`

---

**创建日期**: 2026-06-24  
**版本**: v1.0
