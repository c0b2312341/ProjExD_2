import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_RIGHT: (+5, 0),
    pg.K_LEFT: (-5, 0),
}
# 回転したこうかとんの辞書
import os
print(os.getcwd())
kk_img = pg.transform.rotozoom(pg.image.load("ex2/fig/3.png"), 0, 0.9)
ROTATE_KOUKATON = {
    pg.transform.rotate(kk_img, 45 * 0): (5, 0),  # 単位円上に原点より45度づつ回転
    pg.transform.rotate(kk_img, 45 * 1): (5, -5),
    pg.transform.rotate(kk_img, 45 * 1): (0, -5),
    pg.transform.rotate(kk_img, 45 * 3): (-5, -5),
    pg.transform.rotate(kk_img, 45 * 4): (-5, 0),
    pg.transform.rotate(kk_img, 45 * 5): (-5, 5),
    pg.transform.rotate(kk_img, 45 * 6): (0, 5),
    pg.transform.rotate(kk_img, 45 * 7): (5, 5),
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct):
    """
    引数で与えられたrctが画面の中か外を判定する
    引数: こうかとんrect or 爆弾rect
    戻り値: 真理値タプル(横, 縦), 画面内: True, 画面外: False
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate


def game_over(img):
    """
    黒い背景と5秒間のカウントを行う
    引数: 背景用のimg
    (bg_imgの想定)
    戻り値: なし
    """
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()

    black_img = pg.Surface((1100, 650))
    pg.draw.rect(black_img, (0, 0, 0), pg.Rect(0, 0, 1100, 650))  # 黒色の背景を設定
    black_img.set_alpha(90)  # 透明度90
    kk_right_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)
    kk_left_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 0.9)

    fonto = pg.font.Font(None, 80)  # fontの設定
    text = fonto.render("Game Over", True, (255, 255, 255))  # GAME OVERと文字色の設定
    text_rect = text.get_rect()
    text_rect.center = 550, 325
    kk_right_rect = kk_right_img.get_rect()
    kk_right_rect.center = 550 + 200, 325
    kk_left_rect = kk_left_img.get_rect()
    kk_left_rect.center = 550 - 200, 325

    # 1秒の処理を5回繰り返す, よって5秒間
    for i in range(5):
        screen.blit(img, [0, 0])
        screen.blit(black_img, [0, 0])
        screen.blit(text, text_rect)
        screen.blit(kk_right_img, kk_right_rect)
        screen.blit(kk_left_img, kk_left_rect)
        pg.display.update()
        clock.tick(1)
        print(f"{i + 1}秒")


def get_rotate(sum_mv):
    """
    sum_mvの移動量からこうかとんの向きを決定する
    引数: sum_mvなどx, yの移動量
    戻り値: 回転されたこうかとんimg
    """
    for img, mv in ROTATE_KOUKATON.items():  # 移動量の判定とimgの決定
        if mv == sum_mv:
            return img


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    clock = pg.time.Clock()
    tmr = 0
    bb_img = pg.Surface((20, 20))  # bombのsurface
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # bomb
    bb_rct = kk_img.get_rect()
    bb_img.set_colorkey((0, 0, 0))
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, 5

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            if kk_rct.colliderect(bb_rct):
                game_over(bg_img)
                print("GAME OVER")
                return  # gameover
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, tpl in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += tpl[0]
                sum_mv[1] += tpl[1]
        
        kk_rct.move_ip(tuple(sum_mv))
        print(type(sum_mv))
        kkr_img = get_rotate(tuple(sum_mv))  # こうかとんの向き決定

        #こうかとんが画面内なら元の場所に戻す
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if yoko == False:
            vx *= -1
        if tate == False:
            vy *= -1

        # screen.blit(kk_img, kk_rct)
        screen.blit(kkr_img, kk_rct)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
