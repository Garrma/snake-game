
from typing import Callable, Union
import time

from settings import *

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
                x = x0 + i * snake_block
                if x > dis_width:
                    x = x % dis_width
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
        block = snake_block
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
        block = snake_block
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

        if headx >= dis_width:  # hits right border
            headx = 0
        elif headx < 0:  # hits left border
            headx = dis_width

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
        block = snake_block
        xpos = round(random.randrange(0, dis_width - width * block) / 10.0) * 10.0
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
        super().__init__((dis_width / 2, my_screen.get_screen_height() / 2), 1, 1, dark_green)
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

        Moving_object.__init__(self, (dis_width / 2, my_screen.get_screen_height() / 2),
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
        default_move_up = -3 * snake_block  # by default any up move will be by 3 times the normal move
        default_move_down = 2 * snake_block

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