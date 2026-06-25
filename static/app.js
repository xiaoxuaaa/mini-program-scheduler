// 全局变量
let tasks = [];
let timelinePointCounter = 0;
let editingTaskId = null;  // 当前正在编辑的任务ID
let actionCounter = 0;  // 操作计数器

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    loadTasks();
    updateSchedulerStatus();
    setInterval(updateSchedulerStatus, 3000);
});

// ==================== 任务列表相关 ====================

// 加载任务列表
async function loadTasks() {
    try {
        const response = await fetch('/api/tasks');
        const result = await response.json();

        if (result.success) {
            tasks = result.data;
            renderTasks();
        }
    } catch (error) {
        showToast('加载任务失败', 'error');
    }
}

// 渲染任务列表
function renderTasks() {
    const taskList = document.getElementById('taskList');
    const taskCount = document.getElementById('taskCount');

    taskCount.textContent = `${tasks.length} 个任务`;

    if (tasks.length === 0) {
        taskList.innerHTML = `
            <div class="empty-state">
                <p>暂无任务，点击上方"添加任务"开始</p>
            </div>
        `;
        return;
    }

    taskList.innerHTML = tasks.map(task => {
        const timeline = task.timeline || [];
        const timeLabel = timeline.length > 0
            ? timeline.map(t => t.time).join(', ')
            : (task.time || '未设置');

        let timeInfo = `<div class="task-time">${timeline.length > 0 ? timeline.length + ' 个时间点' : (task.time || '未设置')}</div>`;
        let detailInfo = timeline.length > 0
            ? `时间: ${timeline.map(t => t.time).join(', ')}`
            : `${task.clicks?.length || 0} 个点击坐标`;

        return `
            <div class="task-card ${task.enabled ? '' : 'disabled'}">
                <div class="task-header">
                    <div>
                        <div class="task-title">
                            ${task.name}
                        </div>
                        <div class="task-info">${task.description || '无描述'}</div>
                    </div>
                    ${timeInfo}
                </div>
                <div class="task-info">
                    ${detailInfo}
                    ${task.last_run ? ` · 上次运行: ${new Date(task.last_run).toLocaleString('zh-CN')}` : ''}
                </div>
                <div class="task-actions">
                    <button class="btn btn-secondary btn-small" onclick="editTask(${task.id})">编辑</button>
                    <button class="btn btn-secondary btn-small" onclick="toggleTask(${task.id})">
                        ${task.enabled ? '禁用' : '启用'}
                    </button>
                    <button class="btn btn-secondary btn-small" onclick="deleteTask(${task.id})">删除</button>
                </div>
            </div>
        `;
    }).join('');
}

// ==================== 调度器控制 ====================

// 更新调度器状态
async function updateSchedulerStatus() {
    try {
        const response = await fetch('/api/scheduler/status');
        const result = await response.json();

        if (result.success) {
            const { running } = result.data;
            const statusDot = document.getElementById('statusDot');
            const statusText = document.getElementById('statusText');
            const startBtn = document.getElementById('startBtn');
            const stopBtn = document.getElementById('stopBtn');

            if (running) {
                statusDot.classList.add('active');
                statusText.textContent = '调度器运行中';
                startBtn.disabled = true;
                stopBtn.disabled = false;
            } else {
                statusDot.classList.remove('active');
                statusText.textContent = '调度器未运行';
                startBtn.disabled = false;
                stopBtn.disabled = true;
            }
        }
    } catch (error) {
        console.error('获取状态失败', error);
    }
}

// 启动调度器
async function startScheduler() {
    try {
        const response = await fetch('/api/scheduler/start', { method: 'POST' });
        const result = await response.json();
        showToast(result.message, result.success ? 'success' : 'error');
        updateSchedulerStatus();
    } catch (error) {
        showToast('启动失败', 'error');
    }
}

// 停止调度器
async function stopScheduler() {
    try {
        const response = await fetch('/api/scheduler/stop', { method: 'POST' });
        const result = await response.json();
        showToast(result.message, result.success ? 'success' : 'error');
        updateSchedulerStatus();
    } catch (error) {
        showToast('停止失败', 'error');
    }
}

// ==================== 任务操作 ====================

// 切换任务状态
async function toggleTask(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}/toggle`, { method: 'POST' });
        const result = await response.json();
        showToast(result.message, result.success ? 'success' : 'error');
        loadTasks();
    } catch (error) {
        showToast('操作失败', 'error');
    }
}

// 删除任务
async function deleteTask(taskId) {
    if (!confirm('确定要删除这个任务吗？')) return;

    try {
        const response = await fetch(`/api/tasks/${taskId}`, { method: 'DELETE' });
        const result = await response.json();
        showToast(result.message, result.success ? 'success' : 'error');
        loadTasks();
    } catch (error) {
        showToast('删除失败', 'error');
    }
}

// ==================== 操作编辑器相关 ====================

// 添加时间轴操作
function addTimelineAction(pointId, actionType) {
    const point = document.querySelector(`[data-point-id="${pointId}"]`);
    const actionsEditor = point.querySelector('[data-field="actions"]');

    // 移除空状态提示
    const emptyState = actionsEditor.querySelector('.empty-actions');
    if (emptyState) {
        emptyState.remove();
    }

    const actionId = actionCounter++;
    const div = document.createElement('div');
    div.className = 'action-item';
    div.dataset.actionId = actionId;

    let badgeClass = actionType;
    let badgeLabel = {
        'click': '点击',
        'type': '输入',
        'paste': '粘贴',
        'hotkey': '按键',
        'wait': '等待'
    }[actionType];

    div.innerHTML = `
        <div class="action-item-header">
            <span class="action-type-badge ${badgeClass}">${badgeLabel}</span>
            <div class="action-buttons">
                <button type="button" class="btn btn-secondary btn-icon" onclick="moveActionUp(this)" title="上移">↑</button>
                <button type="button" class="btn btn-secondary btn-icon" onclick="moveActionDown(this)" title="下移">↓</button>
                <button type="button" class="btn btn-secondary btn-icon" onclick="removeAction(this)" title="删除">×</button>
            </div>
        </div>
        <div class="action-item-body">
            ${getActionBodyHTML(actionType, actionId)}
        </div>
    `;

    actionsEditor.appendChild(div);
}

// 获取操作主体HTML
function getActionBodyHTML(actionType, actionId) {
    switch (actionType) {
        case 'click':
            return `
                <input type="text" placeholder="操作描述" class="form-input" data-action-field="label" value="点击操作">
                <input type="number" placeholder="X坐标" class="form-input" data-action-field="x">
                <input type="number" placeholder="Y坐标" class="form-input" data-action-field="y">
                <input type="number" placeholder="点击次数" class="form-input" data-action-field="clicks" value="1" min="1" max="3" style="max-width: 100px;">
                <button type="button" class="btn btn-secondary btn-small" onclick="getCurrentMousePosition(${actionId})">获取坐标</button>
            `;

        case 'type':
            return `
                <input type="text" placeholder="操作描述" class="form-input" data-action-field="label" value="输入文本（仅英文）">
                <input type="text" placeholder="要输入的文本" class="form-input" data-action-field="text" style="flex: 2;">
                <input type="number" placeholder="字符间隔(秒)" class="form-input" data-action-field="interval" value="0.05" step="0.01" min="0" style="max-width: 120px;">
            `;

        case 'paste':
            return `
                <input type="text" placeholder="操作描述" class="form-input" data-action-field="label" value="粘贴文本（支持中文）">
                <input type="text" placeholder="要粘贴的文本（支持中文）" class="form-input" data-action-field="text" style="flex: 2;">
            `;

        case 'hotkey':
            return `
                <input type="text" placeholder="操作描述" class="form-input" data-action-field="label" value="按键操作">
                <input type="text" placeholder="按键（用+分隔，如：ctrl+c）" class="form-input" data-action-field="keys" style="flex: 2;">
                <small style="width: 100%; color: #5C635D; font-size: 12px; margin-top: 4px;">
                    示例: enter, tab, ctrl+c, ctrl+v, alt+tab, win+d
                </small>
            `;

        case 'wait':
            return `
                <input type="text" placeholder="操作描述" class="form-input" data-action-field="label" value="等待">
                <input type="number" placeholder="等待秒数" class="form-input" data-action-field="seconds" value="1" step="0.1" min="0" style="max-width: 150px;">
            `;

        default:
            return '';
    }
}

// 移除操作
function removeAction(button) {
    const actionItem = button.closest('.action-item');
    const actionsEditor = actionItem.closest('.actions-editor');

    actionItem.remove();

    // 如果没有操作了，显示空状态
    if (actionsEditor.querySelectorAll('.action-item').length === 0) {
        actionsEditor.innerHTML = '<div class="empty-actions">暂无操作，点击下方按钮添加</div>';
    }
}

// 上移操作
function moveActionUp(button) {
    const actionItem = button.closest('.action-item');
    const prevItem = actionItem.previousElementSibling;

    // 如果不是第一个，且上一个不是空状态提示
    if (prevItem && !prevItem.classList.contains('empty-actions')) {
        actionItem.parentNode.insertBefore(actionItem, prevItem);
    }
}

// 下移操作
function moveActionDown(button) {
    const actionItem = button.closest('.action-item');
    const nextItem = actionItem.nextElementSibling;

    // 如果不是最后一个
    if (nextItem) {
        actionItem.parentNode.insertBefore(nextItem, actionItem);
    }
}

// 获取当前鼠标位置（用于操作）
async function getCurrentMousePosition(actionId) {
    showToast('请移动鼠标到目标位置...', 'success');

    for (let i = 10; i > 0; i--) {
        showToast(`${i} 秒后获取坐标...`, 'success');
        await new Promise(resolve => setTimeout(resolve, 1000));
    }

    try {
        const response = await fetch('/api/mouse/position');
        const result = await response.json();

        if (result.success) {
            const { x, y } = result.data;
            const actionItem = document.querySelector(`[data-action-id="${actionId}"]`);

            if (actionItem) {
                actionItem.querySelector('[data-action-field="x"]').value = x;
                actionItem.querySelector('[data-action-field="y"]').value = y;
                showToast(`✓ 已获取坐标 (${x}, ${y})`, 'success');
            }
        }
    } catch (error) {
        showToast('获取坐标失败', 'error');
    }
}

// 从操作编辑器收集数据
function collectActionsFromEditor(actionsEditor) {
    const actions = [];
    const actionItems = actionsEditor.querySelectorAll('.action-item');

    actionItems.forEach(item => {
        const actionType = item.querySelector('.action-type-badge').textContent.trim();
        const typeMap = {
            '点击': 'click',
            '输入': 'type',
            '粘贴': 'paste',
            '按键': 'hotkey',
            '等待': 'wait'
        };

        const type = typeMap[actionType];
        const action = { type };

        // 收集该操作的所有字段
        const fields = item.querySelectorAll('[data-action-field]');
        fields.forEach(field => {
            const fieldName = field.dataset.actionField;
            let value = field.value;

            // 类型转换
            if (fieldName === 'x' || fieldName === 'y' || fieldName === 'clicks') {
                value = parseInt(value) || 0;
            } else if (fieldName === 'seconds' || fieldName === 'interval') {
                value = parseFloat(value) || 0;
            } else if (fieldName === 'keys') {
                // 将字符串分割成数组
                value = value.split('+').map(k => k.trim()).filter(k => k);
            }

            action[fieldName] = value;
        });

        actions.push(action);
    });

    return actions;
}

// ==================== 时间轴点编辑 ====================

// 添加时间轴点
function addTimelinePoint() {
    const editor = document.getElementById('timelineEditor');
    const pointId = timelinePointCounter++;

    const div = document.createElement('div');
    div.className = 'timeline-point';
    div.dataset.pointId = pointId;
    div.innerHTML = `
        <div class="timeline-point-header">
            <div class="timeline-point-title">时间点 ${pointId + 1}</div>
            <button type="button" class="timeline-point-remove" onclick="removeTimelinePoint(${pointId})">×</button>
        </div>

        <div class="form-group">
            <label class="form-label">步骤名称 *</label>
            <input type="text" class="form-input" data-field="name" placeholder="例如：登录并抢课">
        </div>

        <div class="form-group">
            <label class="form-label">执行时间 *</label>
            <input type="time" class="form-input" data-field="time">
        </div>

        <div class="form-group">
            <label class="form-label">
                <input type="checkbox" data-field="show_desktop"> 执行前回到桌面（Win+D）
            </label>
        </div>

        <div class="form-group">
            <label class="form-label">操作间隔（秒）</label>
            <input type="number" step="0.1" class="form-input" data-field="interval" value="0.5" placeholder="0.5">
        </div>

        <div class="form-group">
            <label class="form-label">操作序列 *</label>
            <div class="actions-editor" data-field="actions">
                <div class="empty-actions">暂无操作，点击下方按钮添加</div>
            </div>
            <div class="action-add-buttons">
                <button type="button" class="btn btn-secondary btn-small" onclick="addTimelineAction(${pointId}, 'click')">+ 点击</button>
                <button type="button" class="btn btn-secondary btn-small" onclick="addTimelineAction(${pointId}, 'type')">+ 输入文本</button>
                <button type="button" class="btn btn-secondary btn-small" onclick="addTimelineAction(${pointId}, 'paste')">+ 粘贴</button>
                <button type="button" class="btn btn-secondary btn-small" onclick="addTimelineAction(${pointId}, 'hotkey')">+ 按键</button>
                <button type="button" class="btn btn-secondary btn-small" onclick="addTimelineAction(${pointId}, 'wait')">+ 等待</button>
            </div>
        </div>
    `;

    editor.appendChild(div);
}

// 移除时间轴点
function removeTimelinePoint(pointId) {
    const point = document.querySelector(`[data-point-id="${pointId}"]`);
    if (point) {
        point.remove();
    }
}

// ==================== 模态框控制 ====================

// 打开添加任务模态框
function openAddTaskModal() {
    editingTaskId = null;
    document.getElementById('addTaskModal').classList.add('active');
    document.querySelector('.modal-header').textContent = '添加新任务';
    document.getElementById('submitTaskBtn').textContent = '创建任务';
    document.getElementById('taskName').value = '';
    document.getElementById('taskDesc').value = '';

    // 清空时间轴编辑器
    const editor = document.getElementById('timelineEditor');
    editor.innerHTML = '';
    timelinePointCounter = 0;
    actionCounter = 0;

    // 添加一个默认时间点
    addTimelinePoint();
}

// 关闭模态框
function closeAddTaskModal() {
    document.getElementById('addTaskModal').classList.remove('active');
}

// ==================== 创建/更新任务 ====================

// 创建任务
async function createTask() {
    const name = document.getElementById('taskName').value.trim();
    const description = document.getElementById('taskDesc').value.trim();

    if (!name) {
        showToast('请输入任务名称', 'error');
        return;
    }

    let taskData = {
        name,
        description,
        type: 'multi_time'
    };

    // 收集时间点任务
    const points = document.querySelectorAll('.timeline-point');
    const timeline = [];

    for (let point of points) {
        const pointName = point.querySelector('[data-field="name"]').value.trim();
        const pointTime = point.querySelector('[data-field="time"]').value;
        const showDesktop = point.querySelector('[data-field="show_desktop"]').checked;
        const interval = parseFloat(point.querySelector('[data-field="interval"]').value) || 0.5;

        const actionsEditor = point.querySelector('[data-field="actions"]');
        const actions = collectActionsFromEditor(actionsEditor);

        if (!pointName || !pointTime) {
            showToast('请完整填写所有时间点的名称和时间', 'error');
            return;
        }

        if (actions.length === 0) {
            showToast(`时间点"${pointName}"至少需要一个操作`, 'error');
            return;
        }

        timeline.push({
            time: pointTime,
            name: pointName,
            show_desktop: showDesktop,
            actions: actions,
            interval: interval
        });
    }

    if (timeline.length === 0) {
        showToast('请至少添加一个时间点', 'error');
        return;
    }

    taskData.timeline = timeline;

    // 发送请求
    try {
        let response;
        if (editingTaskId) {
            response = await fetch(`/api/tasks/${editingTaskId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(taskData)
            });
        } else {
            response = await fetch('/api/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(taskData)
            });
        }

        const result = await response.json();
        showToast(result.message, result.success ? 'success' : 'error');

        if (result.success) {
            closeAddTaskModal();
            loadTasks();
        }
    } catch (error) {
        showToast(editingTaskId ? '更新任务失败' : '创建任务失败', 'error');
    }
}

// ==================== 编辑任务 ====================

async function editTask(taskId) {
    try {
        const response = await fetch(`/api/tasks/${taskId}`);
        const result = await response.json();

        if (!result.success) {
            showToast('获取任务失败', 'error');
            return;
        }

        const task = result.data;
        editingTaskId = taskId;

        document.getElementById('addTaskModal').classList.add('active');
        document.querySelector('.modal-header').textContent = '编辑任务';
        document.getElementById('submitTaskBtn').textContent = '更新任务';
        document.getElementById('taskName').value = task.name || '';
        document.getElementById('taskDesc').value = task.description || '';

        const editor = document.getElementById('timelineEditor');
        editor.innerHTML = '';
        timelinePointCounter = 0;
        actionCounter = 0;

        const timeline = task.timeline || [];

        // 如果是旧格式（simple任务），转换为新格式
        if (!timeline.length && task.clicks && task.time) {
            addTimelinePoint();
            const pointId = timelinePointCounter - 1;
            const pointDiv = document.querySelector(`[data-point-id="${pointId}"]`);
            pointDiv.querySelector('[data-field="name"]').value = '点击操作';
            pointDiv.querySelector('[data-field="time"]').value = task.time;

            const actionsEditor = pointDiv.querySelector('[data-field="actions"]');
            actionsEditor.innerHTML = '';

            task.clicks.forEach(click => {
                addTimelineAction(pointId, 'click');
                const lastActionItem = actionsEditor.lastElementChild;
                lastActionItem.querySelector('[data-action-field="x"]').value = click[0];
                lastActionItem.querySelector('[data-action-field="y"]').value = click[1];
                if (click[2]) {
                    lastActionItem.querySelector('[data-action-field="clicks"]').value = click[2];
                }
            });
        } else {
            // 新格式，直接加载
            timeline.forEach((point, index) => {
                addTimelinePoint();
                const pointId = timelinePointCounter - 1;

                const pointDiv = document.querySelector(`[data-point-id="${pointId}"]`);
                pointDiv.querySelector('[data-field="name"]').value = point.name || '';
                pointDiv.querySelector('[data-field="time"]').value = point.time || '';
                pointDiv.querySelector('[data-field="show_desktop"]').checked = point.show_desktop || false;
                pointDiv.querySelector('[data-field="interval"]').value = point.interval || 0.5;

                // 加载操作
                const actions = point.actions || [];
                const actionsEditor = pointDiv.querySelector('[data-field="actions"]');

                if (actions.length > 0) {
                    actionsEditor.innerHTML = '';
                    actions.forEach(action => {
                        addTimelineAction(pointId, action.type);
                        const lastActionItem = actionsEditor.lastElementChild;

                        // 填充字段
                        Object.keys(action).forEach(key => {
                            if (key === 'type') return;

                            const field = lastActionItem.querySelector(`[data-action-field="${key}"]`);
                            if (field) {
                                if (key === 'keys' && Array.isArray(action[key])) {
                                    field.value = action[key].join('+');
                                } else {
                                    field.value = action[key];
                                }
                            }
                        });
                    });
                }
            });
        }
    } catch (error) {
        console.error('编辑任务错误:', error);
        showToast('编辑失败: ' + error.message, 'error');
    }
}

// ==================== 工具函数 ====================

// Toast 通知
function showToast(message, type = 'success') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// 点击模态框背景关闭
document.getElementById('addTaskModal').addEventListener('click', function(e) {
    if (e.target === this) {
        closeAddTaskModal();
    }
});
