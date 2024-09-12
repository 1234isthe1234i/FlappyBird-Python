from __future__ import annotations
import pygame
from pygame.locals import *
from random import randint


FPS = 60


class Bird:
    def __init__(self, screen: pygame.Surface):
        self.bird: pygame.Surface = pygame.transform.scale(pygame.image.load("images/bird.png"), (100,56))
        self.x_pos = screen.get_width()*0.2
        self.y_pos = screen.get_height()*0.5
        self.width = 52
        self.height = 36
        self.vel = 0

    def key_pressed(self): 
        self.vel = 12

    def move(self) -> bool:
        self.y_pos -= self.vel
        self.vel -= 1 if self.vel > -12 else 0

        if self.y_pos <= 0:
            return False
        
        if self.y_pos + self.bird.get_height()*0.8>= 700:
            
            return False
        
        return True
    
    def reset(self, screen: pygame.Surface):
        self.__init__(screen)
    
    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x_pos+22, self.y_pos+9, self.width, self.height)


class Pipes:
    def __init__(self, screen: pygame.Surface, game_imgs: dict[str, pygame.Surface]):
        self.width = game_imgs['up_pipe'].get_width()
        self.height = game_imgs['up_pipe'].get_height()
        self.up_pipe = [screen.get_width(), randint(350, int(screen.get_height() * 0.7))]
        self.down_pipe = [screen.get_width(), self.up_pipe[1] - 200 - self.height]
        self.game_imgs = game_imgs
        self.screen = screen
    
    def display_pipes(self):
        self.screen.blit(self.game_imgs['up_pipe'], self.up_pipe)
        self.screen.blit(self.game_imgs['down_pipe'], self.down_pipe)

    def move_pipes(self):
        self.up_pipe[0] -= 5
        self.down_pipe[0] -= 5

    def get_rects(self):
        return (pygame.Rect(*self.up_pipe, self.width, self.height), pygame.Rect(*self.down_pipe, self.width, self.height))


class Game:
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont("Times New Roman", 50)
        self.screen = pygame.display.set_mode((1000, 800))
        self.clock = pygame.time.Clock()
        self.bird = Bird(self.screen)
        self.game_imgs: dict[str, pygame.Surface] = {"up_pipe": pygame.transform.scale(pygame.image.load("images/pipe.png"), (100, 579)),
                                                     "down_pipe": pygame.transform.scale(pygame.image.load("images/reverse_pipe.png"), (100,579)),
                                                     "background": pygame.transform.scale(pygame.image.load("images/background.jpg"), (1000, 700)),
                                                     "base": pygame.transform.scale(pygame.image.load("images/base.png"), (1000, 100))
                                                    }
        self.pipes: list[Pipes] = []
        self.pipes.append(Pipes(self.screen, self.game_imgs))
        self.score = 0
        play = True 
        while play:
            play = self.game_loop()
            self.bird.reset(self.screen)

    
    def game_loop(self):
        game_start = False
        play_again_t = self.font.render("Play Again", 0,'red', 'black')
        play_again_r = play_again_t.get_rect()
        play_again_r[0], play_again_r[1] = self.screen.get_width()/2 - play_again_r[2]/2, self.screen.get_height()*0.6
        

        self.screen.blit(self.game_imgs['background'], (0,0,1000,700))
        self.screen.blit(self.game_imgs['base'], (0,700,1000,100))
        self.screen.blit(self.bird.bird, (self.bird.x_pos, self.bird.y_pos, 100, 100))
        for pipe in self.pipes: pipe.display_pipes()
        pygame.display.flip()

        while not game_start:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key in [K_SPACE, K_UP, K_w]:
                        game_start = True
                        self.bird.key_pressed()

        self.screen.fill((0,0,0))
        
        while game_start:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    exit()
                if event.type == KEYDOWN:
                    if event.key in [K_SPACE, K_UP, K_w]:
                        self.bird.key_pressed()

            
            self.screen.blit(self.game_imgs['background'], (0,0,1000,700))
            self.screen.blit(self.game_imgs['base'], (0,700,1000,100))
            self.screen.blit(self.bird.bird, (self.bird.x_pos, self.bird.y_pos, 100, 100))
            

            for pipe in self.pipes:
                pipe.display_pipes()
                pipe.move_pipes()
                if pipe.up_pipe[0] == 600:
                    self.pipes.append(Pipes(self.screen, self.game_imgs))
                if pipe.up_pipe[0] + pipe.width <= 0:
                    self.pipes.remove(pipe)
                if pipe.up_pipe[0] == 255:
                    self.score += 1
                
            score_t = self.font.render(str(self.score), 0, (0, 0, 0))
            score_r = score_t.get_rect()
            score_r[0] += 20
            self.screen.blit(score_t, score_r)
            
            game_start = (not self.game_over()) and self.bird.move()

            pygame.display.flip()
            self.clock.tick(FPS)

        self.screen.fill('red')
        self.screen.blit(play_again_t, play_again_r)
        pygame.display.flip()
        while not game_start:
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pygame.quit()
                    exit()
                if event.type == MOUSEBUTTONDOWN:
                    if play_again_r.collidepoint(*event.pos):
                        self.pipes = [Pipes(self.screen, self.game_imgs)]
                        self.score = 0 
                        return True
    def game_over(self):
        for pipes in self.pipes:
            for pipe in pipes.get_rects():
                if pipe.colliderect(self.bird.get_rect()):
                    return True
        return False
        



if __name__ == '__main__':
    flappy_bird = Game()
