import pygame
import random
#player class
class Player(pygame.sprite.Sprite):
    def __init__(self,width,height,color):
        pygame.sprite.Sprite.__init__(self)
        self.WIDTH = width
        self.HEIGHT = height
        self.color = color
        self.image =pygame.Surface((50,40))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.WIDTH/2     # puts it in centre of the screen
        self.rect.bottom = self.HEIGHT-10    # puts it 10px from bottom of screen
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
        if self.rect.right > self.WIDTH:
            self.rect.right = self.WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
class Mob(pygame.sprite.Sprite):
    #enemy mobile object which inherits from the sprite
    def __init__(self,width,height,color):
        pygame.sprite.Sprite.__init__(self)
        self.WIDTH = width
        self.HEIGHT = height
        self.color = color
        self.image = pygame.Surface((30,40))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()

        #make the enemy spawn off top of the screen to appear off the screen and then start dropping down
        self.rect.x = random.randrange(0, self.WIDTH - self.rect.width) #appears within the limits of the screen
        self.rect.y = random.randrange(-100,-40) #this is off the screen
        self.speedy = random.randrange(1, 8)

    def update(self):
        #move downwards
        self.rect.y += self.speedy
        #deal with enemy when they get to bottom of the screen
        if self.rect.top > self.HEIGHT +10:
            self.rect.x = random.randrange(0, self.WIDTH - self.rect.width) #appears within the limits of the screen
            self.rect.y = random.randrange(-100,-40) #this is off the screen
            self.speedy = random.randrange(1, 8)
