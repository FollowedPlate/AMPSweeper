import random

from helpers import Queens


class Game:
    def __init__(self):
        self.n = 8
        self.__board = [[0] * self.n for _ in range(self.n)]
        self.title = "AMPSweeper"
        self.symbols = {
            ' ': '🚩',
            '🚩': ' ',
            '0':'0',
            '1':'1',
            '2':'2',
            '3':'3',
            '4':'4',
            '5':'5',
            '6':'6',
            '7':'7',
            '8':'8',
            '9':'9',
            '💥':'💥',
            ' ':' '
            # 'Ｏ':'Ｘ',
            # 'Ｘ':'♛',
            # '♛':'Ｏ'
            # '_':'X',
            # 'X':'Q',
            # 'Q':'_'
            # '🧺': '🦗',
            # '🦗': '🐜',
            # '🐜': '🧺'
        }
        # remember to reset any values when create_board is called, as there is only one Game.Game() object
        self.random = random
        self.color_map = None
        pass

    @property
    def board(self):
        return self.__board

    def process_click(self, data:dict[str, str]) -> dict[str, ...]:
        ret = {}
        # ret["0_0"] = ("9", "test1")
        # ret["3_3"] = ("2", "test1")
        print(data)
        for key in data:
            rkey = (int(key[0]), int(key[2]))
            if self.__board[rkey[0]][rkey[1]] != 9:
                ret[key] = (" ", "test1")
                self.color_map[rkey] = "test1"
            else:
                for i in range(self.n):
                    for j in range(self.n):
                        ret[f"{i}_{j}"] = ("💥", "test3")
        return ret

    def is_solved(self, data):
        # data = {"0_0":"🧺","0_1":"🧺","0_2":"🧺","0_3":"🧺","0_4":"🧺","1_0":"🧺","1_1":"🧺","1_2":"🧺","1_3":"🧺","1_4":"🧺","2_0":"🧺","2_1":"❌","2_2":"🧺","2_3":"🧺","2_4":"🧺","3_0":"🧺","3_1":"🧺","3_2":"🧺","3_3":"🧺","3_4":"🧺","4_0":"🧺","4_1":"🧺","4_2":"🧺","4_3":"🧺","4_4":"🧺"}

        return False

    def generate_color_map(self, answer: list[tuple[int, int]]) -> dict[int, str]:
        ret = {}
        for r, c in answer:
            ret[(r, c)] = "test1"
        for r in range(0, self.n):
            for c in range(0, self.n):
                if not (r, c) in ret:
                    ret[(r, c)] = ret.get((r, c), "test")
        return ret

    def create_board(self, n: int, seed):
        if not seed or seed == "":
            seed = random.random()
        self.n = n
        self.__board = [[0] * self.n for _ in range(self.n)]
        self.__board[0][0] = 9
        self.random.seed(seed)
        self.color_map = self.generate_color_map(list())


    def select_color(self, r, c):
        return self.color_map[(r, c)]

    def html(self):
        '''HTML-formatted board'''
        symbols_list = list(self.symbols.keys())
        board_str = "<table class='centerTable'>"
        for i in range(self.n):
            board_str += "<tr>"
            for c in range(self.n):
                # board_str += f"<td id='{i}_{c}' class='{self.select_color(i, c)}' width='50' height='50'>{symbols_list[self.__board[i][c]]}</td>"
                board_str += f"<td id='{i}_{c}' class='{self.select_color(i, c)}' width='50' height='50'>{symbols_list[0]}</td>"
            board_str += "</tr>"
        board_str += "</table>"
        return board_str


    def __str__(self):
        '''Human-formatted board'''
        symbols_list = list(self.symbols.keys())

        board_str = ""
        for i in range(self.n):
            for c in range(self.n):
                board_str += f"{symbols_list[self.__board[3 * i + c]]}"
                if c < self.n - 1:
                    board_str += "|"
                else:
                    board_str += "\n"
            if i < self.n - 1:
                board_str += "-" * ((self.n - 1) * 3 + 2) + "\n"
        return board_str


if __name__ == "__main__":
    game = Game()
    # print(game)
    # game.create_board(4)
    # print(game.html())
    # print(game)
