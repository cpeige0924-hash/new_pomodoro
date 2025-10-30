# core/pet.py
import json, os

GROWING_FILE = "pet_data.json"

class Pet:
    """当前成长中的宠物（唯一）"""
    def __init__(self, name: str, species: str, growth_value: float = 0.0, stage: int = 1):
        self.name = name
        self.species = species  # "cat" | "rabbit" | "dog" | "duck"
        self.growth_value = float(growth_value)  # 以“50分钟”为 1 单位，25 分钟记 0.5
        self.stage = int(stage)  # 1=幼崽, 2=成长中, 3=成熟
        icons = {
            "cat": "🐱",
            "dog": "🐶",
            "rabbit": "🐰",
            "duck": "🦆",
        }
        self.icon = icons.get(species.lower(), "🐾")
    # ---------- 持久化 ----------
    @staticmethod
    def exists() -> bool:
        return os.path.exists(GROWING_FILE)

    @staticmethod
    def load():
        if not os.path.exists(GROWING_FILE):
            return None
        with open(GROWING_FILE, "r", encoding="utf-8") as f:
            d = json.load(f)
        return Pet(d["name"], d["species"], d["growth_value"], d["stage"])

    def save(self):
        with open(GROWING_FILE, "w", encoding="utf-8") as f:
            json.dump({
                "name": self.name,
                "species": self.species,
                "growth_value": self.growth_value,
                "stage": self.stage
            }, f, indent=4)

    @staticmethod
    def clear():
        if os.path.exists(GROWING_FILE):
            os.remove(GROWING_FILE)

    # ---------- 业务逻辑 ----------
    def add_progress(self, minutes: float):
        """
        根据番茄钟时长增加成长值：
        - 50 分钟 → +1
        - 25 分钟 → +0.5
        返回元组 (stage_changed, matured)
        """
        delta = 1.0 if minutes >= 50 - 1e-6 else 0.5
        self.growth_value += delta

        stage_changed = False
        matured = False

        # 阶段判定：0~<10: stage1; 10~<20: stage2; >=20: stage3(成熟)
        if self.growth_value >= 2 and self.stage != 3:
            self.stage = 3
            stage_changed = True
            matured = True
        elif self.growth_value >= 1 and self.stage == 1:
            self.stage = 2
            stage_changed = True

        self.save()
        return stage_changed, matured

    def to_dict(self, assign_id: int):
        """导出到花园的结构（携带一个分配的 id）"""
        return {
            "id": assign_id,
            "name": self.name,
            "species": self.species,
            "growth_value": self.growth_value,
            "stage": self.stage
        }

    # ---------- 展示 ----------
    def ascii_small(self):
        """简易占位 ASCII（可后续替换为更精美版本）"""
        if self.species == "cat":
            return " /\\_/\\\n( o.o )\n > ^ <"
        if self.species == "rabbit":
            return "(\\_/)\n( •_•)\n/ >🍃"
        if self.species == "dog":
            return "U・ᴥ・U"
        if self.species == "duck":
            return "<(• )___\n ( ._> /"
        return "(?)"

    def pretty_status(self):
        return (
            f"Name: {self.name}\n"
            f"Species: {self.species}\n"
            f"Stage: {self.stage} / 3\n"
            f"Progress (50-min units): {self.growth_value:.1f}"
        )
