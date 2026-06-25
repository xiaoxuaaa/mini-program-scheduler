"""
定时点击助手 - Web 服务
Flask API 后端
"""

import sys
import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config_manager import ConfigManager
from src.scheduler import TaskScheduler
from src.clicker import Clicker
from src.web_clicker import WebClicker

app = Flask(__name__)
CORS(app)  # 允许跨域访问

# 全局实例
config_manager = ConfigManager()
scheduler = None
clicker = Clicker()
web_clicker = None  # 网页点击器实例


# ==================== 页面路由 ====================

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')


# ==================== API 路由 ====================

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """获取所有任务"""
    tasks = config_manager.load_tasks()
    return jsonify({
        'success': True,
        'data': tasks
    })


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """创建新任务（支持简单任务和多时间点任务）"""
    data = request.json

    name = data.get('name', '').strip()
    description = data.get('description', '').strip()
    task_type = data.get('type', 'simple')

    # 验证必填字段
    if not name:
        return jsonify({
            'success': False,
            'message': '任务名称不能为空'
        }), 400

    # 简单任务
    if task_type == 'simple':
        time_str = data.get('time', '').strip()
        clicks = data.get('clicks', [])

        if not time_str or not clicks:
            return jsonify({
                'success': False,
                'message': '缺少必填字段（时间或坐标）'
            }), 400

        if config_manager.add_task(name, time_str, clicks, description, task_type="simple"):
            return jsonify({
                'success': True,
                'message': '任务创建成功'
            })

    # 多时间点任务
    elif task_type == 'multi_time':
        timeline = data.get('timeline', [])

        if not timeline:
            return jsonify({
                'success': False,
                'message': '时间轴不能为空'
            }), 400

        if config_manager.add_task(name, description=description, timeline=timeline, task_type="multi_time"):
            return jsonify({
                'success': True,
                'message': '多时间点任务创建成功'
            })

    else:
        return jsonify({
            'success': False,
            'message': f'不支持的任务类型: {task_type}'
        }), 400

    return jsonify({
        'success': False,
        'message': '任务创建失败'
    }), 500


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """获取单个任务详情"""
    task = config_manager.get_task(task_id)

    if not task:
        return jsonify({
            'success': False,
            'message': '任务不存在'
        }), 404

    return jsonify({
        'success': True,
        'data': task
    })


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """更新任务"""
    task = config_manager.get_task(task_id)

    if not task:
        return jsonify({
            'success': False,
            'message': '任务不存在'
        }), 404

    data = request.json

    # 更新任务数据
    update_data = {}

    if 'name' in data:
        update_data['name'] = data['name']
    if 'description' in data:
        update_data['description'] = data['description']
    if 'type' in data:
        update_data['type'] = data['type']

    # 简单任务
    if data.get('type') == 'simple' or task.get('type') == 'simple':
        if 'time' in data:
            update_data['time'] = data['time']
        if 'clicks' in data:
            update_data['clicks'] = data['clicks']

    # 多时间点任务
    if data.get('type') == 'multi_time' or task.get('type') == 'multi_time':
        if 'timeline' in data:
            update_data['timeline'] = data['timeline']

    if config_manager.update_task(task_id, **update_data):
        return jsonify({
            'success': True,
            'message': '任务更新成功'
        })
    else:
        return jsonify({
            'success': False,
            'message': '任务更新失败'
        }), 500


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """删除任务"""
    if config_manager.remove_task(task_id):
        return jsonify({
            'success': True,
            'message': '任务已删除'
        })
    else:
        return jsonify({
            'success': False,
            'message': '任务不存在'
        }), 404


@app.route('/api/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """启用/禁用任务"""
    task = config_manager.get_task(task_id)

    if not task:
        return jsonify({
            'success': False,
            'message': '任务不存在'
        }), 404

    new_status = not task.get('enabled', True)

    if config_manager.update_task(task_id, enabled=new_status):
        return jsonify({
            'success': True,
            'message': f"任务已{'启用' if new_status else '禁用'}",
            'enabled': new_status
        })
    else:
        return jsonify({
            'success': False,
            'message': '操作失败'
        }), 500


@app.route('/api/scheduler/start', methods=['POST'])
def start_scheduler():
    """启动调度器"""
    global scheduler

    if scheduler and scheduler.is_running():
        return jsonify({
            'success': False,
            'message': '调度器已在运行中'
        }), 400

    scheduler = TaskScheduler(config_manager)

    if scheduler.start():
        return jsonify({
            'success': True,
            'message': '调度器已启动'
        })
    else:
        return jsonify({
            'success': False,
            'message': '调度器启动失败'
        }), 500


@app.route('/api/scheduler/stop', methods=['POST'])
def stop_scheduler():
    """停止调度器"""
    global scheduler

    if not scheduler or not scheduler.is_running():
        return jsonify({
            'success': False,
            'message': '调度器未运行'
        }), 400

    if scheduler.stop():
        return jsonify({
            'success': True,
            'message': '调度器已停止'
        })
    else:
        return jsonify({
            'success': False,
            'message': '停止失败'
        }), 500


@app.route('/api/scheduler/status', methods=['GET'])
def get_scheduler_status():
    """获取调度器状态"""
    global scheduler

    if not scheduler:
        return jsonify({
            'success': True,
            'data': {
                'running': False,
                'message': '调度器未初始化'
            }
        })

    return jsonify({
        'success': True,
        'data': {
            'running': scheduler.is_running(),
            'message': scheduler.get_status()
        }
    })


@app.route('/api/mouse/position', methods=['GET'])
def get_mouse_position():
    """获取当前鼠标坐标"""
    x, y = clicker.get_current_position()
    return jsonify({
        'success': True,
        'data': {
            'x': x,
            'y': y
        }
    })


# ==================== 网页选择器 API ====================

@app.route('/api/web/start-selector', methods=['POST'])
def start_web_selector():
    """启动网页选择器，打开浏览器供用户点击元素"""
    global web_clicker

    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({
            'success': False,
            'message': '请提供网页地址'
        }), 400

    try:
        # 关闭之前的浏览器（如果有）
        if web_clicker:
            web_clicker.close()

        # 创建新的 WebClicker
        web_clicker = WebClicker()

        # 启动浏览器
        if not web_clicker.start_browser(url):
            return jsonify({
                'success': False,
                'message': '启动浏览器失败'
            }), 500

        # 注入选择器脚本
        import time
        time.sleep(2)  # 等待页面加载

        if not web_clicker.inject_selector_script():
            return jsonify({
                'success': False,
                'message': '注入选择器脚本失败'
            }), 500

        return jsonify({
            'success': True,
            'message': '浏览器已打开，请点击要抢的按钮'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'启动失败: {str(e)}'
        }), 500


@app.route('/api/web/get-selector', methods=['GET'])
def get_web_selector():
    """获取用户选中的元素信息"""
    global web_clicker

    if not web_clicker:
        return jsonify({
            'success': False,
            'message': '请先启动网页选择器'
        }), 400

    try:
        selector_info = web_clicker.get_selected_element()

        if not selector_info:
            return jsonify({
                'success': False,
                'message': '尚未选择元素'
            }), 400

        return jsonify({
            'success': True,
            'data': selector_info
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'获取选择器失败: {str(e)}'
        }), 500


@app.route('/api/web/test-selector', methods=['POST'])
def test_web_selector():
    """测试选择器是否有效"""
    global web_clicker

    if not web_clicker:
        return jsonify({
            'success': False,
            'message': '请先启动网页选择器'
        }), 400

    data = request.json
    selector = data.get('selector')
    selector_type = data.get('type', 'xpath')

    if not selector:
        return jsonify({
            'success': False,
            'message': '请提供选择器'
        }), 400

    try:
        if web_clicker.test_selector(selector, selector_type):
            return jsonify({
                'success': True,
                'message': '选择器有效，元素已高亮显示'
            })
        else:
            return jsonify({
                'success': False,
                'message': '未找到匹配元素'
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'测试失败: {str(e)}'
        }), 500


@app.route('/api/web/close-selector', methods=['POST'])
def close_web_selector():
    """关闭网页选择器浏览器"""
    global web_clicker

    if web_clicker:
        web_clicker.close()
        web_clicker = None

        return jsonify({
            'success': True,
            'message': '浏览器已关闭'
        })
    else:
        return jsonify({
            'success': True,
            'message': '浏览器未运行'
        })


if __name__ == '__main__':
    print("=" * 60)
    print("         定时点击助手 Web 版 v0.5.0")
    print("=" * 60)
    print()
    print("访问地址:")
    print("  本机: http://localhost:5000")
    print("  局域网: http://<你的IP>:5000")
    print()
    print("提示: 使用 ipconfig 查看本机 IP 地址")
    print()

    app.run(host='0.0.0.0', port=5000, debug=True)
