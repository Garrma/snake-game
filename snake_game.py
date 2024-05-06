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

# %%
import pygame
import time
import random
import sys
from typing import Callable, Union

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
######################## MAIN OBJ CLASS #########################
#################################################################


class Screen:
    screen_height: int
    screen_width: int
    block: int
    __screen: pygame.Surface | pygame.SurfaceType = None  # private attribute
    font_size: int = 20
    font_style: pygame.font.SysFont = pygame.font.SysFont("Arial", font_size)
    bg_color: (int, int, int) = black

    def __init__(self, height, width, block):
        self.screen = pygame.display.set_mode((width, height))
        self.screen_height = height
        self.screen_width = width
        self.block = block

    def get_block(self):
        return self.block

    def get_screen_height(self):
        return self.screen_height

    def get_screen_width(self):
        return self.screen_width

    def display_message(self, msg: str, color: (int, int, int), position: (float, float)):
        mesg = self.font_style.render(msg, True, color)
        self.screen.blit(mesg, [position[0], position[1]])

    def reset_screen(self):
        self.screen.fill(self.bg_color)

    def draw_rect(self, display_color, args=(float, float, float, float)):
        """
        display a rectangle on the screen
        :param display_color: color displayed
        :param args: under format (xpos of rectangle, ypos of rectangle, width, height)
        :return:
        """
        pygame.draw.rect(self.screen, display_color, args)

    def draw_button(self, button_text, x, y, w, h, inactive_color, active_color, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            self.draw_rect(active_color, (x, y, w, h))
            if click[0] == 1 and action is not None:
                action()
        else:
            self.draw_rect(inactive_color, (x, y, w, h))

        text_surf = self.font_style.render(button_text, True, black)
        text_rect = text_surf.get_rect()
        text_rect.center = ((x + (w / 2)), (y + (h / 2)))
        self.screen.blit(text_surf, text_rect)

    @staticmethod
    def update_screen():
        pygame.display.update()

    @staticmethod
    def display_caption(caption):
        """
        display text on top of the window frame
        """
        pygame.display.set_caption(caption)


my_screen = Screen(dis_height, dis_width, snake_block)


class Moving_object:
    head: (int, int)
    length: int     # equivalent to width in 2d
    height: int
    color: (int, int, int)
    current_speed: int
    body: list = []
    base_speed: int = 3
    is_blinking: bool = False
    is_invincible: bool = False
    current_direction: (int, int) = (0, 0)
    end_attributes: time.time = None

    def __init__(self, head, height, length, color):
        self.head = head
        self.height = height
        self.length = length
        self.color = color

        self.body = [self.head]
        if length > 1:
            (x0, y) = self.head

            for i in range(1, length):
                # incrementing body of object one block by one block horizontally
                x = x0 + i * my_screen.get_block()
                if x > my_screen.get_screen_width():
                    x = x % my_screen.get_screen_width()
                self.body.append((x, y))

    # getters / setters
    def get_speed(self):
        return self.current_speed

    def get_length(self):
        return self.length

    def get_height(self):
        return self.length

    def get_head(self):
        return self.head

    def get_body(self):
        return self.body

    def get_direction(self):
        return self.current_direction

    def get_end_attributes(self):
        return self.end_attributes

    def get_invincible(self):
        return self.is_invincible

    def set_body(self, body: list[(int, int)]):
        self.body = body

    def set_color(self, color: (int, int, int)):
        self.color = color

    def set_direction(self, direction: (int, int)):
        self.current_direction = direction

    def set_end_attributes(self, end_attribute):
        self.end_attributes = end_attribute

    def update_position(self, position: (int, int)):
        """
        update position of obstacle on the grid, moving the whole body in the same direction simultaneously
        :param position: change of position on x-axis and y-axis due to player move
        :return:
        """
        (headx, heady) = Moving_object.compute_position(self.head, position)

        self.head = (headx, heady)
        self.current_direction = position

        # updating body of the object
        self.body = [self.head] + self.body
        if len(self.body) > self.length:
            del self.body[-1]

    def draw(self, override_color=None):
        """
        draw object within frame
        :param override_color: rgb color in case need to display in specific value
        :return:
        """
        block = my_screen.get_block()
        # 1 -
        display_color = self.color
        if override_color:
            display_color = override_color

        for (xpos, ypos) in self.body:
            if self.height > 1:
                block_height = self.height * block
                my_screen.draw_rect(display_color, (xpos, ypos, block, block_height))
            else:
                my_screen.draw_rect(display_color, (xpos, ypos, block, block))

        return 0

    def draw_blinking(self):
        """

        :return: draw object blinking - 1 frame normal & 1 frame in blink_color
        """
        # if blinking then switch to normal color

        if self.is_blinking:
            blink_color = None
            self.is_blinking = False
        else:
            blink_color = gold
            self.is_blinking = True

        self.draw(override_color=blink_color)

    def reset_attributes(self):
        """
        reset all temporary attributes to standard value
        :return:
        """
        self.is_invincible = False
        self.current_speed = self.base_speed

    def hits_element(self, other_obj) -> bool:
        """
        test if any part of the object hits any part of the second object
        remark : used by snake and food
        :param other_obj: other object of type Moving_object
        :return:
        """
        block = my_screen.get_block()
        for (headx, heady) in self.body:
            for (xpos, ypos) in other_obj.body:
                height = other_obj.height

                ylast = ypos + (height - 1) * block

                if xpos == headx and ypos <= heady <= ylast:
                    return True

            # source of improvement :
            """ 
            when the two objects hitting each other with both 1 block length (on the side they hit each other) 
            or moving in two opposite directions ,they visually hit each other
            but they actually cross witout hitting as one does +10 on the right and the other -10 on the left
            ex T1 : 1 (50,100) vs 2 (60, 100)  & T2 : 1 (60, 100) 2 (50,100)
            """
        return False

    def __str__(self):
        # useful when in debug mode
        header = f"""
        head    :  {self.head}
        height  :  {self.height}
        width   :  {self.length}
        color   :  {self.color}
        """
        body = "body    :  "
        for ele in self.body:
            body += f"{ele}|"

        fulltext = header + body
        return fulltext

    @staticmethod
    def compute_position(position: (int, int), direction: (int, int)) -> (int, int):
        """
        answers to question 1°. Calculate new position of element after receiving new direction and updates it accross
        the map including crossing the limitations and appearing in the other direction
        :param position: position of element in grid
        :param direction: direction applied to the element
        :return: new position in the grid
        """
        # 1° add the feature to appear on the other side

        (headx, heady) = position
        (changex, changey) = direction

        if headx >= my_screen.get_screen_width():  # hits right border
            headx = 0
        elif headx < 0:  # hits left border
            headx = my_screen.get_screen_width()

        if heady >= my_screen.get_screen_height():  # hits top border
            heady = 0
        elif heady < 0:  # hits bottom border
            heady = my_screen.get_screen_height()

        headx += changex
        heady += changey

        return headx, heady

    @staticmethod
    def generate_randomxy(height: int = 1, width: int = 1) -> (int, int):
        """
        generate random coordinates for the upper left corner of a block
        :param height: height of object to generate
        :param width: width of object to generate
        :return: (x,y)
        """
        block = my_screen.get_block()
        xpos = round(random.randrange(0, my_screen.get_screen_width() - width * block) / 10.0) * 10.0
        ypos = round(random.randrange(0, my_screen.get_screen_height() - height * block) / 10.0) * 10.0

        return xpos, ypos


class Obstacle(Moving_object):

    def __init__(self, head, height, length):
        super().__init__(head, height, length, color=orange_red)

    def update_position(self, position: (int, int)):
        """
        update position of obstacle on the grid, moving the whole body in the same direction simultaneously
        :param position: change of position on x-axis and y-axis due to player move
        :return:
        """
        # as object is a rectangle, whole body moves simultaneously
        for i, block in enumerate(self.body):
            self.body[i] = Moving_object.compute_position(self.body[i], position)

        self.head = self.body[0]
        self.current_direction = position


class Food(Moving_object):
    color_name: str
    increment: int = 0
    speed_coeff: float = 1.
    attribute_time: int = None  # nb seconds given by specific type of food

    def __init__(self, color_name=None, override_x=None):
        # if color not set, generate a random color by default
        if not color_name:
            self.color_name = Food.generate_rd_foodtype()
        else:
            self.color_name = color_name

        # generating random position in grid
        (headx, heady) = Moving_object.generate_randomxy()
        if override_x:
            headx = override_x

        super().__init__((headx, heady), 1, 1, None)  # color will be updated below
        self.update_settings()

    def update_settings(self):
        """
        according color of food object, updates settings of rgb, increment and speed
        :return:
        """
        rgb_dict = {
            "blue": blue,  # normal food type
            "purple": purple,  # increase score by 2
            "yellow": yellow,  # increase speed by 2
            "gold": gold,  # make invincible
            "pink": pink  # slow speed by 2
        }

        color = self.color_name
        self.color = rgb_dict[color]

        if color == "blue":
            self.increment = 1
        elif color == "purple":
            self.increment = 2
        elif color == "yellow":
            self.increment = 1
            self.speed_coeff = 2
            self.attribute_time = 5
        elif color == "gold":
            self.is_invincible = True
            self.attribute_time = 6
        elif color == "pink":
            self.speed_coeff = 0.5
            self.attribute_time = 5
        else:
            raise NotImplementedError("Unknown color, please investigate")

    def get_increment(self):
        return self.increment

    def get_speed_coeff(self):
        return self.speed_coeff

    def is_in_layout(self, obstacles: list[Obstacle]) -> bool:
        """
        test that food is not contained within an obstacle
        :param obstacles: list of obstacle constituting layout
        :return: boolean
        """
        if not obstacles or not len(obstacles):
            return False
        return any([self.hits_element(obs) for obs in obstacles])

    @staticmethod
    def generate_rd_foodtype() -> str:
        """
        generate type of food given pre-set probability of appearance
        :return: string of color name
        """
        color_prob = {
            "blue": 0.5,  # normal food type
            "purple": 0.3,  # increase score by 2
            "yellow": 0.2  # increase speed by 2
        }

        random_color = random.choices(list(color_prob.keys()), list(color_prob.values()))[0]
        return random_color


class Snake(Moving_object):

    def __init__(self, speed):
        super().__init__((my_screen.get_screen_width() / 2, my_screen.get_screen_height() / 2), 1, 1, dark_green)
        self.base_speed = speed
        self.current_speed = speed

    def eat_tail(self):
        """
        checks if snake eats own tail and dies
        :return:
        """

        for (x, y) in self.body[1:]:
            if (x, y) == self.head:
                return True

        return False

    def eat_food(self, my_food: Food):
        """
        change parameters of the snake when meets food
        :param my_food: food encountered in game
        :return:
        """

        self.length += my_food.get_increment()
        self.current_speed *= my_food.get_speed_coeff()
        self.is_invincible = my_food.get_invincible()


class Flying_snake(Snake):
    is_going_up: bool = False

    def __init__(self, speed):
        width_snake = 1
        height_snake = 1

        Moving_object.__init__(self, (my_screen.get_screen_width() / 2, my_screen.get_screen_height() / 2),
                               height_snake, width_snake, red)
        self.base_speed = speed
        self.current_speed = speed

    def update_position(self, position: (int, int)):
        """
        update position of obstacle on the grid, moving the whole body in the same direction simultaneously
        remark : after going up, the object stays at same position for one period before starting to fall
        :param position: change of position on x-axis and y-axis due to player move
        :return:
        """
        default_move_up = -3 * my_screen.get_block()  # by default any up move will be by 3 times the normal move
        default_move_down = 2 * my_screen.get_block()

        (movex, movey) = position

        # if move is not UP, apply gravity and make the bird fall
        if movey < 0:
            movey = default_move_up
            self.is_going_up = True
        elif self.is_going_up:
            self.is_going_up = False
            movey = 0
        else:
            movey = default_move_down

        # as object is a rectangle, whole body moves simultaneously
        direction = (0, movey)
        for i, block in enumerate(self.body):
            self.body[i] = Moving_object.compute_position(self.body[i], direction)

        self.head = self.body[0]
        self.current_direction = direction


#################################################################
######################### GAME CLASS ############################
#################################################################


class Game:
    name: str
    level: str = ""
    player: Union[Snake, Flying_snake] = None
    food: Food = None
    game_over: bool = False
    game_on_hold: bool = False
    game_close: int = 0
    layout: list[Obstacle] = None  # list of obstacles in the game
    moving_layout: bool = True
    enable_layout: bool = True

    def __init__(self, name):
        self.name = name
        Screen.display_caption(name)

    def set_level(self, level):
        self.level = level

    def set_enable_layout(self, has_layout):
        self.enable_layout = has_layout

    def set_moving_layout(self, is_layout_moving):
        self.moving_layout = is_layout_moving

    def display_score(self):
        """

        :return: screen
        """
        if self.name == 'snake':
            score = self.player.get_length() - 1
            text = f"Your score: {score}"
        elif self.name == 'survival':
            score = len(self.layout)
            text = f"Obstacles remaining: {score}"
        elif self.name == 'flappy_snake':
            if self.game_close:
                return

            global global_start_time
            score = int(time.time() - global_start_time)
            text = f"Alive for: {score}s"
        else:
            raise NotImplementedError(f"No obstacles generated for game {self.name}")

        if self.player.get_end_attributes():
            current_time = time.time()
            seconds_remaining = int(self.player.get_end_attributes() - current_time)
            boost_text = f"Boost : {seconds_remaining}s"
            my_screen.display_message(boost_text, white, (0, my_screen.font_size))

        my_screen.display_message(text, white, (0, 0))

    def display_instructions(self):
        """
        display instructions corresponding to game mode
        :return:
        """

        def display_paragraph(text, color, position):
            """
            display paragraph in different lines
            """
            (x, y) = position
            lines = text.splitlines()
            for i, l in enumerate(lines):
                my_screen.display_message(l, color, (x, y + my_screen.font_size * i))

        msg = """"""
        if self.name == "survival":
            msg = """INSTRUCTIONS: 
                If you hit the obstacles, you die. 
                However, the gold candy will give you immunity for a limited time. 
                During this time, hit as many obstacles as possible!
                The game ends when no obstacles remain.
                 """
        elif self.name == "snake":
            msg = """ INSTRUCTIONS: 
                The legendary snake game is here ! Eat as much candies as possible to grow. 
                But be careful not to hit any obstacles (if any) or to eat your own tail ! 
                                
                Food : 
                blue : increases length by 1
                purple : increases length by 2
                yellow : multiplies speed by 2 for 5 seconds
                  """
        elif self.name == "flappy_snake":
            msg = """INSTRUCTIONS: 
                Navigate between the walls as long as possible without hitting them.
                You can only go up using the keyboard, gravity will do the rest and bring you down anyway!
                Eating the pink candy will slow down the screen for a limited period. 
                Hope you will like this game called 'flappy snake'!! """
        display_paragraph(msg, white, (my_screen.get_screen_width() / 5, my_screen.get_screen_height() * 0.7))

    def generate_food(self):
        color = None
        override_x = None  # when flappy_snake need to simulate where snake is flying
        if self.name == 'survival':
            color = "gold"
        elif self.name == "flappy_snake":
            color = "pink"
            override_x = my_screen.get_screen_width() / 2

        food = Food(color, override_x)
        while food.is_in_layout(self.layout):
            food = Food(color, override_x)
        self.food = food

    def generate_random_move(self):
        """
        generate random move either vertically or horizontally depending on games rules
        :return: set of move proportional to either (my_screen.get_block(),10) or (my_screen.get_block(),0)
        """
        block = my_screen.get_block()
        if self.name in ['snake', 'survival']:
            up_or_down = random.choices([-1, 1], [0.5, 0.5])[0]
            h_or_v = random.choices([0, 1], [0.5, 0.5])[0]
        elif self.name == 'flappy_snake':
            # only moving from right to left
            up_or_down = -1
            h_or_v = 1
        else:
            raise NotImplementedError(f"No obstacles generated for game {self.name}")

        return block * up_or_down * h_or_v, block * up_or_down * (1 - h_or_v)

    def is_game_over(self) -> int:
        """
        checks if condition in the game is reached and if must end
        :return: 0 if must continue, else int corresponding to reason of end
        """
        game_close = self.game_close
        my_player = self.player

        if any([my_player.hits_element(obs) for obs in self.layout]):
            # if snake is invincible temporarily, cannot die from collision
            if my_player.get_invincible() and self.name == 'survival':
                position_bloc_hit = [my_player.hits_element(obs) for obs in self.layout].index(True)
                del self.layout[position_bloc_hit]
            else:
                game_close = 1

        elif self.name == 'snake':
            if my_player.eat_tail():
                if not my_player.get_invincible():
                    game_close = 2

        elif self.name == 'survival' and len(self.layout) == 0:
            game_close = 3

        elif self.name == "flappy_snake":
            head = my_player.get_head()
            if head[1] >= my_screen.get_screen_height() or head[1] - my_player.get_height() * my_screen.get_block() < 0:
                game_close = 4

        return game_close

    def generate_layout(self):
        """
        depending on game and difficulty, generate obstacles on the map
        for snake : simply rectangles at random locations
        for flappy snake : a wall with a whole in between
        :return:
        """
        if self.name in ['snake', 'survival']:
            if self.name == "survival":
                min_obstacles = 30
                max_obstacles = 40

                nb_obstacles = random.randint(min_obstacles, max_obstacles)
            else:
                # snake game
                if self.level == "easy":
                    min_obstacles = 5
                    max_obstacles = 10
                elif self.level == "medium":
                    min_obstacles = 11
                    max_obstacles = 20
                elif self.level == "hard":
                    min_obstacles = 21
                    max_obstacles = 35
                else:
                    raise NotImplementedError("Please investigate level name")

                nb_obstacles = random.randint(min_obstacles, max_obstacles) if self.enable_layout else 0

            my_obstacles = []
            for i in range(nb_obstacles):
                random_h = random.randint(1, MAX_H)
                random_w = random.randint(1, MAX_W)
                # make sure player is not included in an obstacle at the beginning which would make game stop before it
                # even begins

                (xpos, ypos) = Moving_object.generate_randomxy(random_h, random_w)
                new_obs = Obstacle((xpos, ypos), random_h, random_w)
                if not self.player :
                    raise TimeoutError("Please generate player before layout when playing snake")

                while self.player.hits_element(new_obs):
                    (xpos, ypos) = Moving_object.generate_randomxy(random_h, random_w)
                    new_obs = Obstacle((xpos, ypos), random_h, random_w)

                my_obstacles.append(new_obs)

        elif self.name == 'flappy_snake':
            """
            a wall consit of two blocks 
            1° going from the top to the whole 
            2° going from the bottom of the whole to the floor
            """
            # remark : we need the first wall coming at the player to be opened in the center so we can play
            first_wall = False
            start_positiony = my_screen.get_screen_height() / 2
            start_positionx = my_screen.get_screen_width() / 2

            len_hole = my_screen.get_block() * 20  # pre defining whole between two walls
            number_of_walls = 8

            # partitioning grid width
            # number of blocks remaining once walls displayed
            nb_blocks_remaining = my_screen.get_screen_width() - number_of_walls * my_screen.get_block()
            space_between_walls = nb_blocks_remaining // number_of_walls
            x_locations = [(space_between_walls * i + my_screen.get_block()) for i in range(number_of_walls)]

            # generate random height for whole
            random_generator: Callable[[], int] = lambda: random.randint(1 * my_screen.get_block(),
                                                                         my_screen.get_screen_height() - 1 - len_hole)

            my_obstacles = []
            for wall_location in x_locations:
                if not first_wall:
                    whole_head_position = random_generator()
                else:
                    whole_head_position = start_positiony - 2 * my_screen.get_block()
                    first_wall = False

                if wall_location > start_positionx and not first_wall:
                    first_wall = True

                # top wall
                top_wall_height = whole_head_position // my_screen.get_block()
                top_wall = Obstacle(head=(wall_location, 0), height=top_wall_height, length=1)

                # bottom wall
                bottom_wall_height = (my_screen.get_screen_height() - (
                        whole_head_position + len_hole - 1)) // my_screen.get_block()
                bottom_wall_head = (
                    wall_location, my_screen.get_screen_height() - bottom_wall_height * my_screen.get_block())
                bottom_wall = Obstacle(head=bottom_wall_head, height=bottom_wall_height, length=1)

                top_wall.set_color(green)
                bottom_wall.set_color(green)

                my_obstacles.append(top_wall)
                my_obstacles.append(bottom_wall)
        else:
            raise NotImplementedError(f"No obstacles generated for game {self.name}")

        self.layout = my_obstacles

    def set_direction_for_layout(self):
        nb_obstacles = len(self.layout)
        for i in range(nb_obstacles):
            if self.name == "snake" and not self.moving_layout:
                (movex, movey) = (0, 0)
            else:
                (movex, movey) = self.generate_random_move()
            self.layout[i].set_direction((movex, movey))

    def update_position_for_layout(self):
        nb_obstacles = len(self.layout)
        for i in range(nb_obstacles):
            (movex, movey) = self.layout[i].get_direction()
            self.layout[i].update_position((movex, movey))

    def display_layout_from_obstacles(self):
        obs_list = self.layout
        for obs in obs_list:
            obs.draw()

    def generate_countdown(self):
        """
        display a countdown before elements start moving
        :return:
        """
        # Does not take place in snake game without elements moving
        if self.name == "snake" and (not self.moving_layout or not self.enable_layout):
            return

        countdown_seconds = 4
        current_time = time.time()
        end_time = current_time + countdown_seconds
        my_screen.display_message("Get ready to play and avoid the walls !", white,
                                  (my_screen.get_screen_width() / 3, my_screen.get_screen_height() / 2))

        while time.time() < end_time:
            my_screen.reset_screen()
            self.draw_game()

            current_time = time.time()
            remaining_sec = int(end_time - current_time)
            my_screen.display_message(f"Walls will start moving in {remaining_sec}s", white,
                                      (my_screen.get_screen_width() / 3, my_screen.get_screen_height() * 0.6))

            Screen.update_screen()

    def generate_player(self):
        """
        generate player depending on name of the game played
        :return:
        """
        speed = 15

        if self.name in ["snake", "survival"]:
            if self.name == "survival":
                speed = 20
            elif self.level == "medium":
                speed = 20
            elif self.level == "hard":
                speed = 30

            my_player = Snake(speed)
        elif self.name == "flappy_snake":
            my_player = Flying_snake(speed)
        else:
            raise NotImplementedError(f"No obstacles generated for game {self.name}")

        self.player = my_player

    def draw_game(self):
        my_screen.reset_screen()
        self.food.draw()
        self.player.draw()
        self.display_score()
        self.display_layout_from_obstacles()

    def play(self):
        global global_start_time

        # 0° Initiating
        x1_change = 0
        y1_change = 0
        block = my_screen.get_block()
        global_start_time = time.time()
        start_time_pause = time.time()

        # 1° Generate initial parameters to start the game
        self.generate_player()
        self.generate_layout()
        self.generate_food()
        self.set_direction_for_layout()
        self.draw_game()
        self.generate_countdown()

        # generate food

        while not self.game_over:
            while self.game_close:
                game_close = self.game_close
                my_screen.reset_screen()
                my_screen.display_message("Press Q-Quit or C-Play Again", red,
                                          (my_screen.get_screen_width() / 3, my_screen.get_screen_height() / 2))

                # display reason of game over
                msg = ""
                color = red
                if game_close == 1:
                    msg = "You lost by hitting an obstacle !"
                elif game_close == 2:
                    msg = "You lost by hitting your tail !"
                elif game_close == 3:
                    msg = "You won the survival mode !"
                    color = green
                elif game_close == 4:
                    msg = "You lost by hitting the limitations !"

                my_screen.display_message(msg, color,
                                          (my_screen.get_screen_width() / 3, my_screen.get_screen_height() / 3))
                self.display_score()
                Screen.update_screen()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            self.game_over = True
                            self.game_close = 0
                        if event.key == pygame.K_c:
                            main_menu()

            while self.game_on_hold:
                self.draw_game()
                my_screen.display_message("Press M-Menu or SPACE-resume", red,
                                          (my_screen.get_screen_width() / 3, my_screen.get_screen_height() / 3))
                self.display_instructions()
                Screen.update_screen()

                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.game_on_hold = False

                            # if had boost, update time
                            end_attributes = self.player.get_end_attributes()
                            if end_attributes:
                                end_attributes += time.time() - start_time_pause
                                self.player.set_end_attributes(end_attributes)

                            global_start_time += (time.time() - start_time_pause)

                        if event.key == pygame.K_m:
                            self.game_close = 0
                            self.game_on_hold = False
                            main_menu()

            # 3 ° getting commands
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_over = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.game_on_hold = True
                        start_time_pause = time.time()
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_KP4:
                        x1_change = -block
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_KP6:
                        x1_change = block
                        y1_change = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_KP8:
                        y1_change = -block
                        x1_change = 0
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_KP2:
                        y1_change = block
                        x1_change = 0

            # 4° updating position on the grid
            self.player.update_position((x1_change, y1_change))

            if self.name == 'flappy_snake':
                # reset coordinates to stop object from pursuing its move
                x1_change, y1_change = 0, 0

            # 5 ° updating position of the obstacles
            self.update_position_for_layout()

            # 6 ° testing if games ended due to new position
            self.game_close = self.is_game_over()

            # 7° display new elements
            self.draw_game()

            if self.player.hits_element(self.food):
                # change attributes of snake
                self.player.eat_food(self.food)

                # check if food given temporary attributes
                if self.food.attribute_time:
                    end_attributes = self.player.get_end_attributes()
                    start_attributes = time.time() if not end_attributes else end_attributes
                    self.player.set_end_attributes(start_attributes + self.food.attribute_time)

                # generate new position for food
                self.generate_food()

            # go to next iteration
            clock.tick(self.player.get_speed())

            # check bonus for limited time only
            end_attributes = self.player.get_end_attributes()
            if end_attributes and time.time() > end_attributes:
                self.player.set_end_attributes(None)
                self.player.reset_attributes()
            elif end_attributes and time.time() <= end_attributes:
                # still affected by food
                self.player.draw_blinking()

            # display
            Screen.update_screen()

        pygame.quit()
        quit()


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


# Call the main menu function
main_menu()

# %%
