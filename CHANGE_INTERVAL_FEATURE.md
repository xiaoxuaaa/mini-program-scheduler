# ⚡ 调整间隔功能 - 动态控制操作速度

**更新日期**: 2026-06-25  
**版本**: v0.7.4  

---

## 🎯 功能说明

新增 **"调整间隔"** 操作类型，允许在任务执行过程中动态改变操作之间的间隔时间。

### 使用场景

- 前几步操作正常速度（0.5秒），抢课时加速（0.2秒）
- 登录页面慢速操作（1秒），登录后快速操作（0.3秒）
- 先慢后快，或先快后慢，灵活调节

---

## 🚀 如何使用

### 步骤 1：创建任务

1. 添加时间点，设置默认间隔（如 0.5秒）
2. 添加前几个操作（点击、输入等）

### 步骤 2：插入"调整间隔"操作

1. 点击 **"⚡ 调整间隔"** 按钮
2. 设置新的间隔时间（如 0.2秒）
3. 添加描述（如："加速抢课"）

### 步骤 3：继续添加后续操作

- 后续所有操作将使用新的间隔时间
- 可以多次插入"调整间隔"操作

---

## 📝 完整示例

### 场景：小程序抢课

```
时间点：21:00，默认间隔 0.5秒

操作 1：[点击] 点击微信图标 (0.5秒后)
操作 2：[等待] 等待 2 秒
操作 3：[点击] 点击小程序入口 (0.5秒后)
操作 4：[点击] 点击课程列表 (0.5秒后)

操作 5：[⚡ 调整间隔] 改为 0.2秒 ← 加速开始

操作 6：[点击] 点击目标课程 (0.2秒后) ⚡
操作 7：[点击] 点击立即预约 (0.2秒后) ⚡
操作 8：[点击] 点击确认按钮 (0.2秒后) ⚡
操作 9：[粘贴] 粘贴学员姓名 (0.2秒后) ⚡

操作 10：[⚡ 调整间隔] 改为 0.5秒 ← 恢复正常

操作 11：[按键] 按 Enter 提交 (0.5秒后)
```

### 执行效果

- 操作 1-4：每步等待 0.5秒（正常速度）
- 操作 6-9：每步等待 0.2秒（加速）
- 操作 11：等待 0.5秒（恢复正常）

---

## 🎨 界面特点

### "⚡ 调整间隔" 按钮
- 位置：操作添加按钮组最右侧
- 颜色：橙色背景（#F2E3D6）
- 图标：⚡ 闪电图标

### 操作卡片
- 徽章颜色：橙色（#C4612F）
- 徽章标签：调整间隔
- 输入字段：
  - 操作描述（可自定义）
  - 新间隔时间（秒，支持小数）
- 提示文字：⚡ 此操作之后的所有操作将使用新的间隔时间

---

## 🔧 技术实现

### 后端 - `src/clicker.py`

#### 1. 新增操作类型

```python
elif action_type == "change_interval":
    # 调整间隔（这个操作本身不执行任何动作，只是标记）
    new_interval = action.get("interval", 0.5)
    print(f"  → {label}: 调整操作间隔为 {new_interval} 秒")
    return True
```

#### 2. 动态间隔执行

```python
def execute_actions(self, actions: List[Dict[str, Any]], interval: float = None) -> bool:
    current_interval = interval  # 当前间隔，可以动态改变
    
    for i, action in enumerate(actions, 1):
        # 检查是否是调整间隔操作
        if action.get("type") == "change_interval":
            new_interval = action.get("interval", 0.5)
            current_interval = new_interval
            print(f"  ⚡ 调整操作间隔为 {new_interval} 秒")
            continue  # 跳过等待，直接执行下一个操作
        
        if not self.execute_action(action):
            success = False
        
        # 使用当前间隔
        if i < len(actions):
            time.sleep(current_interval)
```

### 前端 - `static/app.js`

#### 1. 添加操作类型映射

```javascript
let badgeLabel = {
    'click': '点击',
    'type': '输入',
    'paste': '粘贴',
    'hotkey': '按键',
    'wait': '等待',
    'change_interval': '调整间隔'  // 新增
}[actionType];
```

#### 2. 操作表单 HTML

```javascript
case 'change_interval':
    return `
        <input type="text" placeholder="操作描述" class="form-input" 
               data-action-field="label" value="调整操作间隔">
        <input type="number" placeholder="新间隔(秒)" class="form-input" 
               data-action-field="interval" value="0.3" 
               step="0.1" min="0.1" max="5" style="max-width: 150px;">
        <small style="width: 100%; color: #5C635D; font-size: 12px; margin-top: 4px;">
            ⚡ 此操作之后的所有操作将使用新的间隔时间
        </small>
    `;
```

#### 3. 数据收集

```javascript
const typeMap = {
    '点击': 'click',
    '输入': 'type',
    '粘贴': 'paste',
    '按键': 'hotkey',
    '等待': 'wait',
    '调整间隔': 'change_interval'  // 新增
};
```

### 前端样式 - `templates/index.html`

```css
.action-type-badge.change_interval {
    background: #F2E3D6;
    color: #C4612F;
    font-weight: 600;
}
```

---

## 📁 文件修改

### 1. `src/clicker.py`
- 在 `execute_action()` 添加 `change_interval` 类型处理
- 修改 `execute_actions()` 支持动态间隔

### 2. `static/app.js`
- 添加 `change_interval` 到类型映射
- 添加 `change_interval` 表单 HTML
- 添加 `change_interval` 按钮

### 3. `templates/index.html`
- 添加 `change_interval` CSS 样式
- 更新帮助文档操作类型说明
- 更新示例2展示用法

---

## ✅ 优点

1. **灵活控制**：无需固定间隔，可随意调整
2. **操作简单**：只需插入一个操作即可
3. **逻辑清晰**：一目了然哪里改变速度
4. **可多次调整**：慢→快→慢都可以
5. **向后兼容**：不影响现有任务

---

## ⚠️ 注意事项

1. **间隔范围**：建议 0.1秒 - 5秒
2. **最小值**：不建议小于 0.1秒（可能导致操作失败）
3. **抢课建议**：0.2 - 0.3秒是较好的平衡
4. **执行顺序**：调整间隔操作本身不消耗时间

---

## 🎯 使用建议

### 推荐间隔设置

| 场景 | 推荐间隔 | 说明 |
|------|---------|------|
| 正常操作 | 0.5秒 | 默认值，适合大部分场景 |
| 抢课/抢购 | 0.2-0.3秒 | 快速但稳定 |
| 等待加载 | 1-2秒 | 页面加载、动画等 |
| 超快速 | 0.1秒 | 极限速度，可能不稳定 |

### 最佳实践

1. **前慢后快**：准备操作慢一点，关键操作快一点
2. **测试间隔**：先测试确定最优间隔值
3. **适当保守**：间隔太快可能导致操作失败
4. **多次调整**：不同阶段可以多次调整

---

## 📊 性能对比

### 场景：5个抢课操作

| 方案 | 总时间 | 说明 |
|------|--------|------|
| 固定 0.5秒 | 2.5秒 | 5 × 0.5 = 2.5s |
| 固定 0.2秒 | 1.0秒 | 5 × 0.2 = 1.0s |
| **动态调整** | **可变** | 前面慢，抢课快 |

---

## 🔄 向后兼容

- ✅ 旧任务不受影响（不包含 `change_interval` 操作）
- ✅ 新功能可选（不强制使用）
- ✅ 默认间隔保持不变

---

## 💡 常见问题

### Q: 调整间隔操作本身需要时间吗？
A: 不需要。它只是一个标记，不消耗执行时间。

### Q: 可以多次调整间隔吗？
A: 可以。每次调整都会影响后续操作。

### Q: 间隔最小可以设置多少？
A: 最小 0.1秒，但建议不低于 0.2秒以确保稳定性。

### Q: 调整间隔会影响"等待"操作吗？
A: 不会。"等待"操作有自己的等待时间。

---

**功能已完成！** ✅  
现在你可以灵活控制操作速度，让抢课更快更稳！🚀
