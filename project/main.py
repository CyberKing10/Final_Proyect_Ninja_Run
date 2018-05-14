from livewires import games, color

games.init(screen_width = 1024, screen_height = 576, fps = 50)

class Ninja(games.Sprite):
    """ A moving ship. """
    def update(self):
        """ Move ship based on keys pressed. """
        if games.keyboard.is_pressed(games.K_z):
            self.y -= 2           
        """if games.keyboard.is_pressed(games.K_DOWN):
            self.y += 2"""
        if games.keyboard.is_pressed(games.K_LEFT):
            self.x -= 2
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.x += 2

"""-----------------------------Main Program Definition-------------------------------------"""
class Main():
    """ Defining the main """
    def main(self):
        forest_image = games.load_image("Assets/layouts/forest.bmp", transparent = False)
        games.screen.background = forest_image
        
        ninja_image = games.load_image("Assets/sprites/modified/ninja/Idle__000.png")
        ninja = Ninja(image = ninja_image, x= 30, y = 526)
        
        games.screen.add(ninja)
        """Event Validations and Rules"""
        games.screen.mainloop()

"""-----------------------------Main Program Declaration-------------------------------------"""
# Main object creation
main_object = Main()

#Game Program Initialization
main_object.main()

