import pygame
import math

players_list = pygame.sprite.Group()
class Players(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image_path):
        super().__init__()
        self.x, self.y = x, y
        self.image_path = image_path
        self.original_image = pygame.image.load(image_path)
        self.original_image = pygame.transform.scale(self.original_image, (width, height))
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft = (self.x, self.y))
        self.angle = 0
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.1
        self.deceleration = 0.05
        self.angular_velocity = 0
        self.max_angular_velocity = 3
        self.angular_acceleration = 0.2
        self.angular_deceleration = 0.1

    def draw(self, screen):
        screen.blit(self.image, self.rect.center)
    
    def movment(self):
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_w]:
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        elif user_input[pygame.K_s]:
            self.speed = max(self.speed - self.acceleration, -self.max_speed / 2)
        else:
            if self.speed > 0:
                self.speed = max(self.speed - self.deceleration, 0)
            elif self.speed < 0:
                self.speed = min(self.speed + self.deceleration, 0)
        # rotation
        if user_input[pygame.K_a]:
            self.angular_velocity = min(self.angular_velocity + self.angular_acceleration, self.max_angular_velocity)
        elif user_input[pygame.K_d]:
            self.angular_velocity = max(self.angular_velocity - self.angular_acceleration, -self.max_angular_velocity)
        else:
            if self.angular_velocity > 0:
                self.angular_velocity = max(self.angular_velocity - self.angular_deceleration, 0)
            elif self.angular_velocity < 0:
                self.angular_velocity = min(self.angular_velocity + self.angular_deceleration, 0)
        self.angle += self.angular_velocity
        self.angle %= 360
        # calculate new position
        rad_angle = math.radians(self.angle)
        self.x += self.speed * math.sin(rad_angle)
        self.y -= self.speed * math.cos(rad_angle)
        # update
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(topleft=(self.x,self.y))
    
    def update(self):
        self.movment()