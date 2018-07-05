import sys, spritesrc, gametiles, pygame, random
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()

player = spritesrc.MainPlayer
# (0,0), pygame.FULLSCREEN
DISPLAYSURF = pygame.display.set_mode((712, 512))

displaywidth, displayheight = pygame.display.get_surface().get_size()
#RIGHT INVT MARGIN (10px) 522 y x 10

pygame.display.set_caption('Codey Blocks')
# pygame.key.set_repeat()

WHITE   =   (255,255,255)
BLACK   =   (0,0,0)
RED     =   (255,0,0)
GREEN   =   (0,255,0)
BLUE    =   (0,0,255)

#MAP VARIABLES
MAPGENERATED = 0

#TEXTURE MAP
BLOCKTEXTURES = {
    0   :   pygame.image.load("images/grass.png"),
    1   :   pygame.image.load("images/water.png")
}

#PLAYER ANIMATION TEXTURES
ANIMATIONIMAGE = {
    0   : pygame.image.load("images/playSprite.png"),
    1   : pygame.image.load("images/spriteWaterer.png")
}

#PLAYER VARIABLES
PMOVECALL = True #Is the player requested to move?
MovementDelay = 0
PlayerImage = pygame.image.load("images/playSprite.png")

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

def checkPlayerAnimation():
    global PlayerImage
    pos = player.getPos()
    if player.checkPos(pos[0],pos[1]):
        # print(pos[0]//16,pos[1]//16)

        BLOCKID = gametiles.getActiveTile(pos[0],pos[1]).blockid
        PlayerImage = ANIMATIONIMAGE[BLOCKID]

#TILE GENERATOR
def drawGameMap():
    global MAPGENERATED
    if MAPGENERATED == 0:
        gametiles.initGenTile()
        MAPGENERATED = 1
    #Draw tiles
    for row in TILEMAP:
        for TILE in row:
            try:
                DISPLAYSURF.blit(BLOCKTEXTURES[TILE.blockid],(TILE.xpos, TILE.ypos))
            except:
                try:
                    pygame.draw.rect(DISPLAYSURF, BLOCKLIST[TILE.blockid][1], (TILE.xpos, TILE.ypos, 16, 16))
                except:
                    print("TILE @ {0},{1} has invalid blockid of {2}".format(TILE.xpos, TILE.ypos, TILE.blockid))

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

    pressed = pygame.key.get_pressed()
    # player movements
    if pressed[pygame.K_UP]:
        movePlayer("up")
    elif pressed[pygame.K_RIGHT]:
        movePlayer("right")
    elif pressed[pygame.K_LEFT]:
        movePlayer("left")
    elif pressed[pygame.K_DOWN]:
        movePlayer("down")

    DISPLAYSURF.fill(WHITE)
    drawGameMap()
    checkPlayerAnimation()
    drawPlayer()
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

