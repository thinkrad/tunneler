import sys, os
from Grid import *
from Object import *
from Movable import *
from Player import *
from Constants import *
import pygame
from pygame.locals import *

class Game():
    def __init__(self):
        # Required to get pygame's event handling
        pygame.init()
        screen = pygame.display.set_mode((1, 1))
        pygame.mouse.set_visible(0)
        self.clock = pygame.time.Clock()
        #pygame.event.set_grab(True)
        
        self.grid = Grid()
        self.grid.addBase(B1, 3, 4)  
        self.grid.addBase(B2, 10, 10)
        
        self.player1 = Player(5, 6, self.grid, P1, P2, B1, B2)
        self.player2 = Player(12, 12, self.grid, P2, P1, B2, B1)
        self.players = [self.player1, self.player2]
        
        self.vp1 = Viewport(self.grid, self.player1)
        self.vp2 = Viewport(self.grid, self.player2)
        self.viewports = [self.vp1, self.vp2]
        
    def clearScreen(self):
        if os.name == 'posix':
            os.system('clear')
        elif os.name in ("nt", "dos", "ce"):
            # DOS/Windows
            os.system('CLS')
            
    def startGame(self):
        ''' Starts the game. '''
        
        self.gameOn = True        
    
    def endGame(self):
        ''' Ends the game. '''
        
        self.gameOn = False

    def mainLoop(self):
        # frameCount is a way of controlling the speed
        # of movement when a movement button is held
        frameCount = 0
        
        self.startGame()
        
        # Main game loop
        while self.gameOn:
            self.clearScreen()

            for player in self.players:
                player.update()
                if player.getDead() == True:
                    self.endGame()
                for bullet in player.getBullets():
                    bullet.move()
                
            for viewport in self.viewports:
                # Display everything
                viewport.display()
                viewport.HUD()
                if DEBUG == True:
                    for e in error:
                        print e
            
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    frameCount = 0
                    if event.key == K_ESCAPE:
                        done = True
                    if event.key == K_w:
                        self.player1.move(NORTH) 
                    if event.key == K_s:
                        self.player1.move(SOUTH)
                    if event.key == K_d:
                        self.player1.move(EAST)
                    if event.key == K_a:
                        self.player1.move(WEST)
                    if event.key == K_SPACE:
                        self.player1.shoot()
                    if event.key == K_UP:
                        self.player2.move(NORTH)
                    if event.key == K_LEFT:
                        self.player2.move(WEST)
                    if event.key == K_RIGHT:
                        self.player2.move(EAST)
                    if event.key == K_DOWN:
                        self.player2.move(SOUTH)
                    if event.key == K_RCTRL:
                        self.player2.shoot()
                
            #pygame.event.pump()
            if frameCount == MAX_FPS / 3:
                frameCount = 0
                pressed = pygame.key.get_pressed()
                if pressed[K_w] == 1:
                    self.player1.move(NORTH)   
                if pressed[K_s] == 1:
                    self.player1.move(SOUTH)
                if pressed[K_d] == 1:
                    self.player1.move(EAST)
                if pressed[K_a] == 1:
                    self.player1.move(WEST)
                if pressed[K_SPACE] == 1:
                    self.player1.shoot()
                if pressed[K_UP] == 1:
                    self.player2.move(NORTH)   
                if pressed[K_DOWN] == 1:
                    self.player2.move(SOUTH)
                if pressed[K_RIGHT] == 1:
                    self.player2.move(EAST)
                if pressed[K_LEFT] == 1:
                    self.player2.move(WEST)
                if pressed[K_RCTRL] == 1:
                    self.player2.shoot()

            frameCount += 1
            
            # keep the game running at the right speed
            self.clock.tick(MAX_FPS)

        # The game's over, clear the terminal
        #self.clearScreen()
        
