from typing import Literal


class Piece:
    def __init__(self, name, color):
        self.name = name
        self.moves = {"up": self.up,
                      "down": self.down,
                      "left": self.left,
                      "right": self.right,
                      "diagonal": self.diagonal,
                      }
        self.color = color
        self.pos = "A1"
        self.range = 1

    def posstr_to_pos(self):
        return ord(self.pos[0]) - 64, int(self.pos[1])

    def color_side(self):
        return 1 if self.color == "W" else -1

    def up(self):
        self.pos = self.pos[0] + str(int(self.pos[1]) + self.color_side())
        return self
    def right(self):
        self.pos = str(self.posstr_to_pos()[0] + self.color_side()) + self.pos[1]
        return self
    def down(self):
        self.pos = self.pos[0] + str(int(self.pos[1]) - self.color_side())
        return self
    def left(self):
        self.pos = str(self.posstr_to_pos()[0] - self.color_side()) + self.pos[1]
        return self
    def diagonal(self, xdir:Literal["left", "right"]="right",
                 ydir:Literal["up", "down"]="up"):
        self.pos = self.moves[xdir]
        self.pos = self.moves[ydir]
        return self

row_init = {"W":1, "B":8}


class Roi(Piece):
    def __init__(self, color):
        Piece.__init__(self, "K", color)
        self.moves_known = ["diagonal", "up", "down", "left", "right"]
        self.special_moves = ["castle"]
        self.pos = "E" + str(row_init[color])
        self.range = 1

    def move(self, action, **kwargs):
        self.moves[action](**kwargs)

class Pion(Piece):
    def __init__(self, column:Literal["A", "B", "C", "D", "E", "F", "G", "H"], color):
        Piece.__init__(self, "P", color)
        self.moves_known = ["up"]
        self.special_moves = ["diagonal", "left", "right", "start"]
        self.pos = column + str(row_init[color] + self.color_side())
        self.range = 1

    def move(self, action, **kwargs):
        if action == "start":
            self.up().up()
        else:
            self.moves[action](**kwargs)
        self.special_moves.remove("start")

class Fou(Piece):
    def __init__(self, column, color):
        Piece.__init__(self, "F", color)
        self.moves_known = ["diagonal"]
        self.directions = ["up", "down", "left", "right"]

        self.pos = column + str(row_init[color])
        self.range = 8

    def move(self, xdir, ydir, nb_case):
        for _ in range(nb_case):
            self.diagonal(xdir, ydir)

class Dame(Piece):
    def __init__(self, color):
        Piece.__init__(self, "Q", color)
        self.moves_known = ["diagonal", "up", "down", "left", "right"]

        self.pos = "D" + str(row_init[color])
        self.range = 8

    def move(self, action, nb_cases, **kwargs):
        for _ in range(nb_cases):
            self.moves[action](**kwargs)

class Tour(Piece):
    def __init__(self, column, color):
        Piece.__init__(self, "T", color)
        self.moves_known = ["up", "down", "left", "right"]

        self.pos = column + str(row_init[color])
        self.range = 8

    def move(self, action, nb_cases):
        for _ in range(nb_cases):
            self.moves[action]()

class Cavalier(Piece):
    def __init__(self, column, color):
        Piece.__init__(self, "C", color)
        self.moves_known = ["up", "down", "left", "right"]

        self.pos = column + str(row_init[color])

    def move(self, action1, action2):
        self.moves[action1]()
        self.moves[action1]()
        self.moves[action2]()