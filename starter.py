import sys, spritesrc, gametiles, pygame, drawStack, buffer
from pygame.locals import *

pygame.init()

#PYGAME variables
TILESIZE = spritesrc.TILESIZE
TILEWIDTH = gametiles.TILEWIDTH
TILEHEIGHT = gametiles.TILEHEIGHT

clock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode(((TILESIZE * TILEWIDTH)+200, TILESIZE * TILEHEIGHT))   # pygame.FULLSCREEN
BUFFERSURF = pygame.display.set_mode((TILESIZE * TILEWIDTH+200,   TILESIZE * TILEHEIGHT))     # Buffer surface
displaywidth, displayheight = pygame.display.get_surface().get_size()
pygame.display.set_caption('Codey Blocks')
TestText = pygame.font.SysFont("Comic Sans MS",256)

#COLOUR PALETTE
WHITE   =   (255,255,255)
BLACK   =   (0,0,0)
RED     =   (255,0,0)
GREEN   =   (0,255,0)
BLUE    =   (0,0,255)
YELLOW  = 	(255,255,0)

#MAP VARIABLES
MAPGENERATED = 0
MAPUNCHANGED = 0
BUFFERDRAWN = 0
TILEMAP = gametiles.TILEMAP
BLOCKLIST = gametiles.BLOCKLIST
BLOCKTEXTURES = {}
BUFFERTEXTURES = {}
PASSABLEBLOCKS = gametiles.PASSABLEBLOCKS

#Surfaces
wholesurf = pygame.Surface((TILESIZE * TILEWIDTH, TILESIZE * TILEHEIGHT), pygame.SRCALPHA, 32)

basetilesurf = gametiles.basetilesurf

#TEXTURE MAP
for block in gametiles.BLOCKLIST.keys():
    if isinstance(BLOCKLIST[block][1],str): BLOCKTEXTURES[block] = pygame.image.load("images/blocks/"+BLOCKLIST[block][1])
    else:   BLOCKTEXTURES[block] = BLOCKLIST[block][1]

def displayTile(requestedDisplay, x, y, SURFACE=DISPLAYSURF):
    scale = (TILESIZE,TILESIZE)
    displayType = type(requestedDisplay)
    if displayType in [gametiles.Tile, buffer.Buffer, pygame.Surface, tuple]:
        if displayType == gametiles.Tile:
            try:
                SURFACE.blit(pygame.transform.scale(BLOCKTEXTURES[requestedDisplay.blockid],scale), (x, y))  # for textured tiles
            except:
                newSurf = pygame.Surface((TILESIZE, TILESIZE))
                newSurf.fill(BLOCKTEXTURES[requestedDisplay.blockid])
                SURFACE.blit(pygame.transform.scale(newSurf,scale), (x,y))
        elif displayType == pygame.Surface:
            SURFACE.blit(pygame.transform.scale(requestedDisplay,scale), (x,y))
        elif displayTile == buffer.Buffer:
            BUFFERSURF.blit(pygame.transform.scale(requestedDisplay, scale), (x,y))

#PLAYER ANIMATION TEXTURES
ANIMATIONIMAGE = {
    0: {x:pygame.image.load(str("images/sprites/spritePlayer_"+str(x)+".png")) for x in range(0,4)},
    1: {x:pygame.image.load("images/sprites/spriteWaterer.png") for x in range(0,4)}
}

#PLAYER VARIABLES
player = spritesrc.Player()
MovementDelay = 0
cloudDelay = 0

#PLAYER GENERATOR
def drawPlayer():
    x, y = player.getPos()
    if player.checkPos(x, y):
        BLOCKID = gametiles.getActiveTile(x, y).blockid
        if BLOCKID in ANIMATIONIMAGE:
            IMG = ANIMATIONIMAGE[BLOCKID][player.orientation]
        else:
            IMG = ANIMATIONIMAGE[1][player.orientation]
        DISPLAYSURF.blit(pygame.transform.scale(IMG,(TILESIZE,TILESIZE)),(player.getPos()))

def movePlayer(dir):
    global MovementDelay
    if MovementDelay <= 8:  MovementDelay += 1
    else:   
        player.move(dir)
        MovementDelay = 0

# def checkPlayerAnimation():
#     global PlayerImage
#     x, y = player.getPos()
#     if player.checkPos(x,y):
#         BLOCKID = gametiles.getActiveTile(x,y).blockid


def bufferDisplayCreator(listVar):
    global wholesurf
    for key in listVar.keys():
        diagimage = pygame.image.load("images/buffers/blank.png")
        mask = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
        mask.fill((255,255,255))
        mask.set_alpha(255)
        displayTile(wholesurf, key[0], key[1], mask)
        vertimage = diagimage.copy()
        horimage = diagimage.copy()
        wholeimage = diagimage.copy()

        for buf in [x for x in listVar[key] if x.getType() in [4, 6]]:    diagimage.blit(
            pygame.image.load(buffer.BUFFERIMAGES[buf.type]), (buf.xadd, buf.yadd))

        for buf in [x for x in listVar[key] if x.getType() in [1, 5]]:    vertimage.blit(
            pygame.image.load(buffer.BUFFERIMAGES[buf.type]), (buf.xadd, buf.yadd))

        for buf in [x for x in listVar[key] if x.getType() in [3, 7]]:     horimage.blit(
            pygame.image.load(buffer.BUFFERIMAGES[buf.type]), (buf.xadd, buf.yadd))

        tempsurflist = [vertimage, horimage, diagimage]

        for surface in tempsurflist: wholeimage.blit(surface, (0, 0))

        displayTile(wholeimage, key[0], key[1], wholesurf)

#TILE GENERATOR
def drawGameMap():
    global MAPGENERATED, MAPUNCHANGED, BLOCKCOUPLER, BUFFERDRAWN, wholesurf, BUFFERLIST
    if MAPGENERATED == 0:   #Checks if map has been generated
        BUFFERDRAWN = 0
        wholesurf = pygame.Surface((TILESIZE * TILEWIDTH, TILESIZE * TILEHEIGHT), pygame.SRCALPHA, 32)
        gametiles.initGenTile()
        bufferDisplayCreator(gametiles.BUFFERLIST)
        BUFFERDRAWN = 1
        [[displayTile(TILE, TILE.xpos, TILE.ypos, basetilesurf) for TILE in row] for row in TILEMAP]  # Draw tiles
        MAPGENERATED = 1
    else:
        if len(drawStack.stackToDraw.stack) > 0:
            # print(drawStack.stackToDraw.stack)
            superNeighbourList = []
            tempDict = {}
            for item in drawStack.stackToDraw.stack:
                neighbourList = gametiles.getRowNeighbor(item)+gametiles.getColumnNeighbor(item)+[item]
                print(neighbourList)
                for tiles in neighbourList:
                    tiles.setBlockID(100)
                    displayTile(tiles, item.xpos, item.ypos, basetilesurf)
                    tempBuffer = buffer.Buffer()
                    tempBuffer.setPos(tiles.xpos,tiles.ypos)
                    if (tiles.xpos,tiles.ypos) in tempDict.keys():  tempDict[(tiles.xpos,tiles.ypos)].append(tempBuffer)
                    else:   tempDict[(tiles.xpos, tiles.ypos)] = [tempBuffer]
                [superNeighbourList.append(x) for x in neighbourList]
                print(tempDict)
            listOfFreshBuffers = gametiles.grassWaterBuffer(tempDict, superNeighbourList)
            for x in listOfFreshBuffers.keys():
                buf = tempDict[x][0]
                gametiles.BUFFERLIST[(buf.x, buf.y)] = buf
            bufferDisplayCreator(listOfFreshBuffers)

            drawStack.stackToDraw.clearStack()
    DISPLAYSURF.blit(basetilesurf, (0,0))
    DISPLAYSURF.blit(wholesurf,(0,0))

def drawInventory(): #Testing Inventories, may have to refactor later
    # RIGHT INVT MARGIN (10px) 522 y x 10
    inventory = player.inv.grabList()
    keyListing = 0
    for key in inventory.keys():
        if key in BLOCKTEXTURES:    displayTile(BLOCKTEXTURES[key], (TILESIZE * TILEWIDTH+TILESIZE), keyListing)    #For textured blocks
        COUNTTEXT = TestText.render(str(inventory[key]), False, BLACK, None)
        BLOCKTEXT = TestText.render(BLOCKLIST[key][0], False, BLACK, None)
        displayTile(COUNTTEXT, (TILESIZE * TILEWIDTH)+TILESIZE * 2, keyListing-(TILESIZE//4))
        displayTile(BLOCKTEXT, (TILESIZE * TILEWIDTH)+TILESIZE * 3, keyListing-(TILESIZE//4))
        keyListing += TILESIZE

while True: # main game loop

    font = pygame.font.Font(None, 30)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == K_q:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_m:
                MAPGENERATED = 0
            if event.key == pygame.K_w:
                x,y = player.getPos()
                TILE = gametiles.getActiveTile(x,y)
                for Tile in gametiles.getSurrounding(TILE):
                    Tile.setBlockID(100)
                    displayTile(Tile,Tile.xpos,Tile.ypos,wholesurf)
            if event.key == pygame.K_SPACE: player.grabTile()
            if event.key == pygame.K_p:
                player.placeTile()


    # player movements
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]:        movePlayer("up")
    elif pressed[pygame.K_RIGHT]:   movePlayer("right")
    elif pressed[pygame.K_LEFT]:    movePlayer("left")
    elif pressed[pygame.K_DOWN]:    movePlayer("down")

    DISPLAYSURF.fill(WHITE)
    drawGameMap()
    drawPlayer()
    drawInventory()
    fps = font.render(str(int(clock.get_fps())), True, pygame.Color('white'))
    DISPLAYSURF.blit(fps,(0,0))
    pygame.display.flip()
    clock.tick(120)



"""
#CLOUD TEST (Doesn't work)
def cloudsTest():
    global cloudDelay
    for Tile in gametiles.BLOCKCOUPLER[2]:
        if cloudDelay <= 320:
            cloudDelay += 1
        else:
            Tile.moveTile("right")
            cloudDelay = 0
    for Tile in gametiles.BLOCKCOUPLER[2]:
        displayTile(Tile, Tile.xpos, Tile.ypos)
        
Cool Mining Animation for later? Rock layer that peels away
    # pos = player.getPos()
    # TILE = gametiles.getActiveTile(pos[0], pos[1])
    # print(pos)
    # for Tile in gametiles.getSurrounding(TILE):
    #     print(Tile.xpos // 16, Tile.ypos // 16)
    #     Tile.setBlockID(100)

BUGS:
- Buggy Player movement [Slightly Fixed]

"""
