import sys, spritesrc, gametiles, pygame, random
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
    if displayType in [gametiles.Tile, gametiles.buffer.Buffer, pygame.Surface, tuple]:
        if displayType == gametiles.Tile:
            try:
                SURFACE.blit(pygame.transform.scale(BLOCKTEXTURES[requestedDisplay.blockid],scale), (x, y))  # for textured tiles
            except:
                newSurf = pygame.Surface((TILESIZE, TILESIZE))
                newSurf.fill(BLOCKTEXTURES[requestedDisplay.blockid])
                SURFACE.blit(pygame.transform.scale(newSurf,scale), (x,y))
        elif displayType == pygame.Surface:
            SURFACE.blit(pygame.transform.scale(requestedDisplay,scale), (x,y))
        elif displayTile == gametiles.buffer.Buffer:
            BUFFERSURF.blit(pygame.transform.scale(requestedDisplay, scale), (x,y))


#PLAYER ANIMATION TEXTURES
ANIMATIONIMAGE = {
    0: pygame.image.load("images/sprites/spriteBoxer.png"),
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
        IMG = pygame.transform.flip(PlayerImage,False,False)
    elif player.orientation == 3:
        IMG = pygame.transform.flip(PlayerImage,False,False)
    DISPLAYSURF.blit(pygame.transform.scale(IMG,(TILESIZE,TILESIZE)),(player.getPos()))

def movePlayer(dir):
    global MovementDelay
    if MovementDelay <= 8:  MovementDelay += 1
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
    global MAPGENERATED, MAPUNCHANGED, BLOCKCOUPLER, BUFFERDRAWN, wholesurf
    if MAPGENERATED == 0:   #Checks if map has been generated
        BUFFERDRAWN = 0
        wholesurf = pygame.Surface((TILESIZE * TILEWIDTH, TILESIZE * TILEHEIGHT), pygame.SRCALPHA, 32)
        gametiles.initGenTile()
        BUFFERLIST = gametiles.BUFFERLIST
        for key in BUFFERLIST.keys():
            diagimage = pygame.image.load("images/buffers/blank.png")
            vertimage = diagimage.copy()
            horimage = diagimage.copy()
            wholeimage = diagimage.copy()

            for buf in [x for x in BUFFERLIST[key] if x.getType() in [4, 6]]:    diagimage.blit(pygame.image.load(gametiles.buffer.BUFFERIMAGES[buf.type]), (buf.xadd, buf.yadd))

            for buf in [x for x in BUFFERLIST[key] if x.getType() in [1,5]]:    vertimage.blit(pygame.image.load(gametiles.buffer.BUFFERIMAGES[buf.type]), (buf.xadd, buf.yadd))

            for buf in [x for x in BUFFERLIST[key] if x.getType() in [3, 7]]:     horimage.blit(pygame.image.load(gametiles.buffer.BUFFERIMAGES[buf.type]), (buf.xadd, buf.yadd))

            tempsurflist = [vertimage, horimage, diagimage]

            for surface in tempsurflist: wholeimage.blit(surface, (0,0))
            # BUFFERLIST[key] = wholeimage
            displayTile(wholeimage, key[0], key[1], wholesurf)
        BUFFERDRAWN = 1
        [[displayTile(TILE, TILE.xpos, TILE.ypos, basetilesurf) for TILE in row] for row in TILEMAP]  # Draw tiles
        MAPGENERATED = 1
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
                    MAPGENERATED = 0
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
