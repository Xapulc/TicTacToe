class ElemCourse:
    def __init__(self, x, y, value=None):
        if value is not None:
            if value == 'x':
                self.value = 1
            elif value == 'o':
                self.value = 0
            else:
                raise Exception("Wrong value")
        else:
            self.value = None

        assert (0 <= x < 3)
        assert (0 <= y < 3)
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x) and (self.y == other.y)

    def onGenDiag(self):
        return self.x == self.y

    def onSndDiag(self):
        return self.x + self.y == 2
