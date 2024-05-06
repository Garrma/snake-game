"""
Question 1° : see Moving_object.compute_position
Question 2° & 3° : see Food.__init__ function & Food.generate_rd_foodtype functions
Question 4° & 5° : see Obstacle class and Game.generate_layout function
Question 6° : see survival mode and surprise (& click on moving obstacles)

SHORT INTRODUCTION :

Welcome to my snake project. I really enjoyed programming this little game and hope you will like it.
Be sure that everything is my own as I have been programming in python intensively during my last 3 internships.
That being said, let's get into the project !!

There are 3 main classes : Screen , Game & Moving object
. Screen is used to generate the global object on which we display and update the game and the
    information all along the game

. Game is used to provide everything related to the rules and how the different levels and type of games are played
    this includes the main function **play() while rules the whole game**

. Moving object is mother class of food, obstacles, snake & Flying_snake. it contains all the attributes & functions
    relative to how to update position of the elements on the grid the effect of the update_position function is
    surcharged depending on the object, wether it is a snake, a flying snake or an obstacle

for snake game only :
depending on the level difficulty from easy to hard, a random number from a certain range (depending on the level
difficulty) is generated. Once the number of obstacles is set, they are set randomly placed on the grid.

***important functions*** :
Moving_object.compute_position : **ANSWERS TO QUESTION 1** and allows snake not to die when hitting the limits of
    the grid
is_game_over(self) : tests all the conditions relative to the game played testing if the game is over or not (ex : snake
    eats tail, ...)
play(self) : contains the step of actions from a game and is the function allowing the game to run
generate_layout(self) : generate the list of obstacles in the game depending on the game type (snake or flappy_snake)
Food.__init__(self) : **ANSWERS TO QUESTION 2** as it generates random type of food with different proba for each type
    of  food

"""

import time
import pygame


from Game.screen import Screen
from Game.game import Game

pygame.init()

#################################################################
############################# SETTINGS ##########################
#################################################################

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (213, 50, 80)
gold = (255, 215, 0)
green = (0, 255, 0)
blue = (50, 153, 213)
purple = (128, 0, 128)
yellow = (255, 255, 0)
orange_red = (255, 69, 0)
dark_green = (0, 155, 0)  # Darker shade for the snake
bright_red = (255, 0, 0)
bright_green = (0, 174, 88)
bright_yellow = (255, 255, 102)
bright_blue = (0, 0, 255)
pink = (255, 102, 178)
grey = (169, 169, 169)
bright_grey = (211, 211, 211)

# Define settings for obstacles
MAX_H = 10  # maximum height for obstacles in terms of blocks
MAX_W = 10

# Set up display (only use to call constructor for global variable my_screen)
dis_width = 1200
dis_height = 800
snake_block = 10

clock = pygame.time.Clock()

# global variables
global_start_time = time.time()
is_layout, is_moving = True, False

#################################################################
############################# LAYOUT ############################
#################################################################

# Functions to set difficulty
def set_game_mode(name, difficulty=None):
    global is_layout, is_moving
    my_game = Game(name)
    if difficulty:
        my_game.set_level(difficulty)

    my_game.set_enable_layout(is_layout)
    my_game.set_moving_layout(is_moving)
    my_game.play()


def switch_layout():
    global is_layout
    is_layout = not is_layout


def switch_moving_layout():
    global is_moving
    is_moving = not is_moving


# setting new screen for the game 
my_screen = Screen(dis_height, dis_width, snake_block)


# Main menu function
def main_menu():
    global is_layout, is_moving

    menu_active = True
    Screen.display_caption("Welcome to Maxime Garriga's version of snake")

    while menu_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        my_screen.reset_screen()

        # display information for obstacles
        my_screen.display_message("Click here to change obstacles settings for snake game", gold, (150, 10))
        my_screen.draw_button('Obstacles :', 150, 40, 200, 40, grey, bright_grey, switch_layout)
        my_screen.display_message(f"{is_layout}", green if is_layout else red, (370, 50))
        my_screen.draw_button('Moving Obstacles :', 150, 100, 200, 40, grey, bright_grey, switch_moving_layout)
        my_screen.display_message(f"{is_moving}", green if is_moving else red, (370, 110))
        my_screen.display_message(f"(Please play with this feature)", white, (430, 110))

        my_screen.display_message("!! Press SPACE in a game to pause & see instructions !!", gold,
                                  (my_screen.get_screen_width() / 3, 250))

        my_screen.display_message("Snake :", white, (70, 320))
        my_screen.draw_button('Easy', 150, 300, 150, 50, green, bright_green, lambda: set_game_mode("snake", "easy"))
        my_screen.draw_button('Medium', 325, 300, 150, 50, blue, bright_blue, lambda: set_game_mode("snake", "medium"))
        my_screen.draw_button('Hard', 500, 300, 150, 50, red, bright_red, lambda: set_game_mode("snake", "hard"))

        my_screen.display_message("Extra games :", white, (10, 470))
        my_screen.draw_button('Survival', 150, 450, 150, 50, yellow, bright_yellow,
                              lambda: set_game_mode("survival"))
        my_screen.draw_button('Surprise', 325, 450, 150, 50, yellow, bright_yellow,
                              lambda: set_game_mode("flappy_snake"))

        Screen.update_screen()


if __name__ == "__main__":
        
    # Call the main menu function
    main_menu()

    # %%