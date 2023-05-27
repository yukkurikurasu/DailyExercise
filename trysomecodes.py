class Ring:
    def __init__(self, init, multi):
        self.init = init
        self.multi = multi
        self.curang = self.init

    def roll(self):
        self.curang += self.multi
        if self.curang > 359:
            self.curang -= 360
        # print(self.curang)


def rolltoge(a, b):
    a.roll()
    b.roll()
    print(inner.curang, middle.curang, outer.curang)


def kaizhuan(array):
    for i in range(0, array[0]):
        rolltoge(inner, middle)
    for i in range(0, array[1]):
        rolltoge(inner, outer)
    for i in range(0, array[2]):
        rolltoge(middle, outer)


def reset(a,b,c):
    a = Ring(0, 240)
    b = Ring(180, -60)
    c = Ring(120, 120)


inner = Ring(0, 240)
middle = Ring(180, -60)
outer = Ring(120, 120)

kaizhuan([1,3,2])




