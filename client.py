import pygame
import random, sys, math, time
import socket
import pickle
# ---
import menuFile, game_sprites
# screen
pygame.init()
current_time = time.time()
random.seed(current_time)
# Setting up the display
screenWidth, screenHeight = 700, 700
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption("Game")
clock = pygame.time.Clock()
# server
SERVER = "localhost"
PORT = 5555
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
# main menu
main_menu = menuFile.MainMenu(screen, screenWidth, screenHeight)
player_screen = menuFile.CreatePlayer(screen, screenWidth, screenHeight)

def on_resize() -> None:
    window_size = screen.get_size()
    new_w, new_h = window_size[0], window_size[1]
    main_menu.main_menu.resize(new_w, new_h)
    main_menu.settings_screen.resize(new_w, new_h)
    player_screen.flag_screen.resize(new_w, new_h)
    player_screen.car_screen.resize(new_w, new_h)

testPlayer = game_sprites.Players(300,300,125,100,r"Topdown_vehicle_sprites_pack_Unluckystudio\Topdown_vehicle_sprites_pack\Audi.png")
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
        screen.fill((255, 255, 255))
        # menu
        if not (main_menu.singlePlayer or main_menu.multiplayer):
            main_menu.main_menu.update(events)
            main_menu.main_menu.draw(screen)
        if not player_screen.play:
            if main_menu.singlePlayer:
                player_screen.menu.update(events)
                player_screen.menu.draw(screen)
        else:
            testPlayer.draw(screen)
            testPlayer.update()
        # This is to update the scene
        clock.tick(64)
        pygame.display.flip()
        pygame.display.update()

# loop
if __name__ == "__main__":
    main()