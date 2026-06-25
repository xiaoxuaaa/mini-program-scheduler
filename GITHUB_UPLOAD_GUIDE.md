# 📤 上传到 GitHub 指南

## 前提条件

✅ Git 已安装  
✅ 拥有 GitHub 账号  

---

## 方式 1：使用命令行（推荐）

### 1. 配置 Git（首次使用）

```bash
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
```

### 2. 在 GitHub 上创建仓库

1. 登录 https://github.com
2. 点击右上角 "+" → "New repository"
3. 填写：
   - Repository name: `mini-program-scheduler`
   - Description: `定时点击助手 - 自动化工具`
   - 选择 Public 或 Private
   - **不要**勾选 "Add a README file"
4. 点击 "Create repository"

### 3. 初始化本地仓库

```bash
cd "C:\learning materials\vibe coding\mini-program-scheduled-tasks"

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: v0.7.2 - 功能完整版本"

# 设置主分支为 main
git branch -M main
```

### 4. 关联远程仓库并推送

```bash
# 关联（替换为你的 GitHub 用户名和仓库名）
git remote add origin https://github.com/你的用户名/mini-program-scheduler.git

# 推送
git push -u origin main
```

第一次推送会要求输入 GitHub 用户名和密码（或 Personal Access Token）

---

## 方式 2：使用 GitHub Desktop（更简单）

### 1. 打开 GitHub Desktop

### 2. 添加仓库

- File → Add Local Repository
- 选择项目文件夹：`C:\learning materials\vibe coding\mini-program-scheduled-tasks`
- 如果提示"不是 Git 仓库"，点击 "Create a repository"

### 3. 提交更改

- 在左侧看到所有文件
- 输入 Commit message: `Initial commit: v0.7.2`
- 点击 "Commit to main"

### 4. 发布到 GitHub

- 点击 "Publish repository"
- 填写仓库名和描述
- 点击 "Publish Repository"

---

## 📝 重要提醒

### 已自动排除的文件（.gitignore）

以下文件**不会**上传到 GitHub：
- ✅ `config/tasks.json` - 你的任务配置（保护隐私）
- ✅ `__pycache__/` - Python 缓存
- ✅ `.claude/` - Claude 相关文件
- ✅ `*_old.*` - 备份文件

### 会上传的文件

- ✅ 所有源代码（`.py`, `.js`, `.html`, `.css`）
- ✅ 文档文件（`.md`）
- ✅ 配置示例（`tasks.example.json`）
- ✅ 依赖列表（`requirements.txt`）

---

## 🔐 GitHub Token 设置（如果需要）

如果 GitHub 要求 Personal Access Token：

1. 访问 https://github.com/settings/tokens
2. "Generate new token" → "Classic"
3. 勾选 `repo` 权限
4. 生成并复制 Token
5. 推送时使用 Token 作为密码

---

## ✅ 验证上传成功

1. 访问 `https://github.com/你的用户名/mini-program-scheduler`
2. 看到所有文件
3. README 显示正常

---

## 🔄 后续更新代码

修改代码后，更新到 GitHub：

```bash
git add .
git commit -m "更新说明"
git push
```

或使用 GitHub Desktop：
1. 查看更改
2. 输入更新说明
3. Commit → Push

---

## 🚀 分享给朋友

上传成功后，把仓库地址发给朋友：

```
https://github.com/你的用户名/mini-program-scheduler
```

朋友可以：
```bash
git clone https://github.com/你的用户名/mini-program-scheduler.git
cd mini-program-scheduler
pip install -r requirements.txt
python app.py
```

---

## 💡 进阶：添加 GitHub Actions（自动化）

可以配置自动化测试、部署等，需要的话再告诉我！

---

**准备好了吗？重启终端，然后按照上面的步骤操作！** 🚀
