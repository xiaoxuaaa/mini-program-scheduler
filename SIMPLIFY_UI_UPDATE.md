# 界面简化更新 - 移除"简单任务"选项

**更新日期**: 2026-06-24  
**版本**: v0.7.2+  
**目的**: 为朋友使用简化界面，统一为操作编辑器

---

## 🎯 更新内容

### 移除的功能
- ❌ "简单任务"/"多时间点任务"切换标签
- ❌ 简单任务表单（单时间 + 坐标列表）
- ❌ 任务类型徽章显示
- ❌ `switchTaskType()` 函数
- ❌ `addSimpleCoordinate()` 函数
- ❌ `getCurrentPositionSimple()` 函数
- ❌ `currentTaskType` 全局变量

### 简化后的界面
- ✅ 统一使用操作编辑器（原多时间点任务）
- ✅ 默认打开就可以添加时间点和操作
- ✅ 更直观的操作流程
- ✅ 更少的选择困惑

---

## 📝 文件修改

### 1. `templates/index.html`

**移除内容**:
```html
<!-- 移除任务类型选择标签 -->
<div class="task-type-tabs">
    <div class="task-type-tab active" onclick="switchTaskType('simple', event)">简单任务</div>
    <div class="task-type-tab" onclick="switchTaskType('multi_time', event)">多时间点任务</div>
</div>

<!-- 移除简单任务表单 -->
<div id="simpleTaskForm">...</div>

<!-- 移除多时间点任务表单的隐藏 -->
<div id="multiTimeTaskForm" style="display: none;">...</div>
```

**替换为**:
```html
<!-- 任务表单 -->
<div id="taskForm">
    <div class="timeline-editor" id="timelineEditor"></div>
    <button type="button" class="btn btn-secondary btn-small" onclick="addTimelinePoint()">+ 添加时间点</button>
</div>
```

### 2. `static/app.js`

**移除**:
```javascript
let currentTaskType = 'simple';  // 不再需要
function switchTaskType(type, event) {...}  // 删除
function addSimpleCoordinate() {...}  // 删除
function getCurrentPositionSimple() {...}  // 删除
```

**简化任务渲染**:
```javascript
// 之前：根据 taskType 判断显示什么
const taskType = task.type || 'simple';
const typeLabel = taskType === 'multi_time' ? '多时间点' : '简单任务';

// 现在：统一显示时间点信息
const timeline = task.timeline || [];
let timeInfo = `<div class="task-time">${timeline.length > 0 ? timeline.length + ' 个时间点' : (task.time || '未设置')}</div>`;
```

**简化任务创建**:
```javascript
// 之前：根据 currentTaskType 分支处理
if (currentTaskType === 'simple') {
    // 简单任务逻辑
} else {
    // 多时间点任务逻辑
}

// 现在：直接使用操作编辑器
let taskData = {
    name,
    description,
    type: 'multi_time'
};
// 收集时间点...
```

**简化编辑任务**:
```javascript
// 自动兼容旧格式
if (!timeline.length && task.clicks && task.time) {
    // 将旧格式转换为新格式显示
    addTimelinePoint();
    // ...转换逻辑
}
```

---

## 🔄 向后兼容

### 旧任务自动转换
程序会自动将旧的"简单任务"格式转换为操作编辑器格式显示：

**旧格式**:
```json
{
  "type": "simple",
  "time": "14:30",
  "clicks": [[500, 600], [700, 800]]
}
```

**编辑时自动转换为**:
```
时间点 1: 14:30
  操作 1: 点击 (500, 600)
  操作 2: 点击 (700, 800)
```

---

## ✅ 测试检查

### 功能测试
- [x] 打开"添加任务"模态框，直接显示操作编辑器
- [x] 默认有一个时间点
- [x] 可以添加多个时间点
- [x] 可以添加点击/输入/按键/等待/粘贴操作
- [x] 保存任务成功
- [x] 任务列表正确显示时间点信息
- [x] 编辑新任务正常工作
- [x] 编辑旧格式任务自动转换显示

### 界面测试
- [x] 没有任务类型切换标签
- [x] 没有任务类型徽章
- [x] 界面更简洁
- [x] 移动端显示正常

---

## 📱 用户体验改进

### 之前（复杂）
```
用户打开添加任务
↓
看到"简单任务"和"多时间点任务"
↓
困惑：我应该选哪个？
↓
选择"简单任务"
↓
只能添加点击坐标
↓
想要按键操作，需要切换到"多时间点任务"
↓
重新配置
```

### 现在（简单）
```
用户打开添加任务
↓
直接看到操作编辑器
↓
添加时间点
↓
添加任意类型的操作（点击/按键/输入/等待）
↓
完成
```

---

## 🎉 优点

1. **降低学习成本** - 不需要理解"简单任务"和"多时间点任务"的区别
2. **减少选择困惑** - 只有一种方式添加任务
3. **功能更强大** - 统一使用最强大的操作编辑器
4. **界面更简洁** - 减少不必要的UI元素
5. **适合新手** - 朋友使用时更容易上手

---

## 💡 给朋友的使用说明

### 添加任务很简单
1. 点击"添加任务"
2. 输入任务名称（如：抢课）
3. 点击"+ 添加时间点"
4. 设置时间（如：20:57）
5. 点击"+ 点击"添加点击操作
6. 点击"获取当前位置"来获取坐标
7. 继续添加更多操作
8. 点击"创建任务"

### 操作类型
- **🖱️ 点击** - 点击某个位置
- **⌨️ 输入文本** - 输入英文（如网址）
- **📋 粘贴** - 粘贴中文或任何文本
- **🔘 按键** - 按键盘（如 Enter、Tab、Ctrl+C）
- **⏱️ 等待** - 等待几秒（如等待页面加载）

---

## 📚 相关文档

- **打包指南**: 需要创建给朋友用的 .exe
- **ngrok设置**: `NGROK_SETUP_GUIDE.md`
- **使用指南**: `WEB_GUIDE.md`

---

**更新完成**：界面已简化，适合发送给朋友使用！

下一步：打包成 .exe 或配置 ngrok 分享
