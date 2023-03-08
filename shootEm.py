#Shoot them up game
import pygame
import random
import player_Enemy_Classes
from os import path
'''
- dealing with images
- load all game graphics
- convert() methods will draw the image in memory before it is displyed  which is
- much faster than drawng it in real time i.e. pixel by pixel'''
img_dir = path.join(path.dirname(__file__),'img') #img is the folder where the graphics are
#to place the image somewhere, make a rect for it

mApp = player_Enemy_Classes.MainApp() #moved some variables into the classes module

#initialise common pygame objects
pygame.init()
pygame.mixer.init() #this is required if you are going to do sound

#now create the window
screen = mApp.screen
pygame.display.set_caption("Shoot them up")

#load other image
background = pygame.image.load(path.join(img_dir,"starfield.png")).convert()
player_img = pygame.image.load(path.join(img_dir, "spaceShip.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "spaceMissile.png")).convert()
mob_img = pygame.image.load(path.join(img_dir, "spaceMeteor.png")).convert()
background_rect = background.get_rect()
#create a player emeny and bullet sprite group
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
#create player object
player = player_Enemy_Classes.Player(all_sprites,bullets,player_img,bullet_img)
all_sprites.add(player)

#create and spawn enemy object
for i in range(8):
    m = player_Enemy_Classes.Mob()
    all_sprites.add(m) 
    mobs.add(m)
#create a bullet object

#Game loop
running = True
while running:
    #keep the game running at the right speed
    mApp.gameClock.tick(mApp.fps)
    #process input (events)
    for event in pygame.event.get():
        #check event for closing the window
        if event.type == pygame.QUIT:
            running = False
        # check if player has initiated a shoot action
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
        #check if a bullet hits a mob
        #you have to consider a group of bullets and a group of mobs
        #using a pygame.sprite.groupcollide() method helps to collide two groups together
        #Setting the last two parameters will delete the bullet and the mob which collide with each other
        #notice that this will kill the mobs so there needs to be a way of respawning them if the get killed
    hits = pygame.sprite.groupcollide(mobs,bullets,True,True)

    #respawn mobs destroyed by bullets
    for hit in hits:
        m = player_Enemy_Classes.Mob()
        all_sprites.add(m)
        mobs.add(m)

    # Check to see if a mob hit the playe r
    hits = pygame.sprite.spritecollide(player,mobs,False) # parameters are object to check agaist and group against
    #FALSE indicates whether hit item in group should be deleted or not
    if hits:
        running = False


  
    #update
    all_sprites.update()
    #draw / render
    screen.fill(mApp.bgColor)
    #draw the background image onto the screen
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    #always do this afer drawing everying
    pygame.display.flip()

#terminate the game window and close everything up
pygame.quit()
 