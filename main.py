import pygame as pg
import sys, os, random, time
from typing import List, Tuple, Optional

from window import *

# ---------------- フォント解決 ----------------
def get_jp_font(size: int) -> pg.font.Font:
    bundle = os.path.join("assets", "fonts", "NotoSansJP-VariableFont_wght.ttf")
    if os.path.exists(bundle):
        return pg.font.Font(bundle, size)
    candidates = [
        "Noto Sans CJK JP", "Noto Sans JP",
        "Yu Gothic UI", "Yu Gothic",
        "Meiryo", "MS Gothic",
        "Hiragino Sans", "Hiragino Kaku Gothic ProN",
    ]
    for name in candidates:
        path = pg.font.match_font(name)
        if path:
            return pg.font.Font(path, size)
    return pg.font.SysFont(None, size)

# ---------------- メイン ----------------
def main():
    pg.init()
    screen = pg.display.set_mode((WIN_W, WIN_H))
    pg.display.set_caption("Puzzle & Monsters - Team7")
    font = get_jp_font(26)

    party = {
        "player_name":"Player",
        "allies":[
            {"name":"青龍","element":"風","hp":150,"max_hp":150,"ap":15,"dp":10},
            {"name":"朱雀","element":"火","hp":150,"max_hp":150,"ap":25,"dp":10},
            {"name":"白虎","element":"土","hp":150,"max_hp":150,"ap":20,"dp":5},
            {"name":"玄武","element":"水","hp":150,"max_hp":150,"ap":20,"dp":15},
        ],
        "hp":600, "max_hp":600, "dp":(10+10+5+15)/4
    }
    enemies = [
        {"name":"スライム","element":"水","hp":100,"max_hp":100,"ap":10,"dp":1},
        {"name":"ゴブリン","element":"土","hp":200,"max_hp":200,"ap":20,"dp":5},
        {"name":"オオコウモリ","element":"風","hp":300,"max_hp":300,"ap":30,"dp":10},
        {"name":"ウェアウルフ","element":"風","hp":400,"max_hp":400,"ap":40,"dp":15},
        {"name":"ドラゴン","element":"火","hp":600,"max_hp":600,"ap":50,"dp":20},
    ]
    enemy_idx=0
    enemy = enemies[enemy_idx]
    field = init_field()

    drag_src: Optional[int] = None
    drag_elem: Optional[str] = None
    hover_idx: Optional[int] = None
    message = "ドラッグで A..N の宝石を移動（例：A→F）"

    clock = pg.time.Clock()
    running=True
    while running:
        for e in pg.event.get():
            if e.type==pg.QUIT:
                running=False

            elif e.type==pg.MOUSEBUTTONDOWN and e.button==1:
                mx,my = e.pos
                if FIELD_Y<=my<=FIELD_Y+SLOT_W:
                    i = (mx-LEFT_MARGIN)//(SLOT_W+SLOT_PAD)
                    if 0<=i<14:
                        drag_src = i
                        drag_elem = field[i]
                        message=f"{SLOTS[i]} を掴んだ"

            elif e.type==pg.MOUSEMOTION:
                mx,my = e.pos
                if FIELD_Y<=my<=FIELD_Y+SLOT_W:
                    hi = (mx-LEFT_MARGIN)//(SLOT_W+SLOT_PAD)
                    hover_idx = hi if 0<=hi<14 else None
                else:
                    hover_idx = None

            elif e.type==pg.MOUSEBUTTONUP and e.button==1:
                if drag_src is not None:
                    mx,my = e.pos
                    j = (mx-LEFT_MARGIN)//(SLOT_W+SLOT_PAD)
                    if 0<=j<14:
                        i = drag_src
                        if i != j:
                            step = 1 if j>i else -1
                            k = i
                            while k!=j:
                                nxt = k + step
                                field[k], field[nxt] = field[nxt], field[k]
                                k = nxt
                                message=f"{SLOTS[k-step]}↔{SLOTS[k]} を交換"
                                screen.fill((22,22,28))
                                draw_top(screen, enemy, party, font)
                                draw_field(screen, field, font, hover_idx=None, drag_src=None, drag_elem=None)
                                draw_message(screen, message, font)
                                pg.display.flip()
                                time.sleep(FRAME_DELAY)

                        # 評価ループ
                        combo=0
                        while True:
                            run = leftmost_run(field)
                            if not run: break
                            start,L = run
                            combo+=1
                            elem = field[start]
                            if elem=="命":
                                heal=jitter(20*(1.5**((L-3)+combo)))
                                party["hp"]=min(party["max_hp"], party["hp"]+heal)
                                message=f"HP +{heal}"
                            else:
                                dmg=party_attack_from_gems(elem,L,combo,party,enemy)
                                message=f"{elem}攻撃！ {dmg} ダメージ"
                            collapse_left(field,start,L)
                            screen.fill((22,22,28)); draw_top(screen, enemy, party, font)
                            draw_field(screen, field, font); draw_message(screen, "消滅！", font)
                            pg.display.flip(); time.sleep(FRAME_DELAY)
                            fill_random(field)
                            screen.fill((22,22,28)); draw_top(screen, enemy, party, font)
                            draw_field(screen, field, font); draw_message(screen, "湧き！", font)
                            pg.display.flip(); time.sleep(FRAME_DELAY)
                            if enemy["hp"]<=0:
                                message=f"{enemy['name']} を倒した！"
                                break

                        # 敵ターン or 撃破後処理
                        if enemy["hp"]>0:
                            edmg=enemy_attack(party, enemy)
                            message=f"{enemy['name']}の攻撃！ -{edmg}"
                            screen.fill((22,22,28)); draw_top(screen, enemy, party, font)
                            draw_field(screen, field, font); draw_message(screen, message, font)
                            pg.display.flip(); time.sleep(FRAME_DELAY)
                            if party["hp"]<=0:
                                message="パーティは力尽きた…（ESCで終了）"
                        else:
                            enemy_idx+=1
                            if enemy_idx<len(enemies):
                                enemy=enemies[enemy_idx]
                                field=init_field()
                                message=f"さらに奥へ… 次は {enemy['name']}"
                            else:
                                message="ダンジョン制覇！おめでとう！（ESCで終了）"

                # ドラッグ終了
                drag_src = None
                drag_elem = None
                hover_idx = None

        # 常時描画
        screen.fill((22,22,28))
        draw_top(screen, enemy, party, font)
        draw_field(screen, field, font, hover_idx, drag_src, drag_elem)
        draw_message(screen, message, font)
        pg.display.flip()
        clock.tick(60)

        keys=pg.key.get_pressed()
        if keys[pg.K_ESCAPE]:
            running=False

    pg.quit()
    sys.exit()

if __name__=="__main__":
    main()


