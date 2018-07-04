import gametiles

#COLOR VARIABLES
WHITE   =   (255,255,255)
BLACK   =   (0,0,0)
RED     =   (255,0,0)

PLAYER_SPEED = 16

class Player():
    def __init__(self):
        self.xpos = 0
        self.ypos = 0

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

MainPlayer = Player()


