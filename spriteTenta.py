import gametiles

TILESIZE = gametiles.TILESIZE
SPRITE_SPEED = TILESIZE
PASSABLEBLOCKS = gametiles.PASSABLEBLOCKS


class SpriteEnemy():
    def __init__(self):
        self.xpos, self.ypos = 0, 0
        self.orientation = 0

    def move(self, dir):
        if dir == "up" and self.checkPos(self.xpos, self.ypos - SPRITE_SPEED):
            self.ypos -= SPRITE_SPEED
            self.orientation = 1
        if dir == "right" and self.checkPos(self.xpos + SPRITE_SPEED, self.ypos):
            self.xpos += SPRITE_SPEED
            self.orientation = 2
        if dir == "left" and self.checkPos(self.xpos - SPRITE_SPEED, self.ypos):
            self.xpos -= SPRITE_SPEED
            self.orientation = 0
        if dir == "down" and self.checkPos(self.xpos, self.ypos + SPRITE_SPEED):
            self.ypos += SPRITE_SPEED
            self.orientation = 3

    def checkPos(self, x, y):
        if (x//TILESIZE >= gametiles.TILEWIDTH or y//TILESIZE >= gametiles.TILEHEIGHT) or (x < 0 or y < 0):
            return False
        else:
            TargetTile = gametiles.getActiveTile(x, y)
        if not TargetTile.blockid in PASSABLEBLOCKS:
            TargetTile.setBlockID(100)
            return False
        else:   return True