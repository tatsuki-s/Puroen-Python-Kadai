
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

PARTY = {
    "player_name":"Player",
    "allies":[
        {"name":"青龍","element":"風","hp":150,"max_hp":150,"ap":15000,"dp":10},
        {"name":"朱雀","element":"火","hp":150,"max_hp":150,"ap":25000,"dp":10},
        {"name":"白虎","element":"土","hp":150,"max_hp":150,"ap":20000,"dp":5},
        {"name":"玄武","element":"水","hp":150,"max_hp":150,"ap":20000,"dp":15},
    ],
    "hp":600, "max_hp":600, "dp":(10+10+5+15)/4
}
ENEMIES = [
    {"name":"スライム","element":"水","hp":100,"max_hp":100,"ap":10,"dp":1},
    {"name":"ゴブリン","element":"土","hp":200,"max_hp":200,"ap":20000000000000,"dp":5},
    {"name":"オオコウモリ","element":"風","hp":300,"max_hp":300,"ap":30,"dp":10},
    {"name":"ウェアウルフ","element":"風","hp":400,"max_hp":400,"ap":40,"dp":15},
    {"name":"ドラゴン","element":"火","hp":600,"max_hp":600,"ap":50,"dp":20},
]
