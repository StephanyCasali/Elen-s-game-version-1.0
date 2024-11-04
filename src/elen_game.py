import pygame
from pygame.locals import *
import pygame.font
from random import randint
import elen_auxiliary as ex
import elen_class as ec

class ElenGame:
    def __init__(self):
        self._running = True
        self.size = self.weight, self.height = 900, 700
        self.screen = None
        self.clock = None
        self.font = None
        self.points: int = 0
        self.initial_number_of_lifes: int = 5
        self.lifes: int = self.initial_number_of_lifes
        self.message: str = " "
        self.message2: str = " "
        self.message3: str = " "
        self.image_set = {
            "normal": ex.get_images("../assets/normal.png", (105, 110)),
            "happy": ex.get_images("../assets/happy.png", (105, 110)),
            "angry": ex.get_images("../assets/angry.png", (105, 110)),
            "died": ex.get_images("../assets/died.png", (105, 110)),
            "scared": ex.get_images("../assets/scared.png", (105, 110))
        }
        self.player: ec.Player = ec.Player(round(self.weight/2)-52, round(self.height/2)-55, self.image_set["normal"])
        self.initial_number_of_puddles: int = 2
        self.number_of_puddles: float = self.initial_number_of_puddles
        self.puddle: list[ec.Entity] = []
        self.key: ec.Entity = None
        self.keys_needed: float = 10
        self.angry_time: float = 0
        self.happy_time: float = 0

    def on_init(self):
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self._running,self.initial_number_of_puddles,self.initial_number_of_lifes,self.keys_needed = \
            ec.Welcome_screen(self.size, self.initial_number_of_puddles, self.keys_needed, \
                              self.initial_number_of_lifes, self._running, self.clock).run()
        self.number_of_puddles=self.initial_number_of_puddles
        self.lifes = self.initial_number_of_lifes
        if not self._running:
            return
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Help Elen!!!")
        self.font = pygame.font.Font("../assets/blackadder-itc.ttf", 40)
        self.respawn_puddle_and_key()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False
        if event.type == KEYDOWN:
            if event.key == K_r:
                self.reset_game()

    def on_loop(self):
        self.player.move() 

        for puddle in self.puddle:
            if ex.check_collision_circle(self.player, puddle, 5, 70):
                self.player.image = self.image_set["angry"]
                self.lifes -= 1
                self.angry_time = 15
                self.respawn_puddle_and_key()
        
        if ex.check_collision(self.player, (100, 90), self.key, (20,30)):
            self.player.image = self.image_set["happy"]
            self.points += 1
            self.happy_time = 15
            self.number_of_puddles += 0.5
            if self.number_of_puddles > 18:
                self.number_of_puddles = 18
            self.respawn_puddle_and_key()

        self.update_image_state()
        self.check_game_over()

    def respawn_puddle_and_key(self):
        puddle_image = ex.get_images("../assets/puddle.png", (120, 90))
        key_image = ex.get_images("../assets/key.png", (40,50))

        self.puddle = []
        for _ in range(round(self.number_of_puddles)):
            while True:
                x = randint(0, self.weight - 90)
                y = randint(0, self.height - 90)
                if ex.position_is_free(x, y, self.puddle, 85, 85) and ex.position_is_free(x,y, [self.player], 105,110):
                    self.puddle.append(ec.Puddle(x, y, puddle_image))
                    break

        while True:
            x = randint(0, self.weight - 40)
            y = randint(0, self.height - 50)
            if ex.position_is_free(x, y, self.puddle, 90, 90):
                self.key = ec.Key(x, y, key_image)
                break

    def reset_player_position(self):
        while True:
            x = randint(0, self.weight - 105)  
            y = randint(0, self.height - 110)  
            if ex.position_is_free(x, y, self.puddle, 110, 110) and ex.position_is_free(x, y, [self.key], 40, 50):
                self.player.x = x
                self.player.y = y
                break

    def update_image_state(self):
        if self.lifes == 1:
            self.player.image = self.image_set["scared"]
        if self.points >= self.keys_needed and self.lifes > 0:
            self.message2 = "You helped Elen!!!!!"
            self.player.image = self.image_set["happy"]
            self.check_game_over()
        if self.lifes < 1:
            self.message2 = "You killed Elen :("
            self.player.image = self.image_set["died"]
        if self.angry_time > 0:
            self.angry_time -= 1
        elif self.happy_time > 0:
            self.happy_time -= 1
        elif self.lifes > 1 and self.points <= self.keys_needed:
            self.player.image = self.image_set["normal"]

    def on_render(self):
        self.screen.fill((30, 30, 30))
        self.player.draw(self.screen)
        for puddle in self.puddle:
            puddle.draw(self.screen)
        self.key.draw(self.screen)

        if self.points >= self.keys_needed and self.lifes > 0:
            self.screen.fill((30, 30, 30))
            self.player = ec.Player(round(self.weight/2)-52, round(self.height/2)-55, self.image_set["happy"])
            self.player.draw(self.screen)
            self.confete = ec.Key(0,0, ex.get_images("../assets/confete.png", (self.weight, self.height)))
            self.confete.draw(self.screen)

        if self.lifes < 1:
            self.screen.fill((30, 30, 30))
            self.player = ec.Player(round(self.weight/2)-52, round(self.height/2)-55, self.image_set["died"])
            self.player.draw(self.screen)
            
        self.mensagem = f'Help Elen to get her Keys: {self.points} of {self.keys_needed}      Lifes: {self.lifes}'
        
        formatted_text = self.font.render(self.mensagem, False, (255, 255, 255))
        formatted_text2 = self.font.render(self.message2, False, (255, 255, 255))
        formatted_text3 = self.font.render(self.message3, False, (255, 255, 255))

        
        self.screen.blit(formatted_text, (50, 50))
        self.screen.blit(formatted_text2, (80, 100))
        self.screen.blit(formatted_text3, (80, 150))

        pygame.display.update()

    def check_game_over(self):
        if self.lifes <= 0:
            self.message3 = "Game Over! Press R to Restart"
        if self.points >= self.keys_needed:
            self.message3 = "Game Win! Press R to Restart"
        if pygame.key.get_pressed()[K_r]:
            self.reset_game()

    def reset_game(self):
        self.points = 0
        self.lifes = self.initial_number_of_lifes
        self.player.image = self.image_set["normal"]
        self.message2 = " "
        self.message3 = " "
        self.player = ec.Player(round(self.weight/2)-52, round(self.height/2)-55, self.image_set["normal"])
        self.number_of_puddles = self.initial_number_of_puddles
        self.puddle: list[ec.Entity] = []
        self.key = None
        self.angry_time = 0
        self.happy_time = 0
        self.respawn_puddle_and_key()
        self.reset_player_position()

    def on_cleanup(self):
        pygame.quit()
 
    def run(self):
        if self.on_init() == False:
            self._running = False
 
        while(self._running):
            for event in pygame.event.get():
                self.on_event(event)
            if not self._running:
                break
            self.on_loop()
            self.on_render()
            self.clock.tick(30)
            if not self._running:
                break
        self.on_cleanup()

if __name__ == "__main__":
    app = ElenGame()
    app.run()