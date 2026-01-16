import random
from typing import List, Tuple, Optional
import pygame as pg
from config import *

# ---------------- HPバー ----------------
def hp_bar_surf(current: int, max_hp: int, w: int, h: int) -> pg.Surface:
    """HPバー（max600基準でスケーリング）"""
    # HP比（0〜1）
    ratio = max(0, min(1, current / max_hp if max_hp > 0 else 0))
    # 600を基準にスケール（例：max_hp=100なら1/6）
    scale = min(1.0, max_hp / 600.0)
    bar_w = int(w * scale)

    # HP割合で塗り幅を決定
    fill_w = int(bar_w * ratio)

    # 色（体力残量による）
    if ratio >= 0.6:
        col = (40, 200, 90)
    elif ratio >= 0.3:
        col = (230, 200, 60)
    else:
        col = (230, 70, 70)

    # バー描画
    surf = pg.Surface((w, h), pg.SRCALPHA)
    # 背景（透明）
    bg = pg.Surface((bar_w, h), pg.SRCALPHA)
    bg.fill((0, 0, 0, 120))
    surf.blit(bg, (0, 0))
    # 緑バー
    fg = pg.Surface((fill_w, h), pg.SRCALPHA)
    fg.fill(col)
    surf.blit(fg, (0, 0))
    return surf

# ---------------- 盤面ロジック ----------------
def init_field()->List[str]:
    return [random.choice(GEMS) for _ in range(14)]

def leftmost_run(field:List[str])->Optional[Tuple[int,int]]:
    n=len(field); i=0
    while i<n:
        j=i+1
        while j<n and field[j]==field[i]: j+=1
        L=j-i
        if L>=3 and field[i] in GEMS: return (i,L)
        i=j
    return None

def collapse_left(field:List[str], start:int, length:int):
    # 消滅部分を '無' にしてから左詰め（簡略：一気に詰める）
    n=len(field)
    for k in range(start, start+length): field[k]="無"
    rest=[e for e in field if e!="無"]; field[:] = rest + ["無"]*length

def fill_random(field:List[str]):
    for i,e in enumerate(field):
        if e=="無": field[i]=random.choice(GEMS)

# ---------------- ダメージ/回復 ----------------
def jitter(v:float, r:float=0.10)->int:
    return max(1, int(v*random.uniform(1-r,1+r)))

def attr_coeff(att,defe):
    cyc={"火":"風","風":"土","土":"水","水":"火"}
    if att in cyc and cyc[att]==defe: return 2.0
    if defe in cyc and cyc[defe]==att: return 0.5
    return 1.0

def party_attack_from_gems(elem:str, run_len:int, combo:int, party:dict, monster:dict)->int:
    combo_coeff = 1.5 ** ((run_len - 3) + combo)
    if elem=="命":
        heal=jitter(20*combo_coeff); party["hp"]=min(party["max_hp"], party["hp"]+heal); return 0
    ally = next((a for a in party["allies"] if a["element"]==elem), None)
    if not ally: return 0
    base=max(1, ally["ap"]-monster["dp"])
    dmg=jitter(base*attr_coeff(elem,monster["element"])*combo_coeff)
    monster["hp"]=max(0,monster["hp"]-dmg); return dmg

def enemy_attack(party:dict, monster:dict)->int:
    base=max(1, monster["ap"]-party["dp"])
    dmg=jitter(base); party["hp"]=max(0,party["hp"]-dmg); return dmg

