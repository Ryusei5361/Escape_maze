# 20K0112 大村琉聖
# 最終課題-メイン：迷路脱出ゲーム

# pygameを読み込む
import pygame
import time
import random
from dataclasses import dataclass, field
from maze import Maze

SCREEN_WIDTH = 800  # 画面の横幅
SCREEN_HEIGHT = 800  # 画面の縦幅

MAZE_X = 20  # 迷路のマス目のx座標
MAZE_Y = 20  # 迷路のマス目のy座標
MAZE_W = 20  # 迷路のマス目の横幅
MAZE_H = 20  # 迷路のマス目の縦幅

PLAYER_ROW = 0  # プレイヤーのx座標の初期位置
PLAYER_COL = 1  # プレイヤーのy座標の初期位置
PLAYER_D = 5  # プレイヤーの大きさ

ENEMIE_ROW1 = 14  # 敵1の位置、行
ENEMIE_COL1 = 1  # 敵1の位置、列

ENEMIE_ROW2 = 3  # 敵2の位置、行
ENEMIE_COL2 = 16  # 敵2の位置、列

ENEMIE_ROW3 = 17  # 敵3の位置、行
ENEMIE_COL3 = 17  # 敵3の位置、列

ITEMX1 = 160  # item1のx座標
ITEMY1 = 40  # item1のy座標
ITEMX2 = 40  # item2のx座標
ITEMY2 = 340  # item2のy座標
ITEMX3 = 300  # item3のx座標
ITEMY3 = 40  # item3のy座標
ITEMX4 = 380  # item4のx座標
ITEMY4 = 380  # item4のy座標

BLACK = (0, 0, 0)  # 黒
WHITE = (255, 255, 255)  # 白
PURPLE = (167, 87, 168)  # 紫
BLUE = (0, 0, 255)  # 青
GREEN = (0, 255, 0)  # 緑
RED = (255, 0, 0)  # 赤

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # SCREEN_WIDTH×SCREEN_HEIGHTのscreenを生成
font = pygame.font.SysFont('commissars', 30)  # フォントの設定
font2 = pygame.font.SysFont('commissars', 60)  # フォントの設定
image = pygame.image.load("slime.png").convert_alpha()  # 敵の画像を読み込む
image = pygame.transform.scale(image, (20, 20))  # 敵の画像の大きさを調整
image2 = pygame.image.load("GAME_OVER.jpg").convert_alpha()  # GameOverの画像を読み込む
image2 = pygame.transform.scale(image2, (SCREEN_WIDTH, SCREEN_HEIGHT))  # GameOverの画像の大きさを調整
image3 = pygame.image.load("KEY2.png").convert_alpha()  # 鍵の画像を読み込む
image3 = pygame.transform.scale(image3, (20, 20))  # 鍵の画像の大きさを調整
image4 = pygame.image.load("Gameclear.png").convert_alpha()  # GameClearの画像を読み込む
image4 = pygame.transform.scale(image4, (SCREEN_WIDTH, SCREEN_HEIGHT))  # GameClearの画像の大きさを調整


# 迷路のクラス
@dataclass
class MazeGame:
    maze: Maze = field(init=False, default=None)  # 別のファイルから情報を持ってくる
    player: tuple = field(init=False, default=None)  # プレイヤーのタプルを作成
    enemie1: tuple = field(init=False, default=None)  # 敵1のタプルを作成
    enemie2: tuple = field(init=False, default=None)  # 敵2のタプルを作成
    enemie3: tuple = field(init=False, default=None)  # 敵3のタプルを作成
    location_p: tuple = field(init=False, default=None)  # プレイヤーの位置のタプルを作成
    location_e1: tuple = field(init=False, default=None)  # 敵1の位置のタプルを作成
    location_e2: tuple = field(init=False, default=None)  # 敵2の位置のタプルを作成
    location_e3: tuple = field(init=False, default=None)  # 敵3の位置のタプルを作成

    def __init__(self):
        self.key = 0  # 鍵の個数をカウントするための変数
        self.fin = False  # 敵との衝突を判定するための変数
        self.goal = False  # ゴールを判定するための変数
        self.key1 = False  # key1を取得したか判定するための変数
        self.key2 = False  # key2を取得したか判定するための変数
        self.key3 = False  # key3を取得したか判定するための変数
        self.key4 = False  # key4を取得したか判定するための変数
        self.keycheck1 = 0  # key1を1回取得したか判定する変数
        self.keycheck2 = 0  # key2を1回取得したか判定する変数
        self.keycheck3 = 0  # key3を1回取得したか判定する変数
        self.keycheck4 = 0  # key4を1回取得したか判定する変数

    def draw_floormap(self, x, y, w, h):  # 迷路の描画
        x0 = x  # x座標の初期位置を取っておく
        for i in self.maze.floormap:  # 迷路の情報を1つずつ見ていく
            for j in i:
                if j == 1:  # もし、マスの値が1なら緑色に塗る
                    pygame.draw.rect(screen, GREEN, (x, y, w, h))
                    x += w  # x座標を1つ下にずらす
                elif j == 2:  # もし、マス目の値が2なら青色に塗る。ここがスタート地点
                    pygame.draw.rect(screen, BLUE, (x, y, w, h))
                    x += w  # x座標を1つ下にずらす
                elif j == 3:  # もし、マス目の値が3なら赤色に塗る。ここがゴール地点
                    pygame.draw.rect(screen, RED, (x, y, w, h))
                    x += w  # x座標を1つ下にずらす
                else:  # マスの値が0なら何もせずに横に移動
                    x += w  # x座標を1つ下にずらす
            x = x0  # x座標を左端に戻す
            y += h  # y座標を1つ下にずらす
        # Startを表示
        text = font.render("Start", True, WHITE)
        screen.blit(text, (MAZE_X, 0))
        # Goalを表示
        text2 = font.render("Goal", True, WHITE)
        screen.blit(text2, (25, MAZE_Y + MAZE_H * self.maze.height))

    def set_player(self, x, y, d):  # プレイヤーを移動するための関数
        self.player = (x, y, d)

    def set_enemie1(self, x, y):  # 敵1を移動するための関数
        self.enemie1 = (x, y)

    def set_enemie2(self, x, y):  # 敵2を移動するための関数
        self.enemie2 = (x, y)

    def set_enemie3(self, x, y):  # 敵3を移動するための関数
        self.enemie3 = (x, y)

    def set_location_P(self, x, y):  # プレイヤーの位置を設定
        self.location_p = (x, y)

    def set_location_E1(self, x, y):  # 敵1の位置を設定
        self.location_e1 = (x, y)

    def set_location_E2(self, x, y):  # 敵2の位置を設定
        self.location_e2 = (x, y)

    def set_location_E3(self, x, y):  # 敵3の位置を設定
        self.location_e3 = (x, y)

    def draw_player(self):  # プレイヤーの描画
        pygame.draw.circle(screen, PURPLE, (self.player[0] + 5, self.player[1] + 5), self.player[2])

    def draw_enemie(self):  # 敵の描画
        screen.blit(image, (self.enemie1[0], self.enemie1[1]))
        screen.blit(image, (self.enemie2[0], self.enemie2[1]))
        screen.blit(image, (self.enemie3[0], self.enemie3[1]))

    def draw_item(self, x, y):  # アイテムの描画
        screen.blit(image3, (x, y))

    def redraw(self):  # 再描画
        screen.fill(BLACK)  # 画面を黒で塗りつぶす
        self.draw_floormap(MAZE_X, MAZE_Y, MAZE_W, MAZE_H)  # 迷路を描画
        self.draw_player()  # プレイヤーを描画
        self.draw_enemie()  # 敵を描画
        # プレイヤーがカギを取得したかどうか判定。取得していないなら、鍵を描画
        self.check_key(1)
        if not self.key1:
            self.draw_item(ITEMX1, ITEMY1)
        self.check_key(2)
        if not self.key2:
            self.draw_item(ITEMX2, ITEMY2)
        self.check_key(3)
        if not self.key3:
            self.draw_item(ITEMX3, ITEMY3)
        self.check_key(4)
        if not self.key4:
            self.draw_item(ITEMX4, ITEMY4)
        # 現在取得している鍵の個数を表示
        text = font2.render("Key: " + str(self.key) + " / 4", True, GREEN)
        screen.blit(text, [520, 20])
        # プレイヤーと敵の衝突を判定
        self.check_hit(self.location_p, self.location_e1)
        self.check_hit(self.location_p, self.location_e2)
        self.check_hit(self.location_p, self.location_e3)
        # ゴールしたかどうかの判定
        self.check_goal()
        # ディスプレイに表示
        pygame.display.flip()

    def check_up(self, location):  # 上に移動できるかの判定
        if location[0] - 1 < 0:  # スタート地点より上に行けないようにする。
            pass
        elif location == self.location_p:  # プレイヤーなら、スタート地点に戻れるようにする
            if self.maze.floormap[location[0] - 1][location[1]] == 0 \
                    or self.maze.floormap[location[0] - 1][location[1]] == 2:  # 上の移動の条件
                return True
        else:  # 敵なら、スタート地点に侵入できないようにする
            if self.maze.floormap[location[0] - 1][location[1]] == 0:
                return True

    def check_down(self, location):  # 下に移動できるかの判定
        if self.maze.floormap[location[0] + 1][location[1]] == 0 \
                or self.maze.floormap[location[0]][location[1]] == 2:  # 下の移動の条件
            return True
        elif self.maze.floormap[location[0] + 1][location[1]] == 3 and self.key == 4:  # 移動先がゴールなら
            return True

    def check_right(self, location):  # 右に移動できるかの判定
        if self.maze.floormap[location[0]][location[1] + 1] == 0:  # 右の移動の条件
            return True

    def check_left(self, location):  # 左に移動できるかの判定
        if self.maze.floormap[location[0]][location[1] - 1] == 0:  # 左の移動の条件
            return True

    def check_key(self, key_number):  # プレイヤーがカギの位置まで来た時の判定
        # プレイヤーとkey1の位置が重なったら
        if self.location_p[0] == 1 and self.location_p[1] == 7 and key_number == 1:
            self.key1 = True
            self.keycheck1 += 1
            # self.keycheck1が1のときに、持っているkeyの個数をプラス1する
            if self.keycheck1 == 1:
                self.key += 1
        # プレイヤーとkey2の位置が重なったら
        elif self.location_p[0] == 16 and self.location_p[1] == 1 and key_number == 2:
            self.key2 = True
            self.keycheck2 += 1
            # self.keycheck2が1のときに、持っているkeyの個数をプラス1する
            if self.keycheck2 == 1:
                self.key += 1
        # プレイヤーとkey3の位置が重なったら
        elif self.location_p[0] == 1 and self.location_p[1] == 14 and key_number == 3:
            self.key3 = True
            self.keycheck3 += 1
            # self.keycheck3が1のときに、持っているkeyの個数をプラス1する
            if self.keycheck3 == 1:
                self.key += 1
        # プレイヤーとkey4の位置が重なったら
        elif self.location_p[0] == 18 and self.location_p[1] == 18 and key_number == 4:
            self.key4 = True
            self.keycheck4 += 1
            # self.keycheck4が1のときに、持っているkeyの個数をプラス1する
            if self.keycheck4 == 1:
                self.key += 1

    def check_goal(self):  # keyを4つそろえてゴールにたどり着いたとき、self.goalをTrueにする
        if self.maze.floormap[self.location_p[0]][self.location_p[1]] == 3 and self.key == 4:
            self.goal = True

    def check_hit(self, location_p, location_e):  # プレイヤーと敵の位置が重なったらself.finをTrueにする
        if location_p[0] == location_e[0] and location_p[1] == location_e[1]:
            self.fin = True

    def player_up(self):  # 上の移動
        if self.check_up(self.location_p):
            loc_up = self.location_p[0] - 1  # 位置を移動
            move = self.player[1] - 20  # プレイヤーを移動
            self.set_location_P(loc_up, self.location_p[1])  # 位置をセット
            self.set_player(self.player[0], move, self.player[2])  # プレイヤーをセット

    def player_down(self):  # 下の移動
        if self.check_down(self.location_p):
            loc_down = self.location_p[0] + 1  # 位置を移動
            move = self.player[1] + 20  # プレイヤーを移動
            self.set_location_P(loc_down, self.location_p[1])  # 位置をセット
            self.set_player(self.player[0], move, self.player[2])  # プレイヤーをセット

    def player_right(self):  # 右の移動
        if self.check_right(self.location_p):
            loc_right = self.location_p[1] + 1  # 位置を移動
            move = self.player[0] + 20  # プレイヤーを移動
            self.set_location_P(self.location_p[0], loc_right)  # 位置をセット
            self.set_player(move, self.player[1], self.player[2])  # プレイヤーをセット

    def player_left(self):  # 左の移動
        if self.check_left(self.location_p):
            loc_left = self.location_p[1] - 1  # 位置を移動
            move = self.player[0] - 20  # プレイヤーを移動
            self.set_location_P(self.location_p[0], loc_left)  # 位置をセット
            self.set_player(move, self.player[1], self.player[2])  # プレイヤーをセット

    def move_enemie(self, set_location, set_enemie, location, enemie):  # 敵の動きに関する関数
        change_y = random.choice([20, 0, -20])  # 上下の移動をランダムで選ぶ
        if self.check_up(location) and change_y == -20:  # 上の移動の条件
            loc_up = location[0] - 1  # 位置を移動
            move = enemie[1] - 20  # 敵を移動
            set_location(loc_up, location[1])  # 位置をセット
            set_enemie(enemie[0], move)  # 敵をセット
        elif self.check_down(location) and change_y == 20:  # 下の移動の条件
            loc_down = location[0] + 1  # 位置を移動
            move = enemie[1] + 20  # 敵を移動
            set_location(loc_down, location[1])  # 位置をセット
            set_enemie(enemie[0], move)  # 敵をセット
        elif change_y == 0:  # 上下の移動がない場合
            change_x = random.choice([20, -20])  # 左右の移動をランダムで選ぶ
            if self.check_right(location) and change_x == 20:  # 右の移動の条件
                loc_right = location[1] + 1  # 位置を移動
                move = enemie[0] + 20  # 敵を移動
                set_location(location[0], loc_right)  # 位置をセット
                set_enemie(move, enemie[1])  # 敵をセット
            elif self.check_left(location) and change_x == -20:  # 左の移動の条件
                loc_left = location[1] - 1  # 位置を移動
                move = enemie[0] - 20  # 敵を移動
                set_location(location[0], loc_left)  # 位置をセット
                set_enemie(move, enemie[1])  # 敵をセット
        else:  # それ以外はとばす
            pass

    def start(self):  # 全体の動きを一気に設定
        self.maze = Maze()  # インスタンス化
        self.maze.from_file("ex11-1-map.txt")  # maze.pyから迷路の情報を持ってくる
        pressed_keys = pygame.key.get_pressed()  # キー入力情報を一括で取得
        # 右矢印キーを押した
        if pressed_keys[pygame.K_RIGHT]:
            # プレイヤーが右に移動
            self.player_right()
        # 左矢印キーを押した
        elif pressed_keys[pygame.K_LEFT]:
            # プレイヤーが左に移動
            self.player_left()
        # 上矢印を押した
        elif pressed_keys[pygame.K_UP]:
            # プレイヤーが上に移動
            self.player_up()
        # 下矢印を押した
        elif pressed_keys[pygame.K_DOWN]:
            # プレイヤーが下に移動
            self.player_down()
        time.sleep(0.1)  # 0.1秒間停止
        # 敵を移動
        self.move_enemie(self.set_location_E1, self.set_enemie1, self.location_e1, self.enemie1)
        self.move_enemie(self.set_location_E2, self.set_enemie2, self.location_e2, self.enemie2)
        self.move_enemie(self.set_location_E3, self.set_enemie3, self.location_e3, self.enemie3)
        self.redraw()  # 再描画


# -------------------------------------------------------------------
# 下準備
game = MazeGame()  # インスタンス化
game.set_location_P(PLAYER_ROW, PLAYER_COL)  # プレイヤーの初期位置をセット
# 敵の初期位置をセット
game.set_location_E1(ENEMIE_ROW1, ENEMIE_COL1)
game.set_location_E2(ENEMIE_ROW2, ENEMIE_COL2)
game.set_location_E3(ENEMIE_ROW3, ENEMIE_COL3)
# プレイヤーを初期位置に描画
game.set_player((PLAYER_COL + 1) * 20 + 5, (PLAYER_ROW + 1) * 20 + 5, PLAYER_D)
# 敵を初期位置に描画
game.set_enemie1((ENEMIE_COL1 + 1) * 20, (ENEMIE_ROW1 + 1) * 20)
game.set_enemie2((ENEMIE_COL2 + 1) * 20, (ENEMIE_ROW2 + 1) * 20)
game.set_enemie3((ENEMIE_COL3 + 1) * 20, (ENEMIE_ROW3 + 1) * 20)
# while文のための変数
loop = True
loop2 = False
loop3 = False
# メインルーチン
while loop:
    for event in pygame.event.get():
        # 「閉じる」ボタンを処理する
        if event.type == pygame.QUIT:
            loop = False
    game.start()  # 全体を動かす
    if game.goal:  # ゴールしたら
        loop2 = True
        break
    if game.fin:  # 敵と接触したら
        loop3 = True
        break

# ゴールしたら、GameClearの画面を表示させる
while loop2:
    for event in pygame.event.get():
        # 「閉じる」ボタンを処理する
        if event.type == pygame.QUIT:
            loop2 = False
    # ゲームを終了させるには、右上の×を押すと表示
    text5 = font2.render("If you want to finish, please click ×.", True, BLUE)
    screen.blit(image4, (0, 0))  # GameClearの画像
    screen.blit(text5, (50, 700))  # text5をscreenに転送
    pygame.display.flip()  # ディスプレイに表示

# 敵と接触したら、GameOverの画面を表示させる
while loop3:
    for event in pygame.event.get():
        # 「閉じる」ボタンを処理する
        if event.type == pygame.QUIT:
            loop3 = False
    # ゲームを終了させるには、右上の×を押すと表示
    text4 = font2.render("If you want to finish, please click ×.", True, RED)
    screen.blit(image2, (0, 0))  # GameOverの画像をscreenに転送
    screen.blit(text4, (50, 700))  # text4をscreenに転送
    pygame.display.flip()  # ディスプレイに表示
pygame.quit()
