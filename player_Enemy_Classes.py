import pygame
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
