#Shoot them up game
import pygame
import random
import player_Enemy_Classes

#Tell pygame to create a window
WIDTH = 480
HEIGHT = 600
FPS = 60    #fast and smooth

#define colours

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)


#initialise common pygame objects
pygame.init()
pygame.mixer.init() #this is required if you are going to do sound

#now create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot them up")
clock = pygame.time.Clock() #handles the speed

#create a player sprite group
all_sprites = pygame.sprite.Group()
#create enemy/mob sprite group
mobs = pygame.sprite.Group()
#create player object
player = player_Enemy_Classes.Player(WIDTH,HEIGHT,GREEN)
all_sprites.add(player)

#create and spawn enemy object
for i in range(8):
    m = player_Enemy_Classes.Mob(WIDTH,HEIGHT,RED)
    all_sprites.add(m)
    mobs.add(m)
#Game loop
running = True
while running:
    #keep the game running at the right speed
    clock.tick(FPS)
    #process input (events)
    for event in pygame.event.get():
        #check event for closing the window
        if event.type == pygame.QUIT:
            running = False



    #update
    all_sprites.update()
    #draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    #always do this afer drawing everying
    pygame.display.flip()

#terminate the game window and close everything up
pygame.quit()
