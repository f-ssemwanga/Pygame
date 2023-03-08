#Shoot them up game
import pygame
import random

from os import path
img_dir = path.join(path.dirname(__file__),'img') #img is the folder where the graphics are

#1. Tell pygame to create a window
WIDTH = 480
HEIGHT = 600
FPS = 30    #fast and smooth

#define colours

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)


#initialise common pygame objects
pygame.init()
pygame.mixer.init() #this is required if you are going to do sound

#now create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shoot them up")
clock = pygame.time.Clock() #handles the speed

#player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image =pygame.Surface((50,40))
        #self.image.fill(GREEN)
        # load the image and scale it using the transform methods
        self.image = pygame.transform.scale(player_img,(50,38))
        #to remove the black rectangle around the image we set a colour key
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.radius = 21
       # pygame.draw.circle(self.image,RED,self.rect.center,self.radius)

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
        bullet = Bullet(self.rect.centerx,self.rect.top)
        #add bullet to all sprites group so that its updated
        all_sprites.add(bullet)
        #add bullet to the bullets sprite group
        bullets.add(bullet)


class Mob(pygame.sprite.Sprite):
    #enemy mobile object which inherits from the sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        ##        self.image = pygame.Surface((30,40))
        ##        self.image.fill(RED)
        self.image = pygame.transform.scale(mob_img,(30,40))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

        self.radius = int(self.rect.width * 0.9/2)
       # pygame.draw.circle(self.image,RED,self.rect.center,self.radius)

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

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        # x and y and respaw positions based on the player's position
        pygame.sprite.Sprite.__init__(self)
        ##        self.image = pygame.Surface((10,20))
        ##        self.image.fill(YELLOW)
        self.image = pygame.transform.scale(bullet_img,(10,20))
        self.image.set_colorkey(BLACK)
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


#load all game graphics
#convert() methods will draw the image in memory before it is displyed  which is
#much faster than drawng it in real time i.e. pixel by pixel

background = pygame.image.load(path.join(img_dir,"starfield.png")).convert()
#to place the image somewhere, make a rect for it
background_rect = background.get_rect()

#load other image
player_img = pygame.image.load(path.join(img_dir, "spaceShip.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "spaceMissile.png")).convert()
mob_img = pygame.image.load(path.join(img_dir, "spaceMeteor.png")).convert()


#create a sprite group
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()    #creating another group would aid during collision detection.
bullets = pygame.sprite.Group() #bullets sprite group
#instantiate the player object
player = Player()
#Spawn some mobs
for i in range(8):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

all_sprites.add(player)
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
        #check event for keydown to shoot
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()



    #update
    all_sprites.update()

    #check if a bullet hits a mob
    hits = pygame.sprite.groupcollide(mobs,bullets,True,True)

    #respawn mobs destroyed by bullets
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # Check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player,mobs,False, pygame.sprite.collide_circle) # parameters are object to check agaist and group against
                                        #FALSE indicates whether hit item in group should be deleted or not
    if hits:
        running = False
    #draw / render
    screen.fill(BLACK) # keep this just incase the background image does not fit the entire screen
    #draw background on the screen
    #blit means copy the pixes of one thing on to another
    screen.blit(background,background_rect)

    all_sprites.draw(screen)
    #always do this afer drawing everying
    pygame.display.flip()

#terminate the game window and close everything up
pygame.quit()
