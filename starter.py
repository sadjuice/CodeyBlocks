import sys, spritesrc, gametiles, pygame, random
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

player = spritesrc.MainPlayer
# (0,0), pygame.FULLSCREEN
DISPLAYSURF = pygame.display.set_mode((712, 512))

displaywidth, displayheight = pygame.display.get_surface().get_size()


pygame.display.set_caption('Codey Blocks')
TestText = pygame.font.SysFont("Comic Sans MS",16)
# pygame.key.set_repeat()

WHITE   =   (255,255,255)
BLACK   =   (0,0,0)
RED     =   (255,0,0)
GREEN   =   (0,255,0)
BLUE    =   (0,0,255)

#MAP VARIABLES
MAPGENERATED = 0

#TEXTURE MAP
BLOCKLIST = gametiles.BLOCKLIST
BLOCKTEXTURES = {}
for block in gametiles.BLOCKLIST.keys():
    if isinstance(BLOCKLIST[block][1],str):
        BLOCKTEXTURES[block] = pygame.image.load("images/blocks/"+BLOCKLIST[block][1])
    else:
        BLOCKTEXTURES[block] = BLOCKLIST[block][1]

def displayTile(TILE, x, y):
    if isinstance(TILE, gametiles.Tile):
        try:
            DISPLAYSURF.blit(BLOCKTEXTURES[TILE.blockid], (x, y))
        except:
            pygame.draw.rect(DISPLAYSURF, BLOCKTEXTURES[TILE.blockid], (x, y, 16, 16))
    elif isinstance(TILE, pygame.Surface):
        DISPLAYSURF.blit(TILE, (x, y))
    else:
        pygame.draw.rect(DISPLAYSURF, TILE, (x, y, 16, 16))

#PLAYER ANIMATION TEXTURES
ANIMATIONIMAGE = {
    0   : pygame.image.load("images/sprites/playSprite.png"),
    1   : pygame.image.load("images/sprites/spriteWaterer.png")
}

#PLAYER VARIABLES
PMOVECALL = True #Is the player requested to move?
MovementDelay = 0
cloudDelay = 0
PlayerImage = pygame.image.load("images/sprites/playSprite.png")

#PLAYER GENERATOR
def drawPlayer():
    # pygame.draw.circle(DISPLAYSURF, RED, (player.xpos, player.ypos), 8, 8)
    DISPLAYSURF.blit(PlayerImage,(player.getPos()))
def movePlayer(dir):
    global MovementDelay
    if PMOVECALL:
        if MovementDelay <= 4:
            MovementDelay += 1
        else:
            player.move(dir)
            MovementDelay = 0

TILEMAP = gametiles.TILEMAP
BLOCKLIST = gametiles.BLOCKLIST

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

def checkPlayerAnimation():
    global PlayerImage
    pos = player.getPos()
    if player.checkPos(pos[0],pos[1]):
        # print(pos[0]//16,pos[1]//16)

        BLOCKID = gametiles.getActiveTile(pos[0],pos[1]).blockid
        try:
            PlayerImage = ANIMATIONIMAGE[BLOCKID]
        except:
            PlayerImage = ANIMATIONIMAGE[0]


#TILE GENERATOR
def drawGameMap():
    global MAPGENERATED
    #Checks if map has been generated
    if MAPGENERATED == 0:
        gametiles.initGenTile()
        MAPGENERATED = 1
    #Draw tiles
    for row in TILEMAP:
        for TILE in row:    displayTile(TILE, TILE.xpos, TILE.ypos)

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
                pos = player.getPos()
                TILE = gametiles.getActiveTile(pos[0],pos[1])
                for Tile in gametiles.getSurrounding(TILE):
                    Tile.setBlockID(100)
            if event.key == pygame.K_SPACE:
                player.grabTile()
            if event.key == pygame.K_p:
                player.placeTile()

    pressed = pygame.key.get_pressed()
    # player movements
    if pressed[pygame.K_UP]:        movePlayer("up")
    elif pressed[pygame.K_RIGHT]:   movePlayer("right")
    elif pressed[pygame.K_LEFT]:    movePlayer("left")
    elif pressed[pygame.K_DOWN]:    movePlayer("down")

    DISPLAYSURF.fill(WHITE)

    drawGameMap()
    # cloudsTest()
    checkPlayerAnimation()
    drawPlayer()
    drawInventory()
    pygame.display.flip()
    clock.tick(60)



"""
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

