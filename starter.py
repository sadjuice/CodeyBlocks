import sys, spritesrc, gametiles, pygame, random
from pygame.locals import *

pygame.init()

#PYGAME variables
clock = pygame.time.Clock()
DISPLAYSURF = pygame.display.set_mode((712, 512))   # pygame.FULLSCREEN
BUFFERSURF = pygame.display.set_mode((512,512))     # Buffer surface
displaywidth, displayheight = pygame.display.get_surface().get_size()
pygame.display.set_caption('Codey Blocks')
TestText = pygame.font.SysFont("Comic Sans MS",16)

#COLOUR PALETTE
WHITE   =   (255,255,255)
BLACK   =   (0,0,0)
RED     =   (255,0,0)
GREEN   =   (0,255,0)
BLUE    =   (0,0,255)
YELLOW  = 	(255,255,0)

#MAP VARIABLES
MAPGENERATED = 0
TILESIZE = spritesrc.TILESIZE
TILEMAP = gametiles.TILEMAP
BLOCKLIST = gametiles.BLOCKLIST
BLOCKTEXTURES = {}
BUFFERTEXTURES = {}
BLOCKCOUPLER = gametiles.BLOCKCOUPLER
PASSABLEBLOCKS = gametiles.PASSABLEBLOCKS
BUFFERLIST = gametiles.BUFFERLIST

#TEXTURE MAP
for block in gametiles.BLOCKLIST.keys():
    if isinstance(BLOCKLIST[block][1],str): BLOCKTEXTURES[block] = pygame.image.load("images/blocks/"+BLOCKLIST[block][1])
    else:   BLOCKTEXTURES[block] = BLOCKLIST[block][1]

def displayTile(requestedDisplay, x, y, SURFACE=DISPLAYSURF):
    if isinstance(requestedDisplay, gametiles.Tile):    #If request is a tile
        try:    DISPLAYSURF.blit(BLOCKTEXTURES[requestedDisplay.blockid], (x, y))   #for textured tiles
        except: pygame.draw.rect(DISPLAYSURF, BLOCKTEXTURES[requestedDisplay.blockid], (x, y, TILESIZE, TILESIZE))  #for non-textured tiles
    elif isinstance(requestedDisplay, pygame.Surface):  DISPLAYSURF.blit(requestedDisplay, (x, y))  #For images, and text
    else:   pygame.draw.rect(DISPLAYSURF, requestedDisplay, (x, y, TILESIZE, TILESIZE)) #For plain int.

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
    DISPLAYSURF.blit(IMG,(player.getPos()))

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
    global MAPGENERATED
    if MAPGENERATED == 0:   #Checks if map has been generated
        gametiles.initGenTile()
        MAPGENERATED = 1
    [[displayTile(TILE, TILE.xpos, TILE.ypos) for TILE in row] for row in TILEMAP]  #Draw tiles

    #Draw buffers tester

    if len(BUFFERLIST) > 0:
        for key in BUFFERLIST.keys():
            if not BUFFERLIST[key] == None:
                if isinstance(BUFFERLIST[key], list):
                    DELLIST = []
                    for buffer in BUFFERLIST[key]:
                        if buffer != None:
                            x, y = buffer.getPos()
                            if buffer.getType() == 0:
                                pygame.draw.rect(BUFFERSURF, buffer.color, (x, y, 16, 8))
                            if buffer.getType() == 1:
                                pygame.draw.rect(BUFFERSURF, buffer.color, (x, y, 8, 16))
                            if buffer.getType() == 2:
                                pygame.draw.rect(BUFFERSURF, buffer.color, (x, y, 8, 8))
                        else:
                            DELLIST.append(buffer)
                    for buffer in DELLIST:
                        BUFFERLIST[key].remove(buffer)
                else:
                    buffer = BUFFERLIST[key]
                    x, y = buffer.getPos()
                    if buffer.getType() == 0:
                        pygame.draw.rect(BUFFERSURF, buffer.color, (x, y, 16, 8))
                    if buffer.getType() == 1:
                        pygame.draw.rect(BUFFERSURF, buffer.color, (x, y, 8, 16))
                    if buffer.getType() == 2:
                        pygame.draw.rect(BUFFERSURF, buffer.color, (x, y, 8, 8))


def drawInventory(): #Testing Inventories, may have to refactor later
    # RIGHT INVT MARGIN (10px) 522 y x 10
    inventory = player.inv.grabList()
    keyListing = 0
    for key in inventory.keys():
        if key in BLOCKTEXTURES:
            displayTile(BLOCKTEXTURES[key], 522, keyListing)    #For textured blocks
        COUNTTEXT = TestText.render(str(inventory[key]), False, BLACK, None)
        BLOCKTEXT = TestText.render(BLOCKLIST[key][0], False, BLACK, None)
        displayTile(COUNTTEXT, 542, keyListing-4)
        displayTile(BLOCKTEXT, 562, keyListing-4)
        keyListing += 26

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
