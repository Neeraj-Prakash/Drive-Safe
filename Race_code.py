#!/usr/bin/python3

import pygame
import time
import random
pygame.init()
pygame.font.init()

display_width = 700
display_height = 600
border_width = 3
LT=None

black = (0,0,0)
white = (255,255,255)
red = (180,0,0)
b_red = (255,0,0)
green = (0,180,0)
b_green = (0,255,0)
blue = (0,0,255)
b_blue = (24,200,231)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Drive Safe')
clock = pygame.time.Clock()
pause=False

carImg = pygame.image.load('.\RaceCar3.png')
gameIcon = pygame.image.load('.\gameIcon.png')
crash_sound = pygame.mixer.Sound('.\CrashSound2.ogg')


pygame.display.set_icon(gameIcon)

car_width = 63
car_height = 96

def obs_dodged(count):
    font = pygame.font.SysFont("Arial Black", 25)
    text = font.render("Score: "+str(count) , True, black)
    gameDisplay.blit(text,(0,0))
    
def car(x,y):
    gameDisplay.blit(carImg,(x,y))

def obstacles(obsx,obsy,obsw,obsh,color):
    pygame.draw.rect(gameDisplay, color ,[obsx,obsy,obsw,obsh])

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
def quitgame():
    pygame.quit()
    quit()
   

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color=black

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(gameDisplay, ac, (x,y,w,h))
            color=white
            if click[0]==1 and action is not None:
                action()
                
    else:
            pygame.draw.rect(gameDisplay, ic, (x,y,w,h))
    pygame.font.init()
    LT = pygame.font.SysFont("Elephant",20)
    textSurf, textRect = text_objects(msg, LT, color)
    textRect.center = ((x+(w/2)),(y+(h/2)))
    gameDisplay.blit(textSurf, textRect)

    
def crash():

    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(crash_sound)
    
    LT = pygame.font.SysFont("Forte",80)
    TextSurf, TextRect = text_objects('You Crashed!', LT, (214,22,22))
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf , TextRect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        button("Play Again",100,450,120,50,green,b_green,game_loop)
        button("Quit",500,450,100,50,red,b_red,quitgame)

        pygame.display.update()
        clock.tick(60)

def unpause():
    global pause
    pygame.mixer.music.unpause()
    pause = False
        
def paused():

    pygame.mixer.music.pause()
    LT = pygame.font.SysFont("Forte",80)
    TextSurf, TextRect = text_objects('Paused', LT, black)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf , TextRect)

    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        button("Continue",100,450,100,50,green,b_green,unpause)
        button("Quit",500,450,100,50,red,b_red,quitgame)

        pygame.display.update()
        clock.tick(60)
                
def game_intro():

    intro = True
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.load('.\Loading.ogg')
    pygame.mixer.music.play(-1)

    gameDisplay.fill(white)
    LT = pygame.font.SysFont("Forte",80)
    TextSurf, TextRect = text_objects('Drive Safe', LT, black)
    TextRect.center = ((display_width/2),(display_height/2-100))
    gameDisplay.blit(TextSurf , TextRect)

    font = pygame.font.SysFont("Calibri", 30)
    text = font.render("Controls:" , True, b_blue)
    gameDisplay.blit(text,(70,300))

    text = font.render("Press "+u'\u2190' +" or "+u'\u2192'+" in Keyboard To Move Left or Right" , True, b_blue)
    gameDisplay.blit(text,(70,340))

    text = font.render("Press 'P' anytime during the game to pause" , True, b_blue)
    gameDisplay.blit(text,(70,370))
    
    font = pygame.font.SysFont("Informal Roman", 20)
    text = font.render("Creator: Neeraj Prakash" , True, (0,26,253))
    gameDisplay.blit(text,(display_width-250,display_height-30))

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        button("GO!",100,450,100,50,green,b_green,game_loop)
        button("Quit",500,450,100,50,red,b_red,quitgame)

        pygame.display.update()
        clock.tick(60)
            
def game_loop():

    global pause
    pygame.mixer.music.load('.\Background3.ogg')
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)
    
    x = (display_width/2 - car_width/2)
    y = (display_height - car_height-5)
    obs_startx = random.randrange(0, display_width - 100)
    obs_starty = -600
    obs_speed = 4
    obs_width = 100
    obs_height = 100
    score = 0
    obs_count = 1
    x_change = 0
    gameExit = False
    
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change += -5
                if event.key == pygame.K_RIGHT:
                    x_change += 5
                if event.key == pygame.K_p:
                    pause = True
                    x_change = 0
                    paused()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    x_change += 5
                if event.key == pygame.K_RIGHT:
                    x_change += -5
            
        x += x_change
        
        gameDisplay.fill(white)
        obstacles(obs_startx,obs_starty,obs_width,obs_height,blue)
        obs_starty += obs_speed
        car(x,y)
        obs_dodged(score)
        
        if x > display_width - car_width or x<0:
            crash()
        if obs_starty > display_height:
            obs_starty = 0 - obs_height
            obs_startx = random.randrange(0 , display_width - obs_width)
            score += 1
            if (score+1) % 5 == 0:
                obs_speed += 1
        
        if y < obs_starty + obs_height -5:
            if x > obs_startx and x < obs_startx + obs_width:
                crash()
            elif x + car_width > obs_startx and x + car_width < obs_startx + obs_width:
                crash()
        
        pygame.display.update()
        clock.tick(60)

game_intro()
pygame.quit()
quit()
