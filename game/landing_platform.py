import pygame
from constants import *

class LandingPlatform:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 10
    
    def draw(self, screen):
        pygame.draw.rect(screen, PLATFORM_COLOR,
                        (self.x - self.width/2,
                         self.y - self.height/2,
                         self.width,
                         self.height)) 