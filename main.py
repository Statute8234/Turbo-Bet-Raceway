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
pygame.display.set_caption("Turbo Raceway")
clock = pygame.time.Clock()
# color
def random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
colors = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0)
}

# Function checked if the window is resized.
def on_resize() -> None:
    window_size = screen.get_size()
    new_w, new_h = window_size[0], window_size[1]
    mainMenu.width, mainMenu.height = window_size[0], window_size[1]
    mainMenu.main_menu.resize(new_w, new_h)
    mainMenu.player_screen.resize(new_w, new_h)
    mainMenu.settings_screen.resize(new_w, new_h)
    mainMenu.loadGame_screen.resize(new_w, new_h)

# mainmenu
class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screenWidth, screenHeight 
        self.create_main_menu()

    def create_main_menu(self):
        self.main_menu = pygame_menu.Menu('Welcome', self.width, self.height, theme=pygame_menu.themes.THEME_DARK)
        self.player_screen = pygame_menu.Menu('Player Screen', self.width, self.height, theme=pygame_menu.themes.THEME_DEFAULT)
        self.loadGame_screen = pygame_menu.Menu('Load Game', self.width, self.height, theme=pygame_menu.themes.THEME_DARK)
        self.settings_screen = pygame_menu.Menu('Settings', self.width, self.height, theme=pygame_menu.themes.THEME_DARK)
        # making the menu
        self.main_menu.add.button('New Game', self.newGame)
        self.main_menu.add.button('Load Game', self.loadGame)
        self.main_menu.add.button('Settings', self.settings)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

    def settings(self):
        self.settings_screen.clear()
        self.music_volume = self.settings_screen.add.range_slider('Music Volume', default=50, range_values=(0, 100), increment=1)
        self.settings_screen.add.range_slider('Sound Effects', default=50, range_values=(0, 100), increment=1)
        self.settings_screen.add.range_slider('Frame Rate', default=60, range_values=(30, 120), increment=1)
        self.settings_screen.add.range_slider('Brightness', default=100, range_values=(0, 100), increment=1)
        self.settings_screen.add.button('Return to Main Menu', pygame_menu.events.BACK)
        self.main_menu._open(self.settings_screen)
    
    def load_game(self, index):
        # Implement loading logic here
        print(f"Loading game from save: {index}")

    def loadGame(self):
        self.loadGame_screen.clear()
        saved_games = [
            "Load Game",
            "Load Game",
            "Load Game"
        ]
        for index, save in enumerate(saved_games):
            self.loadGame_screen.add.button(save, lambda index=index: self.load_game(index))
        self.loadGame_screen.add.button('Return to Main Menu', pygame_menu.events.BACK)
        self.main_menu._open(self.loadGame_screen)

    def newGame(self):
        self.player_screen.clear()
        self.player_screen.add.text_input(title="Country Name: ")
        self.frame = self.player_screen.add.frame_h(width=self.width, height=300, dynamic_width=True)
        carProfile = self.player_screen.add.image(r"assets\carPortfolio_Image.png", scale=(0.5,0.5))
        carImage = self.player_screen.add.image(r"assets\car.png", scale=(0.5,0.5))
        self.player_screen.add.color_input(title="Car Color: ", color_type="rgb", dynamic_width=False, default=random_color())
        self.frame.pack(carProfile)
        self.frame.pack(carImage, align=pygame_menu.locals.ALIGN_RIGHT)
        self.player_screen.add.button('Return to Main Menu', pygame_menu.events.BACK)
        self.main_menu._open(self.player_screen)
mainMenu = MainMenu(screen)

# main
def main():
    global screen
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                on_resize()
        screen.fill(colors["WHITE"])
        mainMenu.main_menu.update(events)
        mainMenu.main_menu.draw(screen)
        # This is to update the scene
        clock.tick(64)
        pygame.display.flip()
        pygame.display.update()

if __name__ == "__main__":
    main()
