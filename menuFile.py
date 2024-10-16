import pygame
import pygame_menu
from pygame_menu import themes
import random
import random, sys, math, time
import pandas as pd
import pygame_menu.locals
current_time = time.time()
random.seed(current_time)

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
        self.flag_color_1 = self.random_color()
        self.flag_color_2 = self.random_color()
        self.symbol_color = self.random_color()
        self.pattern = 'Stripes'
        self.shape = 'Circle'
        self.shape_size = 50
        self.shape_position = (self.width // 2, self.height // 2)
        self.userNumber = random.randint(0, sys.maxsize)
        self.makes = []
        self.models = []
        self.selected_make = None
        self.selected_model = None
        self.car_data = None
        self.play = False
        self.create_main()
    
    def create_main(self):
        self.menu = pygame_menu.Menu('Create Your Player', self.width, self.height, theme=pygame_menu.themes.THEME_DEFAULT)
        self.inputWidth, self.inputHeight = self.width // 2, 100

        try:
            flag_frame = self.menu.add.frame_v(width=self.inputWidth, height=self.inputHeight, padding=0)
            flag_frame.pack(self.menu.add.text_input("Country Name: ", onchange=self.set_country_name, input_underline_len=1, maxchar=15))
            
            color_frame = flag_frame.pack(self.menu.add.frame_v(width=self.inputWidth, height=self.inputHeight))
            color_frame.pack(self.menu.add.color_input("Flag 1 ", default=self.flag_color_1, onchange=self.set_flag_color_1, color_type='rgb', input_underline_len=1))
        
            color_frame.pack(self.menu.add.color_input("Flag 2 ", default=self.flag_color_2, onchange=self.set_flag_color_2, color_type='rgb', input_underline_len=1))
            color_frame.pack(self.menu.add.color_input("Symbol ", default=self.symbol_color, onchange=self.set_symbol_color, color_type='rgb', input_underline_len=1))

            controls_frame = flag_frame.pack(self.menu.add.frame_h(width=self.inputWidth, height=self.inputHeight))
            controls_frame.pack(self.menu.add.toggle_switch('Pattern', ['Stripes', 'Solid', 'Checker'], onchange=self.set_pattern))
            controls_frame.pack(self.menu.add.toggle_switch('Shape', ['Circle', 'Square', 'Star'], onchange=self.set_shape))
            controls_frame.pack(self.menu.add.range_slider('Size', default=self.shape_size, range_values=(10, 100), onchange=self.set_shape_size))
            controls_frame.pack(self.menu.add.range_slider('X', default=self.shape_position[0], range_values=(0, self.width), onchange=self.set_shape_position_x))
            controls_frame.pack(self.menu.add.range_slider('Y', default=self.shape_position[1], range_values=(0, self.height), onchange=self.set_shape_position_y))

            # Car creation section
            car_frame = self.menu.add.frame_v(width=self.inputWidth, height=self.inputHeight, padding=0)
            car_frame.pack(self.menu.add.label('Create Your Car', font_size=24))
            car_frame.pack(self.menu.add.label(f'User Number: {self.userNumber}'))
            car_frame.pack(self.menu.add.image(r"CarPortfolio\carPortfolio_Image.png", scale=(0.5, 0.5)))

            car_color_frame = car_frame.pack(self.menu.add.frame_h(width=self.inputWidth, height=self.inputHeight))
            car_color_frame.pack(self.menu.add.color_input("Car Color", default=self.random_color(), input_underline_len=1))
            car_color_frame.pack(self.menu.add.color_input("Interior", default=self.random_color(), input_underline_len=1))

            self.make_modelsList()
            car_frame.pack(self.menu.add.selector("Make: ", items=self.makes, onchange=self.set_make))
            self.model_selector = car_frame.pack(self.menu.add.selector("Model: ", items=self.models, onchange=self.set_model))
            car_frame.pack(self.menu.add.text_input("Year: ", input_underline_len=4, maxchar=4))

            info_frame = car_frame.pack(self.menu.add.frame_v(width=self.inputWidth, height=self.inputHeight))
            info_frame.pack(self.menu.add.label('Car Information', font_size=20))
            self.transmission_label = info_frame.pack(self.menu.add.label('Transmission: '))
            self.engine_label = info_frame.pack(self.menu.add.label('Engine Size: '))
            self.mass_label = info_frame.pack(self.menu.add.label('Total Mass: '))
            self.size_label = info_frame.pack(self.menu.add.label('Total Size: '))
            self.speed_label = info_frame.pack(self.menu.add.label('Maximum Speed: '))
            self.drag_label = info_frame.pack(self.menu.add.label('Total Drag: '))
        except:
            self.menu.add.button('Play', self.play_game)
        
    def random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def set_country_name(self, value):
        self.country_name = value

    def set_flag_color_1(self, color):
        self.flag_color_1 = color
        self.draw_flag()

    def set_flag_color_2(self, color):
        self.flag_color_2 = color
        self.draw_flag()

    def set_symbol_color(self, color):
        self.symbol_color = color
        self.draw_flag()

    def set_pattern(self, pattern):
        self.pattern = pattern
        self.draw_flag()

    def set_shape(self, shape):
        self.shape = shape
        self.draw_flag()

    def set_shape_size(self, size):
        self.shape_size = int(size)
        self.draw_flag()

    def set_shape_position_x(self, x):
        self.shape_position = (int(x), self.shape_position[1])
        self.draw_flag()

    def set_shape_position_y(self, y):
        self.shape_position = (self.shape_position[0], int(y))
        self.draw_flag()

    def draw_shape(self, surface):
        if self.shape == 'Circle':
            pygame.draw.circle(surface, self.symbol_color, self.shape_position, self.shape_size)
        elif self.shape == 'Square':
            rect = pygame.Rect(0, 0, self.shape_size * 2, self.shape_size * 2)
            rect.center = self.shape_position
            pygame.draw.rect(surface, self.symbol_color, rect)
        elif self.shape == 'Star':
            self.draw_star(surface, self.shape_position, self.shape_size, 5, self.symbol_color)

    def draw_star(self, surface, position, size, points, color):
        x, y = position
        point_list = []
        angle_step = 360 / points
        for i in range(points * 2):
            angle = i * angle_step / 2
            radius = size if i % 2 == 0 else size // 2
            radian_angle = math.radians(angle)
            point_x = x + int(math.cos(radian_angle) * radius)
            point_y = y + int(math.sin(radian_angle) * radius)
            point_list.append((point_x, point_y))
        pygame.draw.polygon(surface, color, point_list)

    def draw_flag(self):
        flag_surface = pygame.Surface((self.width // 2, self.height // 2))
        flag_rect = flag_surface.get_rect()

        if self.pattern == 'Stripes':
            pygame.draw.rect(flag_surface, self.flag_color_1, flag_rect)
            pygame.draw.rect(flag_surface, self.flag_color_2, pygame.Rect(0, flag_rect.height // 2, flag_rect.width, flag_rect.height // 2))
        elif self.pattern == 'Solid':
            pygame.draw.rect(flag_surface, self.flag_color_1, flag_rect)
        elif self.pattern == 'Checker':
            checker_size = flag_rect.width // 2
            pygame.draw.rect(flag_surface, self.flag_color_1, pygame.Rect(0, 0, checker_size, checker_size))
            pygame.draw.rect(flag_surface, self.flag_color_2, pygame.Rect(checker_size, 0, checker_size, checker_size))
            pygame.draw.rect(flag_surface, self.flag_color_2, pygame.Rect(0, checker_size, checker_size, checker_size))
            pygame.draw.rect(flag_surface, self.flag_color_1, pygame.Rect(checker_size, checker_size, checker_size, checker_size))

        self.draw_shape(flag_surface)
        
        self.screen.blit(flag_surface, (self.width // 4, self.height // 4))
        pygame.display.flip()

    def make_modelsList(self):
        data = pd.read_csv('dataFiles/car_db_metric.csv', header=0, usecols=['make', 'model'])
        self.makes = sorted(data['make'].unique().tolist())
        self.models = sorted(data['model'].unique().tolist())

    def set_make(self, selected_value, make):
        self.selected_make = make
        self.update_model_list(make)

    def set_model(self, selected_value, model):
        self.selected_model = model
        self.update_car_info()

    def update_model_list(self, make):
        data = pd.read_csv('dataFiles/car_db_metric.csv', header=0, usecols=['make', 'model'])
        filtered_data = data[data['make'] == make]
        self.models = sorted(filtered_data['model'].unique().tolist())
        self.model_selector.update_items(self.models)

    def update_car_info(self):
        # Implement this method to update car information labels
        # based on the selected make and model
        pass

    def play_game(self):
        self.play = True

    def run(self):
        self.draw_flag()
        self.menu.mainloop(self.screen)
        return (self.play, self.country_name, self.flag_color_1, self.flag_color_2, 
                self.symbol_color, self.pattern, self.shape, self.shape_size, 
                self.shape_position, self.selected_make, self.selected_model)
