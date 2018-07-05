import gametiles, inventory, random

BLOCKLIST = gametiles.BLOCKLIST

#COLOR VARIABLES
WHITE   =   (255,255,255)
BLACK   =   (0,0,0)
RED     =   (255,0,0)

PLAYER_SPEED = 16

class Player():
    def __init__(self):
        self.xpos = 0
        self.ypos = 0
        self.inv = inventory.Inventory()

    def checkPos(self, x, y):
        if x//16 >= gametiles.TILEWIDTH or y//16 >= gametiles.TILEHEIGHT:
            return False
        elif x < 0 or y < 0:
            return False
        else:
            return True

    def move(self, dir):
        if dir == "up":
            if self.checkPos(self.ypos - PLAYER_SPEED, self.ypos):    self.ypos -= PLAYER_SPEED
        if dir == "right":
            if self.checkPos(self.xpos+PLAYER_SPEED, self.ypos):    self.xpos += PLAYER_SPEED
        if dir == "left":
            if self.checkPos(self.xpos-PLAYER_SPEED, self.ypos):    self.xpos -= PLAYER_SPEED
        if dir == "down":
            if self.checkPos(self.ypos+PLAYER_SPEED, self.ypos):    self.ypos += PLAYER_SPEED

    def getPos(self):   return self.xpos, self.ypos

    def grabTile(self):
        inv = self.inv
        tile = gametiles.getActiveTile(self.xpos,self.ypos)
        inv.addItem(tile.blockid, 1)

    def placeTile(self):
        tile = gametiles.getActiveTile(self.xpos, self.ypos)
        if not self.inv.isEmpty():
            d = random.choice(list(self.inv.grabList().keys()))
            if self.inv.inInv(d):
                self.inv.removeItem(d, 1)
                tile.setBlockID(d)


MainPlayer = Player()


