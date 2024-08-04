import random
from loguru import logger

# グリッドサイズの定義
GRID_WIDTH = 5000
GRID_HEIGHT = 3000
SLIDE_WIDTH = 1000
SLIDE_HEIGHT = 750

class BoundingBox:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def intersects(self, other):
        return not (self.x + self.width <= other.x or
                    other.x + other.width <= self.x or
                    self.y + self.height <= other.y or
                    other.y + other.height <= self.y)

def get_random_position(used_bounding_boxes):
    """ランダムな位置を生成し、既存のスライドと重ならないようにする"""
    max_attempts = 100
    for _ in range(max_attempts):
        x = random.randint(0, (GRID_WIDTH - SLIDE_WIDTH) // SLIDE_WIDTH) * SLIDE_WIDTH
        y = random.randint(0, (GRID_HEIGHT - SLIDE_HEIGHT) // SLIDE_HEIGHT) * SLIDE_HEIGHT
        new_box = BoundingBox(x, y, SLIDE_WIDTH, SLIDE_HEIGHT)

        if not any(new_box.intersects(box) for box in used_bounding_boxes):
            return x, y

    logger.warning("スライドの配置に失敗しました。ランダムな位置を返します。")
    return x, y
