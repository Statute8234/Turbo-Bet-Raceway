import pygame
import pygame_menu
from pygame_menu import themes
import random
import random, sys, math, time
import pandas as pd
current_time = time.time()
random.seed(current_time)

# color
def random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

class MainMenu:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.singlePlayer = False
        self.multiplayer = False
        self.create_main()
    
    def create_main(self):
        self.main_menu = pygame_menu.Menu('Welcome', self.width, self.height, theme=pygame_menu.themes.THEME_DARK)
        self.settings_screen = pygame_menu.Menu('Settings', self.width, self.height, theme=pygame_menu.themes.THEME_DARK)
        self.main_menu.add.button('Single Player Game', self.Single_Player)
        self.main_menu.add.button('multiplayer Game', self.Multiplayer)
        self.main_menu.add.button('Settings', self.settings)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)
    
    def Single_Player(self):
        self.singlePlayer = True
    
    def Multiplayer(self):
        self.multiplayer = True
    
    def settings(self):
        self.settings_screen.clear()
        self.music_volume = self.settings_screen.add.range_slider('Music Volume', default=50, range_values=(0, 100), increment=1)
        self.settings_screen.add.range_slider('Sound Effects', default=50, range_values=(0, 100), increment=1)
        self.settings_screen.add.range_slider('Frame Rate', default=60, range_values=(30, 120), increment=1)
        self.settings_screen.add.range_slider('Brightness', default=100, range_values=(0, 100), increment=1)
        self.settings_screen.add.button('Return to Main Menu', pygame_menu.events.BACK)
        self.main_menu._open(self.settings_screen)

class CreatePlayer:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.country_name = ''
        self.flag_color_1 = random_color()
        self.flag_color_2 = random_color()  
        self.symbol_color = random_color()
        self.pattern = 'Stripes'
        self.shape = 'Circle'
        self.shape_size = 50
        self.shape_position = (self.width // 2, self.height // 2)
        self.showflag = False
        # car
        self.userNumber = random.randint(0, sys.maxsize)
        self.api_key = "***"
        self.makes = []
        self.models = []
        self.selected_make = None
        self.selected_model = None
        self.car_data = None
        self.play = False
        self.create_main()
    
    def create_main(self):
        self.flag_screen = pygame_menu.Menu('Create Flag', self.width, self.height, theme=pygame_menu.themes.THEME_DEFAULT)
        self.car_screen = pygame_menu.Menu('Create Car', self.width, self.height, theme=pygame_menu.themes.THEME_DEFAULT)
        self.flag_screen.add.text_input("Country Name: ", onchange=self.set_country_name)
        self.flag_screen.add.color_input("Flag Color 1: ", default=self.flag_color_1, onchange=self.set_flag_color_1, color_type='rgb')
        self.flag_screen.add.color_input("Flag Color 2: ", default=self.flag_color_2, onchange=self.set_flag_color_2, color_type='rgb')
        self.flag_screen.add.color_input("Symbol Color: ", default=self.symbol_color, onchange=self.set_symbol_color, color_type='rgb')
        # Pattern selector (dropdown)
        self.flag_screen.add.selector(
            title="Pattern: ",
            items=[('Stripes', 'Stripes'), ('Solid', 'Solid'), ('Checker', 'Checker')],
            onchange=self.set_pattern
        )

        # Shape selector (dropdown)
        self.flag_screen.add.selector(
            title="Shape: ",
            items=[('Circle', 'Circle'), ('Square', 'Square'), ('Star', 'Star')],
            onchange=self.set_shape
        )

        # Shape size slider
        self.flag_screen.add.range_slider(
            title='Shape Size: ', 
            default=self.shape_size, 
            range_values=(10, 100), 
            increment=10, 
            onchange=self.set_shape_size
        )

        # Shape position sliders (X and Y)
        self.flag_screen.add.range_slider(
            title='Shape Position X: ', 
            default=self.shape_position[0], 
            range_values=(0, self.width), 
            increment=10, 
            onchange=self.set_shape_position_x
        )
        self.flag_screen.add.range_slider(
            title='Shape Position Y: ', 
            default=self.shape_position[1], 
            range_values=(0, self.height), 
            increment=10, 
            onchange=self.set_shape_position_y
        )
        # Button to preview the flag
        self.flag_screen.add.button('Preview Flag', self.preview_flag)
        # Button to play after creating the flag
        self.flag_screen.add.button('Next', self.next_screen)

    def set_country_name(self, value):
        self.country_name = value
    
    def set_flag_color_1(self, color):
        self.flag_color_1 = color

    def set_flag_color_2(self, color):
        self.flag_color_2 = color

    def set_symbol_color(self, color):
        self.symbol_color = color

    def set_pattern(self, selected_value, pattern):
        self.pattern = pattern

    def set_shape(self, selected_value, shape):
        self.shape = shape

    def set_shape_size(self, size):
        self.shape_size = int(size)

    def set_shape_position_x(self, x):
        self.shape_position = (int(x), self.shape_position[1])

    def set_shape_position_y(self, y):
        self.shape_position = (self.shape_position[0], int(y))

    def draw_shape(self, surface):
        # Draw the selected shape at the selected position and size
        if self.shape == 'Circle':
            pygame.draw.circle(surface, self.symbol_color, self.shape_position, self.shape_size)
        elif self.shape == 'Square':
            rect = pygame.Rect(0, 0, self.shape_size * 2, self.shape_size * 2)
            rect.center = self.shape_position
            pygame.draw.rect(surface, self.symbol_color, rect)
        elif self.shape == 'Star':
            self.draw_star(surface, self.shape_position, self.shape_size, 5, self.symbol_color)

    def draw_star(self, surface, position, size, points, color):
        # Draw a star with the specified number of points
        x, y = position
        point_list = []
        angle_step = 360 / points
        for i in range(points * 2):
            angle = i * angle_step / 2
            radius = size if i % 2 == 0 else size // 2
            radian_angle = math.radians(angle)  # Use math.radians() here
            point_x = x + int(math.cos(radian_angle) * radius)
            point_y = y + int(math.sin(radian_angle) * radius)
            point_list.append((point_x, point_y))
        pygame.draw.polygon(surface, color, point_list)

    def preview_flag(self):
        # Clear the screen
        self.showflag = True

        # Draw the flag based on the selected pattern
        flag_rect = pygame.Rect(self.width//4, self.height//4, self.width//2, self.height//2)

        if self.pattern == 'Stripes':
            # Horizontal stripes: 2 stripes of color 1 and color 2
            pygame.draw.rect(self.screen, self.flag_color_1, flag_rect)
            pygame.draw.rect(self.screen, self.flag_color_2, pygame.Rect(flag_rect.x, flag_rect.y + flag_rect.height // 2, flag_rect.width, flag_rect.height // 2))

        elif self.pattern == 'Solid':
            # Solid color 1
            pygame.draw.rect(self.screen, self.flag_color_1, flag_rect)

        elif self.pattern == 'Checker':
            # Checkerboard pattern (2x2 grid of alternating colors)
            checker_size = flag_rect.width // 2
            pygame.draw.rect(self.screen, self.flag_color_1, pygame.Rect(flag_rect.x, flag_rect.y, checker_size, checker_size))
            pygame.draw.rect(self.screen, self.flag_color_2, pygame.Rect(flag_rect.x + checker_size, flag_rect.y, checker_size, checker_size))
            pygame.draw.rect(self.screen, self.flag_color_2, pygame.Rect(flag_rect.x, flag_rect.y + checker_size, checker_size, checker_size))
            pygame.draw.rect(self.screen, self.flag_color_1, pygame.Rect(flag_rect.x + checker_size, flag_rect.y + checker_size, checker_size, checker_size))

        # Draw the selected shape
        self.draw_shape(self.screen)

        # Refresh the display
        pygame.display.flip()

    def make_modelsList(self):
        data = pd.read_csv('dataFiles\car_db_metric.csv', header=0, usecols=['make','model'])
        self.makes = data['make'].unique().tolist()
        self.models = data['model'].unique().tolist()

    def next_screen(self):
        self.car_screen.clear()
        self.frame = self.car_screen.add.frame_h(width=self.width, height=300, dynamic_width=True)
        self.car_screen.add.label('User Number: ' + str(self.userNumber))
        self.flag_screen._open(self.car_screen)
        carProfile = self.car_screen.add.image(r"ImageFile/carPortfolio_Image.png", scale=(0.5,0.5))
        self.car_screen.add.color_input(title="Car Color: ", color_type="rgb", dynamic_width=False, default=random_color())
        self.car_screen.add.color_input(title="Interior Color: ", color_type="rgb", dynamic_width=False, default=random_color())
        self.frame.pack(carProfile)
        self.make_modelsList()
        # ---
        self.car_screen.add.selector(
            title="Model: ",
            items=self.models,
            onchange=self.set_shape
        )

        self.car_screen.add.selector(
            title="Make: ",
            items=self.makes,
            onchange=self.set_shape
        )
        # ----
        self.car_screen.add.text_input(title="Year: ")
        self.car_screen.add.label('Car information')
        # ---
        self.car_screen.add.label('Transmission: ')
        self.car_screen.add.label('Engine Size: ')
        self.car_screen.add.label('Total Mass: ')
        self.car_screen.add.label('Total size: ')
        self.car_screen.add.label('Acceleration: ')
        self.car_screen.add.label('Maximum Speed: ')
        self.car_screen.add.label('Total Drag: ')
        # --- play button
        self.car_screen.add.button('Play', self.play_game)

    def set_model(self, selected_value, model):
        self.model = model
    
    def play_game(self):
        self.play = True