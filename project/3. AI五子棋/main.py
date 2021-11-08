import numpy as np


# 棋盘
class Map(object):
    def __init__(self):
        self.m = []
        for i in range(3):
            self.m.append([])
            for j in range(3):
                self.m[i].append(0)

    # 打印棋盘
    def print_map(self):
        for i in range(3):
            for j in range(3):
                if self.m[i][j] == 0:
                    print("   ", end='')
                elif self.m[i][j] == 1:
                    print(" X ", end='')
                elif self.m[i][j] == 2:
                    print(" 〇 ", end='')
                if 0 <= j < 2:
                    print("|", end="")
            if i < 2:
                print("\n---+---+---")
            else:
                print("")

    # 终止检测
    def teminate(self):
        n = 0
        m2 = self.m
        m3 = np.transpose(m2).tolist()
        l = [m2[0], m2[1], m2[2], m3[0], m3[1], m3[2], [m2[0][0], m2[1][1], m2[2][2]], [m2[0][2], m2[1][1], m2[2][0]]]
        for i in l:
            if 0 in i:
                n += 1
        if [1, 1, 1] in l or [2, 2, 2] in l:
            return True
        elif n == 0:
            return True
        else:
            return False

    # 获取赢家
    def get_winner(self):
        m2 = self.m
        m3 = np.transpose(m2).tolist()
        l = [m2[0], m2[1], m2[2], m3[0], m3[1], m3[2], [m2[0][0], m2[1][1], m2[2][2]], [m2[0][2], m2[1][1], m2[2][0]]]
        if [1, 1, 1] in l:
            return 1
        elif [2, 2, 2] in l:
            return 2
        else:
            return 0

    def move(self, x, player):
        a = (9 - x) // 3
        b = x - 7 + a * 3
        if self.m[a][b] == 0:
            self.m[a][b] = player
            return True
        return False

    def vaild_move(self):
        t = []
        for i in range(3):
            for j in range(3):
                if self.m[i][j] == 0:
                    t.append(j - i * 3 + 7)
        return t

    def unmove(self, x):
        a = (9 - x) // 3
        b = x - 7 + a * 3
        self.m[a][b] = 0


# 玩家
class Player(object):

    def __init__(self, take=1):  # 默认执的棋子为 take = 'X'
        self.take = take

    def think(self, board):
        pass

    def move(self, board, action):
        board.move(action, self.take)


class HumanPlayer(Player):
    def __init__(self, take):
        super().__init__(take)

    def think(self, board):
        while True:
            action = input("输入你落子的位置,[1~9]")
            if len(action) == 1 and action in '123456789':
                return int(action)


# 电脑玩家
class AIPlayer(Player):
    def __init__(self, take):
        super().__init__(take)

    def think(self, board):
        take = [1, 2][self.take == 1]
        player = AIPlayer(take)  # 假想敌！！！
        _, action = self.minimax(board, player)
        # print('OK')
        return action

    # 极大极小法搜索，α-β剪枝
    def minimax(self, board, player, depth=0):
        if self.take == 2:
            bestVal = -10
        else:
            bestVal = 10

        if board.teminate():
            if board.get_winner() == 1:
                return -10 + depth, None
            elif board.get_winner() == 2:
                return 10 - depth, None
            elif board.get_winner() == 0:
                return 0, None

        for action in board.vaild_move():  # 遍历合法走法
            board.move(action, self.take)
            val, _ = player.minimax(board, self, depth + 1)  # 切换到 假想敌！！！
            board.unmove(action)  # 撤销走法，回溯
            if self.take == 2:
                if val > bestVal:
                    bestVal, bestAction = val, action
            else:
                if val < bestVal:
                    bestVal, bestAction = val, action

        return bestVal, bestAction


# 游戏
class Game(object):
    def __init__(self):
        self.player = Player()
        self.map = Map()
        self.current_player = None
        self.method = None

    # 打印赢家
    def print_winner(self, winner):  # winner in [0,1,2]
        if 1 == winner:
            print("X方获胜")
        elif 2 == winner:
            print("〇方获胜")
        elif 0 == winner:
            print("不胜不败, 平局")

    # 切换玩家
    def switch_player(self, player):
        if player == 1:
            return 2
        else:
            return 1

    # 运行游戏
    def run(self):
        self.current_player = int(input("请选择您是否先手(先:1 后:2):"))

        print('\nGame start!\n')
        self.map.print_map()  # 显示棋盘
        while True:
            if self.current_player == 1:
                action = HumanPlayer(self.current_player).think(self.map)  # 当前玩家对棋盘进行思考后，得到招法
            else:
                action = AIPlayer(self.current_player).think(self.map)  # 当前玩家对棋盘进行思考后，得到招法
            if self.map.move(action, self.current_player):  # 当前玩家执行招法，改变棋盘
                self.current_player = self.switch_player(self.current_player)  # 切换当前玩家
            self.map.print_map()  # 显示当前棋盘
            if self.map.teminate():  # 根据当前棋盘，判断棋局是否终止
                winner = self.map.get_winner()  # 得到赢家 0,1,2
                break

        self.print_winner(winner)
        print('Game over!')


if __name__ == "__main__":
    Game().run()
