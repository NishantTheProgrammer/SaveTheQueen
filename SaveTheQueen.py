import pygame
import random
pygame.init()

screenSize=900
gameDisplay=pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #it takes height and width we need to pass tuple here!

#-----------------------------------------------Variables-------------------------------
gameOver=False
exitGame=False
background=pygame.image.load("queenBackground.jpg")
queen=pygame.image.load("queen.png")
queen=pygame.transform.scale(queen, (80, 160))  # height of image 60px and width 160px
clock=pygame.time.Clock()
fps=30 #I need 30 freams per second
cursor=pygame.image.load("cursor.png")
cursor=pygame.transform.scale(cursor, (200, 200))       #This will turn picture to 200x200p image
gameOverImage=pygame.image.load("go.png")
shoot=pygame.mixer.Sound("shoot.wav")


devil1=pygame.image.load("devil1.png")
devil1=pygame.transform.scale(devil1, (80,80))
devil2=pygame.image.load("devil2.png")
devil2=pygame.transform.scale(devil2, (80,80))
devil3=pygame.image.load("devil3.png")
devil3=pygame.transform.scale(devil3, (80,80))
devil4=pygame.image.load("devil4.png")
devil4=pygame.transform.scale(devil4, (80,80))
devil5=pygame.image.load("devil5.png")
devil5=pygame.transform.scale(devil5, (80,80))      #This will turn devil's picture to 80x80p

devil6=pygame.image.load("devil6.png")
devil6=pygame.transform.scale(devil6, (80,80))

dList=[devil1, devil2, devil3, devil4, devil5, devil6]
x=y=0       #to store x and y cordinates of cursor
pygame.mouse.set_visible(0)     #zero for invisible pointer
enemyCreation=True
speed=2
divider=300

enemyList=[]

#-----------------------------------------------Classes and functions----------------
def randomColor():
    x=random.randrange(50,205)  #This will select random value for red
    y=random.randrange(50,205)  #This will select random value for green
    z=random.randrange(50,205)  #This will select random value for blue
    return (x, y, z)


class Enemy:
    def __init__(self):     
        centerX=960
        centerY=540
        self.x=random.randrange(0, 1920-80)        #x cordinate of enemy because we don't want to spawn enemy outside the screen
        self.y=random.randrange(0, 1080-80)        #for y cordinate
        self.devil=random.choice(dList)             #A randomly choosen image of enemy
        self.distance=300

        while abs(centerY-self.y)<400 and abs(centerX-self.x)<600:
            self.y=random.randrange(0, 1080-80)
            if self.y<centerY:
                self.y-=80

        while abs(centerX-self.x)<600 and abs(centerY-self.y)>400:
            self.x=random.randrange(0, 1920-80)
            if self.x<centerX:
                self.x-=80
        if self.x<centerX and self.y<centerY:
            self.xSpeed=abs(960-40-self.x)/divider
            self.ySpeed=abs(540-40-self.y)/divider
        

        if self.x<centerX and self.y>centerY:
            self.xSpeed=abs(960-40-self.x)/divider
            self.ySpeed=-abs(540-40-self.y)/divider
        

        if self.x>centerX and self.y<centerY:
            self.xSpeed=-abs(960-40-self.x)/divider
            self.ySpeed=abs(540-40-self.y)/divider
        

        if self.x>centerX and self.y>centerY:
            self.xSpeed=-abs(960-40-self.x)/divider
            self.ySpeed=-abs(540-40-self.y)/divider
        
    def killQueen():
        for enemy in enemyList:
            enemy.x+=enemy.xSpeed
            enemy.y+=enemy.ySpeed
            enemy.distance-=1
        

        
    def display():  #Function for blit all the Enemies
        for enemy in enemyList:
            gameDisplay.blit(enemy.devil, (enemy.x, enemy.y))

def music():
    pygame.mixer.music.load("back.mp3")
    pygame.mixer.music.play(-1)     #-1 for play this music infinitly

def gameOverMusic():
    pygame.mixer.music.load("gameOverSound.mp3")
    pygame.mixer.music.play()

def gameOverFunction():
    global exitGame, gameOver, enemyList
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                exitGame=True
            if event.key==pygame.K_SPACE:       #if user press space then restart the game
                enemyList=[]                    #No Enemy
                music()
                gameOver=False
                break
    gameDisplay.blit(gameOverImage, (0, 0))
    pygame.display.update()
    clock.tick(fps)





def gameloop(): #This is actual function where we write code of game
    global gameOver, exitGame, x, y, enemyList, enemyCreation
    gameDisplay.blit(background,(0, 0))
    gameDisplay.blit(queen, (960-40, 540-80))     #screen height/2-height of image/2 and screen width/2 - width of image/2
    #Let's create a magical circle around queen
    pygame.draw.circle(gameDisplay, randomColor(), (960, 540), 100, 10)     #arguments are window, color(r,g,b), x and y cordinates, radius, width
    Enemy.display()
    Enemy.killQueen()
    for enemy in enemyList:
        if enemy.distance<40:
            gameOverMusic()
            gameOver=True
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                exitGame=True
                gameOver=True #Let's run
        elif event.type==pygame.MOUSEBUTTONDOWN:
            shoot.play()
            x, y=event.pos
            c=pygame.transform.scale(cursor, (180, 180))
            for i, enemy in enumerate(enemyList):
                if abs(x-(enemy.x+40))<10 and abs(y-(enemy.y+40))<10:
                    enemyList.pop(i)
            gameDisplay.blit(c, (x-90, y-90))
        elif event.type==pygame.MOUSEMOTION:
            x, y= event.pos
    if int((pygame.time.get_ticks()/1000)%speed)==0 and enemyCreation==True:
        enemyList.append(Enemy())
        enemyCreation=False
    if int((pygame.time.get_ticks()/1000)%speed)==speed-1:
        enemyCreation=True

    gameDisplay.blit(cursor,(x-100, y-100)) #let's try
    pygame.display.update()
    clock.tick(fps)


music()         #Before starting anything we want music
while not exitGame:     #this loop run till exit over
    if not gameOver:
        gameloop()
    else:
        gameOverFunction()