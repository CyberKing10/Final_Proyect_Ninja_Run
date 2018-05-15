"""
youtube link for explanation: https://youtu.be/4W2AqUetBi4
"""
import pygame
import random

#define some colors
BLACK = (0,0,0)
WHITE = (255,255,255)
RED   = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)

class Ninja(pygame.sprite.Sprite): #Change to ninja character
    
    def __init__(self,color,width,height):
        super().__init__()
        #self.image = pygame.Surface([width, height])
        #self.image.fill(color)
        
        self.image = pygame.image.load("ninja.bmp")
        self.image.set_colorkey(BLUE)
        
        self.rect = pygame.rect.Rect((width,height),self.image.get_size())        

        self.rect = self.image.get_rect()
            
class Kunai(pygame.sprite.Sprite): #Change to Kunai Projectile
    
    def __init__(self,width,height):
        super().__init__()
        
        self.image = pygame.image.load("Kunai.bmp")
        self.image.set_colorkey(BLUE)
        
        self.rect = pygame.rect.Rect((width,height),self.image.get_size())
        
        self.rect = self.image.get_rect()
        
    def update(self):
        self.rect.y += 1
        if self.rect.y > 410:
            self.rect.y = -20
            self.rect.x = random.randrange(screen_width)
            
            
            
#------------------Main--------------------------#  
pygame.init()

#Set the height and width of the screen
screen_width = 700
screen_height = 400

screen = pygame.display.set_mode([screen_width,screen_height])

kunai_list = pygame.sprite.Group()

all_sprites_list = pygame.sprite.Group()

for i in range(20):
    kunai = Kunai(50, 50)
    
    kunai.rect.x = random.randrange(screen_width)
    kunai.rect.y = random.randrange(screen_height)
    
    kunai_list.add(kunai)
    all_sprites_list.add(kunai)
    
ninja = Ninja(RED,20,15) #player sprite
all_sprites_list.add(ninja)

done = False

clock = pygame.time.Clock()

# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)

health = 10

#----------------Main Program Loop-----------------------------#
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
        elif health == 0:
            done = True
            
    screen.fill(WHITE)
    
    if health == 0:
        # If game over is true, draw game over
        all_sprites_list.remove(ninja)
        screen.fill(BLACK)
        text = font.render("Game Over", True, RED)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y])   
        
    else:
        text = font.render("Health: "+str(health), True, BLACK)
        screen.blit(text, [10, 10])        
        
    all_sprites_list.update();
    
    pos = pygame.mouse.get_pos()
    
    ninja.rect.x = pos[0]
    ninja.rect.y = pos[1]
    
    kunai_hit_list = pygame.sprite.spritecollide(ninja, kunai_list,True)
    
    for kunai in kunai_hit_list:
        health -= 1
        print(health)
        
    all_sprites_list.draw(screen)    
    
    clock.tick(60)
    pygame.display.flip()
    
pygame.quit()