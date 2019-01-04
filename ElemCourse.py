class ElemCourse(object):
    """
    A player’s move representation that contains the coordinate and sign (X or O)
    """

    def __init__(self, x, y, value=None):
        if value is not None:
            if value == 'x':
                self.value = 1
            elif value == 'o':
                self.value = 0
            else:
                raise ValueError("Wrong value")
        else:
            self.value = None

        assert (0 <= x < 3)
        assert (0 <= y < 3)
        self.x = x
        self.y = y

    def __hash__(self):
        return self.x + 3*self.y + 9*self.value

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def __str__(self):
        return f"{self.x}{self.y}{self.value}"

    def __repr__(self):
        return self.__str__()

    def on_gen_diag(self):
        return self.x == self.y

    def on_snd_diag(self):
        return self.x + self.y == 2
