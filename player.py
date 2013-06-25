import random


class Player(object):
    def __init__(self, name):
        self.name = name

    def move(self, ):
        raise NotImplementedError

    @property
    def symbol(self,):
        return self.name


class HumanPlayer(Player):
    def move(self, ):
        col = raw_input("enter column number 0 to 6")
        try:
            col = int(col)
        except ValueError:
            col = None
        return col


class DumbCpuPlayer(Player):
    def move(self, ):
        return random.choice([x for x in range(7)])


class DumbestCpuPlayer(Player):
    def move(self, ):
        return 0
