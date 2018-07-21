import random, buffer, operator, pygame, drawStack

#TILE PARAMETERS DO NOT EDIT!
TILEWIDTH = 32
TILEHEIGHT = 32
TILELIMIT = TILEWIDTH * TILEHEIGHT
TILESIZE = 30
TILEGEN = (TILEWIDTH * 10) + 16
#To get a Tile's index of block use dimConvert() x//16

basetilesurf = pygame.Surface((TILESIZE * TILEWIDTH, TILESIZE * TILEHEIGHT), pygame.SRCALPHA, 32)

#COLOR VARIABLES
WHITE   =   (255,255,255)
BLACK   =   (0,0,0)
RED     =   (255,0,0)
GREEN   =   (0,255,0)
BLUE    =   (0,0,255)
PASTEY  =   (222,222,222)
YELLOW  = 	(255,255,0)

#BLOCK INFO
BLOCKLIST = {
    0   :   ["GRASS", "grass.png"],
    1   :   ["WATER", "water.png"],
    2   :   ["SAND",    "sand.png"],
    100 :   ["VOID", BLACK]
}

PASSABLEBLOCKS = [0,1,2,100]  #BlockID's that can be walked on

#GENERATION CONFIG
WATERPERCENTDECLINE = 10
NUMBEROFWATERBLOCKS = 4 * (TILEWIDTH // 16)#Max number of lake spawn blocks that can spawn

#Buffer list
BUFFERLIST = {

    #id : # Buffer Class
    #id is (x,y)
}

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

    def getBlockID(self):
        return self.blockid

def baseGridGen():  return [[Tile() for x in range(0, TILEHEIGHT)] for y in range(0, TILEWIDTH)]
# def baseGridGen():  return {(x,y):Tile() for x in range(0, TILEHEIGHT) for y in range(0, TILEWIDTH)}

def grassWaterBuffer(listVar, searchList):
    global BLOCKCOUPLER
    BUFFERGAP = 12
    for Tile in searchList:
        if Tile.blockid == 1:
            for conBlock in getDiagonals(Tile):
                newBuffer = buffer.Buffer()
                newBuffer.setColour(YELLOW)
                if conBlock.blockid == 0:
                    for x in [operator.gt, operator.lt]:
                        for y in [operator.gt, operator.lt]:
                            xadd, yadd = 0, 0
                            if x == operator.lt:    xadd = BUFFERGAP
                            if y == operator.lt:    yadd = BUFFERGAP
                            if x(conBlock.xpos, Tile.xpos) and y(conBlock.ypos, Tile.ypos):
                                if xadd == 0:
                                    if yadd == BUFFERGAP:
                                        newBuffer.setType(6)
                                        yadd += 1
                                        xadd -= 1
                                    elif yadd == 0:
                                        newBuffer.setType(0)
                                if xadd == BUFFERGAP:
                                    if yadd == BUFFERGAP:
                                        newBuffer.setType(4)
                                        xadd += 1
                                        yadd += 1
                                    if yadd == 0:
                                        newBuffer.setType(2)
                                newBuffer.setAdd(xadd, yadd)
                                newBuffer.setPos(conBlock.xpos + xadd, conBlock.ypos + yadd)

                if (conBlock.xpos, conBlock.ypos) in listVar.keys():
                    listVar[conBlock.xpos, conBlock.ypos].append(newBuffer)
                else:
                    listVar[conBlock.xpos, conBlock.ypos] = [newBuffer]
            for conBlock in getRowNeighbor(Tile):
                newBuffer = buffer.Buffer()
                newBuffer.setType(1)
                newBuffer.setColour(YELLOW)
                if conBlock.blockid == 0:
                    for x in [operator.gt, operator.lt]:
                        xadd = 0
                        if x == operator.lt:    xadd = BUFFERGAP
                        if x(conBlock.xpos, Tile.xpos):
                            newBuffer.setPos(conBlock.xpos + xadd, conBlock.ypos)
                            newBuffer.setAdd(xadd, 0)
                            if xadd == 0:
                                newBuffer.setType(7)
                            elif xadd == BUFFERGAP:
                                newBuffer.setType(3)
                    if (conBlock.xpos, conBlock.ypos) in listVar.keys():
                        listVar[conBlock.xpos, conBlock.ypos].append(newBuffer)
                    else:
                        listVar[conBlock.xpos, conBlock.ypos] = [newBuffer]
            for conBlock in getColumnNeighbor(Tile):
                newBuffer = buffer.Buffer()
                newBuffer.setType(0)
                newBuffer.setColour(YELLOW)
                if conBlock.blockid == 0:
                    for x in [operator.gt, operator.lt]:
                        xadd, yadd = 0, 0
                        if x == operator.lt:    yadd = BUFFERGAP
                        if x(conBlock.ypos, Tile.ypos):
                            newBuffer.setPos(conBlock.xpos, conBlock.ypos + yadd)
                            newBuffer.setAdd(xadd, yadd)
                            if yadd == BUFFERGAP:
                                newBuffer.setType(5)
                            elif yadd == 0:
                                newBuffer.setType(1)
                    if (conBlock.xpos, conBlock.ypos) in listVar.keys():
                        listVar[conBlock.xpos, conBlock.ypos].append(newBuffer)
                    else:
                        listVar[conBlock.xpos, conBlock.ypos] = [newBuffer]
    return listVar
TILEMAP = baseGridGen()

#TILE INDEX
def initGenTile():
    global BLOCKCOUPLER, BUFFERLIST
    BLOCKCOUPLER = {}
    BUFFERLIST = {}
    [TILEMAP[y][x].properties(0, x * TILESIZE, y * TILESIZE) for x in range(0,TILEWIDTH) for y in range(0,TILEHEIGHT)]
    for i in range(0,random.randint(1,NUMBEROFWATERBLOCKS)):
        Tile = TILEMAP[random.randint(0,TILEHEIGHT-1)][random.randint(0,TILEWIDTH-1)]
        waterGen(Tile, 100, 1)
    BUFFERLIST = grassWaterBuffer(BUFFERLIST, BLOCKCOUPLER[1])
    for tile in [TILEMAP[x][y] for x in range(0, TILEHEIGHT) for y in range(0, TILEWIDTH)]:
        try:
            BLOCKCOUPLER[tile.getBlockID()].append(tile)
        except:
            BLOCKCOUPLER[tile.getBlockID()] = [tile]


def dimConvert(val):    return val//TILESIZE #Converts dimensions to // tile dimension

def getActiveTile(x, y):
    Tile = TILEMAP[dimConvert(y)][dimConvert(x)]
    return Tile

def getSurrounding(tile):
    return getRowNeighbor(tile) + getColumnNeighbor(tile) + getDiagonals(tile)

def getRowNeighbor(tile):
    #X-Axis
    #LEFT - LEFT, RIGHT - RIGHT
    newx, newy = dimConvert(tile.xpos), dimConvert(tile.ypos)
    l = []
    for x in [-1,1]:
        var = newx+x
        if var >= 0 and var < TILEWIDTH:
            grabTile = TILEMAP[newy][var]
            l.append(grabTile)
    return l

def getDiagonals(tile):
    newx, newy = dimConvert(tile.xpos), dimConvert(tile.ypos)
    l = []
    for x in [-1,1]:
        for y in [-1,1]:
            varx = newx+x
            vary = newy+y
            if (varx >= 0 and varx < TILEWIDTH) and (vary >= 0 and vary < TILEHEIGHT):
                grabTile = TILEMAP[vary][varx]
                l.append(grabTile)
    return l

def getColumnNeighbor(tile):
    #Y-Axis || LEFT - ROW ABOVE, RIGHT - ROW BELOW
    newx, newy = dimConvert(tile.xpos), dimConvert(tile.ypos)
    l = []
    for y in [-1,1]:
        var = newy+y
        if var >= 0 and var < TILEHEIGHT:
            grabTile = TILEMAP[var][newx]
            l.append(grabTile)
    return l

def waterGen(T, percent, id):
    global BLOCKCOUPLER
    if T == None:
        T = Tile()
    T.setBlockID(id)
    if id in BLOCKCOUPLER.keys():   BLOCKCOUPLER[id].append(T)
    else:   BLOCKCOUPLER[id] = [T]
    for newT in (getRowNeighbor(T) + getColumnNeighbor(T)):
        chanceGen = random.randint(0, 100)
        if chanceGen in [x for x in range(0,percent)]:  waterGen(newT,percent-WATERPERCENTDECLINE, id)
    return True



