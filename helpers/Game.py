import random

BOMB_NUM_SCALE_EASY = 25
BOMB_NUM_SCALE_MEDIUM = 15
BOMB_NUM_SCALE_HARD = 5

BOMB_VAL = -1

class Game:
    def __init__(self, n: int = 8, seed: str = "", difficulty: str = "easy"):
        self.n = n
        self.title = "AMPSweeper"
        self.symbols = {
            ' ': '🚩',
            '🚩': ' ',
            'x':'x',
            '0': '0',
            '1': '1',
            '2': '2',
            '3': '3',
            '4': '4',
            '5': '5',
            '6': '6',
            '7': '7',
            '8': '8',
            '9': '9',
            '💥': '💥',
            ' ': ' '
        }

        # remember to reset any values when create_board is called, as there is only one Game.Game() object
        self.random = random
        self.has_lost = False

        # random seed if none is given
        if seed == "":
            seed = str(random.random())
        self.random.seed(float(seed))

        self.__board = [[0] * self.n for _ in range(self.n)]
        self.color_map = self.generate_color_map(list())

        self.create_board(difficulty)

        print(self.__board)

    @property
    def board(self):
        return self.__board

    # Main ideas for modifications:
    # Difficulty:
    #   - Run a second round of mine placement after the initial one
    #       - Easy has a 0.75 * (Num of mine around square / 8) + 0.25 * (Num of mines in up/down/left/right) chance of generating an extra mine per square to encourage mine clumping and easy patterns
    #       - Medium has a 0.1 chance of generating an extra mine per square
    #       - Hard has a 0.1 + (Num of 1's and 2's around square / 8) chance of generating an extra mine per square to encourage more deduction
    def create_board(self, difficulty: str):
        bomb_scale = BOMB_NUM_SCALE_EASY
        if difficulty == "medium":
            bomb_scale = BOMB_NUM_SCALE_MEDIUM
        elif difficulty == "hard":
            bomb_scale = BOMB_NUM_SCALE_HARD

        bombs = set()
        tiles_to_change = list()

        # Original mine placement
        for _ in range(self.n ** 2 // bomb_scale):
            # Select the tile to be bombed
            rbomb = self.random.randint(0, self.n - 1)
            cbomb = self.random.randint(0, self.n - 1)
            self.__board[rbomb][cbomb] = BOMB_VAL
            bombs.add((rbomb, cbomb))

            # Mark surrounding tiles to be changed if inside board range
            for tup in [(rbomb - 1, cbomb), (rbomb - 1, cbomb + 1), (rbomb, cbomb + 1), (rbomb + 1, cbomb + 1),
                        (rbomb + 1, cbomb), (rbomb + 1, cbomb - 1), (rbomb, cbomb - 1), (rbomb - 1, cbomb - 1)]:
                if self.n > tup[0] >= 0 <= tup[1] < self.n:
                    tiles_to_change.append(tup)

        # Mark tiles based on how many mines are nearby
        for tup in tiles_to_change:
            if self.__board[tup[0]][tup[1]] != BOMB_VAL:
                chk_set = {(tup[0] - 1, tup[1]), (tup[0] - 1, tup[1] + 1), (tup[0], tup[1] + 1), (tup[0] + 1, tup[1] + 1),
                           (tup[0] + 1, tup[1]), (tup[0] + 1, tup[1] - 1), (tup[0], tup[1] - 1), (tup[0] - 1, tup[1] - 1)}
                self.__board[tup[0]][tup[1]] = len(chk_set.intersection(bombs))

        # Difficulty based mines
        for _ in range(self.n ** 2 // bomb_scale):
            rbomb = self.random.randint(0, self.n - 1)
            cbomb = self.random.randint(0, self.n - 1)

            bomb_chance = 0.1
            if difficulty == "easy" or difficulty == "hard":
                surrounding_vals = []
                for tup in [(rbomb - 1, cbomb), (rbomb - 1, cbomb + 1), (rbomb, cbomb + 1), (rbomb + 1, cbomb + 1),
                        (rbomb + 1, cbomb), (rbomb + 1, cbomb - 1), (rbomb, cbomb - 1), (rbomb - 1, cbomb - 1)]:
                    if self.n > tup[0] >= 0 <= tup[1] < self.n:
                        surrounding_vals.append(self.__board[tup[0]][tup[1]])
                    else:
                        surrounding_vals.append(-2)

                if difficulty == "easy":
                    bomb_chance = 0.75 * (surrounding_vals.count(-1) / 8) + 0.25 * ((
                        1 if surrounding_vals[1] == BOMB_VAL else 0 +
                        1 if surrounding_vals[3] == BOMB_VAL else 0 +
                        1 if surrounding_vals[5] == BOMB_VAL else 0 +
                        1 if surrounding_vals[7] == BOMB_VAL else 0
                    ) / 4)
                else:
                    bomb_chance += (surrounding_vals.count(1) + surrounding_vals.count(2)) / 8

            if self.random.random() > bomb_chance:
                continue

            self.__board[rbomb][cbomb] = BOMB_VAL
            bombs.add((rbomb, cbomb))

            for tup in [(rbomb - 1, cbomb), (rbomb - 1, cbomb + 1), (rbomb, cbomb + 1), (rbomb + 1, cbomb + 1),
                        (rbomb + 1, cbomb), (rbomb + 1, cbomb - 1), (rbomb, cbomb - 1), (rbomb - 1, cbomb - 1)]:
                if self.n > tup[0] >= 0 <= tup[1] < self.n:
                    tiles_to_change.append(tup)

        for tup in tiles_to_change:
            if self.__board[tup[0]][tup[1]] != BOMB_VAL:
                chk_set = {(tup[0] - 1, tup[1]), (tup[0] - 1, tup[1] + 1), (tup[0], tup[1] + 1), (tup[0] + 1, tup[1] + 1),
                           (tup[0] + 1, tup[1]), (tup[0] + 1, tup[1] - 1), (tup[0], tup[1] - 1), (tup[0] - 1, tup[1] - 1)}
                self.__board[tup[0]][tup[1]] = len(chk_set.intersection(bombs))

        self.safest_tiles = list()
        for row in range(self.n):
            for col in range(self.n):
                if self.__board[row][col] == 0:
                    self.safest_tiles.append((row, col))

    def process_click(self, data: dict[str, str]) -> dict[str, ...]:
        ret = {}
        # ret["0_0"] = ("9", "test1")
        # ret["3_3"] = ("2", "test1")
        print(data)
        if self.has_lost:
            return ret
        for key in data:
            r = int(key.split("_")[0])
            c = int(key.split("_")[1])
            if self.__board[r][c] == 0:
                to_check = list()
                to_check.append((r, c))
                while len(to_check) > 0:
                    tup = to_check.pop()
                    tlret = self.__board[tup[0]][tup[1]]
                    if tlret == 0:
                        tlret = " "
                    else:
                        tlret = str(tlret)
                    ret[f"{tup[0]}_{tup[1]}"] = (tlret, "test1")
                    self.color_map[(r, c)] = "test1"
                    if self.__board[tup[0]][tup[1]] == 0:
                        for nxt in [(tup[0] - 1, tup[1]), (tup[0] - 1, tup[1] + 1), (tup[0], tup[1] + 1), (tup[0] + 1, tup[1] + 1),
                           (tup[0] + 1, tup[1]), (tup[0] + 1, tup[1] - 1), (tup[0], tup[1] - 1), (tup[0] - 1, tup[1] - 1)]:
                            # print(f"{nxt} one: {self.n > nxt[0] >= 0} two: {0 <= nxt[1] < self.n} three: {self.__board[nxt[0]][nxt[1]] == 0} four: {f"{nxt[0]}_{nxt[1]}" not in ret}")
                            # print(ret)
                            if self.n > nxt[0] >= 0 <= nxt[1] < self.n and f"{nxt[0]}_{nxt[1]}" not in ret:
                                to_check.append((nxt[0], nxt[1]))
            elif self.__board[r][c] != BOMB_VAL:
                ret[key] = (str(self.__board[r][c]), "test1")
                self.color_map[(r, c)] = "test1"
            else:
                for i in range(self.n):
                    for j in range(self.n):
                        if self.__board[i][j] == BOMB_VAL:
                            ret[f"{i}_{j}"] = ("💥", "test3")
                self.has_lost = True

        return ret

    @staticmethod
    def board_to_string(board) -> str:
        ret = ""
        for row in board:
            for cell in row:
                ret += str(cell)
        return ret

    def submit(self, data):
        if self.has_lost:
            return {"return":"you have lost"}
        is_valid_solution = True
        for r in range(self.n):
            for c in range(self.n):
                key = f"{r}_{c}"
                tdata = data[key]
                if tdata == "\u2003":
                    tdata = 0
                elif tdata == "🚩":
                    tdata = 9
                else:
                    tdata = int(tdata)
                if self.__board[r][c] != tdata:
                    print(f"differece at {r},{c}")
                    is_valid_solution = False
        ret = ""
        if is_valid_solution:
            ret = "SOLUTION WORKS YIPPEE"
        else:
            ret = "not done :("
        return {"result": ret}

    def is_solved(self, data):
        # data = {"0_0":"🧺","0_1":"🧺","0_2":"🧺","0_3":"🧺","0_4":"🧺","1_0":"🧺","1_1":"🧺","1_2":"🧺","1_3":"🧺","1_4":"🧺","2_0":"🧺","2_1":"❌","2_2":"🧺","2_3":"🧺","2_4":"🧺","3_0":"🧺","3_1":"🧺","3_2":"🧺","3_3":"🧺","3_4":"🧺","4_0":"🧺","4_1":"🧺","4_2":"🧺","4_3":"🧺","4_4":"🧺"}

        return False

    def generate_color_map(self, answer: list[tuple[int, int]]) -> dict[tuple[int, int], str]:
        ret = {}
        for r, c in answer:
            ret[(r, c)] = "test1"
        for r in range(0, self.n):
            for c in range(0, self.n):
                if not (r, c) in ret:
                    ret[(r, c)] = ret.get((r, c), "test")
        return ret

    def select_color(self, r, c):
        return self.color_map[(r, c)]

    def html(self):
        '''HTML-formatted board'''
        symbols_list = list(self.symbols.keys())
        board_str = "<table class='centerTable'>"
        sr, sc = self.random.choice(self.safest_tiles)
        for r in range(self.n):
            board_str += "<tr>"
            for c in range(self.n):
                # board_str += f"<td id='{i}_{c}' class='{self.select_color(i, c)}' width='50' height='50'>{symbols_list[self.__board[i][c]]}</td>"
                if r==sr and c==sc:
                    board_str += f"<td id='{r}_{c}' class='{self.select_color(r, c)}' width='50' height='50'>x</td>"
                else:
                    board_str += f"<td id='{r}_{c}' class='{self.select_color(r, c)}' width='50' height='50'>{symbols_list[0]}</td>"

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
