import pygame as pg
import sys, time, copy
from typing import Optional

from window import *
from font import get_jp_font

pg.init()
screen = pg.display.set_mode((WIN_W, WIN_H))
pg.display.set_caption(TITLE)
font = get_jp_font(26)

party = PARTY.copy()
enemies = copy.deepcopy(ENEMIES)

enemy_idx=0
enemy = enemies[enemy_idx]
field = init_field()

drag_src: Optional[int] = None
drag_elem: Optional[str] = None
hover_idx: Optional[int] = None
message = "ドラッグで A..N の宝石を移動（例：A→F）"

clock = pg.time.Clock()

# 0: タイトル, 1: プレイ, 2: 未定
status = 0

running=True
while running:
    keys=pg.key.get_pressed()
    for e in pg.event.get():
        if e.type==pg.QUIT:
            running=False


        # 描画関係
        # 背景黒塗り
        screen.fill((22,22,28))
        # statusが0のときタイトル画面を描画
        if status == 0:
            title_screen = font.render(TITLE, True, (255,255,255))
            screen.blit(title_screen, [WIN_W // 3, WIN_H // 4])
            text = font.render("Click to start", True, (255,255,255))
            screen.blit(text, [(WIN_W // 2) - 80, WIN_H // 2])
            if e.type == pg.MOUSEBUTTONDOWN:
                status = 1
                print("starting...")

        # statusが1のときゲームがプレイできる
        elif status == 1:
            draw_top(screen, enemy, party, font)
            draw_field(screen, field, font, hover_idx, drag_src, drag_elem)
            draw_message(screen, message, font)
            if e.type==pg.MOUSEBUTTONDOWN and e.button==1:
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
                                screen.fill((22,22,28)); draw_top(screen, enemy, party, font)
                                pg.display.flip()
                                break

                        # 敵ターン or 撃破後処理
                        if enemy["hp"]>0:
                            edmg=enemy_attack(party, enemy)
                            message=f"{enemy['name']}の攻撃！ -{edmg}"
                            screen.fill((22,22,28)); draw_top(screen, enemy, party, font)
                            draw_field(screen, field, font); draw_message(screen, message, font)
                            pg.display.flip(); time.sleep(FRAME_DELAY)
                            if party["hp"]<=0:
                                message="パーティは力尽きた…"
                                status = 2

                        else:
                            enemy_idx+=1
                            if enemy_idx<len(enemies):
                                enemy=enemies[enemy_idx]
                                field=init_field()
                                message=f"さらに奥へ… 次は {enemy['name']}"
                            else:
                                message="ダンジョン制覇！おめでとう！"
                                status = 2

                # ドラッグ終了
                drag_src = None
                drag_elem = None
                hover_idx = None
                print(enemies, ENEMIES)

        elif status == 2:
            msg = font.render(message, True, (255,255,255))
            screen.blit(msg, [WIN_W // 3, WIN_H // 4])
            enemy_idx = 0
            enemy = enemies[enemy_idx]
            party = PARTY.copy()
            enemies = copy.deepcopy(ENEMIES)

            if e.type == pg.MOUSEBUTTONDOWN:
                status = 0
                print("reset")
        # elif status == 3:
        #     title_screen = font.render(TITLE, True, (255,255,255))
        #     screen.blit(message, [WIN_W // 3, WIN_H // 4])
        print(enemy_idx)

        pg.display.flip()
        clock.tick(60)

    if keys[pg.K_ESCAPE]:
        running=False

pg.quit()
sys.exit()

