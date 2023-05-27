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


def reset():
    global inner, middle, outer
    inner = Ring(0, 240)
    middle = Ring(180, -60)
    outer = Ring(120, 120)


inner = Ring(0, 240)
middle = Ring(180, -60)
outer = Ring(120, 120)

# kaizhuan([2,1,1])
flag = False
for i in range(0,3):
    for j in range(0,3):
        for k in range(0,3):
            reset()
            print("===================")
            print(i,j,k)
            kaizhuan([i,j,k])
            if inner.curang==0 and middle.curang==0 and outer.curang==0:
                print("igoooooooooooooooooooootthis")
                print("内中：",i,"内外：",j,"中外：",k)
                flag = True
                break
        if flag:
            break
    if flag:
        break





