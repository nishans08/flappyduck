import random
from itertools import cycle
import sys
import pygame
from pygame.locals import *

FPS = 30
SCREENWIDTH  = 300
SCREENHEIGHT = 560
GAPSIZE  = 110 # gap between logs
BASEHEIGHT  = SCREENHEIGHT * 0.81

IMAGES, SOUNDS, HIT= {}, {}, {}

# list of all possible players
PLAYERS_LIST = (
    
    (
        'assets/images/duck.png',
        'assets/images/duck.png',
        'assets/images/duck.png',
    ),
    
    (
        'assets/images/duck3.png',
        'assets/images/duck3.png',
        'assets/images/duck3.png',
    ),
    
    (
        'assets/images/duck2.png',
        'assets/images/duck2.png',
        'assets/images/duck2.png',
    ),
)
# log
LOGS_LIST = (
    'assets/images/logt.png',
    'assets/images/logc.png',
)


# backgrounds
BACKGROUNDS_LIST = (

    'assets/images/background4.png',
    'assets/images/backgroundn.png',
)

try:
    xrange
except NameError:
    xrange = range

def main():
    global FPSCLOCK, SCREEN
    pygame.init()
    SCREEN   = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Duck')
    IMAGES['numbers'] = (
        pygame.image.load('assets/images/0.png').convert_alpha(),
        pygame.image.load('assets/images/1.png').convert_alpha(),
        pygame.image.load('assets/images/2.png').convert_alpha(),
        pygame.image.load('assets/images/3.png').convert_alpha(),
        pygame.image.load('assets/images/4.png').convert_alpha(),
        pygame.image.load('assets/images/5.png').convert_alpha(),
        pygame.image.load('assets/images/6.png').convert_alpha(),
        pygame.image.load('assets/images/7.png').convert_alpha(),
        pygame.image.load('assets/images/8.png').convert_alpha(),
        pygame.image.load('assets/images/9.png').convert_alpha()
    )

    IMAGES['base0'] = pygame.image.load('assets/images/base0.png').convert_alpha()
    IMAGES['wastedimgs'] = pygame.image.load('assets/images/wastedimgs.png').convert_alpha()
    IMAGES['start'] = pygame.image.load('assets/images/start.png').convert_alpha()

    #SOUND
    if 'win' in sys.platform:
        sound = '.wav'
    else:
        sound = '.ogg'

    #Sound Effects
    SOUNDS['wasted1']    = pygame.mixer.Sound('assets/audio/wasted1' + sound)
    SOUNDS['wasted1']    = pygame.mixer.Sound('assets/audio/wasted1' + sound)
    SOUNDS['huh']        = pygame.mixer.Sound('assets/audio/huh' + sound)
    SOUNDS['Quack']      = pygame.mixer.Sound('assets/audio/Quack' + sound)

    while True:
        randBg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        IMAGES['background'] = pygame.image.load(BACKGROUNDS_LIST[randBg]).convert()

        randPlayer = random.randint(0, len(PLAYERS_LIST) - 1)
        IMAGES['player'] = (
            pygame.image.load(PLAYERS_LIST[randPlayer][0]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][1]).convert_alpha(),
            pygame.image.load(PLAYERS_LIST[randPlayer][2]).convert_alpha(),
        )
        logIndexx = random.randint(0, len(LOGS_LIST) - 1)
        IMAGES['log'] = (
            pygame.transform.flip(
                pygame.image.load(LOGS_LIST[logIndexx]).convert_alpha(), False, True),
            pygame.image.load(LOGS_LIST[logIndexx]).convert_alpha(),
        )
        HIT['player'] = (
            Hit_Function(IMAGES['player'][0]),
            Hit_Function(IMAGES['player'][1]),
            Hit_Function(IMAGES['player'][2]),
        )
        HIT['log'] = (
            Hit_Function(IMAGES['log'][0]),
            Hit_Function(IMAGES['log'][1]),
        )
        movementInfo = welcomeScreen()
        crashInfo = game(movementInfo)
        displayGame(crashInfo)

#Welcome Screen 
def welcomeScreen():
    index = 0
    playerCycle = cycle([0, 1, 2, 1])
    loopCount = 0
    playerx = int(SCREENWIDTH * 0.45)
    playery = int((SCREENHEIGHT - IMAGES['player'][0].get_height()) / 2)

    messagex = int((SCREENWIDTH - IMAGES['start'].get_width()) / 2)
    messagey = int(SCREENHEIGHT * 0.18)
    basex = 0

    playerVals = {'val': 0, 'dir': 1}

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                
                SOUNDS['Quack'].play()
                return {
                    'playery': playery + playerVals['val'],
                    'basex': basex,
                    'playerCycle': playerCycle,
                }
        # draw images
        SCREEN.blit(IMAGES['background'], (0,0))
        SCREEN.blit(IMAGES['start'], (messagex, messagey))
        SCREEN.blit(IMAGES['base0'], (basex, BASEHEIGHT))

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def game(movementInfo):
    
    score = 0
    index = 0
    playerCycle = movementInfo['playerCycle']
    playerx, playery = int(SCREENWIDTH * 0.45), movementInfo['playery']
    basex = movementInfo['basex']
    baseShift = IMAGES['base0'].get_width() - IMAGES['background'].get_width()
    playerMidPos = playerx + IMAGES['player'][0].get_width() / 2

    # create new logs
    createLog1 = getLogs()
    createLog2 = getLogs()

    lowerLogs = [
        {'x': SCREENWIDTH + 210, 'y': createLog1[1]['y']},
        {'x': SCREENWIDTH + 210 + (SCREENWIDTH / 2), 'y': createLog2[1]['y']},
    ]

    upperLogs = [
        {'x': SCREENWIDTH + 210, 'y': createLog1[0]['y']},
        {'x': SCREENWIDTH + 210 + (SCREENWIDTH / 2), 'y': createLog2[0]['y']},
    ]

 
    vt = FPSCLOCK.tick(FPS)/1250
    LogVelocityXlX = -130 * vt

    
    playerVelY    =  -12   
    playerMaxVelY =  10   
    playerVelRot  =   4   
    playerSpeed =  -11   
    playerAccerationY    =   0.75   
    playerRotation     =  60   
    playerStatus = False 


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > -2 * IMAGES['player'][0].get_height():
                    playerVelY = playerSpeed
                    playerStatus = True
                    SOUNDS['Quack'].play()

        # checks for crash
        crashTest = collisionCheck({'x': playerx, 'y': playery, 'index': index},
                               upperLogs, lowerLogs)
        if crashTest[0]:
            return {
                'y': playery,
                'groundCrash': crashTest[1],
                'basex': basex,
                'upperLogs': upperLogs,
                'lowerLogs': lowerLogs,
                'score': score,
                'playerVelY': playerVelY,
                'playerRotation': playerRotation
            }

        # check for score
        for log in upperLogs:
            logMidPos = log['x'] + IMAGES['log'][0].get_width() / 2
            if logMidPos <= playerMidPos < logMidPos + 4:
                score += 1 #Accumulate score
                SOUNDS['huh'].play()

        loopCount = 0
        # index basex change
        if (loopCount + 1) % 3 == 0:
            index = next(playerCycle)
        loopCount = (loopCount + 1) % 30
        basex = -((-basex + 100) % baseShift)

        # rotate the player
        if playerRotation > -90:
            playerRotation -= playerVelRot

        # player's movement
        if playerVelY < playerMaxVelY and not playerStatus:
            playerVelY += playerAccerationY
        if playerStatus:
            playerStatus = False

            # more rotation to cover the threshold (calculated in visible rotation)
            playerRotation = 45

        playerHeight = IMAGES['player'][index].get_height()
        playery += min(playerVelY, BASEHEIGHT - playery - playerHeight)

        # move logs to left
        for uLog, lLog in zip(upperLogs, lowerLogs):
            uLog['x'] += LogVelocityXlX
            lLog['x'] += LogVelocityXlX

        # add new logs
        if 3 > len(upperLogs) > 0 and 0 < upperLogs[0]['x'] < 5:
            createLog = getLogs()
            upperLogs.append(createLog[0])
            lowerLogs.append(createLog[1])

        # remove log when out of screen
        if len(upperLogs) > 0 and upperLogs[0]['x'] < -IMAGES['log'][0].get_width():
            upperLogs.pop(0)
            lowerLogs.pop(0)
        # draw images
        SCREEN.blit(IMAGES['background'], (0,0))

        for uLog, lLog in zip(upperLogs, lowerLogs):
            SCREEN.blit(IMAGES['log'][1], (lLog['x'], lLog['y']))
            SCREEN.blit(IMAGES['log'][0], (uLog['x'], uLog['y']))
      
        SCREEN.blit(IMAGES['base0'], (basex, BASEHEIGHT))
        
        playerScreen = pygame.transform.rotate(IMAGES['player'][index], 0)
        SCREEN.blit(playerScreen, (playerx, playery))

                # print score so player overlaps the score
        showScore(score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)

    


def displayGame(crashInfo):
    """crashes the player down and shows gameover image"""
    score = crashInfo['score']
    playerx = SCREENWIDTH * 0.45
    playery = crashInfo['y']
    playerHeight = IMAGES['player'][0].get_height()
    playerVelY = crashInfo['playerVelY']
    playerRotation = crashInfo['playerRotation']
    playerAccerationY = 99
    playerVelRot = 99

    basex = crashInfo['basex']
    upperLogs, lowerLogs = crashInfo['upperLogs'], crashInfo['lowerLogs']

    # play hit and die sounds
    SOUNDS['wasted1'].play()
    if not crashInfo['groundCrash']:
        SOUNDS['wasted1'].play()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery + playerHeight >= BASEHEIGHT - 1:
                    return

        # player velocity change
        if playerVelY < 15:
            playerVelY += playerAccerationY

        # playr y shift
        if playery + playerHeight < BASEHEIGHT - 1:
            playery += min(playerVelY, BASEHEIGHT - playery - playerHeight)

        if not crashInfo['groundCrash']:
            if playerRotation > -90:
                playerRotation -= playerVelRot

        # draw images
        SCREEN.blit(IMAGES['background'], (0,0))

        for uLog, lLog in zip(upperLogs, lowerLogs):
            SCREEN.blit(IMAGES['log'][0], (uLog['x'], uLog['y']))
            SCREEN.blit(IMAGES['log'][1], (lLog['x'], lLog['y']))

        SCREEN.blit(IMAGES['base0'], (basex, BASEHEIGHT))
        showScore(score)

        playerScreen = pygame.transform.rotate(IMAGES['player'][1], playerRotation)
        SCREEN.blit(playerScreen, (playerx, playery))
        SCREEN.blit(IMAGES['wastedimgs'], (60, 190))

        FPSCLOCK.tick(FPS)
        pygame.display.update()


def getLogs():
    gapY = random.randrange(0, int(BASEHEIGHT * 0.5 - GAPSIZE))
    gapY += int(BASEHEIGHT * 0.5)
    logx = SCREENWIDTH + 10
    logHeight = IMAGES['log'][0].get_height()

    return [
        {'x': logx, 'y': gapY - logHeight},  # upper log
        {'x': logx, 'y': gapY + GAPSIZE}, # lower log
    ]


def showScore(score):
    scoreDigits = [int(x) for x in list(str(score))]
    width = 0 # number with

    for digit in scoreDigits:
        width += IMAGES['numbers'][digit].get_width()

    Xspace = (SCREENWIDTH - width) / 2

    for digit in scoreDigits:
        SCREEN.blit(IMAGES['numbers'][digit], (Xspace, SCREENHEIGHT * 0.1))
        Xspace += IMAGES['numbers'][digit].get_width()


def player(player):
    if player['dir'] == 1:
         player['val'] += 1
    else:
        player['val'] -= 1

    if abs(player['val']) == 8:
        player['dir'] *= -1


def collisionCheck(player, upperLogs, lowerLogs):
    pi = player['index']
    player['w'] = IMAGES['player'][0].get_width()
    player['h'] = IMAGES['player'][0].get_height()

    if player['y'] + player['h'] >= BASEHEIGHT - 1:  #Check if player crashed
        return [True, True]
    else:

        playerRect = pygame.Rect(player['x'], player['y'],
                      player['w'], player['h'])
        logw = IMAGES['log'][0].get_width()
        logH = IMAGES['log'][0].get_height()

        for uLog, lLog in zip(upperLogs, lowerLogs):
            
            uLogRect = pygame.Rect(uLog['x'], uLog['y'], logw, logH)
            lLogRect = pygame.Rect(lLog['x'], lLog['y'], logw, logH)

            pHIT = HIT['player'][pi]
            uHIT = HIT['log'][0]
            lHIT = HIT['log'][1]

            #If Collison occurs
            uCollide = pixelCollision(playerRect, uLogRect, pHIT, uHIT)
            lCollide = pixelCollision(playerRect, lLogRect, pHIT, lHIT)
            if uCollide or lCollide:
                return [True, False]
    return [False, False]

def Hit_Function(image):
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

def pixelCollision(rectangle1, rectangle2, HIT1, HIT2):
    rect = rectangle1.clip(rectangle2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rectangle1.x, rect.y - rectangle1.y
    x2, y2 = rect.x - rectangle2.x, rect.y - rectangle2.y

    for x in xrange(rect.width):
        for y in xrange(rect.height):
            if HIT1[x1+x][y1+y] and HIT2[x2+x][y2+y]:
                return True
                
    return False

if __name__ == '__main__':
    main()
