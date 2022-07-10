# 20K0112 大村琉聖
# 最終課題-メイン：迷路脱出ゲーム

from dataclasses import dataclass, field

# 迷路のクラス
@dataclass
class Maze:
    height: int = field(init=False, default=None)
    width: int = field(init=False, default=None)
    floormap: list = field(init=False, default=None)
    floormap2: list = field(init=False, default=None)

    def from_file(self, filename):  # ファイルを読み込み、行ごとにリスト化し、それらをさらにまとめてリストにする
        self.floormap = []
        with open(filename) as file:  # ファイルを開く
            first_line = file.readline().rstrip("\n")  # 改行を削除する
            first = first_line.split(",")  # first_lineの行を,で区切る
            self.height = int(first[0])  # first_lineの行の1文字目をheightとする
            self.width = int(first[1])  # first_lineの行の2文字目をwidthとする
            for line in file:  # 各行について確認していく
                line = line.rstrip("\n")  # 改行を削除する
                lines = []
                for i in line:  # 改行を消した行を1文字ずつリストlinesに加えていく
                    lines.append(int(i))
                self.floormap.append(lines)
            return self.floormap
