
# ---------------- 可変パラメータ ----------------
FRAME_DELAY = 0.2
ENEMY_DELAY = 1.0
WIN_W, WIN_H = 980, 720
FIELD_Y = 520
SLOT_W = 60
SLOT_PAD = 8
LEFT_MARGIN = 30
TITLE = "Puzzle & Monsters - Team7" 

# ドラッグ演出
DRAG_SCALE = 1.18
DRAG_SHADOW = (0, 0, 0, 90)

# ---------------- 定義 ----------------
ELEMENT_SYMBOLS = {"火": "$", "水": "~", "風": "@", "土": "#", "命": "&", "無": " "}
COLOR_RGB = {
    "火": (230, 70, 70), "水": (70, 150, 230), "風": (90, 200, 120),
    "土": (200, 150, 80), "命": (220, 90, 200), "無": (160,160,160)
}
GEMS = ["火", "水", "風", "土", "命"]
SLOTS = [chr(ord('A')+i) for i in range(14)]

