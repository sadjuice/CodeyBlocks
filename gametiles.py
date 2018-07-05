import random

#TILE PARAMETERS DO NOT EDIT!
TILEWIDTH = 32
TILEHEIGHT = 32
TILELIMIT = 512
TILESIZE = 16
TILEGEN = (TILEWIDTH * 10) + 16
#To get a Tile's index of block use xpos // 16, ypos // 16

#COLOR VARIABLES
WHITE   =   (255,255,255)
BLACK   =   (0,0,0)
RED     =   (255,0,0)
GREEN   =   (0,255,0)
BLUE    =   (0,0,255)
PASTEY = (222,222,222)

#BLOCK INFO
BLOCKLIST = {
    0       :   ["GRASS", "grass.png"],
    1       :   ["WATER", "water.png"],
    2       :   ["CLOUD",    PASTEY],
    100     :   ["VOID", BLACK]
}

#GENERATION CONFIG
WATERPERCENTDECLINE = 15

BLOCKCOUPLER = {
    #id : # [list of tiles that have that gen]

}

CLOUDSPEED = 16

class Tile():
    def __init__(self):
        self.colour = WHITE
        self.blockid = 0
        self.status = 0  # VOID var, might use later
        self.covered = 0  # Is something covering the block? 0 - False 1 - True
        self.playerActive = 0  #Is player standing on block?
        self.xpos = 0
        self.ypos = 0

    def properties(self, blockid, xpos, ypos):
        self.blockid = blockid
        self.xpos = xpos
        self.ypos = ypos

    def setBlockID(self, ID):
        self.blockid = ID
        
    def moveTile(self, dir):
        if dir == "up":
            self.ypos -= CLOUDSPEED
        if dir == "right":
            self.xpos += CLOUDSPEED
        if dir == "left":
            self.xpos -= CLOUDSPEED
        if dir == "down":
            self.ypos += CLOUDSPEED

def baseGridGen():
    return [[Tile() for x in range(0, TILEHEIGHT)] for x in range(0, TILEWIDTH)]
TILEMAP = baseGridGen()
CLOUDMAP = [[None for x in range(0,TILEHEIGHT)] for x in range(0,TILEWIDTH)]

WATERLIST = []

#TILE INDEX
#(BLOCKID, LOCATION)
def initGenTile():
    for y in range(0, TILEHEIGHT):
        for x in range(0,TILEWIDTH):
            generint = random.randint(0, 100)
            Tile = TILEMAP[y][x]
            Tile.properties(0, x * TILESIZE, y * TILESIZE)
    for i in range(0,random.randint(1,4)):
        Tile = TILEMAP[random.randint(0,TILEHEIGHT-1)][random.randint(0,TILEWIDTH-1)]
        waterGen(Tile, 100, 1)
    # for i in range(0,1):
    #     waterGen(CLOUDMAP[random.randint(0,TILEHEIGHT-1)][random.randint(0,TILEWIDTH-1)], 10, 2)

def getActiveTile(x, y):
    newx = x // 16
    newy = y // 16
    Tile = TILEMAP[newy][newx]
    return Tile

def getSurrounding(tile):
    l = getRowNeighbor(tile) + getColumnNeighbor(tile)
    return l

def getRowNeighbor(tile):
    #X-Axis
    #LEFT - LEFT, RIGHT - RIGHT
    newx = tile.xpos // 16
    newy = tile.ypos // 16
    l = []
    for x in [-1,1]:
        var = newx+x
        if var >= 0 and var < TILEWIDTH:
            grabTile = TILEMAP[newy][var]
            l.append(grabTile)
    return l

def getColumnNeighbor(tile):
    #Y-Axis
    # LEFT - ROW ABOVE, RIGHT - ROW BELOW
    newx = tile.xpos // 16
    newy = tile.ypos // 16
    l = []
    for y in [-1,1]:
        var = newy+y
        if var >= 0 and var < TILEHEIGHT:
            grabTile = TILEMAP[var][newx]
            l.append(grabTile)
    return l

def waterGen(T, percent, id):
    if T == None:
        T = Tile()
    T.setBlockID(id)
    for newT in getSurrounding(T):
        chanceGen = random.randint(0, 100)
        if chanceGen in [x for x in range(0,percent)]:
            waterGen(newT,percent-WATERPERCENTDECLINE, id)
            # if id in BLOCKCOUPLER.keys():
            #     BLOCKCOUPLER[id].append(T)
            # else:
            #     BLOCKCOUPLER[id] = [T]
    return True



