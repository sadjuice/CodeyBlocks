class Buffer():
    """
    Buffer's are small texture overlays for texturing purposes.
    These are NOT tiles.
    """
    def __init__(self):
        self.x, self.y = 0, 0
        self.type = 0
        self.orientation = 0
        self.color = (255,255,255)
        """
            Type list
            0 - Vertical
            1 - Horizontal
            2 - Diagonal
        """
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