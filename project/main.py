
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

        self.image = pygame.image.load("Assets/sprites/modified/ninja/ninja.bmp")
        self.image.set_colorkey(BLUE)

        self.rect = pygame.rect.Rect((width,height),self.image.get_size())

        self.rect = self.image.get_rect()
    def update(self):
        if key[pygame.K_LEFT]:
            self.rect.x -= 10
        if key[pygame.K_RIGHT]:
            self.rect.x += 10

class Shuriken(pygame.sprite.Sprite):

    def __init__(self,width,height):
        super().__init__()

        self.image = pygame.image.load("Shuriken.bmp")#add correct path
        self.image.set_colorkey(BLUE)

        self.rect = pygame.rect.Rect((width,height),self.image.get_size())

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 3

class Boss(pygame.sprite.Sprite): #partes de boss estan en livewire
    """
    A boss which moves left and right, throwing kunais.
    """
    self.image = pygame.image.load("Boss.bmp") #add boss path
    self.image.set_colorkey(BLUE)

    self.rect = pygame.rect.Rect((width,height),self.image.get_size())

    self.rect = self.image.get_rect()

    def __init__(self,width,height, speed = 2, odds_change = 200):
        """ Initialize the boss object. """
        super().__init__(image = Boss.self.image,
                         x = games.screen.width / 2,
                         y = y,
                         dx = speed)

        self.odds_change = odds_change
        self.time_til_drop = 0

    def update(self):
        """ Determine if direction needs to be reversed. """
        if self.left < 0 or self.right > games.screen.width:
            self.dx = -self.dx
        elif random.randrange(self.odds_change) == 0:
            self.dx = -self.dx

        self.check_drop()


    def check_drop(self):
        """ Decrease countdown or drop kunai and reset countdown. """
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            new_kunai = Kunai(x = self.x)
            games.screen.add(new_kunai)

            self.time_til_drop = int(new_kunai.height * 1.3 / kunai.speed) + 1


class Kunai(pygame.sprite.Sprite): #Change to Kunai Projectile

    def __init__(self,width,height):
        super().__init__()

        self.image = pygame.image.load("Kunai.bmp") #add correct path
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
screen_width = 1024
screen_height = 576

screen = pygame.display.set_mode([screen_width,screen_height])

forest_image = games.load_image("Assets/layouts/forest.bmp", transparent = False) #check si forest.bmp esta ahi
games.screen.background = forest_image

all_sprites_list = pygame.sprite.Group()

kunai_list = pygame.sprite.Group()
shuriken_list = pygame.sprite.Group()

ninja = Ninja()
all_sprites_list = add(ninja)

boss = Boss()
all_sprites_list = add(boss)

for i in range(20): #Boss ya tiene para tirar kunais
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
boss_health = 50

#----------------Main Program Loop-----------------------------#
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True
        elif health <= 0:
            done = True

    screen.fill(WHITE)

    if health <= 0:
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

    if boss_health <= 0:
        # If game over is true, draw game over
        all_sprites_list.remove(boss)
        screen.fill(BLACK)
        text = font.render("You win!", True, RED)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y])

    else:
        text = font.render("Boss Health: "+str(boss_health), True, RED)
        screen.blit(text, [10, 10])

    for shuriken in shuriken_list: #handles shuriken collision with boss. Removes shuriken and decreases boss health

        shuriken_hit_list = pygame.sprite.spritecollide(shuriken, boss, True)

        for boss in shuriken_hit_list:
            shuriken_list.remove(shuriken)
            all_sprites_list.remove(shuriken)
            boss_health -= 1
            print(boss_health)

        if shuriken.rect.y < -10:
            shuriken_list.remove(shuriken)
            all_sprites_list.remove(shuriken)


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
