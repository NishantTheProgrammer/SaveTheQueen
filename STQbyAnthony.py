"""
 _____  ____  __ __    ___      ______  __ __    ___       ___   __ __    ___    ___  ____  
/ ___/ /    T|  T  |  /  _]    |      T|  T  T  /  _]     /   \ |  T  T  /  _]  /  _]|    \
(   \_ Y  o  ||  |  | /  [_     |      ||  l  | /  [_     Y     Y|  |  | /  [_  /  [_ |  _  Y
\__  T|     ||  |  |Y    _]    l_j  l_j|  _  |Y    _]    |  Q  ||  |  |Y    _]Y    _]|  |  |
/  \ ||  _  |l  :  !|   [_       |  |  |  |  ||   [_     |     ||  :  ||   [_ |   [_ |  |  |
\   ||  |  | \  / |     T      |  |  |  |  ||     T    l     |l     ||     T|     T|  |  |
 \___jl__j__j  \_/  l_____j      l__j  l__j__jl_____j     \__,_j \__,_jl_____jl_____jl__j__j
"""
# heading font http://patorjk.com/software/taag/#p=display&h=0&v=0&f=Crawford&t=testing
# sub heading font http://patorjk.com/software/taag/#p=display&h=2&v=2&f=Small%20Slant&t=testing
 
# This game was inspired by Nishant in the Pygame Facebook group (fb.com/groups/pygame)
# Shoot the enemies before they touch the queen
# Coding by Anthony Cook fb.com/anthony.cook78
 
import math, random, sys, time
import pygame
from pygame.locals import *
from pygame import gfxdraw
 
 
"""
  ___                      __              
 / _ \_______  _______ ___/ /_ _________ ___
/ ___/ __/ _ \/ __/ -_) _  / // / __/ -_|_-<
/_/  /_/  \___/\__/\__/\_,_/\_,_/_/  \__/___/
"""
def quit():
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            return True
    return False
 
def threshold_table(size, steps, reverse = False, opposite = False):
    t = 2.0 * size / (steps * (steps - 1))
    a = 0
    table = []
    for i in range(steps):
        a += t * i
        if opposite: table.append(size - a)
        else: table.append(a)
    if reverse: table.reverse()
    return table
 
 
"""
 _____                 ____    __          
/ ___/__ ___ _  ___   / __/__ / /___ _____
/ (_ / _ `/  ' \/ -_) _\ \/ -_) __/ // / _ \
\___/\_,_/_/_/_/\__/ /___/\__/\__/\_,_/ .__/
                                    /_/    
"""
# define display surface           
W, H = 1280, 720
HW, HH = W / 2, H / 2
 
# initialise display
pygame.init()
FONT = pygame.font.SysFont(None, 72)
DS = pygame.display.set_mode((W, H))
pygame.display.set_caption("Kill The Queen")
pygame.mouse.set_visible(False)
 
# start FPS monitoring
FPS = 120
SPF = 1.00 / FPS
FPSTime = time.time()
FRAME_COUNT = 0
 
 
"""
 _____     __          
/ ___/__  / /__  _______
/ /__/ _ \/ / _ \/ __(_-<
\___/\___/_/\___/_/ /___/
"""
FUCHSIA     = (255,   0, 255)
PURPLE      = (128,   0, 128)
TEAL        = (  0, 128, 128)
LIME        = (  0, 255,   0)
GREEN       = (  0, 128,   0)
OLIVE       = (128, 128,   0)
YELLOW      = (255, 255,   0)
ORANGE      = (255, 165,   0)
RED         = (255,   0,   0)
MAROON      = (128,   0,   0)
SILVER      = (192, 192, 192)
GRAY        = (128, 128, 128)
BLUE        = (  0,   0, 255)
NAVY        = (  0,   0, 128)
AQUA        = (  0, 255, 255)
DARK_GRAY   = ( 25,  25,  25)
WHITE       = (255, 255, 255)
BLACK       = (  0,   0,   0)
 
VECTOR_TABLE = [[math.cos(math.radians(degrees)), math.sin(math.radians(degrees))] for degrees in range(360)]
 
 
"""
  ____                      ___  _ __
 / __/__  ___ __ _  __ __  / _ )(_) /_
/ _// _ \/ -_)  ' \/ // / / _  / / __/
/___/_//_/\__/_/_/_/\_, / /____/_/\__/
                  /___/              
"""
ENEMY_SIZE = 20
ENEMY_GROW_STEPS = 25
ENEMY_SIZE_TABLE = threshold_table(ENEMY_SIZE, ENEMY_GROW_STEPS)
 
class enemy:
    def __init__(s):
        global HW, HH, WHITE
        global VECTOR_TABLE
 
        s.color = WHITE
 
        degrees = random.randint(0, 359)
       
        dx = random.randint(HW - 50, HW)
        s.x = HW + VECTOR_TABLE[degrees][0] * dx
       
        dy = random.randint(HH - 50, HH)
        s.y = HH + VECTOR_TABLE[degrees][1] * dy
 
        s.angle = int(math.degrees(math.atan2(HH - s.y, HW - s.x))) % 360
 
        s.sizeIndex = 0
       
        s.dead = False
        s.stopped = False
       
    def howClose(s):
        global HW, HH
        global QUEEN_SIZE, ENEMY_SIZE        
        return int(math.hypot(s.x - HW, s.y - HH))
 
    def move(s):
        global VECTOR_TABLE
        if s.stopped: return
 
        if s.sizeIndex < ENEMY_GROW_STEPS - 1:
            s.sizeIndex += 1
            return
 
        s.x += VECTOR_TABLE[s.angle][0]
        s.y += VECTOR_TABLE[s.angle][1]
 
    def draw(s):
        global DS
        global ENEMY_SIZE_TABLE
        pygame.draw.circle(DS, s.color, (int(s.x), int(s.y)), int(ENEMY_SIZE_TABLE[s.sizeIndex]))
 
class enemies:
    def __init__(s):
        global FRAME_COUNT
        s.container = []
        s.frameCounter = FRAME_COUNT
        s.newTimer()
 
    def newTimer(s):
        global FPS
        s.nextEnemyTimer = random.randint(0, FPS)
 
    def do(s):
        global HW, HH
        global RED, WHITE
        global FRAME_COUNT
        global QUEEN_SHAKE_RADIUS, QUEEN_SIZE, ENEMY_SIZE
        global queenHandler, crosshairHandler, explosionHandler
 
        queenHandler.shakeRadius = 0
        deleteEnemies = []
        for e in s.container:
            if e.dead:
                deleteEnemies.append(e)
                continue
            distanceToCrossHair = math.hypot(crosshairHandler.x - e.x, crosshairHandler.y - e.y)
            if distanceToCrossHair <= ENEMY_SIZE:
                e.color = RED
                crosshairHandler.enemyInSight = e
            elif crosshairHandler.enemyInSight == e:
                e.color = WHITE
                crosshairHandler.enemyInSight = None
 
            e.draw()
            e.move()
            distanceToQueen = e.howClose()
            if distanceToQueen < QUEEN_SHAKE_RADIUS:
                queenHandler.shakeRadius = QUEEN_SHAKE_TABLE[distanceToQueen]
 
            if distanceToQueen < QUEEN_SIZE + ENEMY_SIZE and not queenHandler.dead:
                e.stopped = True
                queenHandler.dead = True
                explosionHandler.add(HW, HH, 32)
 
        for dead in deleteEnemies:
            s.container.remove(dead)
 
        if FRAME_COUNT - s.frameCounter > s.nextEnemyTimer:
            s.frameCounter = FRAME_COUNT
            s.newTimer()
            s.container.append(enemy())
 
 
"""
 ____                      ___  _ __
/ __ \__ _____ ___ ___    / _ )(_) /_
/ /_/ / // / -_) -_) _ \ / _  / / __/
\___\_\_,_/\__/\__/_//_/ /____/_/\__/
"""
QUEEN_SIZE = 32
QUEEN_SHAKE_RADIUS = 300
QUEEN_SHAKE_SIZE = 10
QUEEN_SHAKE_TABLE = threshold_table(QUEEN_SHAKE_SIZE, QUEEN_SHAKE_RADIUS, True)
 
class queen:
    def __init__(s):
        global HW, HH
        s.dead = False
        s.shakeRadius = 0
        s.x, s.y = HW, HH
 
    def draw(s):
        global DS, HW, HH
        global QUEEN_SIZE
        if not s.dead: pygame.draw.circle(DS, ORANGE, (int(s.x), int(s.y)), QUEEN_SIZE)
   
    def move(s):
        global HW, HH
        global VECTOR_TABLE
 
        if s.shakeRadius == 0:
            s.x, s.y = HW, HH
            return
        angle = random.randint(0, 359)
        s.x = HW + VECTOR_TABLE[angle][0] * s.shakeRadius
        s.y = HH + VECTOR_TABLE[angle][1] * s.shakeRadius
 
    def do(s):
        s.move()
        s.draw()        
 
 
"""
 _____                 __        _       ___  _ __
/ ___/______  ___ ___ / /  ___ _(_)___  / _ )(_) /_
/ /__/ __/ _ \(_-<(_-</ _ \/ _ `/ / __/ / _  / / __/
\___/_/  \___/___/___/_//_/\_,_/_/_/   /____/_/\__/
"""
CROSS_HAIR_SIZE = 30
 
class crosshair:
    def __init__(s):
        s.enemyInSight = None
        s.buttonStatus = False
        s.move()
 
    def move(s):
        s.x, s.y = pygame.mouse.get_pos()
 
    def draw(s):
        global DS
        global GREEN
        global CROSS_HAIR_SIZE
        pygame.gfxdraw.hline(DS, s.x - CROSS_HAIR_SIZE, s.x + CROSS_HAIR_SIZE, s.y, GREEN)
        pygame.gfxdraw.vline(DS, s.x, s.y - CROSS_HAIR_SIZE, s.y + CROSS_HAIR_SIZE, GREEN)
 
    def trigger(s):
        global HW, HH
        global ENEMY_SIZE, QUEEN_SIZE, BULLET_HOLE_SIZE
        global explosionHandler, bulletHoleHandler, enemyHandler
        global kills, started
 
        mb = pygame.mouse.get_pressed()
        if s.buttonStatus == False and mb[0] == 1:
            started = True
            s.buttonStatus = True
            if s.enemyInSight:
                explosionHandler.add(s.enemyInSight.x, s.enemyInSight.y, ENEMY_SIZE)
                enemyHandler.container.remove(s.enemyInSight)
                s.enemyInSight = None
                kills += 1
            else:
                distanceFromQueen = math.hypot(HW - s.x, HH - s.y)
                if distanceFromQueen > QUEEN_SIZE + BULLET_HOLE_SIZE:
                    bulletHoleHandler.add(s.x, s.y)
        elif s.buttonStatus == True and mb[0] == 0:
            s.buttonStatus = False
 
    def do(s):
        s.draw()
        s.move()
        s.trigger()
 
 
"""
  ____           __         _                 ___  _ __
 / __/_ __ ___  / /__  ___ (_)__  ___  ___   / _ )(_) /_
/ _/ \ \ // _ \/ / _ \(_-</ / _ \/ _ \(_-<  / _  / / __/
/___//_\_\/ .__/_/\___/___/_/\___/_//_/___/ /____/_/\__/
        /_/                                          
"""
PARTICLE_SIZE = 10
 
PARTICLE_COUNT_TABLE = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 60, 72, 90, 120, 180, 360]
PARTICLE_COUNT_TABLE_INDEX = 13 # 20
PARTICLE_SPAWN_RADIUS_PERCENT = 0.20
 
PARTICLE_MIN_DISTANCE = 25
PARTICLE_MAX_DISTANCE = 200
PARTILCE_DISTANCE_STEP = 25
PARTICLE_DISOLVE_STEP = 20
 
PARTICLE_SHRINK_TABLE = threshold_table(PARTICLE_SIZE, PARTICLE_DISOLVE_STEP, True)
PARTICLE_COLOR_TABLE = threshold_table(255, PARTICLE_DISOLVE_STEP, True)
 
PARTICLE_DISTANCE_TABLE = [threshold_table(particleDistance, PARTICLE_DISOLVE_STEP, True, True) for particleDistance in range(PARTICLE_MIN_DISTANCE, PARTICLE_MAX_DISTANCE + PARTILCE_DISTANCE_STEP, PARTILCE_DISTANCE_STEP)]
PARTICLE_DISTANCE_TABLE_COUNT = len(PARTICLE_DISTANCE_TABLE) - 1
 
class particle:
    def __init__(s, a, x, y):
        global PARTICLE_DISTANCE_TABLE_COUNT
 
        s.angle = a
        s.distance_index = random.randint(0, PARTICLE_DISTANCE_TABLE_COUNT)
 
        s.originX, s.originY = x, y
        s.x, s.y = s.originX, s.originY
 
    def draw(s, index):
        global DS, WHITE
        global PARTICLE_SHRINK_TABLE, PARTICLE_COLOR_TABLE
        color = (255, PARTICLE_COLOR_TABLE[index], 0)
        pygame.draw.circle(DS, color, (int(s.x), int(s.y)), int(PARTICLE_SHRINK_TABLE[index]))
 
    def move(s, index):
        global VECTOR_TABLE, PARTICLE_DISTANCE_TABLE
        s.x = s.originX + VECTOR_TABLE[s.angle][0] * PARTICLE_DISTANCE_TABLE[s.distance_index][index]
        s.y = s.originY + VECTOR_TABLE[s.angle][1] * PARTICLE_DISTANCE_TABLE[s.distance_index][index]
 
    def do(s, index):
         s.draw(index)
         s.move(index)
 
class explosion:
    def __init__(s, x, y, group_radius_size):
        global WHITE
        global VECTOR_TABLE
        global PARTICLE_COUNT_TABLE, PARTICLE_COUNT_TABLE_INDEX, PARTICLE_SPAWN_RADIUS_PERCENT
 
        s.dead = False
       
        s.disolveStepCount = 0
 
        minimum_group_radius = group_radius_size - int(group_radius_size * PARTICLE_SPAWN_RADIUS_PERCENT)
        s.particles = []
        for degrees in range(0, 359, PARTICLE_COUNT_TABLE[PARTICLE_COUNT_TABLE_INDEX]):
            radius = random.randint(minimum_group_radius, group_radius_size)
            px = x + VECTOR_TABLE[degrees][0] * radius
            py = y + VECTOR_TABLE[degrees][1] * radius
            s.particles.append(particle(degrees, px, py))
 
    def do(s):
        global PARTICLE_DISOLVE_STEP
        if s.dead: return
 
        for p in s.particles:
            p.do(s.disolveStepCount)
       
        if s.disolveStepCount < PARTICLE_DISOLVE_STEP - 1:
            s.disolveStepCount += 1
        else:
            s.dead = True
 
class explosions:
    def __init__(s):
        s.container = []
   
    def do(s):
        delete_list = []
        for e in s.container:
            e.do()
            if e.dead:
                delete_list.append(e)
        for dead in delete_list:
            s.container.remove(dead)
 
    def add(s, x, y, size):
        s.container.append(explosion(x, y, size))
 
 
"""
  ___       ____    __    __ __     __          ___  _ __
 / _ )__ __/ / /__ / /_  / // /__  / /__ ___   / _ )(_) /_
/ _  / // / / / -_) __/ / _  / _ \/ / -_|_-<  / _  / / __/
/____/\_,_/_/_/\__/\__/ /_//_/\___/_/\__/___/ /____/_/\__/
 
"""
BULLET_HOLE_SIZE = 15
BULLET_HOLE_DURATION = FPS / 4
BULLET_HOLE_DISSOLVE_STEPS = FPS
BULLET_HOLE_DISSOLVE_TABLE = threshold_table(BULLET_HOLE_SIZE, BULLET_HOLE_DISSOLVE_STEPS)
BULLET_HOLE_COLOR = DARK_GRAY
 
class bulletHole:
    def __init__(s, x, y):
        global FRAME_COUNT
 
        s.x, s.y = x, y
        s.spawnTime = FRAME_COUNT
        s.dissolveIndex = 0
        s.dead = False
   
    def draw(s):
        global DS, BLACK
        global BULLET_HOLE_COLOR, BULLET_HOLE_SIZE, BULLET_HOLE_DISSOLVE_TABLE
 
        pygame.draw.circle(DS, BULLET_HOLE_COLOR, (s.x, s.y), BULLET_HOLE_SIZE)
        if s.dissolveIndex:
            pygame.draw.circle(DS, BLACK, (s.x, s.y), int(BULLET_HOLE_DISSOLVE_TABLE[s.dissolveIndex]))
   
    def do(s):
        global FRAME_COUNT
        global BULLET_HOLE_DURATION, BULLET_HOLE_DISSOLVE_STEPS
 
        s.draw()
 
        if FRAME_COUNT - s.spawnTime >= BULLET_HOLE_DURATION:
            s.dissolveIndex += 1
            if s.dissolveIndex == BULLET_HOLE_DISSOLVE_STEPS: s.dead = True
 
class bulletHoles:
    def __init__(s):
        s.container = []
   
    def add(s, x, y):
        s.container.append(bulletHole(x, y))
   
    def do(s):
        deleteBulletHole = []
        for bh in s.container:
            bh.do()
            if bh.dead: deleteBulletHole.append(bh)
        for dead in deleteBulletHole:
            s.container.remove(dead)
 
 
"""
 _____                 _   __         _      __   __      
/ ___/__ ___ _  ___   | | / /__ _____(_)__ _/ /  / /__ ___
/ (_ / _ `/  ' \/ -_)  | |/ / _ `/ __/ / _ `/ _ \/ / -_|_-<
\___/\_,_/_/_/_/\__/   |___/\_,_/_/ /_/\_,_/_.__/_/\__/___/
"""
enemyHandler = enemies()
queenHandler = queen()
crosshairHandler = crosshair()
explosionHandler = explosions()
bulletHoleHandler = bulletHoles()
 
kills = 0
started = False
 
 
"""
  __  ___     _        __              
 /  |/  /__ _(_)__    / / ___  ___  ___
/ /|_/ / _ `/ / _ \ / /_/ _ \/ _ \/ _ \
/_/  /_/\_,_/_/_//_/ /____|___/\___/ .__/
                                 /_/  
"""
while not quit():
    frameTime = time.time() - FPSTime
    if frameTime < SPF: continue
    FPSTime += frameTime
    FRAME_COUNT += 1
 
    bulletHoleHandler.do()
    queenHandler.do()
    if started:
        enemyHandler.do()
    explosionHandler.do()
    crosshairHandler.do()
 
    pygame.display.update()
    DS.fill(BLACK)
 
    if queenHandler.dead and not explosionHandler.container: break
 
print("YOU SCORED {} KILLS!".format(kills))
pygame.quit()
sys.exit()