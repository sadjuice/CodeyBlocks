BUFFERIMAGES = ["images/buffers/buff_"+str(x)+".png" for x in range(0,8)]

class Buffer():
    """
    Buffer's are small texture overlays for texturing purposes.
    These are NOT tiles.
    """
    def __init__(self):
        self.x, self.y = 0, 0
        self.type = -1
        self.orientation = 0
        self.color = (255,255,255)
        self.xadd, self.yadd = 0, 0
        """
            Type list
            0 - Vertical
            1 - Horizontal
            2 - Diagonal
        """
    def setAdd(self, x, y):
        self.xadd, self.yadd = x, y

    def getPos(self):
        return self.x,  self.y

    def setPos(self, x, y):
        self.x, self.y = x, y

    def setColour(self, color):
        self.color = color

    def getColour(self, color):
        return self.color

    def setType(self, type):
        self.type = type

    def getType(self):
        return self.type