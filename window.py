import pygame as pg

from typing import List, Optional
from config import *
from calc import *
import os

# ---------------- 画像 ----------------
def load_monster_image(name: str) -> pg.Surface:
    m = {
        "スライム":"slime.png", "ゴブリン":"goblin.png",
        "オオコウモリ":"bat.png", "ウェアウルフ":"werewolf.png",
        "ドラゴン":"dragon.png"
    }
    fn = m.get(name)
    if fn:
        path = os.path.join("assets","monsters",fn)
        if os.path.exists(path):
            img = pg.image.load(path).convert_alpha()
            return pg.transform.smoothscale(img, (256,256))
    surf = pg.Surface((256,256), pg.SRCALPHA); surf.fill((60,60,60,200))
    return surf


# ---------------- 描画ユーティリティ ----------------
def slot_rect(i: int) -> pg.Rect:
    tx = LEFT_MARGIN + i * (SLOT_W + SLOT_PAD)
    return pg.Rect(tx, FIELD_Y, SLOT_W, SLOT_W)

def draw_gem_at(screen, elem: str, x: int, y: int, scale=1.0, with_shadow=False, font=None):
    r = int((SLOT_W//2 - 10) * scale)
    if with_shadow:
        shadow = pg.Surface((r*2+6, r*2+6), pg.SRCALPHA)
        pg.draw.circle(shadow, DRAG_SHADOW, (r+3, r+3), r+3)
        screen.blit(shadow, (x-r-3, y-r-3))
    pg.draw.circle(screen, COLOR_RGB[elem], (x, y), r)
    sym = ELEMENT_SYMBOLS[elem]
    f = font if font else get_jp_font(int(26*scale))
    s = f.render(sym, True, (0,0,0))
    screen.blit(s, (x - s.get_width()//2, y - s.get_height()//2))

def draw_field(screen, field:List[str], font, hover_idx:Optional[int]=None,
               drag_src:Optional[int]=None, drag_elem:Optional[str]=None):
    # スロット見出し
    for i,slot in enumerate(SLOTS):
        tx=LEFT_MARGIN+i*(SLOT_W+SLOT_PAD)
        s=font.render(slot, True, (220,220,220))
        screen.blit(s,(tx, FIELD_Y-28))
    # スロット下地 & ホバー強調
    for i,_ in enumerate(field):
        rect=slot_rect(i)
        base = (35,35,40) if hover_idx!=i else (60,60,80)
        pg.draw.rect(screen, base, rect, border_radius=8)
    # 宝石（ドラッグ開始スロットは空に見せる）-> 見せない
    for i,elem in enumerate(field):
        if drag_src is not None :
            # if i==drag_src:
            #     print(i, elem)
            #     continue
            if i==hover_idx or drag_src ==i:
                continue
        rect=slot_rect(i)
        cx,cy=rect.center
        pg.draw.circle(screen, COLOR_RGB[elem], (cx,cy), SLOT_W//2-10)
        sym = ELEMENT_SYMBOLS[elem]
        s = font.render(sym, True, (0,0,0))
        screen.blit(s,(cx-s.get_width()//2, cy-s.get_height()//2))
    # ドラッグ中の宝石（ゴースト）をカーソル位置に拡大表示
    if drag_elem is not None:
        mx, my = pg.mouse.get_pos()
        draw_gem_at(screen, drag_elem, mx, my-4, scale=DRAG_SCALE, with_shadow=True, font=font)

def draw_top(screen, enemy, party, font):
    # 敵画像/名前
    img = load_monster_image(enemy["name"])
    screen.blit(img, (40, 40))

    # 敵名とHPバー
    name = font.render(enemy["name"], True, (240, 240, 240))
    screen.blit(name, (320, 40))
    enemy_bar = hp_bar_surf(enemy["hp"], enemy["max_hp"], 420, 18)
    screen.blit(enemy_bar, (320, 80))

    # 敵HP数値（バー右側に）
    enemy_hp_text = font.render(f"{enemy['hp']}/{enemy['max_hp']}", True, (240, 240, 240))
    screen.blit(enemy_hp_text, (750, 78))

    # 「パーティ」ラベル
    label = font.render("パーティ", True, (240, 240, 240))
    screen.blit(label, (320, 110))

    # パーティHPバー
    party_bar = hp_bar_surf(party["hp"], party["max_hp"], 420, 18)
    screen.blit(party_bar, (320, 140))

    # パーティHP数値
    party_hp_text = font.render(f"{int(party['hp'])}/{party['max_hp']}", True, (240, 240, 240))
    screen.blit(party_hp_text, (750, 138))

def draw_message(screen, text, font):
    surf = font.render(text, True, (230,230,230))
    screen.blit(surf,(40,460))

def draw_point(screen, point, font):
    msg = font.render(f"経験値：{str(point)}", True, (255,255,255))
    screen.blit(msg, [ 10 , WIN_H - 40])
