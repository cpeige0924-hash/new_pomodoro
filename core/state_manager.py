import json
import os
from datetime import date

STATE_FILE = "focus_data.json"

def _ensure_file():
    if not os.path.exists("data"):
        os.makedirs("data")

def load_state():
    """读取历史数据"""
    if not os.path.exists(STATE_FILE):
        return {}
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_state(data):
    """保存历史数据"""
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def add_focus(minutes):
    """记录当天专注分钟数"""
    today = date.today().isoformat()
    data = load_state()
    if today not in data:
        data[today] = 0
    data[today] += minutes
    save_state(data)

def get_history():
    """获取所有日期的专注记录"""
    return load_state()

