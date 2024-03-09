###### This is Version 0.11 ########
# Import the pygame module
import cProfile
import pygame, math, time, os, sys, pytmx, random, numpy, platform, asyncio
from TWOFOURCSYS import tilesys, filesys, particleSys, levelsys, musicsys, intro, bgsys, scriptInterpetsys, dialogsys
from tkinter import messagebox
from ast import literal_eval #string representation of list into list

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_w,
    K_a,
    K_s,
    K_d,
    K_r,
    K_RETURN,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    KEYUP,
    QUIT,
)

# Initialize pygame
pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = round(640*1.5)
SCREEN_HEIGHT = round(352*1.5)
pygame.display.set_caption('Loading...')
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
global tileScreen
screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
foreScreen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
tileScreen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
tileScreen.set_colorkey([69,42,0])
screenFlush = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, vsync=1)
print(screenFlush.get_width(), screenFlush.get_height())
nearestN = lambda integ, roun: round(integ / roun) * roun


def posNeg(integ, exc):
    try:
        return round(abs(integ) / integ)
    except Exception:
        return exc


def textProp(txt, font):
    return font.render(txt, False, (255, 255, 255)), font.render(txt, False, (255, 255, 255)).get_width(), font.render(txt, False, (255, 255, 255)).get_height() 

mainDir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.abspath(__file__))
rec = []
recEnabled = False
worldConfig = tuple(filesys.readFile(f"{mainDir}/WORLDS/mainWorld/config.txt").split("\n"))

class globalVars():
    def __init__(self):
        
        self.running = True
        self.timer = 0
        self.plSpriteNum = 0
        self.plAnimFlip = 0
        self.plExc = -1
        self.checkpoint = (int(worldConfig[0])*16,int(worldConfig[1])*16, int(worldConfig[2]), int(worldConfig[3]))
        self.playerX = int(worldConfig[0])*16
        self.playerY = int(worldConfig[1])*16
        self.shakeX = 0
        self.shakeY = 0
        self.plWorldX = int(worldConfig[2])
        self.plWorldY = int(worldConfig[3])
        self.plWorldX2 = self.plWorldX
        self.plWorldY2 = self.plWorldY
        self.playerXVel = 0.1
        self.playerXVelLim = 3.75
        self.playerXSprite = 0
        self.playerYVel = 0
        self.playerYVelLim = -6
        self.getTicksLastFrame = 0 
        self.deltaTime = 1
        self.runtimeFPS = 120
        self.plHitLog = []
        self.FPS = 60
        self.TarFPS = 120
        self.startTime = time.time()
        self.deltaAdjust = 1
        self.playerMoveLeft = 0
        self.playerMoveRight = 0
        self.playerEnterKey = False
        self.playerJump = 0
        self.playerJumpCounter = 0
        self.playerOnFloor = 0
        self.playerOnCeiling = 0
        self.levelLoop = [False, False, False, False]
        self.map = pytmx.TiledMap(f"{mainDir}/WORLDS/mainWorld/24cM_x0_y0.tmx")
        self.mapProperties = pytmx.TiledMap(f"{mainDir}/WORLDS/mainWorld/24cM_x0_y0.tmx").get_layer_by_name("Properties/Misc").properties
        self.tileHitSolid = []
        self.tileHitSolid2 = []
        self.tileHitObjs = []
        self.tileHitSpike = []  
        self.tileHitTP = []
        self.particles = []
        self.hurtFlag = False
        self.hurtTimer = 0
        self.trinketCollected = []
        self.diaQueue = []
        self.diaVect2 = (0, 0)
        self.cutsceneInteg = 0
        self.cutsceneOffset = 0
        self.currSong = ""
        self.volTimer = 0
    def respawnPlayer(self):
        musicsys.play(f"{mainDir}/SOUND/FX/hurt.wav", musicsys.sfxCh)
        musicsys.play(f"{mainDir}/SOUND/FX/char3.wav", musicsys.sfxCh)
        self.plWorldX2, self.plWorldY2 = self.plWorldX, self.plWorldY
        self.playerX, self.playerY, self.plWorldX, self.plWorldY = self.checkpoint

gv = globalVars()

# GAME VARIABLES

## Clock Variables
clock = pygame.time.Clock()

## Font
regularFont = pygame.font.Font(f"{mainDir}//FONT//24Colors_Font.ttf",16)
subFont = pygame.font.Font(f"{mainDir}//FONT//24Colors_Font.ttf",8)
print(regularFont)
## Player Variables
player = pygame.Rect(gv.playerX, gv.playerY, 20, 32)
ceilHit = pygame.Rect(gv.playerX, gv.playerY, 10, 10)

## Player Sprite

## Glow Effect



## World/Tileset Variables
tilesetTest = pygame.image.load(
    f"{mainDir}/24cTileset.png"
).convert_alpha()
playerTileset = pygame.image.load(
    f"{mainDir}/24cChar.png"
).convert_alpha()
objectTileset = pygame.image.load(
    f"{mainDir}/24cObjs.png"
).convert_alpha()
objBlcTileset = pygame.image.load(
    f"{mainDir}/24cBlck.png"
).convert_alpha()
levelTilelist = tilesys.imgTileSeg(tilesetTest, 16)
playerTilelist = tilesys.imgTileSeg(playerTileset, 32)
objectTilelist = tilesys.imgTileSeg(objectTileset, 32)
objBlcTilelist = tilesys.imgTileSeg(objBlcTileset, 32)
pygame.display.set_icon(playerTilelist[0])
mapProperties = pytmx.TiledMap

tileXIndList = []
tileYIndList = []
for i in range(33*60):
    tileXIndList.append((i% 60) * 16)
    tileYIndList.append(i // 60 * 16)

tilesetInd1 = [str(i) for i in range(72*72)]
tilesetInd2 = [str(i+72*72) for i in range(12*12)]
### Tile Generation
def tileTeleGen():
    tempMap = pytmx.TiledMap(f"{mainDir}/WORLDS/mainWorld/24cM_x{gv.plWorldX}_y{gv.plWorldY}.tmx").get_layer_by_name("Object Interactables")
    print(type(gv.plWorldX),type(gv.plWorldY))
    for obj in tempMap:
        objProp = obj.properties
        objProp["curWX"] = gv.plWorldX
        objProp["curWY"] = gv.plWorldY
        if "x16" in objProp:
            objId = 3
        elif "Script (.ccc)" in objProp:
            objId = 4
        elif "Script_ (.ccc)" in objProp:
            objId = 5
        else:
            objId = obj.gid-29
        print(objProp)
        gv.tileHitObjs.append([pygame.Rect( obj.x, obj.y, 32, 32), 0, objId, False, objProp, True, 0])
def tileGenerateCol(map, forceObjRegen): # Involved with tile colision and generation 
    print(f"24cM_x{gv.plWorldX}_y{gv.plWorldY}.tmx | {gv.plWorldX2}, {gv.plWorldY2}")
    #mapTest = levelsys.readTmx(f"{mainDir}/WORLDS/mainWorld/24cM_x{gv.plWorldX}_y{gv.plWorldY}.tmx")
    gv.tileHitSolid = []
    if (gv.plWorldX2 != gv.plWorldX or gv.plWorldY2 != gv.plWorldY) or forceObjRegen:tileScreen.fill([69,42,0]); gv.tileHitObjs = []; tileTeleGen()
    gv.tileHitSpike = []
    tempRoom = map
    for tLayerInd, tempLayer in enumerate(tempRoom):
        for tRoomInd, tile in enumerate(tempLayer):
            if tile != '0':
                tileX = tileXIndList[tRoomInd]
                tileY = tileYIndList[tRoomInd]
                
                try:
                    if tile in tilesetInd1:
                        tileScreen.blit(levelTilelist[int(tile)-1] ,(tileX, tileY))
                except Exception:
                    pass
                if tLayerInd == 1:
                    gv.tileHitSolid.append(pygame.Rect( tileX, tileY, 16, 16))
                elif tLayerInd == 2:
                    gv.tileHitSpike.append(pygame.Rect( tileX, tileY, 16, 16))
                elif tLayerInd == 5 and ((gv.plWorldX2 != gv.plWorldX or gv.plWorldY2 != gv.plWorldY) or forceObjRegen):
                    gv.tileHitObjs.append([pygame.Rect( tileX, tileY-16, 32, 32), 0, int(tile)-1-(72*72), False, True, True])
    print(f"Done generating tileHitObjs with a len of {len(gv.tileHitObjs)}!")
def tileObjsAction():
    if getColHits(gv.tileHitSpike):
        gv.hurtFlag = True
    for i in gv.tileHitObjs:
        i[3] = bool(player.colliderect(i[0]))
        i[5] = (i[0].x, i[0].y, gv.plWorldX, gv.plWorldY) not in gv.trinketCollected
        if i[2] == 0:
            tileObjCheckpoint(i)
        if i[2] == 4:
            if i[3] and gv.playerEnterKey and gv.cutsceneInteg < 2:
                scriptRead = i[4]["Script (.ccc)"]
                gv.diaQueue = dialogsys.sort(scriptInterpetsys.readScript(scriptRead, mainDir))
                dialogSound()
                gv.playerEnterKey = False
                gv.diaVect2 = i[0].center
            i[1] += gv.deltaAdjust*0.1
            screen.blit(objectTilelist[math.floor( math.fmod( i[1], 15 ) )+20], i[0])
        if i[2] == 5:
            if i[3] and i[6] == 0:
                scriptRead = i[4]["Script_ (.ccc)"]
                gv.diaQueue = dialogsys.sort(scriptInterpetsys.readScript(scriptRead, mainDir))
            if i[3]:
                i[6] += 1
            else:
                i[6] = 0
            i[1] += gv.deltaAdjust*0.1
        tileObjsMisc(i)
        if i[1] > 30:
            i[1] = 0
            
def tileObjsMisc(i):  # sourcery skip: merge-nested-ifs
    if i[2] in [1, 3]:
        i[1] += gv.deltaAdjust*0.015
        if i[5]: screen.blit(objectTilelist[15+i[2]+round( math.fmod( i[1], 1 ) )], i[0])
    if i[2] == 1 and i[3] and not gv.hurtFlag and gv.cutsceneInteg <= 0 and i[5]:
        gv.trinketCollected.append((i[0].x, i[0].y, gv.plWorldX, gv.plWorldY))
        musicsys.play(f"{mainDir}/SOUND/FX/trink1.wav", musicsys.sfxCh)
        print(gv.trinketCollected)
    if i[2] == 3 and i[3] and not gv.hurtFlag and gv.cutsceneInteg <= 0:
        if i[4]["curWX"] == gv.plWorldX and i[4]["curWY"] == gv.plWorldY: # Not every i[4] has "curWX" and "curWY"
            tileObjTele(i)

def fx_shake():
    musicsys.play(f"{mainDir}/SOUND/FX/hurt3.wav", musicsys.sfxCh)
    gv.shakeX = random.randint(-10, 10)
    gv.shakeY = random.randint(-10, 10)

def tileObjCheckpoint(i):
    if i[3] and not gv.hurtFlag and gv.cutsceneInteg <= 0:
        gv.checkpoint = i[0].center+(gv.plWorldX, gv.plWorldY)
    if gv.checkpoint == i[0].center + (gv.plWorldX, gv.plWorldY) and math.floor(math.fmod(i[1], 15)) == 0 and i[4]:
        i[4] == False
        musicsys.play(f"{mainDir}/SOUND/FX/checkpoint1.wav", musicsys.sfxCh)
    if gv.checkpoint == i[0].center+(gv.plWorldX, gv.plWorldY) and math.floor( math.fmod( i[1], 15 ) ) < 9:
        i[1] += gv.deltaAdjust*0.1
        i[4] = False
    if gv.checkpoint != i[0].center+(gv.plWorldX, gv.plWorldY) and math.floor( math.fmod( i[1], 15 )) != 0:
        i[1] += gv.deltaAdjust*0.1
        i[4] = True
    screen.blit(objectTilelist[math.floor( math.fmod( i[1], 15 ) )], i[0])

def tileObjTele(i):
    musicsys.play(f"{mainDir}/SOUND/FX/tele1.wav", musicsys.sfxCh)
    fx_shake()
    gv.plWorldX2, gv.plWorldY2 = gv.plWorldX, gv.plWorldY
    gv.playerX, gv.playerY = i[4]["x16"]*16, i[4]["y16"]*16
    gv.plWorldX, gv.plWorldY = i[4]["worldX"], i[4]["worldY"]
    reloadMap(False)
    gv.playerXVel = 0
    gv.playerYVel = 0

def tileGenerateRender(map): # Involved with tile colision and generation 

    # sourcery skip: use-contextlib-suppress
    #mapTest = levelsys.readTmx(f"{mainDir}/WORLDS/mainWorld/24cM_x{gv.plWorldX}_y{gv.plWorldY}.tmx")

    tempRoom = map
    for tempLayer in tempRoom:
        for tRoomInd, tile in enumerate(tempLayer):
            if tile != '0':
                tileX = tileXIndList[tRoomInd]
                tileY = tileYIndList[tRoomInd]
                try:
                    if tile in tilesetInd1:
                        screen.blit(levelTilelist[int(tile)-1] ,(tileX, tileY))
                except Exception:
                    pass

def adjustColSolid():
    tColContainer = [
        tileCol
        for tileCol in gv.tileHitSolid
        if math.hypot(tileCol.x - gv.playerX, tileCol.y - gv.playerY) < 50
    ]
    gv.tileHitSolid2 = tColContainer
            

def getColHits(tilesCol, mode=None, obj=player):
    if mode is None:
        return [tileCol for tileCol in tilesCol if obj.colliderect(tileCol)]
    currentlyHitting = [[tileCol for tileCol in tilesCol if obj.colliderect(tileCol)]]
    """
    obj.y -= 16
    currentlyHitting.append([tileCol for tileCol in tilesCol if obj.colliderect(tileCol)])
    obj.y += 32
    currentlyHitting.append([tileCol for tileCol in tilesCol if obj.colliderect(tileCol)])
    obj.y -= 16
    """
    return currentlyHitting
    
### Tile Collision

def tileXCollisionCheck(tileList):
    ifXHit = 0

    colTiles = getColHits(tileList, 1)
    for tempTile in colTiles[0]:
        if gv.playerXVel > 0:
            player.right = tempTile.left
            gv.playerX = tempTile.left - player.width / 2
            ifXHit += 1
            if gv.playerJump and not gv.hurtFlag and gv.cutsceneInteg <= 0 and gv.playerMoveRight and colTiles[0] != []: #  and gv.playerMoveRight
                musicsys.play(f"{mainDir}/SOUND/FX/jump.wav", musicsys.sfxCh)
                gv.playerXVel = -4
                gv.playerYVel = 3.5
            elif (
                gv.playerJump
                and not gv.hurtFlag
                and gv.cutsceneInteg <= 0
                and gv.playerMoveRight
            ): # Condition state if only bottom half of player is next to tiles
                gv.playerYVel = 2.5
            else:
                gv.playerXVel = 0

    colTiles = getColHits(tileList, 1)
    for tempTile in colTiles[0]:
        if gv.playerXVel < 0:
            player.left = tempTile.right
            gv.playerX = tempTile.right + player.width / 2
            ifXHit -= 1
            if gv.playerJump and not gv.hurtFlag and gv.cutsceneInteg <= 0 and gv.playerMoveLeft and colTiles[0] != []: # and gv.playerMoveLeft
                musicsys.play(f"{mainDir}/SOUND/FX/jump.wav", musicsys.sfxCh)
                gv.playerXVel = 4
                gv.playerYVel = 3.5
            elif (
                gv.playerJump
                and not gv.hurtFlag
                and gv.cutsceneInteg <= 0
                and gv.playerMoveLeft
            ):
                gv.playerYVel = 2.5
            else:
                gv.playerXVel = 0

    gv.playerYVelLim = -1.5 if ifXHit != 0 else -6
    if ifXHit:
        particleRad = math.atan2(gv.playerYVel, gv.playerXVel)
        gv.particles += particleSys.generate(2, 2, 0.01, 0.02, particleRad, particleRad, -10, -20, 0.5, (0, 255//2, 255//2), ( gv.playerX+([10,-10][gv.plAnimFlip]), gv.playerY+16 ) )

def jumpTrigger(a, vel):
    gv.playerYVel = vel
    gv.playerJumpCounter -= 1
    gv.particles += particleSys.generate(10, 16, 0.01, 0.02, a, a, -10, -50, 0.5, (0, 255//2, 255//2), ( gv.playerX, gv.playerY ) )
    musicsys.play(f"{mainDir}/SOUND/FX/jump2.wav", musicsys.sfxCh)

def tileYCollisionCheck(tileList):  # sourcery skip: low-code-quality

    ifYHit = 0
    gv.playerOnFloor = False
    gv.playerOnCeiling  = False

    ceilHit.centerx = player.centerx
    ceilHit.top = player.top - 1

    colTiles = getColHits(tileList)
    for tempTile in colTiles:
        if gv.playerYVel < 0:
            player.bottom = tempTile.top
            gv.playerY = tempTile.top - player.height / 2
            gv.playerOnFloor = True

            particleRad = math.atan2(gv.playerYVel, gv.playerXVel)*-64+90
            gv.playerJumpCounter = 3
            if gv.playerJump and not gv.hurtFlag and gv.cutsceneInteg <= 0 and gv.playerJumpCounter == 3:
                jumpTrigger(particleRad, 4.75)
            else:
                gv.playerYVel = 0
            ifYHit += 1

    player.y -= 1
    player.x += 1
    xCheck1 = [getColHits(tileList, ceilHit)]
    player.x -= 2
    xCheck2 = [getColHits(tileList, ceilHit)]
    player.x += 1
    player.y += 1

    colTiles = getColHits(tileList)
    for tempTile in colTiles:
        if gv.playerYVel > 0:
            player.top = tempTile.bottom
            gv.playerY = tempTile.bottom + player.height / 2
            gv.playerOnCeiling  = True
            gv.playerYVel = 1 if xCheck1 + xCheck2 != [[], []] and gv.playerJump and not gv.hurtFlag and gv.cutsceneInteg <= 0 else 0

            ifYHit -= 1
    gv.playerYVel -= .1*gv.deltaAdjust
    gv.playerXVelLim = 3.75
    if ifYHit > 0:
        #print(f"ifYHit is {ifYHit}")
        gv.playerXSprite += abs(gv.playerXVel * gv.deltaAdjust/4)
    elif ifYHit < 0:
        gv.playerXSprite += abs(gv.playerXVel * gv.deltaAdjust/32)
        gv.playerXVelLim = 2

### Get Room Properties

def drawRoomConfig(item):
    #print(mapProperties)
    if item == "levelTitle":
        levelTitle_rConf=regularFont.render(gv.mapProperties["levelTitle"], True, (255, 255, 255) )
        levelTitle_rConf2=regularFont.render(gv.mapProperties["levelTitle"], True, (0, 0, 0) )
        subTitle = subFont.render(
                gv.mapProperties["additionalTitle"], True, (255, 255, 255)
            )
        subTitle2 = subFont.render(
                gv.mapProperties["additionalTitle"], True, (0, 0, 0)
            )
        diaBox = pygame.Surface((SCREEN_WIDTH, levelTitle_rConf.get_height()+2))
        diaBox.fill((0, 0, 0))
        diaBox.set_alpha(125)
        if gv.mapProperties["levelTitle"] is None:
            screen.blit(subTitle2, (SCREEN_WIDTH//2-subTitle.get_width()//2+2, SCREEN_HEIGHT-subTitle.get_height()//2+1-20))
            screen.blit(subTitle2, (SCREEN_WIDTH//2-subTitle.get_width()//2-2, SCREEN_HEIGHT-subTitle.get_height()//2-1-20))
            screen.blit(subTitle2, (SCREEN_WIDTH//2-subTitle.get_width()//2+2, SCREEN_HEIGHT-subTitle.get_height()//2-1-20))
            screen.blit(subTitle2, (SCREEN_WIDTH//2-subTitle.get_width()//2-2, SCREEN_HEIGHT-subTitle.get_height()//2+1-20))

            screen.blit(
                    subTitle,
                    (SCREEN_WIDTH//2-subTitle.get_width()//2, SCREEN_HEIGHT-subTitle.get_height()//2-20)
                )

        else:
            screen.blit(diaBox, (0, SCREEN_HEIGHT-diaBox.get_height()))
            screen.blit(subTitle2, (SCREEN_WIDTH//2-subTitle.get_width()//2+2, SCREEN_HEIGHT-diaBox.get_height()//2-subTitle.get_height()//2+1-20))
            screen.blit(subTitle2, (SCREEN_WIDTH//2-subTitle.get_width()//2-2, SCREEN_HEIGHT-diaBox.get_height()//2-subTitle.get_height()//2-1-20))
            screen.blit(subTitle2, (SCREEN_WIDTH//2-subTitle.get_width()//2+2, SCREEN_HEIGHT-diaBox.get_height()//2-subTitle.get_height()//2-1-20))
            screen.blit(subTitle2, (SCREEN_WIDTH//2-subTitle.get_width()//2-2, SCREEN_HEIGHT-diaBox.get_height()//2-subTitle.get_height()//2+1-20))

            screen.blit(
                    subTitle,
                    (SCREEN_WIDTH//2-subTitle.get_width()//2, SCREEN_HEIGHT-diaBox.get_height()//2-subTitle.get_height()//2-20)
                )
        screen.blit(levelTitle_rConf2, (SCREEN_WIDTH//2-levelTitle_rConf.get_width()//2+2, SCREEN_HEIGHT-diaBox.get_height()//2-levelTitle_rConf.get_height()//2+2))
        screen.blit(levelTitle_rConf2, (SCREEN_WIDTH//2-levelTitle_rConf.get_width()//2-2, SCREEN_HEIGHT-diaBox.get_height()//2-levelTitle_rConf.get_height()//2-2))
        screen.blit(levelTitle_rConf2, (SCREEN_WIDTH//2-levelTitle_rConf.get_width()//2+2, SCREEN_HEIGHT-diaBox.get_height()//2-levelTitle_rConf.get_height()//2-2))
        screen.blit(levelTitle_rConf2, (SCREEN_WIDTH//2-levelTitle_rConf.get_width()//2-2, SCREEN_HEIGHT-diaBox.get_height()//2-levelTitle_rConf.get_height()//2+2))

        screen.blit(levelTitle_rConf, (SCREEN_WIDTH//2-levelTitle_rConf.get_width()//2, SCREEN_HEIGHT-diaBox.get_height()//2-levelTitle_rConf.get_height()//2))


    elif item == "levelLoop":
        return [gv.mapProperties[key] for key in ["loopUp", "loopDown", "loopLeft", "loopRight"]]
    elif item == "bgCol":
        return [gv.mapProperties[key] for key in ["bgCol", "bgCol2"]]
    elif item == "bgFlip":
        return [gv.mapProperties[key] for key in ["bgHorizontal", "bgVertical"]]
    elif item == "additionalTitle":
        if gv.mapProperties["additionalTitle"] not in ["", None]:
            pygame.display.set_caption(f'24Colors - {gv.mapProperties["additionalTitle"]}')
        else:
            pygame.display.set_caption('24Colors')

### Player

def animPlayer(tileList):
    # sourcery skip: merge-list-append, move-assign-in-block

    if ((gv.playerMoveLeft or gv.playerMoveRight or round(gv.playerXVel * 2) != 0)) and gv.cutsceneInteg <= 0:
        if gv.playerOnFloor:
            gv.plSpriteNum = round(abs(math.fmod(gv.playerXSprite, 5))) + 1
    else:
        gv.plSpriteNum = 0

    animPlayer_wallside(tileList)
    gv.plAnimFlip = [True, False, True][posNeg(gv.playerXVel, gv.plExc)]
    if gv.hurtFlag:
        gv.plSpriteNum = 13 + round(math.fmod(gv.hurtTimer*2,1))
    
def animPlayer_wallside(tileList):
    player.x += 1
    colTilesRight = [getColHits(tileList)]
    colTilesX = [getColHits(tileList)]
    player.x -= 2
    colTilesX.append(getColHits(tileList))
    colTilesLeft = [getColHits(tileList)]
    player.x += 1
    player.y += 2
    colTilesY = [getColHits(tileList)]
    player.y -= 2
    if colTilesY == [[]]:
        if gv.playerMoveLeft or gv.playerMoveRight or round(gv.playerXVel / 2) != 0:
            gv.plSpriteNum = 16 if gv.playerYVel > 0 else 17
        else:
            gv.plSpriteNum = 15

        if colTilesX != [[],[]]:
            gv.plSpriteNum = 12
            if gv.playerMoveLeft or colTilesLeft != [[],[]]:
                gv.plAnimFlip = True
                #gv.plExc = -1
            elif gv.playerMoveRight or colTilesRight != [[],[]]:
                gv.plAnimFlip = False
                #gv.plExc = 1
            #print("floa")
    if gv.playerOnCeiling:
        if math.fabs(gv.playerXVel) <= 1.9:
            gv.plSpriteNum = round(abs(math.fmod(gv.playerXSprite, 1))) + 18
        else:
            gv.plSpriteNum = 20
    if (gv.playerMoveLeft or gv.playerMoveRight) and colTilesX != [[],[]]:
        gv.plSpriteNum = 12
            #print("flor")
    #print(colTilesX, colTilesY, playerMoveLeft, playerMoveRight)
    
def playerWrap():
    ifOutOfBounds = 0
    if gv.playerX > SCREEN_WIDTH or player.centerx > SCREEN_WIDTH:
        gv.playerX = 0
        if not gv.levelLoop[3]:
            ifOutOfBounds = world2Update()
            gv.plWorldX += 1
    if gv.playerY > SCREEN_HEIGHT or player.centery  > SCREEN_HEIGHT:
        gv.playerY = 0
        if not gv.levelLoop[0]:
            ifOutOfBounds = world2Update()
            gv.plWorldY += 1
    if gv.playerX < 0 or player.centerx < 0:
        gv.playerX = SCREEN_WIDTH
        if not gv.levelLoop[2]:
            ifOutOfBounds = world2Update()
            gv.plWorldX -= 1
    if gv.playerY < 0 or player.centery < 0:
        gv.playerY = SCREEN_HEIGHT
        if not gv.levelLoop[1]:
            ifOutOfBounds = world2Update()
            gv.plWorldY -= 1
    if gv.plWorldX < 0:
        gv.plWorldX = int(worldConfig[4])-1
    if gv.plWorldY < 0:
        gv.plWorldY = int(worldConfig[5])-1
    if gv.plWorldX > int(worldConfig[4])-1:
        gv.plWorldX = 0
    if gv.plWorldY > int(worldConfig[5])-1:  
        gv.plWorldY = 0



    return ifOutOfBounds


# TODO Rename this here and in `playerWrap`
def world2Update():
    gv.plWorldX2 = gv.plWorldX
    gv.plWorldY2 = gv.plWorldY
    return 1

def pl_lvlRender():
    if playerWrap():
        reloadMap(False)
    bgColors = [tuple(int(j.strip("#")[i : i + 2], 16) for i in (2, 4, 6, 0)) for j in drawRoomConfig("bgCol")]
    bgColors += drawRoomConfig("bgFlip")
    if bgColors[2] or bgColors[3]:screen.blit(bgsys.generate(bgColors[2], bgColors[3], 32, gv.timer*100%32, bgColors[0], bgColors[1], SCREEN_WIDTH//32+2, SCREEN_WIDTH, SCREEN_HEIGHT), (0, 0))
    else:
        gv.particles += particleSys.generate(2, SCREEN_HEIGHT, 0.01, 0.02, 90, 90, 10, 100, 0.5, (50, 50, 50), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2) )
    gv.particles = particleSys.process(gv.particles, screen, 1, gv.deltaTime)
    screen.blit(tileScreen, (0, 0))
    tileObjsAction()
    
def playerMovement():
    """
        Player Movement
    """
    # XVel Friction
    if not gv.hurtFlag and gv.cutsceneInteg <= 0:
        if gv.playerMoveLeft:
            gv.playerXVel += (-gv.playerXVel + -gv.playerXVelLim) / 24* gv.deltaAdjust
            gv.plExc = -1
        if gv.playerMoveRight:
            gv.playerXVel += (-gv.playerXVel + gv.playerXVelLim) / 24* gv.deltaAdjust
            gv.plExc = 1
    if (gv.playerMoveLeft == gv.playerMoveRight) or gv.hurtFlag or gv.cutsceneInteg > 0:
        gv.playerXVel -= gv.playerXVel/24* gv.deltaAdjust
    if gv.playerYVel < gv.playerYVelLim:
        gv.playerYVel = gv.playerYVelLim
    if math.fabs(gv.playerXVel) > 8: 
        gv.playerXVel = posNeg(gv.playerXVel, 8)

    if gv.playerX < 240:
        gv.cutsceneOffset = -120
    elif gv.playerX > SCREEN_WIDTH - 240:
        gv.cutsceneOffset = 120
    else:
        gv.cutsceneOffset = 0

    # Main Movement
    gv.map = levelsys.readTmx(f"{mainDir}/WORLDS/mainWorld/24cM_x{gv.plWorldX}_y{gv.plWorldY}.tmx")
    pl_lvlRender()
    adjustColSolid()
    if gv.deltaTime < 0.100:
        gv.playerX += gv.playerXVel * gv.deltaAdjust
        player.centerx = gv.playerX
        tileXCollisionCheck(gv.tileHitSolid2)
        gv.playerY -= gv.playerYVel * gv.deltaAdjust
        player.centery = gv.playerY
        tileYCollisionCheck(gv.tileHitSolid2)

    if gv.hurtFlag:
        if gv.hurtTimer > 1.5:
            gv.respawnPlayer()
            reloadMap(False)
            player.height = 32
            gv.hurtFlag = False
        elif gv.hurtTimer == 0:
            musicsys.play(f"{mainDir}/SOUND/FX/hurt2.wav", musicsys.sfxCh)
            musicsys.play(f"{mainDir}/SOUND/FX/char1.wav", musicsys.sfxCh)
            gv.particles += particleSys.generate(5, 20, 0.01, 1, -180, 180, 100, 100, 4, (0, 255//4, 255//4), (gv.playerX, gv.playerY) )
            gv.particles += particleSys.generate(5, 20, 0.01, 1, -180, 180, 100, 100, 4, (255//4, 0, 0), (gv.playerX, gv.playerY) )
            player.height = 20   
        gv.hurtTimer += gv.deltaTime

    else:
        gv.hurtTimer = 0

    animPlayer(gv.tileHitSolid2)


# TODO Rename this here and in `playerMovement`
def reloadMap(forceObjRegen):
    gv.map = levelsys.readTmx(f"{mainDir}/WORLDS/mainWorld/24cM_x{gv.plWorldX}_y{gv.plWorldY}.tmx")
    if gv.checkpoint[2:4] != (gv.plWorldX, gv.plWorldY):
            gv.particles = []
    player.centerx = gv.playerX
    player.centery = gv.playerY
    tileGenerateCol(gv.map, forceObjRegen)
    gv.mapProperties = pytmx.TiledMap(f"{mainDir}/WORLDS/mainWorld/24cM_x{gv.plWorldX}_y{gv.plWorldY}.tmx").get_layer_by_name("Properties/Misc").properties
    drawRoomConfig("additionalTitle")
    gv.levelLoop = drawRoomConfig("levelLoop")

def main_inputCheck():  # sourcery skip: low-code-quality
    global rec, recEnabled
    for event in pygame.event.get():
        if event.type == pygame.VIDEORESIZE:
            screenFlush = pygame.display.set_mode((pygame.display.get_surface().get_size()), pygame.RESIZABLE, vsync=1)
        # Did the user hit a key?
        if event.type == KEYDOWN:
            if event.key == K_w:
                gv.playerJump = True
                if gv.playerJumpCounter == 2:
                    jumpTrigger(math.atan2(gv.playerYVel, gv.playerXVel)*-64+90, 2.75)
                elif gv.playerJumpCounter == 1:
                    jumpTrigger(math.atan2(gv.playerYVel, gv.playerXVel)*-64+90, -5)
            if event.key == K_d:
                gv.playerMoveRight = True
            if event.key == K_a:
                gv.playerMoveLeft = True
            if event.key == K_RETURN:
                gv.playerEnterKey = True
            if event.key == K_r:
                gv.hurtFlag = True
            if event.key == pygame.K_z:
                if recEnabled:
                    filesys.writeFile("tutData", str(rec))
                recEnabled = not recEnabled
            if event.key == K_SPACE and gv.diaQueue != []:
                del gv.diaQueue[0]
                dialogSound()
                
        elif event.type == KEYUP:

            if event.key == K_w:
                gv.playerJump = False
            if event.key == K_d:
                gv.playerMoveRight = False
            if event.key == K_a:
                gv.playerMoveLeft = False
            if event.key == K_RETURN:
                gv.playerEnterKey = False

        elif event.type == QUIT:
            gv.running = False

def dialogSound():
    if gv.diaQueue != []:
        if gv.diaQueue[0][1] == "P":
            musicsys.play(f"{mainDir}/SOUND/FX/char4.wav", musicsys.sfxCh)
        elif gv.diaQueue[0][1] == "T":
            musicsys.play(f"{mainDir}/SOUND/FX/sign1.wav", musicsys.sfxCh)      

def dialogRender():
    if gv.diaQueue != []:
        print(gv.cutsceneInteg)
        if gv.cutsceneInteg <= 120:
            gv.cutsceneInteg += (-gv.cutsceneInteg + 120) / 32 * gv.deltaAdjust
        if gv.diaQueue[0][1] == "SHK":
            fx_shake()
            del gv.diaQueue[0]
        elif gv.diaQueue[0][1] == "DEST":
            if gv.diaQueue[0][2] == "Tele":
                gv.tileHitTP = []
            elif gv.diaQueue[0][2] == "Misc":
                gv.tileHitObjs = []
            del gv.diaQueue[0]
        elif gv.diaQueue[0][1] == "TRINK":
            if len(gv.trinketCollected) >= 8:
                gv.tileHitTP = []
                gv.tileHitObjs = []
            del gv.diaQueue[0]
        elif gv.diaQueue[0][1] == "MSC":
            if gv.diaQueue[0][2] == "None":
                pygame.mixer.music.unload()
                pygame.mixer.music.stop()
            else:
                if gv.currSong != f"{mainDir}/SOUND/MUSIC/{gv.diaQueue[0][2]}":
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(f"{mainDir}/SOUND/MUSIC/{gv.diaQueue[0][2]}")
                    pygame.mixer.music.play(-1)
                    gv.currSong = f"{mainDir}/SOUND/MUSIC/{gv.diaQueue[0][2]}"
                    gv.volTimer = 0
                del gv.diaQueue[0]
        elif gv.diaQueue[0][1] in ["P", "T"]:
            
            colMap = {"T":pygame.Vector3(125, 125, 125), "P":pygame.Vector3(0, 255, 255)}
            dia = regularFont.render(gv.diaQueue[0][2], False, colMap[gv.diaQueue[0][1]], colMap[gv.diaQueue[0][1]]//3)
            pygame.draw.rect(
                screen,
                colMap[gv.diaQueue[0][1]]//2,
                pygame.Rect(
                    SCREEN_WIDTH//2-dia.get_width()//2-10 + gv.cutsceneOffset//3, 
                    (SCREEN_HEIGHT//2-dia.get_height()//2 + gv.diaVect2[1])//2-10,
                    dia.get_width()+10*2, 
                    dia.get_height()+10*2
                )
            )
            pygame.draw.rect(
                screen,
                colMap[gv.diaQueue[0][1]]//3,
                pygame.Rect(
                    SCREEN_WIDTH//2-dia.get_width()//2-5 + gv.cutsceneOffset//3, 
                    (SCREEN_HEIGHT//2-dia.get_height()//2 + gv.diaVect2[1])//2-5,
                    dia.get_width()+5*2, 
                    dia.get_height()+5*2
                )
            )
            screen.blit(
                dia,
                (SCREEN_WIDTH//2-dia.get_width()//2 + gv.cutsceneOffset//3, (SCREEN_HEIGHT//2-dia.get_height()//2 + gv.diaVect2[1])//2)
            )
    elif gv.cutsceneInteg >= -120:
        gv.cutsceneInteg += (-gv.cutsceneInteg + -120) / 32 * gv.deltaAdjust
def main_renderCode():
    """
    for i in playerTilelist:
        screen.blit(i, (playerTilelist.index(i) * 32, 0))
    """
    # pygame.draw.rect(screen,(255,255,0),playerShadowA)
    # pygame.draw.rect(screen,(255,255,0),playerShadowB)
    screen.blit(
        pygame.transform.flip(
            playerTilelist[gv.plSpriteNum], # Surface
            gv.plAnimFlip, # FlipX
            False, # FlipY
        ),
        (nearestN(gv.playerX - 16, 2),nearestN(gv.playerY - 16, 2)),
    )
    screen.blit(
        pygame.transform.flip(
            playerTilelist[gv.plSpriteNum], # Surface
            gv.plAnimFlip, # FlipX
            False, # FlipY
        ),
        (nearestN(gv.playerX - 16, 2), nearestN(gv.playerY - 16, 2)),
    )
    screen.blit(
        pygame.transform.flip(
            playerTilelist[gv.plSpriteNum], # Surface
            gv.plAnimFlip, # FlipX
            False, # FlipY
        ),
        (nearestN(gv.playerX - 16, 2), nearestN(gv.playerY - 16, 2)),
    )
    # print(playerX-16-(-SCREEN_WIDTH, SCREEN_WIDTH)[playerX > SCREEN_WIDTH//2],playerY-32-(-SCREEN_HEIGHT, SCREEN_HEIGHT)[playerY > SCREEN_HEIGHT//2],32,32)
    #pygame.draw.rect(screen,(255,255,0),player)
    if gv.diaQueue != []:
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(0, 0, gv.cutsceneInteg + gv.cutsceneOffset, SCREEN_HEIGHT))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(SCREEN_WIDTH-gv.cutsceneInteg + gv.cutsceneOffset, 0, gv.cutsceneInteg - gv.cutsceneOffset, SCREEN_HEIGHT))

    dialogRender()
def gui_debug_log():
    hhh = regularFont.render(f"Beta 0.11 / Demo | FPS: {str(1//gv.deltaTime)}", False, (255, 255, 255))
    screen.blit(
        hhh,
        (0, 0)
    )
    osuser = f"Running on {platform.system()} {platform.release()}"
    screen.blit(
        regularFont.render(osuser, False, (255, 255, 255)),
        (0,20)
    )
    res = f"{screenFlush.get_width()}, {screenFlush.get_height()}"
    screen.blit(
        regularFont.render(res, False, (255, 255, 255)),
        (0,40)
    )
def screenFx(opac = 255):

    screenSizeAdj = min(screenFlush.get_width(), screenFlush.get_height())
    screenSizeAdj2 = max(screenFlush.get_width(), screenFlush.get_height())

    screenSizeDict = {screenSizeAdj:528, screenSizeAdj2:960}
    
    screenSizeAdjFactor = screenSizeAdj/screenSizeDict[screenSizeAdj]
    screenSizeAdjFactor2 = screenSizeAdj2/screenSizeDict[screenSizeAdj2]

    if screenSizeAdjFactor <= screenSizeAdjFactor2:
        screenSizeMax = (960*screenSizeAdjFactor,528*screenSizeAdjFactor)
    elif screenSizeAdjFactor2 <= screenSizeAdjFactor:
        screenSizeMax = (960*screenSizeAdjFactor2,528*screenSizeAdjFactor2)
    screenFit = pygame.transform.scale(screen, screenSizeMax)
    screenFit.set_alpha(opac)
    #screenFit = screen
    screenFlush.fill((0,0,0))
    screenFlush.blit(screenFit,pygame.Rect(gv.shakeX+screenFlush.get_width()//2-screenFit.get_width()//2,gv.shakeY+screenFlush.get_height()//2-screenFit.get_height()//2,1,1))
    if random.randint(0,1):
        gv.shakeX, gv.shakeY = gv.shakeY * -0.9, gv.shakeX * -0.9
    elif random.randint(0,1):
        gv.shakeY = gv.shakeY * -0.9
    else:
        gv.shakeX = gv.shakeX * -0.9

def subTitleTut(text, xDiv, yDiv):
    screen.blit(
        textProp(text, regularFont)[0],
        (SCREEN_WIDTH//xDiv-textProp(text, regularFont)[1]//2, SCREEN_HEIGHT//yDiv-textProp(text, regularFont)[2]//2)
    )
def controlHelpScene(): #HIGHLY INEFFICIENT - FIX WHEN GETTING HOME FROM CHRISTMAS 2022
    a = 3 # main timer
    a2 = 0
    b = 1 #walk
    b2 = -25
    b3 = -1
    c = 20 #trinket
    d = 18 #ceilingslide
    e = -90
    f = 0 #triple jump
    f3 = []
    g = 0 #wall jump
    g3 = []
    g5 = list("|Wall Jump|")
    g6 = "- - - - - - - - - - - - - - - - - - - - ^ Triple Jump ^ - - - - - - - - - - - - - - - - - - - -"
    tripleJump = literal_eval(filesys.readFile(f"{mainDir}/tutData1"))
    wallJump = literal_eval(filesys.readFile(f"{mainDir}/tutData"))
    print(tripleJump)
    gv.deltaTime = clock.tick(gv.FPS)/1000
    while a > 0 or a2 > 0:
        gv.deltaTime = clock.tick(gv.FPS)/1000
        gv.timer += gv.deltaTime
        gv.deltaAdjust = gv.deltaTime*(gv.TarFPS/gv.FPS)*gv.FPS
        for event in pygame.event.get():
            if event.type in [KEYDOWN, pygame.MOUSEBUTTONDOWN]:
                a -= 1
            elif event.type == QUIT:
                gv.running = False
                a = 0
                a2 = 0
        screen.fill((0, 0, 0))
        gv.particles = particleSys.process(gv.particles, screen, 1, gv.deltaTime)
        if a == 3:
            subTitleTut("- - - Movement - WAD - - -", 2, 3)
            subTitleTut("- - - Interact with Signs - Enter - - -", 2, 2)
            subTitleTut("- - - Hang on to ceiling - Hold W - - -", 2, 1.5)
            screen.blit(
                pygame.transform.flip(
                    playerTilelist[round(b)], # Surface
                    b3 == -1, # FlipX
                    False, # FlipY
                ),
                (SCREEN_WIDTH//2-10-b2, SCREEN_HEIGHT//2.5-16)
            )
            screen.blit(
                pygame.transform.flip(
                    objectTilelist[round(c)], # Surface
                    gv.plAnimFlip, # FlipX
                    False, # FlipY
                ),
                (SCREEN_WIDTH//2-10, SCREEN_HEIGHT//1.75-16)
            )
            screen.blit(
                pygame.transform.flip(
                    playerTilelist[round(d)], # Surface
                    gv.plAnimFlip, # FlipX
                    False, # FlipY
                ),
                (SCREEN_WIDTH//2-10+round(math.sin(e*math.pi))*10, SCREEN_HEIGHT//1.3-16)
            )
            b += gv.deltaAdjust*0.1
            if b3 == -1:
                b2 += gv.deltaAdjust
            else:
                b2 -= gv.deltaAdjust
            c += gv.deltaAdjust*0.1
            d += gv.deltaAdjust*0.01
            e += gv.deltaAdjust*0.01
            if b > 6:
                b = 1
                b3 *= -1
            if c > 35:
                c = 20
            if d > 19:
                d = 18
        if a == 2:
            for i in range(len(g5)):
                screen.blit(
                    textProp(g5[i], regularFont)[0],
                    (SCREEN_WIDTH//2-textProp(g5[i], regularFont)[1]//2-240, SCREEN_HEIGHT//1.8-textProp(g5[i], regularFont)[2]//4+i*20-250)
                )
            subTitleTut(g6, 2, 1.1)
            f += 0.5*gv.deltaAdjust
            g += 0.5*gv.deltaAdjust
            if round(f)+1 >= len(tripleJump): f = 0; f3 = []
            if round(g)+1 >= len(wallJump): g = 0; g3 = []
            f2 = round(f)
            g2 = round(g)
            for f4 in f3:
                if f4[1] <= 0:
                    f3.remove(f4)
                txtW = regularFont.render("W - Jump", False, (255, 255, 255))
                txtW.set_alpha(f4[1])
                screen.blit(
                    txtW,
                    (f4[0][0]+math.cos(f4[1]*270/3)*2, f4[0][1]+f4[1]//3+math.sin(f4[1]*270/3)*2-255//3+100)
                )
                f4[1] -= 3
            for i in range(5):
                try:
                    playerEx = pygame.transform.flip(
                            playerTilelist[tripleJump[f2-i*10][2]], # Surface
                            tripleJump[f2-i*10][3], # FlipX
                            False, # FlipY
                        )
                    if i != 0: playerEx.set_alpha(50)
                    screen.blit(
                        playerEx,
                        (tripleJump[f2-i*10][0], tripleJump[f2-i*10][1]+100)
                    )
                except Exception:
                    pass
            if tripleJump[f2][4] != tripleJump[f2+1][4]:
                print(tripleJump[f2][4], tripleJump[f2+1][4])
                if (tripleJump[f2][4] != 0 and tripleJump[f2+1][4] != 3):
                    f3.append([tripleJump[f2], 255])
                musicsys.play(f"{mainDir}/SOUND/FX/jump2.wav", musicsys.sfxCh)
                gv.particles += particleSys.generate(10, 16, 0.01, 0.02, a, a, -10, -50, 0.5, (0, 255//2, 255//2), (tripleJump[f2][0], tripleJump[f2][1]+100) )
            ###
            for g4 in g3:
                if g4[1] <= 0:
                    g3.remove(g4)
                txtW = regularFont.render("W - Jump", False, (255, 255, 255))
                txtW.set_alpha(g4[1])
                screen.blit(
                    txtW,
                    (g4[0][0]+math.cos(g4[1]*270/3)*2, g4[0][1]+g4[1]//3+math.sin(g4[1]*270/3)*2-255//3-170)
                )
                g4[1] -= 3
            for i in range(5):
                try:
                    playerEx = pygame.transform.flip(
                            playerTilelist[wallJump[g2-i*10][2]], # Surface
                            wallJump[g2-i*10][3], # FlipX
                            False, # FlipY
                        )
                    if i != 0: playerEx.set_alpha(50)
                    screen.blit(
                        playerEx,
                        (wallJump[g2-i*10][0], wallJump[g2-i*10][1]-170)
                    )
                except Exception:
                    pass
            if wallJump[g2][4] != wallJump[g2+1][4]:
                print(wallJump[g2][4], wallJump[g2+1][4])
                if (wallJump[g2][4] != 0 and wallJump[g2+1][4] != 3):
                    f3.append([wallJump[g2], 255])
                musicsys.play(f"{mainDir}/SOUND/FX/jump2.wav", musicsys.sfxCh)
                gv.particles += particleSys.generate(10, 16, 0.01, 0.02, a, a, -10, -50, 0.5, (0, 255//2, 255//2), (wallJump[g2][0], wallJump[g2][1]-170) )
            subTitleTut("<- Lean towards a wall then press W", 1.8, 3)
        if a <= 1:
            subTitleTut("---------- Music ----------", 2, 4)
            subTitleTut("OrangeLeaf36, TheMIDIMan", 2, 3.25)
            subTitleTut("---------- Art ----------", 2, 2.65)
            subTitleTut("Adenator, OrangeLeaf36", 2, 2.35)
            subTitleTut("---------- Programming ----------", 2, 2)
            subTitleTut("OrangeLeaf36", 2, 1.8)
        subTitleTut("Click anywhere / Press any key", 2, 1.035)
        if a in [3,2]:
            subTitleTut("- - - - [ Controls Help ] - - - -", 2, 10)
        else:
            subTitleTut("- - - - [ Credits ] - - - -", 2, 10)
        if a <= 0:
            a2 -= gv.deltaAdjust*1.5
        elif a2 < 250:
            a2 += gv.deltaAdjust*1.5
        screenFx(a2)
        pygame.display.update()
def recorder():
    global rec, recEnabled
    if recEnabled:
        rec.append([gv.playerX, gv.playerY, gv.plSpriteNum, gv.plAnimFlip, gv.playerJumpCounter])

# Main Function
async def mainScene():  # sourcery skip: extract-method
    """
        Main Game Code
    """
    gv.deltaTime = clock.tick(gv.FPS)/1000
    gv.timer = 0
    while gv.running:
        gv.deltaTime = clock.tick(gv.FPS)/1000
        gv.timer += gv.deltaTime
        gv.volTimer += gv.deltaTime
        gv.runtimeFPS = 1/gv.deltaTime
        gv.deltaAdjust = gv.deltaTime*(gv.TarFPS/gv.FPS)*gv.FPS
        screen.fill((0,0,10))
        ##### ----- KEYCHECK ----- #####
        main_inputCheck()
        ##### ----- RECORDER ----- #####
        recorder()
        ##### ----- PLAYER CODE ----- #####
        # Makes sure the deltatime gets settled before allowing player to move
        #print(round(gv.playerXVel*100)/100, round(gv.playerYVel*100)/100, gv.plWorldX, gv.plWorldX2, gv.plWorldY, gv.plWorldY2)
        if gv.timer > 0.5: playerMovement()
        
        ##### ----- PRERENDER ----- #####
        ##### ----- ROOM/MAP CODE ----- #####
        
        pygame.mixer.music.set_volume(gv.volTimer)
        ##### ----- DISPLAY ----- #####
        main_renderCode()
        
        ###
        gui_debug_log()
        drawRoomConfig("levelTitle")
        screenFx(gv.timer*65)
        pygame.display.update()



# Main loop
#musicsys.play(f"{mainDir}/SOUND/MUSIC/24C - C4 For Lunch.mp3")
gv.map = levelsys.readTmx(f"{mainDir}/WORLDS/mainWorld/24cM_x{gv.plWorldX}_y{gv.plWorldY}.tmx")
reloadMap(True)
#mainScene()
musicsys.play(f"{mainDir}/SOUND/MUSIC/orangeleafdev_opening.mp3")
gv.running = intro.main(screenFlush,mainDir)
controlHelpScene()
musicsys.defaultCh.stop()
cProfile.run('asyncio.run(mainScene())')
pygame.display.quit()
pygame.quit()
sys.exit()
quit()
exit()
