import random #for generating random numbers
import sys #we will use sys.exit to exit the program
import pygame
from pygame.locals import * #basic pygame imports
#global variables for the game
fps=30
screenwidth=800
screenheight=600
screen=pygame.display.set_mode((screenwidth,screenheight))
groundY=screenheight*0.8
Game_Sprites={}
Game_Sounds={}
Player='Flappy Bird\Images\Player.png'
Background='Flappy Bird\Images\Background.png'
Pipe='Flappy Bird\Images\Pipe.png'
def welcomeScreen():
    
    #Shows welcome images on the screen
    playerX=int(screenwidth/6)
    playerY=int((screenheight-Game_Sprites['Player'].get_height())/2)
    TitleX=int((screenheight-Game_Sprites['Title'].get_width())/2)
    TitleY=int(screenheight*0.13)
    baseX=-30
    while True:
        for event in pygame.event.get():
            #if user clicks on cross button,close the game
            if event.type==QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            #if the user presses space or up key,start the game for them
            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                screen.blit(Game_Sprites['Background'],(0,0))
                screen.blit(Game_Sprites['Player'],(playerX,playerY))
                screen.blit(Game_Sprites['Title'],(TitleX,TitleY))
                screen.blit(Game_Sprites['Base'],(baseX,groundY))
                pygame.display.update()
                fpsclock.tick(fps)
def mainGame():
    score=0
    playerX=int(screenwidth/5)
    playerY=int(screenheight/2)
    baseX=-30
    #create 2 pipes for blitting on the screen
    newPipe1=getRandomPipe()
    newPipe2=getRandomPipe()
    #my list of upper pipes
    upperPipes=[
        {'x':screenwidth/3,'y':newPipe1[0]['x']},
        {'x':screenwidth/3+(screenwidth/2),'y':newPipe2[0]['y']}
    ]
    #my list of lower pipes
    lowerPipes=[
        {'x':screenwidth/3,'y':newPipe1[1]['x']},
        {'x':screenwidth/3+(screenwidth/2),'y':newPipe2[1]['y']}
    ]
    pipevelocityX=-10
    playervelocityY=-9
    playerMaxVelocity=10
    playerMinvelocity=-8
    playerAccelerationY=1
    playerflapAccV=-8#velocity while flapping
    playerFlapped=False#it is true only when the bird in flapping
    while True:
        for event in pygame.event.get():
            if event.type==QUIT or(event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playerY>0:
                    playervelocityY=playerflapAccV
                    playerflapped=True
                    Game_Sounds['wing'].play()
        crashTest=isCollide(playerX,playerY,upperPipes,lowerPipes)#this function will return true if the player is crashed
        if crashTest:
            return
        #check for score
        playerMidPos=playerX+Game_Sprites['Player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos=pipe['x']+Game_Sprites['Pipe'][0].get_height()
            if pipeMidPos<=playerMidPos<pipeMidPos +8:
                score+=1
                print("Your score is ",score)
                Game_Sounds['point'].play()
        if playervelocityY<playerMaxVelocity and not playerFlapped:
            playervelocityY+=playerAccelerationY
        if playerFlapped:
            playerFlapped=False
        playerHeight=Game_Sprites['Player'].get_height()
        playerY=playerY+min(playervelocityY,groundY-playerY-playerHeight/3)
        #move pipes to the left
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x']+=pipevelocityX
            lowerPipe['x']+=pipevelocityX
        #add a new pipe when the first pipe is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<11:
            newpipe=getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
        #if the pipe is out of the screen,remove it
        if upperPipes[0]['x']< -Game_Sprites['Pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        #lets blit our sprites now screen.blit(Game_Sprites['Pipe'][0],(upperPipe,lowerPipe))
        screen.blit(Game_Sprites['Background'],(0,0))
        for upperPipe,lowerPipe in zip(upperPipes,lowerPipes):
            screen.blit(Game_Sprites['Pipe'][0],(upperPipe['x'],upperPipe['y']))
            screen.blit(Game_Sprites['Pipe'][1],(lowerPipe['x'],lowerPipe['y']))               
        screen.blit(Game_Sprites['Base'],(baseX,groundY))
        screen.blit(Game_Sprites['Player'],(playerX,playerY))
        myDigits=[int(x) for x in list(str(score))]
        width=0
        for digit in myDigits:
            width+=Game_Sprites['Numbers'][digit].get_width()
        Xoffset=((screenwidth-width)/4)+100
        for digit in myDigits:
            screen.blit(Game_Sprites['Numbers'][digit],(Xoffset-250,30))
            Xoffset+=(Game_Sprites['Numbers'][digit].get_width())
        pygame.display.update()
        fpsclock.tick(fps)
def isCollide(playerX,playerY,upperPipes,lowerPipes):
    if playerY>groundY-25 or playerY<10:
        Game_Sounds['hit'].play()
        q=True
        if q==True:
            screen.blit(pygame.image.load('Flappy Bird/Images/Gameover.png'),(300,200))
            pygame.display.update()
            fpsclock.tick(60)
        return True
    for pipe in upperPipes:
        pipeheight=Game_Sprites['Pipe'][0].get_height()
        if ((playerY<pipeheight-abs(pipe['y']-10)) and ((pipe['x']+Game_Sprites['Pipe'][1].get_width()-150)>abs(playerX)>=pipe['x']+50)):
            Game_Sounds['hit'].play()
            q=True
            if q==True:
                screen.blit(pygame.image.load('Flappy Bird/Images/Gameover.png'),(300,200))
                pygame.display.update()
                fpsclock.tick(60)
            return True
    for pipe in lowerPipes:
        pipeheight=Game_Sprites['Pipe'][1].get_height()
        if ((playerY>pipe['y']-screenheight+pipeheight+100) and ((pipe['x']+Game_Sprites['Pipe'][1].get_width()-150)>abs(playerX)>=pipe['x']+50)):
            Game_Sounds['hit'].play()
            q=True
            if q==True:
                screen.blit(pygame.image.load('Flappy Bird/Images/Gameover.png'),(300,200))
                pygame.display.update()
                fpsclock.tick(60)
            return True
def getRandomPipe():
    #generate positions of two pipes(one bottom straight and one top rotated)for blitting on the screen
    pipeHeight=Game_Sprites['Pipe'][0].get_height()
    offset=screenheight/3
    y2=offset+random.randrange(0,int(screenheight-Game_Sprites['Base'].get_height()))
    pipeX=screenwidth
    y1=-(screenheight-y2/0.9)
    pipe=[
        {'x':pipeX,'y':y1},#upper pipe
        {'x':pipeX,'y':y2}#lower pipe
        ]
    return pipe
if __name__=="__main__":
    #this will be the main point from where our game will start
    pygame.init()#initializes all the pygame modules
    fpsclock=pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird By Shreshth Srivastava')
    Game_Sprites['Numbers']=(
        pygame.image.load('Flappy Bird/Images/0.png').convert_alpha(),
        pygame.image.load('Flappy Bird/Images/1.png').convert_alpha(),
        pygame.image.load('Flappy Bird/Images/2.png').convert_alpha(),
        pygame.image.load('Flappy Bird/Images/3.png').convert_alpha(),
        pygame.image.load('Flappy Bird/Images/4.png').convert_alpha(),
        pygame.image.load('Flappy Bird/Images/5.png').convert_alpha(),
        pygame.image.load('Flappy Bird/Images/6.png').convert_alpha(),
        pygame.image.load('Flappy Bird/Images/7.png').convert_alpha(),
        pygame.image.load('Flappy Bird/Images/8.png').convert_alpha(),
        pygame.image.load('Flappy Bird/Images/9.png').convert_alpha(),
    )
    Game_Sprites['Title']=pygame.image.load('Flappy Bird\Images\Title.png').convert_alpha()
    Game_Sprites['Base']=pygame.image.load('Flappy Bird\Images\Ground.png').convert_alpha()
    Game_Sprites['Pipe']=(pygame.transform.rotate(pygame.image.load(Pipe).convert_alpha(),180),
    pygame.image.load(Pipe).convert_alpha())
    #Game sounds
    Game_Sounds['die']=pygame.mixer.Sound('Flappy Bird\Sounds\sfx_die.wav')
    Game_Sounds['hit']=pygame.mixer.Sound('Flappy Bird\Sounds\sfx_hit.wav')
    Game_Sounds['swooshing']=pygame.mixer.Sound('Flappy Bird\Sounds\sfx_swooshing.wav')
    Game_Sounds['point']=pygame.mixer.Sound('Flappy Bird\Sounds\sfx_point.wav')
    Game_Sounds['wing']=pygame.mixer.Sound('Flappy Bird\Sounds\sfx_wing.wav')
    Game_Sprites['Background']=pygame.image.load(Background).convert()
    Game_Sprites['Player']=pygame.image.load(Player).convert_alpha()
    while True:
        welcomeScreen()#Shows welcome screen to the user until he presses a button
        mainGame()#This is the main game function