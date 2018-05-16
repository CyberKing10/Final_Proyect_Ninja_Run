from livewires import games, color
import random

games.init(screen_width = 1024, screen_height = 576, fps = 50)

#------------------------------------------------Boss and BossProjectile Class ----------------------------------------------------------------------------#
class Boss(games.Sprite):
    """
    A boss which moves left and right, dropping projectiles of varying sizes.
    """
    boss_health = 500
    image = games.load_image("Assets/sprites/boss/spritesheets/boss.gif")

    def __init__(self, y = 55, speed = 3, odds_change = 200):
        """ Initialize the Boss object. """
        super(Boss, self).__init__(image = Boss.image,
                                   x = games.screen.width / 2,
                                   y = y,
                                   dx = speed)
        
        self.odds_change = odds_change
        self.time_til_drop = 0
        
        self.score = games.Text(value = 500, size = 25, color = color.white,
                                    top = 5, left = 120)
        games.screen.add(self.score)
    
        boss_health_label = games.Text(value = 'Boss Health:', size = 25, color = color.white,
                                             top = 5, left = 10)     
        games.screen.add(boss_health_label)

    def update(self):
        """ Determine if direction needs to be reversed. """
        if self.left < 0 or self.right > games.screen.width:
            self.dx = -self.dx
        elif random.randrange(self.odds_change) == 0:
            self.dx = -self.dx
                
        self.fire_bullet()
        
    def fire_bullet(self):
        """ Decrease countdown or drop boss bullet and reset countdown. """
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            new_boss_projectile = BossProjectile(x = self.x)
            games.screen.add(new_boss_projectile)

            # set buffer to approx 30% of pizza height, regardless of pizza speed   
            self.time_til_drop = int(new_boss_projectile.height * 1.3 / BossProjectile.speed) + 1    

class BossProjectile(games.Sprite):
    """
    A projectile which falls to the ground.
    """ 
    image = games.load_image("Assets/sprites/projectiles/red_projectile_001.png")
    speed = 3   

    def __init__(self, x, y = 90):
        """ Initialize a BossProjectile object. """
        super(BossProjectile, self).__init__(image = BossProjectile.image,
                                    x = x, y = y,
                                    dy = BossProjectile.speed)

    def update(self):
        """ Check if bottom edge has reached screen bottom. """
        if self.bottom > games.screen.height:
            self.destroy()

    def handle_caught(self):
        """ Destroy self if caught. """
        self.destroy()
#---------------------------------------------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------------------Player and PlayerProjectile Class---------------------------------------------------------------#
        
class Player(games.Sprite):
    """ A moving player. """
    
    
    image = games.load_image("Assets/sprites/player/mech_sprites_001.png")

    def __init__(self):
        """ Initialize Player object and create Text object for score. """
        
        super(Player, self).__init__(image = Player.image,
                                  x = games.screen.width/2,
                                  bottom = games.screen.height)
        self.time_til_drop = 0
        
        self.score = games.Text(value = 200, size = 25, color = color.white,
                                top = 5, right = games.screen.width - 10)
        games.screen.add(self.score)
        
        player_health_label = games.Text(value = 'Player Health:', size = 25, color = color.white,
                                    top = 5, right = games.screen.width - 45)  
        games.screen.add(player_health_label)
        
    def update(self):
        """ Move character based on keys pressed. """
        
        if games.keyboard.is_pressed(games.K_LEFT):
            #check if we reach the edge of the screen, so we do not pass border
            if self.x == 20 or self.x == games.screen.width-20:
                self.x = 40
            else:
                self.x -= 2
            
        if games.keyboard.is_pressed(games.K_RIGHT):
            #check if we reach the edge of the screen, so we do not pass border
            if self.x == 20 or self.x == games.screen.width-20:
                self.x = games.screen.width-40
            else:
                self.x += 2 
                
        if games.keyboard.keypress(games.K_z):
            self.fire_bullet()
            
        self.get_hit()
        
        if self.score.value == 0:
            self.end_game()
            
    def fire_bullet(self):
        """ Decrease countdown or drop boss bullet and reset countdown. """
        if self.time_til_drop > 0:
            self.time_til_drop -= 1
        else:
            new_player_projectile = PlayerProjectile(x = self.x)
            games.screen.add(new_player_projectile)

            # set buffer to approx 30% of pizza height, regardless of pizza speed   
            self.time_til_drop = int(new_player_projectile.height * 1.3 / PlayerProjectile.speed) + 1    
        
    def get_hit(self):
        """ Check if player got hit by  enemies projectiles. """
        for bossProjectile in self.overlapping_sprites:
            self.score.value -= 10
            self.score.right = games.screen.width - 10 
            bossProjectile.handle_caught()
            
    def end_game(self):
        """ End the game. """
        end_message = games.Message(value = "Game Over",
                                    size = 90,
                                    color = color.red,
                                    x = games.screen.width/2,
                                    y = games.screen.height/2,
                                    lifetime = 3.3 * games.screen.fps,
                                    after_death = games.screen.quit)
        games.screen.add(end_message)

class PlayerProjectile(games.Sprite):
    """
    A projectile which falls to the ground.
    """ 
    image = games.load_image("Assets/sprites/projectiles/blue_projectile_002.png")
    speed = -2   

    def __init__(self, x, y = 505):
        """ Initialize a PlayerProjectile object. """
        super(PlayerProjectile, self).__init__(image = PlayerProjectile.image,
                                    x = x, y = y,
                                    dy = PlayerProjectile.speed)

    def update(self):
        """ Check if bottom edge has reached top screen. """
        if self.top > games.screen.height:
            self.destroy()

    def handle_caught(self):
        """ Destroy self if caught in collision with the boss """
        self.destroy()
        
        #---------------------------------------------------------------------------------------------------------------------------------------------------------#
        
        #---------------------------------------------------------Layouts Class-----------------------------------------------------------------------------------#
        
            
class Layouts():
    """Layouts class, depending on the level, the background changes """
    def first_level(self):
        forest_image = games.load_image("Assets/layouts/forest.bmp", transparent = False)
        games.screen.background = forest_image 
        
    def second_level(self):
        dark_fantasy_image = games.load_image("Assets/layouts/dark_fantasy.png", transparent = False)
        games.screen.background = dark_fantasy_image 
        
    def third_level(self):
        space_image = games.load_image("Assets/layouts/space.png", transparent = False)
        games.screen.background = space_image
        
    def game_over_screen(self):
        game_over_image = games.load_image("Assets/layouts/game_over.png", transparent = False)
        games.screen.background = space_image
        

"""-----------------------------Main Program Definition-------------------------------------"""
class Main():
    """ Defining the main """
    def main(self):
        
        layout = Layouts()
        layout.third_level()
        
        the_boss = Boss()
        games.screen.add(the_boss)
        
        the_player = Player()
        games.screen.add(the_player)        
        
        """Game Loop"""
        games.screen.mainloop()

"""-----------------------------Main Program Declaration-------------------------------------"""
# Main object creation
main_object = Main()

#Game Program Initialization
main_object.main()
