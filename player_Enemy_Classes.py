import pygame
import random

#constants
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
WIDTH = 480
HEIGHT = 600
FPS = 60    #fast and smooth
clock = pygame.time.Clock() #handles the speed




#Main app handler
class MainApp():
    def __init__(self):
        #Tell pygame to create a window
        self.width = WIDTH
        self.height = HEIGHT
        self.fps = FPS    #fast and smooth
        self.bgColor =BLACK
        self.gameClock = clock
        #now create the window
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
       
        
#Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,spgroup):
        # x and y and respawn positions based on the player's position
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,20))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        #set re-spawn position to right infront of the player
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        #rect moves upwards at the speed
        self.rect.y += self.speedy
        #kill it if it moves off the top of the screen
        if self.rect.bottom  < 0:
            self.kill()

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self,spgroup,bspgroup,player_img):
        pygame.sprite.Sprite.__init__(self)
        self.spgroup = spgroup
        self.bspgroup = bspgroup
        #self.image =pygame.Surface((50,40))
        #self.image.fill(GREEN)
        '''Load image ad scale it using the transform methods'''
        self.image = pygame.transform.scale(player_img,(50,38))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH/2     # puts it in centre of the screen
        self.rect.bottom = HEIGHT-10    # puts it 10px from bottom of screen
        #it needs to move side to side so we need speed
        self.speedx = 0

    def update(self):
        #we will keep the default speed of the object to zero and only alter it with a key press
        # this way we avoid coding for what happens when the key is released
        self.speedx = 0
        keystate = pygame.key.get_pressed() # returned a list of keys that are down
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5

        self.rect.x += self.speedx      # move at speed to be set by controls

        #constrain the object within the width of the screen
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
    def shoot(self):
        #spawns new bullet at centrex of player
        #y will spawn at the top - i.e.bottom of the bullet at the top of the player
        bullet = Bullet(self.rect.centerx,self.rect.top,self.spgroup)
        #add bullet to all sprites group so that its updated
        self.spgroup.add(bullet)
        #add bullet to the bullets sprite group
        self.bspgroup.add(bullet)
class Mob(pygame.sprite.Sprite):
    #enemy mobile object which inherits from the sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((30,40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()

        #make the enemy spawn off top of the screen to appear off the screen and then start dropping down
        self.rect.x = random.randrange(0, WIDTH - self.rect.width) #appears within the limits of the screen
        self.rect.y = random.randrange(-100,-40) #this is off the screen
        self.speedy = random.randrange(1, 8)

    def update(self):
        #move downwards
        self.rect.y += self.speedy
        #deal with enemy when they get to bottom of the screen
        if self.rect.top > HEIGHT +10:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width) #appears within the limits of the screen
            self.rect.y = random.randrange(-100,-40) #this is off the screen
            self.speedy = random.randrange(1, 8)
