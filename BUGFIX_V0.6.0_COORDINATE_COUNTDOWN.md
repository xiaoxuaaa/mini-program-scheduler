# Bug 修复 - 坐标获取倒计时

## 问题描述

**Bug**：点击"获取当前位置"按钮时，立即获取坐标，导致获取到的是按钮位置而不是目标位置。

**影响**：无法正确获取目标坐标，用户体验差。

---

## 修复方案

### 实现 3 秒倒计时

点击"获取当前位置"后：
1. 显示提示："请移动鼠标到目标位置..."
2. 倒计时 3 秒（3...2...1...）
3. Toast 实时显示倒计时
4. 3 秒后自动获取鼠标位置
5. 显示成功提示："✓ 已获取坐标 (x, y)"

---

## 修复位置

**文件**：`static/app.js`

**修复的函数**：
1. `getCurrentPositionSimple()` - 简单任务坐标获取
2. `getCurrentPositionTimeline(pointId)` - 多时间点任务坐标获取

---

## 使用方式

### 修复后的操作流程

1. 点击 **"获取当前位置"** 按钮
2. 看到提示："请移动鼠标到目标位置..."
3. **快速移动鼠标到目标位置**（有 3 秒时间）
4. 等待倒计时（3...2...1...）
5. 坐标自动获取并填入表单
6. 看到确认提示："✓ 已获取坐标 (x, y)"

---

## 技术细节

### 实现代码

```javascript
async function getCurrentPositionSimple() {
    // 倒计时提示
    showToast('请移动鼠标到目标位置...', 'success');

    for (let i = 3; i > 0; i--) {
        showToast(`${i} 秒后获取坐标...`, 'success');
        await new Promise(resolve => setTimeout(resolve, 1000));
    }

    // 获取坐标
    const response = await fetch('/api/mouse/position');
    const result = await response.json();
    
    if (result.success) {
        const { x, y } = result.data;
        // 添加到表单...
        showToast(`✓ 已获取坐标 (${x}, ${y})`, 'success');
    }
}
```

### 关键点

- 使用 `async/await` 实现倒计时
- 每秒显示 Toast 提示
- 3 秒延迟确保用户有时间移动鼠标

---

## 优化建议

### 可配置倒计时（未实现）

可以让用户自定义倒计时时间：
- 快速模式：3 秒（默认）
- 标准模式：5 秒
- 慢速模式：10 秒

### 取消功能（未实现）

倒计时期间显示"取消"按钮，允许用户中止获取。

---

## 测试方法

1. 启动服务：`python app.py`
2. 访问 http://localhost:5000
3. 点击"添加任务"
4. 点击"获取当前位置"
5. 观察倒计时提示
6. 移动鼠标到任意位置
7. 等待 3 秒
8. 确认获取到正确的坐标

---

## 版本信息

**修复版本**：v0.6.0  
**修复日期**：2026-06-23  
**修复文件**：`static/app.js`  
**影响功能**：坐标获取（简单任务 + 多时间点任务）

---

## 相关问题

如果你觉得 3 秒太短或太长，可以修改代码：

**位置**：`static/app.js`

**修改倒计时时间**：
```javascript
// 修改这行的数字（当前是 3）
for (let i = 3; i > 0; i--) {
    showToast(`${i} 秒后获取坐标...`, 'success');
    await new Promise(resolve => setTimeout(resolve, 1000));
}
```

例如改为 5 秒：
```javascript
for (let i = 5; i > 0; i--) {
```

---

## 用户反馈

如有其他问题或建议，欢迎反馈！

---

**Bug 已修复，现在可以正确获取目标位置的坐标了！** ✅
