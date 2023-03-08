#import required modules
from  PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import sqlite3
#Shoot them up game
import pygame
import random
score =0


from os import path
img_dir = path.join(path.dirname(__file__),'img') #img is the folder where the graphics are
snd_dir = path.join(path.dirname(__file__),'snd') #snd is the folder where the sounds are

#1. Tell pygame to create a window
WIDTH = 480
HEIGHT = 600
FPS = 60    #fast and smooth

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

#search for a maching font
font_name = pygame.font.match_font('arial')

def draw_text(surf,text,size, x,y):
    #create a font object
    font = pygame.font.Font(font_name,size) # this will create text
    text_surface = font.render(text,True,WHITE) # True is for anti aliasing
    text_rect = text_surface.get_rect() #get the rectangle for the text
    text_rect.midtop = (x,y) #put x,y at the midtop of the rectangle
    surf.blit(text_surface, text_rect)

def newmob():
    m = Mob() #spawn a mob
    all_sprites.add(m) # add it to the all sprites group
    mobs.add(m) # add it to the mobs group
def draw_shield_bar(surf,x,y,pct):
    #pct is the percentage to fill
    #to avoid issues with the shape do not let the percentage fill to go below zero
    if pct<0:
        pct=0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct/100)*BAR_LENGTH # works out the fill percentage based on bar length
    outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT) #outline rectangle
    fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
    #draw the rectangle
    pygame.draw.rect(surf,GREEN,fill_rect)  # draw fill
    pygame.draw.rect(surf,WHITE,outline_rect,2) # draw outline, 2 is width of outline


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
        self.rect.centerx = WIDTH/2     # puts it in centre of the screen
        self.rect.bottom = HEIGHT-10    # puts it 10px from bottom of screen
        self.speedx = 0 #it needs to move side to side so we need speed
        self.shield = 100 #shielf variable

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
        #play a sound
        shoot_sound.play()


class Mob(pygame.sprite.Sprite):
    #enemy mobile object which inherits from the sprite
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        mob_img = random.choice(meteor_images)
        self.image_orig = pygame.transform.scale(mob_img,(30,30))
        self.image_orig.set_colorkey(BLACK)
        #set sprite image to a copy
        self.image = self.image_orig.copy()

        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.9/2)
       # pygame.draw.circle(self.image,RED,self.rect.center,self.radius)

        #make the enemy spawn off top of the screen to appear off the screen and then start dropping down
        self.rect.x = random.randrange(0, WIDTH - self.rect.width) #appears within the limits of the screen
        self.rect.y = random.randrange(-100,-40) #this is off the screen
        self.speedy = random.randrange(1, 8)
        #rotating the enemy sprite
        self.rot = 0 # angle of rotation
        self.rot_speed = random.randrange(-8,8)

        #get time since last update
        #the variable will be updated each time the rotation happens
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        #rotation code
        #find out whether it is time to rotate
        now = pygame.time.get_ticks()
        #figure out how long it has been in milliseconds and if its more than 50 then rotate
        if now - self.last_update > 50:
            self.last_update = now #take last update and set it to now
            self.rot = (self.rot + self.rot_speed) % 360 # modulo 360 will ensure rotation doesnt exceed 360

            #rotated image will be set to new image
            # figure out where the original center of the rect was
            #set the image to new image and get the new rectangle
            #take the new rect and put it at the same spot as the old center
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center





    def update(self):
        self.rotate()
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



#widget class
class Ui(QtWidgets.QMainWindow):
    #this changes based on the class used in the XML file
    '''Constructor'''
    def __init__(self):
        super(Ui, self).__init__() #call to the inherited class' constructor method
        uic.loadUi('saveScoreUi.ui',self) #loads the uic file 
        global score
        #Button event listeners / connection to buttons on the form
        self.lblScore.setText(str(score))
        self.btnSave.clicked.connect(self.saveButtonMethod)
        self.btnCancel.clicked.connect(self.cancelButtonMethod)
     
        self.show()
   
    #Event handler methods are added here
    def cancelButtonMethod(self):
        self.close()
    
    def saveButtonMethod(self):
        global score
        #Save button Method handler
        enteredUsername = self.username.text()
        print(f'username: {enteredUsername}| score: {score}')  # only for testing purposes
        
        '''Perform some validation - presence check! and display appropriate message box'''
        if enteredUsername =="":
            messageBox('Blank Fields detected!','You must enter a username!', 'warning')
        else:
            id = validIdGenerator()
            try:
                saveScoreHelper(id, enteredUsername, score)
                #inform user that their score was saved
                messageBox('Score Saved Successfully', 'Save Success!')
                self.close() #closes the current window
            except:
                messageBox('Was not able to save the score!', 'Please try agan','warning')
    
#create a messageBox function to display warnings and confirmations
def messageBox(title, content,iconType="info"):
    #creates a message box object
    msgBox =QtWidgets.QMessageBox()
    #set the message box icon based on icon type passed
    if iconType =="info": 
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
    elif iconType =="question":
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
    elif iconType =="warning":
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
    else:
        msgBox.setIcon(QtWidgets.QMessageBox.Critical)
        #Set title and content password into the method
    msgBox.setText(content)
    msgBox.setWindowTitle(title)        
    #show the message box
    msgBox.exec()
#connecting to the database
def connection():
    #this method establishes a connection to the database
    con =sqlite3.connect('scores.db')
    cur = con.cursor()
    print(con,cur)
    return con, cur   
#Execute the insert statement to save data
def saveScoreHelper(ID,Name,Score):
    #connects and executes a given query on the database
    con,cur = connection()
    query =f'''INSERT INTO tblSpaceInvaderScores VALUES ('{ID}','{Name}','{Score}') '''
    cur.execute(query, )
    #commit changes if there are any, close connection 
    con.commit()
    con.close()
def validIdGenerator():
    '''Fetch data from a database and iterate to over IDs to determine a unique value for the new record'''
    con,cur =connection()
    query =f'''SELECT ID FROM tblSpaceInvaderScores '''
    cur.execute(query, )
    #fetch data from the database and iterate to check if an ID has been used already"
    currentIDs = cur.fetchall()
    id = random.randint(1,100) #generate a random ID
    usedIds = [] #store all used IDs
    for i in range(len(currentIDs)):
        usedIds.append(currentIDs[i][0])
    #Try and find an ID which has not been used already
    while id in usedIds:
        id = random.randint(1,100)
        if id not in usedIds:
            return id
        else:
            continue
    return id
            
    
    

        
#load all game graphics
#convert() methods will draw the image in memory before it is displyed  which is
#much faster than drawng it in real time i.e. pixel by pixel

background = pygame.image.load(path.join(img_dir,"starfield.png")).convert()
#to place the image somewhere, make a rect for it
background_rect = background.get_rect()

#load other image
player_img = pygame.image.load(path.join(img_dir, "spaceShip.png")).convert()
bullet_img = pygame.image.load(path.join(img_dir, "spaceMissile.png")).convert()
#mob_img = pygame.image.load(path.join(img_dir, "spaceMeteor.png")).convert()

#create a list meteor images
meteor_images = []
meteor_list = ['spaceMeteor.png','spaceMeteor1.png','spaceMeteor2.png',
                'spaceMeteor3.png', 'spaceMeteor4.png']

#loop througj list of files
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir,img)).convert())

#load sound files
shoot_sound = pygame.mixer.Sound(path.join(snd_dir,'Laser_Shoot.wav'))
#load explosion sounds
expl_sounds = []
for snd in ['explosion_0.wav', 'explosion_1.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir,snd)))

#load background Sound
pygame.mixer.music.load(path.join(snd_dir,'bgaudio.ogg'))
pygame.mixer.music.set_volume(0.4)


#create a sprite group
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()    #creating another group would aid during collision detection.
bullets = pygame.sprite.Group() #bullets sprite group
#instantiate the player object
player = Player()
#Spawn some mobs
for i in range(8):
    newmob()

all_sprites.add(player)


#play background audio
#parameters could include - play list, looping
#loops=-1 - tells pygame to look each time audio gets to the end
pygame.mixer.music.play(loops=-1)

#Game loop
running = True
while running:
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
    hits = pygame.sprite.groupcollide(mobs,bullets,True,True) #check if a bullet hits a mob
    #respawn mobs destroyed by bullets
    for hit in hits:
        score +=1 # 1 point for every hit you make - challenge is can you award points based on the size
        newmob()

    # Check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player,mobs,True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius*2
        newmob()
        if player.shield <= 0:
            app = QtWidgets.QApplication ([]) 
            window = Ui() # creates window object from the constructor
            app.exec_()
            running = False
    #draw / render
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    #draw the score here
    draw_text(screen,str(score),18,WIDTH/2,10)
    #draw shield bar
    draw_shield_bar(screen,5,5,player.shield)

    #always do this afer drawing everying
    pygame.display.flip()

#terminate the game window and close everything up
pygame.quit()
