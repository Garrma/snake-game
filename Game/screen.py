import pygame

from settings import *


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

    def draw(self,my_game : object):
        raise NotImplementedError("")
    
    @staticmethod
    def update_screen():
        pygame.display.update()

    @staticmethod
    def display_caption(caption):
        """
        display text on top of the window frame
        """
        pygame.display.set_caption(caption)