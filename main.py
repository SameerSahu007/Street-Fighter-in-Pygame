import pygame
import math
from pygame import mixer
import os

pygame.init()

WIDTH, HEIGHT = 800, 600

#create the screen
screen = pygame.display.set_mode((WIDTH , HEIGHT))

# Title and Icon
pygame.display.set_caption("Space Fighter")
icon = pygame.image.load(os.path.join('assets', 'icon.png'))
pygame.display.set_icon(icon)


# Background
background = pygame.image.load(os.path.join('assets', 'bg.png'))

# Background Music 
mixer.music.load(os.path.join('sounds', 'bgmusic.mp3'))
mixer.music.play(-1)

#Player 1
player1 = pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join('assets', 'player1.png')), True, False), (70,70))
player1X = 20
player1Y = HEIGHT/2 - 35
player1_change = 0

#Player 2
player2 = pygame.transform.scale(pygame.transform.flip(pygame.image.load(os.path.join('assets', 'player2.png')), False, False), (70,70))
player2X = WIDTH - 90
player2Y = HEIGHT/2 - 35
player2_change = 0

#Bullet of PLayer 1
bullet1 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(os.path.join('assets', 'bullet1.png')), 90), (40, 40))
bullet1X = 0
bullet1Y = 0
bullet1_change = 1.5
fire1 = True

#Bullet of PLayer 2
bullet2 = pygame.transform.scale(pygame.transform.rotate(pygame.image.load(os.path.join('assets', 'bullet2.png')), -90), (40, 40))
bullet2X = 0
bullet2Y = 0
bullet2_change = 1.5
fire2 = True

# Score Variable 
scoreOne = 0
scoreTwo = 0

# Loading Font
font = pygame.font.Font(os.path.join('fonts', 'Gameplay.ttf'), 32)
over_font = pygame.font.Font(os.path.join('fonts', 'Gameplay.ttf'), 70)

# Score display coordinates of player 1
text1X = 20
text1Y = 20

# Score display coordinates of player 2
text2X = WIDTH - 230
text2Y = 20

def playerOneMovement(X, Y):
    screen.blit(player1, (X, Y + 15))

def playerTwoMovement(X, Y):
    screen.blit(player2, (X, Y + 15))

def bullet1Movement(X, Y):
    global fire1
    fire1 = False
    screen.blit(bullet1, (X + 45, Y + 22))

def bullet2Movement(X, Y):
    global fire2
    fire2 = False
    screen.blit(bullet2, (X - 15, Y + 22))

def collisionDetectorPlayerOne(b1x, b1y, p2x , p2y):
    global fire1
    global bullet1X 
    global bullet1Y 
    
    if int(math.sqrt(math.pow(p2x - b1x, 2) + math.pow(p2y - b1y, 2)))  < 70:
        fire1 = True
        bullet1X = 0
        bullet1X = 0
        return True


def collisionDetectorPlayerTwo(b2x, b2y, p1x, p1y):
    global fire2
    global bullet2X 
    global bullet2Y 
    distance = int(math.sqrt(math.pow(b2x - p1x, 2) + math.pow(b2y - p1y, 2)))
    if distance < 70 and distance > 20 :
        fire2 = True
        bullet2X = 0
        bullet2Y = 0
        return True

def displayScore(X, Y):
    score = font.render("Score : " + str(scoreOne), True, (255, 255, 255))
    screen.blit(score, (X, Y))

def displayScoreTwo(X, Y)   :
    score = font.render("Score : " + str(scoreTwo), True, (255, 255, 255))
    screen.blit(score, (X, Y))

def gameover():
    global scoreOne
    global scoreTwo
    score = over_font.render("GAMEOVER", True, (255, 255, 255))
    screen.blit(score, (200, 250))

    if scoreOne == 10:
       display = font.render("PLAYER ONE WON", True, (255, 255, 255))
       screen.blit(display, (260, 330))

    elif scoreTwo == 10:
       display = font.render("PLAYER TWO WON", True, (255, 255, 255))
       screen.blit(display, (260, 330))

running = True
while running:

    #Backgroung Image 
    screen.blit(background, (0, 0))

    
    for event in pygame.event.get():
          if event.type == pygame.QUIT:
             running = False
        
        #Movement Detection for player 1
          if event.type == pygame.KEYDOWN:
              if event.key  == pygame.K_w:
                  player1_change = -2
               
              if event.key == pygame.K_s:
                  player1_change = +2

              if event.key == pygame.K_SPACE:
                  if fire1 is True:
                    fire1_sound = mixer.Sound(os.path.join('sounds', 'fire1.wav'))
                    fire1_sound.play()
                    bullet1X = player1X
                    bullet1Y = player1Y
                    bullet1Movement(bullet1X, bullet1Y)
            
          if event.type == pygame.KEYUP:
              if event.key == pygame.K_w or event.key == pygame.K_s:
                 player1_change = 0

          #Movement Detection for player 2
          if event.type == pygame.KEYDOWN:
              if event.key  == pygame.K_UP:
                  player2_change = -2
               
              if event.key == pygame.K_DOWN:
                  player2_change = +2

              if event.key == pygame.K_RCTRL:
                  if fire2 is True:
                    fire2_sound = mixer.Sound(os.path.join('sounds', 'fire1.wav'))
                    fire2_sound.play()  
                    bullet2X = player2X
                    bullet2Y = player2Y
                    bullet2Movement(bullet2X, bullet2Y)
            
          if event.type == pygame.KEYUP:
              if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                 player2_change = 0

    #Movement Calculation for player 1
    player1Y += player1_change 

    if player1Y <= 70:
        player1Y = 70
    
    if player1Y >= HEIGHT-90:
        player1Y = HEIGHT-90
    
    #Movement Calculation for player 2
    player2Y += player2_change 

    if player2Y <= 70:
        player2Y = 70
    
    if player2Y >= HEIGHT-90:
        player2Y = HEIGHT-90

    # Bullet Movement for player 1 
    if bullet1X >= WIDTH :
        fire1 = True

    if fire1 is False:
        bullet1Movement(bullet1X, bullet1Y)    
        bullet1X += bullet1_change

    
    # Bullet Movement for player 2
    if bullet2X <= 0:
        fire2 = True

    if fire2 is False:
        bullet2Movement(bullet2X, bullet2Y)    
        bullet2X -= bullet2_change

    #Checking for Collision 
    if collisionDetectorPlayerOne(bullet1X, bullet1Y, player2X, player2Y) is True:
       scoreOne += 1

    if collisionDetectorPlayerTwo(bullet2X, bullet2Y, player1X, player1Y) is True:
       scoreTwo += 1

    #Checking for Who Won
    if scoreOne == 10 or scoreTwo == 10:
       gameover()
    
    displayScore(text1X, text1Y)
    displayScoreTwo(text2X, text2Y)
    playerOneMovement(player1X, player1Y)
    playerTwoMovement(player2X, player2Y)


    pygame.display.update() 
