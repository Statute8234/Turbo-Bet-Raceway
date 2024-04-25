import pygame
import random, sys, math, time
import pygame_menu
from pygame_menu import themes

pygame.init()
current_time = time.time()
random.seed(current_time)
# Seting up the display
screenWidth, screenHeight = 700, 700
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption("Race Game")
clock = pygame.time.Clock()
# color
def random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
colors = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "GRAY": (128, 128, 128),
    "DARK_GRAY": (169, 169, 169),
    "CYAN": (0, 255, 255),
    "DIM_GRAY": (105, 105, 105),
    "GOLD": (255, 215, 0)
}

# main menu
class MainMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.create_main_menu()
    
    def create_main_menu(self):
        self.main_menu = pygame_menu.Menu('Welcome', self.width, self.height, theme=pygame_menu.themes.THEME_DARK)
        self.main_menu.add.button('Play', self.game)
        self.main_menu.add.button('Settings', self.settings)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

    def quitMenu(self):
        self.main_menu.disable()

    def game(self):
        self.player_screen = pygame_menu.Menu('Player Screen', self.width, self.height, theme=pygame_menu.themes.THEME_DEFAULT)
        self.player_screen.add.text_input(title="Name: ")
        carImages = pygame.image.load('path_to_your_play_button_image.png').convert_alpha()
        self.player_screen.add.image(carImages, scale=(0.5, 0.5), onselect=self.game)
        
        self.player_screen.add.button('Play', self.quitMenu)
        self.main_menu._open(self.player_screen)

    def settings(self):
        self.settings_screen = pygame_menu.Menu('Settings', self.width, self.height, theme=pygame_menu.themes.THEME_DARK)
        self.music_volume = self.settings_screen.add.range_slider('Music Volume', default=50, range_values=(0, 100), increment=1)
        self.settings_screen.add.range_slider('Sound Effects', default=50, range_values=(0, 100), increment=1)
        self.settings_screen.add.range_slider('Frame Rate', default=60, range_values=(30, 120), increment=1)
        self.settings_screen.add.range_slider('Brightness', default=100, range_values=(0, 100), increment=1)
        self.settings_screen.add.button('Return to Main Menu', pygame_menu.events.BACK)
        self.main_menu._open(self.settings_screen)
mainMenu = MainMenu(screen, screenWidth, screenHeight)

# main
def main():
    global screen
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if not(mainMenu.main_menu.is_enabled()):
                        mainMenu.main_menu.enable()
            # main menu
            if mainMenu.main_menu.is_enabled():
                mainMenu.main_menu.mainloop(screen)

        screen.fill(colors["WHITE"])
        if not(mainMenu.main_menu.is_enabled()):
            pass
        # This is to update the scene
        clock.tick(64)
        pygame.display.flip()
        pygame.display.update()

if __name__ == "__main__":
    main()
