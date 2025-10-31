# core/pet_manager.py
import json, os
from core.pet import Pet

GARDEN_FILE = "garden.json"
COMPANION_FILE = "companion.json"

def _load_json(path, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return default

def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ---------- 花园 ----------
def list_garden():
    """返回花园宠物列表（list of dict）"""
    return _load_json(GARDEN_FILE, [])

def _next_garden_id(items):
    return (max((p.get("id", 0) for p in items), default=0) + 1) if items else 1

def add_to_garden(pet: Pet):
    """将成熟宠物加入花园"""
    garden = list_garden()
    new_id = _next_garden_id(garden)
    garden.append(pet.to_dict(assign_id=new_id))
    _save_json(GARDEN_FILE, garden)
    return new_id

# ---------- 当前成长宠物 ----------
def load_growing():
    """返回当前成长宠物 Pet 或 None"""
    return Pet.load()

def save_growing(pet: Pet):
    pet.save()

def clear_growing():
    Pet.clear()

# ---------- 陪伴宠物（来自花园） ----------
GARDEN_FILE = "garden.json"

def load_garden():
    """读取花园中的所有宠物"""
    if not os.path.exists(GARDEN_FILE):
        return []
    try:
        with open(GARDEN_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

