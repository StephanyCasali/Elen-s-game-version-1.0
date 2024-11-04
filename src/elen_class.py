import pygame
from pygame.locals import *
from random import randint
from abc import ABC, abstractmethod
import time

class Entity(ABC):
    def __init__(self, x: int, y: int, image: str) -> None:
        self.x: int = x
        self.y: int = y
        self.image: str = image

    @abstractmethod
    def draw(self, scren):
        pass

class Player(Entity):
    def __init__(self, x: int, y: int, image: str) -> None:
        super().__init__(x, y, image)
    
    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            self.x -= 10
        if keys[K_d] or keys[K_RIGHT]:
            self.x += 10
        if keys[K_w] or keys[K_UP]:
            self.y -= 10
        if keys[K_s] or keys[K_DOWN]:
            self.y += 10
        
        if self.x < 0:
            self.x = 0
        if self.x > 900 - 105:
            self.x = 900 - 105
        if self.y < 0:
            self.y = 0
        if self.y > 700 - 110:
            self.y = 700 - 110
        
class Puddle(Entity):
    def __init__(self, x: int, y: int, image: str) -> None:
        super().__init__(x, y, image)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Key(Entity):
    def __init__(self, x: int, y: int, image: str) -> None:
        super().__init__(x, y, image)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

class Button:
    def __init__(self, x: float, y: float, width:float, height: float, text:str, font:str, color_normal, color_hover, text_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.text = text
        self.font = font
        self.text_color = text_color
        self.hovered = False

    def draw(self, screen):
        color = self.color_hover if self.hovered else self.color_normal
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        if self.hovered and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return True
        return False

class Welcome_screen():
        
    def __init__(self, size: tuple, initial_number_of_puddles: float, keys_needed:float, initial_number_of_lifes:float, running: bool, clock):
        self.size = size
        self.width, self.height = size
        self.initial_number_of_puddles = initial_number_of_puddles
        self.keys_needed=keys_needed
        self.initial_number_of_lifes = initial_number_of_lifes
        self._running= running
        self.clock = clock
        self.screen = pygame.display.set_mode(self.size)
        self.display = pygame.display.set_caption("Help Elen!!!")
        self.button_width, self.button_height = 200, 60
        self.bar_width, self.bar_height = 400, 25
        self.blackadder_font = pygame.font.Font("../assets/blackadder-itc.ttf", 40)
        
    def execute(self):
        self.display
        loading_message = self.blackadder_font.render("Help Elen!!", True, (255, 255, 255))
        self.button_width = 200
        self.button_height = 60
        dict_of_button = {}
        dict_of_button["button_start"]= Button(self.width//2 - self.button_width//4+70, self.height//2, self.button_width, self.button_height,\
                          "Start", self.blackadder_font, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_settings"]= Button(self.width//2 - self.button_width-50, self.height//2, self.button_width, self.button_height,\
                          "Settings", self.blackadder_font, (255,255,255),(255,25,25), (0,0,0))
        
        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(loading_message, (self.width // 2 - loading_message.get_width() // 2, self.height // 2 - 50))
            for key in dict_of_button:
                dict_of_button[key].draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    for key in dict_of_button:
                        dict_of_button[key].check_hover(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_start"].is_clicked(event):
                    running = False 
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_settings"].is_clicked(event):
                    running = False 
                    return 1

        pygame.time.Clock().tick(30)

    def run(self):
        pygame.init()
        welcome = True
        while welcome:
            if self.execute() == 1:
                settings = True
                while settings:
                    option = self.seting_screen()
                    if option == 1 or option == 2 or option == 3 or option == 4:
                        self.initial_number_of_puddles,self.initial_number_of_lifes,self.keys_needed=self.options(option)
                        settings = True
                    else:
                        settings = False
                    if not self._running:
                        return self._running
            else:
                welcome = False
            if not self._running:
                return self._running
        if not self._running:
            return self._running
        self.show_loading_screen()
        return self._running, self.initial_number_of_puddles,self.initial_number_of_lifes,self.keys_needed

    def show_loading_screen(self):
        self.screen
        self.display
        loading_message = self.blackadder_font.render("Carregando... Por favor, aguarde.", True, (255, 255, 255))

        self.screen.fill((0, 0, 0))
        self.screen.blit(loading_message, (self.width//2 - loading_message.get_width()//2, self.height//2 - 50))

        bar_x, bar_y = (self.width - self.bar_width) // 2, (self.height // 2) + 10  

        for i in range(self.bar_width):
            pygame.draw.rect(self.screen, (255, 255, 255), (bar_x, bar_y, i, self.bar_height))
            pygame.display.flip()
            pygame.time.delay(5)

        time.sleep(2)

    def seting_screen(self):
        self.screen 
        self.display
        loading_message = self.blackadder_font.render(f"Number of puddles = {self.initial_number_of_puddles}, Number of keys = {self.keys_needed}, "
                                                 +f"Number of lifes = {self.initial_number_of_lifes}", True, (255, 255, 255))

        button_width, button_height = 300, 60
        dict_of_button = {}
        dict_of_button["button_number_of_puddles"]=Button(self.width//2 - button_width//4+70, self.height//2 - 100, button_width, button_height,\
                          "number_of_puddles", self.blackadder_font, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_number_of_lifes"]=Button(self.width//2 - button_width-50, self.height//2 - 100, button_width, button_height,\
                          "number_of_lifes", self.blackadder_font, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_number_of_keys"]=Button(self.width//2 - button_width//4+70, self.height//2, button_width, button_height,\
                          "number_of_keys", self.blackadder_font, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_back"]=Button(self.width//2 - button_width-50, self.height//2, button_width, button_height,\
                          "back", self.blackadder_font, (255,255,255),(255,25,25), (0,0,0))
        self.clock = pygame.time.Clock()

        running = True
        while running:
            self.screen.fill((0, 0, 0))
            for key in dict_of_button:
                dict_of_button[key].draw(self.screen)
            self.screen.blit(loading_message, (self.width // 2 - loading_message.get_width() // 2, self.height // 2 - 200))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    running = False
                    return 0
                elif event.type == pygame.MOUSEMOTION:
                    for key in dict_of_button:
                        dict_of_button[key].check_hover(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_number_of_puddles"].is_clicked(event):
                    running = False
                    return 1
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_number_of_lifes"].is_clicked(event):
                    running = False
                    return 2
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_number_of_keys"].is_clicked(event):
                    running = False
                    return 3
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_back"].is_clicked(event):
                    running = False
                    return 0
        pygame.time.Clock().tick(30)
    
    def options(self, option):
        self.screen
        self.display
        self.button_width, self.button_height = 300, 60
        dict_of_button = {}
        dict_of_button["button_easy"] =Button(self.width//2 - self.button_width-50, self.height//2 - 100, self.button_width, self.button_height,\
                          "Easy", self.blackadder_font, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_normal"]=Button(self.width//2 - self.button_width//4+70, self.height//2 - 100, self.button_width, self.button_height,\
                          "Normal", self.blackadder_font, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_hard"]=Button(self.width//2 - self.button_width-50, self.height//2, self.button_width, self.button_height,\
                          "Hard", self.blackadder_font, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_hardcore"]=Button(self.width//2 - self.button_width//4 +70, self.height//2, self.button_width, self.button_height,\
                          "Hardcore", self.blackadder_font, (255,255,255),(255,25,25), (0,0,0))
        dict_of_button["button_back"]=Button(self.width//2 - self.button_width + 100, self.height//2 + 100, self.button_width, self.button_height,\
                          "Back", self.blackadder_font, (255,255,255),(255,25,25), (0,0,0))
        self.clock = pygame.time.Clock()

        running = True
        while running:
            self.screen.fill((0, 0, 0))
            for key in dict_of_button:
                dict_of_button[key].draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    running = False
                elif event.type == pygame.MOUSEMOTION:
                    for key in dict_of_button:
                        dict_of_button[key].check_hover(event.pos)
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_easy"].is_clicked(event):
                    if option == 1:
                        self.initial_number_of_puddles = 1
                    elif option == 2:
                        self.initial_number_of_lifes = 10
                    elif option == 3:
                        self.keys_needed=5
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_normal"].is_clicked(event):
                    if option == 1:
                        self.initial_number_of_puddles = 2
                    elif option == 2:
                        self.initial_number_of_lifes = 5
                    elif option == 3:
                        self.keys_needed = 10
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_hard"].is_clicked(event):
                    if option == 1:
                        self.initial_number_of_puddles = 3
                    elif option == 2:
                        self.initial_number_of_lifes = 2
                    elif option == 3:
                        self.keys_needed= 15
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_hardcore"].is_clicked(event):
                    if option == 1:
                        self.initial_number_of_puddles = 5
                    elif option == 2:
                        self.initial_number_of_lifes = 1
                    elif option == 3:
                        self.keys_needed= 20
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and dict_of_button["button_back"].is_clicked(event):
                    running = False
        pygame.time.Clock().tick(30)
        return self.initial_number_of_puddles,self.initial_number_of_lifes,self.keys_needed