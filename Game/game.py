
from typing import Callable, Union

from Game.movingObject import Flying_snake,Snake,Obstacle
from Game.screen import Screen

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