import sys, spritesrc, gametiles, pygame, random
from pygame.locals import *

pygame.init()

#PYGAME variables
TILESIZE = spritesrc.TILESIZE
clock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode(((TILESIZE * gametiles.TILEWIDTH)+200, TILESIZE * gametiles.TILEHEIGHT))   # pygame.FULLSCREEN
BUFFERSURF = pygame.display.set_mode((TILESIZE * gametiles.TILEWIDTH+200,   TILESIZE * gametiles.TILEHEIGHT))     # Buffer surface
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
TILEMAP = gametiles.TILEMAP
BLOCKLIST = gametiles.BLOCKLIST
BLOCKTEXTURES = {}
BUFFERTEXTURES = {}
PASSABLEBLOCKS = gametiles.PASSABLEBLOCKS

#TEXTURE MAP
for block in gametiles.BLOCKLIST.keys():
    if isinstance(BLOCKLIST[block][1],str): BLOCKTEXTURES[block] = pygame.image.load("images/blocks/"+BLOCKLIST[block][1])
    else:   BLOCKTEXTURES[block] = BLOCKLIST[block][1]

testList = []
def displayTile(requestedDisplay, x, y, SURFACE=DISPLAYSURF):
    scale = (TILESIZE,TILESIZE)
    # if isinstance(requestedDisplay, gametiles.Tile):    #If request is a tile
    #     try:    DISPLAYSURF.blit(BLOCKTEXTURES[requestedDisplay.blockid], (x, y))   #for textured tiles
    #     except: pygame.draw.rect(DISPLAYSURF, BLOCKTEXTURES[requestedDisplay.blockid], (x, y, TILESIZE, TILESIZE))  #for non-textured tiles
    # elif isinstance(requestedDisplay, gametiles.buffer.Buffer):
    #     DISPLAYSURF.blit(pygame.image.load(gametiles.buffer.BUFFERIMAGES[requestedDisplay.type]), (x, y))
    # elif isinstance(requestedDisplay, pygame.Surface):  DISPLAYSURF.blit(requestedDisplay, (x, y))  #For images, and text
    # else:   pygame.draw.rect(DISPLAYSURF, requestedDisplay, (x, y, TILESIZE, TILESIZE)) #For plain int.
    displayType = type(requestedDisplay)
    if displayType in [gametiles.Tile, gametiles.buffer.Buffer, pygame.Surface, tuple]:
        if displayType == gametiles.Tile:
            try:
                DISPLAYSURF.blit(pygame.transform.scale(BLOCKTEXTURES[requestedDisplay.blockid],scale), (x, y))  # for textured tiles
            except:
                newSurf = pygame.Surface((TILESIZE, TILESIZE))
                newSurf.fill(BLOCKTEXTURES[requestedDisplay.blockid])
                DISPLAYSURF.blit(pygame.transform.scale(newSurf,scale), (x,y))
        elif displayType == pygame.Surface:
            DISPLAYSURF.blit(pygame.transform.scale(requestedDisplay,scale), (x,y))
        elif displayTile == gametiles.buffer.Buffer:
            BUFFERSURF.blit(pygame.transform.scale(requestedDisplay, scale), (x,y))


#PLAYER ANIMATION TEXTURES
ANIMATIONIMAGE = {
    0: pygame.image.load("images/sprites/playSprite.png"),
    1: pygame.image.load("images/sprites/spriteWaterer.png")
}

#PLAYER VARIABLES
player = spritesrc.Player()
MovementDelay = 0
cloudDelay = 0
PlayerImage = pygame.image.load("images/sprites/playSprite.png")

#PLAYER GENERATOR
def drawPlayer():
    IMG = PlayerImage
    checkPlayerAnimation()
    if player.orientation == 0:
        IMG = pygame.transform.flip(PlayerImage,True,False)
    elif player.orientation == 1:
        IMG = pygame.transform.flip(PlayerImage,False,True)
    elif player.orientation == 3:
        IMG = pygame.image.load("images/sprites/spriteWaterer.png")
    DISPLAYSURF.blit(pygame.transform.scale(IMG,(TILESIZE,TILESIZE)),(player.getPos()))

def movePlayer(dir):
    global MovementDelay
    if MovementDelay <= 4:  MovementDelay += 1
    else:   
        player.move(dir)
        MovementDelay = 0

def checkPlayerAnimation():
    global PlayerImage
    x, y = player.getPos()
    if player.checkPos(x,y):
        BLOCKID = gametiles.getActiveTile(x,y).blockid
        try:    PlayerImage = ANIMATIONIMAGE[BLOCKID]
        except: PlayerImage = ANIMATIONIMAGE[0]

#TILE GENERATOR
def drawGameMap():
    global MAPGENERATED, BLOCKCOUPLER
    if MAPGENERATED == 0:   #Checks if map has been generated
        gametiles.initGenTile()
        MAPGENERATED = 1
    [[displayTile(TILE, TILE.xpos, TILE.ypos) for TILE in row] for row in TILEMAP]  #Draw tiles
    BLOCKCOUPLER = gametiles.BLOCKCOUPLER
    BUFFERLIST = gametiles.BUFFERLIST
    #Draw buffers tester
    for key in BUFFERLIST.keys():
        if isinstance(BUFFERLIST[key], list):
            diag = [x for x in BUFFERLIST[key] if x.getType() in [4, 6]]
            diagimage = pygame.image.load("images/buffers/blank.png")
            for buf in diag:
                diagimage.blit(pygame.image.load(gametiles.buffer.BUFFERIMAGES[buf.type]), (buf.xadd, buf.yadd))

            vertimage = pygame.image.load("images/buffers/blank.png")
            vert = [x for x in BUFFERLIST[key] if x.getType() in [1,5]]
            for buf in vert:
                vertimage.blit(pygame.image.load(gametiles.buffer.BUFFERIMAGES[buf.type]), (buf.xadd, buf.yadd))

            horimage = pygame.image.load("images/buffers/blank.png")
            hor = [x for x in BUFFERLIST[key] if x.getType() in [3, 7]]
            for buf in hor:
                horimage.blit(pygame.image.load(gametiles.buffer.BUFFERIMAGES[buf.type]), (buf.xadd, buf.yadd))

            BUFFERLIST[key] = [vertimage, horimage, diagimage]

            wholeimage = pygame.image.load("images/buffers/blank.png")
            for surface in BUFFERLIST[key]:
                wholeimage.blit(surface,(0,0))
            BUFFERLIST[key] = wholeimage
        else:
            displayTile(BUFFERLIST[key], key[0], key[1])
    DISPLAYSURF.blit(BUFFERSURF,(0,0))


def drawInventory(): #Testing Inventories, may have to refactor later
    # RIGHT INVT MARGIN (10px) 522 y x 10
    inventory = player.inv.grabList()
    keyListing = 0
    for key in inventory.keys():
        if key in BLOCKTEXTURES:
            displayTile(BLOCKTEXTURES[key], (TILESIZE * gametiles.TILEWIDTH+TILESIZE), keyListing)    #For textured blocks
        COUNTTEXT = TestText.render(str(inventory[key]), False, BLACK, None)
        BLOCKTEXT = TestText.render(BLOCKLIST[key][0], False, BLACK, None)
        displayTile(COUNTTEXT, (TILESIZE * gametiles.TILEWIDTH)+TILESIZE * 2, keyListing-(TILESIZE//4))
        displayTile(BLOCKTEXT, (TILESIZE * gametiles.TILEWIDTH)+TILESIZE * 3, keyListing-(TILESIZE//4))
        keyListing += TILESIZE

while True: # main game loop
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
                for Tile in gametiles.getSurrounding(TILE): Tile.setBlockID(100)
            if event.key == pygame.K_SPACE: player.grabTile()
            if event.key == pygame.K_p: player.placeTile()

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
    pygame.display.flip()
    clock.tick(60)



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
