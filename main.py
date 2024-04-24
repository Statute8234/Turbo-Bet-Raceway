import pygame
import numpy as np
import random, sys, math, time
pygame.init()
current_time = time.time()
random.seed(current_time)
# Seting up the display
WIDTH, HEIGHT = 700, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Race Game")
clock = pygame.time.Clock()
# color
def random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GRAY = (128,128,128)
DARK_GRAY = (169,169,169)
Cyan = (0,255,255)
DIM_GRAY = (105,105,105)
GOLD = (255,215,0)
# button
class Button:
    def __init__(self, x, y, width, height, text, active_color, inactive_color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.color = self.inactive_color
        self.textColor = BLACK
        self.font_size = min(self.width // len(self.text) + 10, self.height)
        self.font = pygame.font.Font(None, self.font_size)
        self.clicked = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 2)
        text_surface = self.font.render(self.text, True, self.textColor)
        text_rect = text_surface.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        if self.x < mouse_pos[0] < self.x + self.width and self.y < mouse_pos[1] < self.y + self.height:
            self.color = self.active_color
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.clicked = True
                    self.color = self.active_color
        else:
            self.color = self.inactive_color
    def reset(self):
        self.clicked = False
        self.color = self.inactive_color
startButton = Button((WIDTH / 2) - 55, (HEIGHT / 2) - 55, 100, 100, "Play", RED, BLACK)
buttonWidth = (WIDTH / 2) - 55
back = Button(buttonWidth - 120, HEIGHT - 120, 100, 100, "Back", RED, BLACK)
placeBet = Button(buttonWidth, HEIGHT - 120, 100, 100, "Bet", RED, GOLD)
placeBet.textColor = GOLD
nextButton = Button(buttonWidth + 120, HEIGHT - 120, 100, 100, "Next", RED, BLACK)

# coins
class Coins:
    def __init__(self, x, y, width, height, image_path):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.original_image = pygame.image.load(image_path).convert_alpha()
    
    def scaleImage(self):
        self.original_image = pygame.transform.scale(self.original_image, (self.width, self.height))

    def draw(self):
        self.scaleImage()
        screen.blit(self.original_image, (self.x, self.y))

# flag
class Flag:
    def __init__(self, x, y, width, height, colors = []):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colors = random.sample(colors, 4)
        self.type = random.choice(['horizontal', 'vertical'])
        self.symbol = random.choice(['star', 'circle', 'triangle', 'none'])
        self.symbol_color = random.choice(self.colors)
        self.coins = 0 # lagest number 5
        self.coinsList = []

    def add_coins(self, num_coins):
        # This function will be called to add coins to the flag
        start_x = (self.x + (len(self.coinsList) * 20) + 3) # Start right of the flag
        start_y = self.y + 40
        for i in range(num_coins):
            new_coin = Coins(start_x, start_y + i * 25, 20, 20, 'coin.png')
            self.coinsList.append(new_coin)

    def drawCoins(self):
        for coin in self.coinsList:
            coin.draw()
            
    def draw(self, screen):
        block_size = self.height // 3 if self.type == 'horizontal' else self.width // 3
        for i in range(3):
            color = self.colors[i]
            if self.type == 'horizontal':
                pygame.draw.rect(screen, color, (self.x, self.y + i * block_size, self.width, block_size))
            else:
                pygame.draw.rect(screen, color, (self.x + i * block_size, self.y, block_size, self.height))
        # Add a symbol if needed
        symbol_size = min(self.width, self.height) // 7

        # Add a symbol if needed
        center_x, center_y = self.x + self.width // 2, self.y + self.height // 2
        if self.symbol == 'star':
            pygame.draw.polygon(screen, self.symbol_color, self.calculate_star_points(center_x, center_y, 5, symbol_size, symbol_size // 2))
        elif self.symbol == 'circle':
            pygame.draw.circle(screen, self.symbol_color, (center_x, center_y), symbol_size)
        elif self.symbol == 'triangle':
            self.point1 = (self.width // 6) - 10
            self.point2 = (self.height // 6) - 5
            self.draw_triangle(screen, self.symbol_color, (center_x - self.point1, center_y + self.point2), (center_x, center_y - self.point2), (center_x + self.point1, center_y + self.point2))
        self.drawCoins()

    def draw_triangle(self, screen, color, point1, point2, point3):
        pygame.draw.polygon(screen, color, [point1, point2, point3])

    def calculate_star_points(self, center_x, center_y, points, outer_radius, inner_radius):
        # Calculate the points of a star
        step = 2 * math.pi / points
        points_list = []
        angle = 0
        for i in range(points * 2):
            radius = outer_radius if i % 2 == 0 else inner_radius
            x = center_x + int(math.cos(angle) * radius)
            y = center_y - int(math.sin(angle) * radius)
            points_list.append((x, y))
            angle += step / 2
        return points_list

# car images
class  CarImage:
    def __init__(self, x, y, width, height, color, image_path, flag):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.associatedFlag = flag

    def change_image_color(self, image):
        colored_image = pygame.Surface(image.get_size())
        colored_image.fill(self.color)
        colored_image.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return colored_image

    def scaleImage(self):
        self.colored_image = self.change_image_color(self.original_image).convert_alpha()
        background_color = self.colored_image.get_at((0, 0))
        self.colored_image.set_colorkey(background_color)
        self.colored_image = pygame.transform.scale(self.colored_image, (self.width, self.height))

    def draw(self):
        self.scaleImage()
        screen.blit(self.colored_image, (self.x, self.y))

# car portfolio
class CarPortfolio:
    def __init__(self, x, y, width, height, flag, image_path, colors=[]):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.colors = colors
        self.flag = flag
        self.flag.x = 0
        self.flag.y = 0
        self.flag.width = WIDTH + 1
        self.flag.height = HEIGHT + 1
        # Initialize flag dimensions outside of this class or pass them directly.
        self.carPortfolioList = []
        for color in self.colors:
            original_image = pygame.image.load(image_path).convert_alpha()
            colored_image = self.change_image_color(original_image, color)
            scaled_image = self.scaleImage(colored_image)
            circle_image = self.convertImage_circle(scaled_image)
            self.carPortfolioList.append(circle_image)

    def scaleImage(self, image):
        """ Scale the colored image. """
        return pygame.transform.scale(image, (self.width, self.height))
    
    def change_image_color(self, image, color):
        """ Apply a color filter to the image. """
        colored_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        colored_image.fill(color)  # Fill with the desired color
        colored_image.blit(image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return colored_image
    
    def convertImage_circle(self, image):
        """ Create a circular mask and apply it to the scaled image. """
        mask = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (self.width // 2, self.height // 2), min(self.width, self.height) // 2)
        image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        return image
    
    def draw(self, screen):
        """ Draw the circular car image and the flag on the screen. """
        # Draw the flag if it has a draw method
        if hasattr(self.flag, 'draw'):
            self.flag.draw(screen)
        # Draw the circular car image
        for idx, car_image in enumerate(self.carPortfolioList):
            screen.blit(car_image, (self.x, (self.y + idx * 100) - 400))
# image
flagList = []
carList = []
for y in range(6):
    flag = Flag(WIDTH - 100, (y * 100) + 100, 90, 60, [random_color(), random_color(), random_color(), random_color()])
    carImage = CarImage(WIDTH - 100, (y * 100) + 30, 100, 100, random_color(), r'car.png', flag)
    flagList.append(flag)
    carList.append(carImage)

# car port
flag = Flag(WIDTH - 100, (y * 100) + 100, 90, 60, [random_color(), random_color(), random_color(), random_color()])
carPortfolio = CarPortfolio(0, HEIGHT - 200, 100, 100, flag, r"carPortfolio_Image.png", [random_color(), random_color(), random_color(), random_color(), random_color()])

# check winner
def check_winner(cars):
    for car in cars:
        if car.x <= 10:
            return car
    return None

# This is running the game loop
show_carPortfolio = True
play = False
start_race = False
finished = False
race_reset = False
winner = None
# loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
        if show_carPortfolio:
            back.handle_event(event)
            placeBet.handle_event(event)
            nextButton.handle_event(event)
        if play:
            startButton.handle_event(event)
            if startButton.clicked:
                startButton.reset()
                play = False
    screen.fill(WHITE)
    if play:
        startButton.draw(screen)
    # draw function
    for flag in flagList:
        flag.draw(screen)
    for carImage in carList:
        carImage.draw()
    # draw
    if show_carPortfolio:
        carPortfolio.draw(screen)
        back.draw(screen)
        placeBet.draw(screen)
        nextButton.draw(screen)
    # Update game state
    if not show_carPortfolio:
        if not play and not start_race:
            start_race = True
            race_reset = True
            finished = False
            winner = None
        # Reset car positions
        if race_reset:
            for car in carList:
                car.x = WIDTH - 100
            race_reset = False
        # Move cars
        if start_race and not finished:
            for car in carList:
                if car.x > 10:
                    car.x -= random.randint(0, 1)
                winner = check_winner(carList)
                if winner:
                    if car.x <= 10:
                        car.associatedFlag.add_coins(1)
                    finished = True
        # finished
        if finished:
            play = True
            start_race = False
            race_reset = False
        # Display "Winner!" next to the winning car
        if winner:
            font = pygame.font.Font(None, 40)
            winner_text = font.render("Winner!", True, BLACK)
            screen.blit(winner_text, (winner.x, winner.y))
    # This is to update the scene
    clock.tick(64)
    pygame.display.flip()
    pygame.display.update()