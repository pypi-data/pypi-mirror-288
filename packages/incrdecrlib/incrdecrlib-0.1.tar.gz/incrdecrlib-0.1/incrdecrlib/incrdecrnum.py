class incrdecrnum:
    def __init__(self, value=0):
        self.value = value

    def incr(self):
        self.value += 1
        return self

    def decr(self):
        self.value -= 1
        return self

    def __repr__(self):
        return str(self.value)