class Square:

    def __init__(self, xcoordinate, ycoordinate, piececolor, type, available):
        self.xcoordinate = xcoordinate
        self.ycoordinate = ycoordinate
        self.piececolor = piececolor # 1 = black, 2 = white
        self.type = type
        self.available = available