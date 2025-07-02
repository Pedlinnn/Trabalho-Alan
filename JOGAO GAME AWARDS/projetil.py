import pygame
from os.path import join
from os import walk
import random 
import math

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, destino_x, destino_y, dano):
        super().__init__()

        self._dano = dano    
        self._x = x
        self._y = y
        self.velocidade = 7
        self.raio = 5

        try:
            self.image = pygame.image.load("sprites/projetil.png")
            self.image = pygame.transform.scale(self.image, (50, 50))
        except:
            print(f"Erro ao carregar a imagem do projetil")
            self.image = pygame.Surface((self.raio * 2, self.raio * 2), pygame.SRCALPHA)

        dx = destino_x - x
        dy = destino_y - y
        distancia = math.hypot(dx, dy)

        if distancia == 0:
            self.direcao = pygame.Vector2(0, 0)
        else:
            self.direcao = pygame.Vector2(dx, dy).normalize()

        self.rect = pygame.Rect(self.x, self.y, self.raio * 2, self.raio * 2)

    @property
    def x(self) -> None:
        return self._x

    @x.setter
    def x(self, valor: int) -> None:
        self._x = float(valor)
        self.rect.centerx = int(self._x)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, valor):
        self._y = float(valor)
        self.rect.centery = int(self._y)

    @property
    def dano(self):
        return self._dano

    @dano.setter
    def dano(self, valor):
        self._dano = valor
    
    @property
    def direcao_x(self):
        return self.direcao.x

    @property
    def direcao_y(self):
        return self.direcao.y

    def atualizar(self):
        self.x += self.velocidade * self.direcao.x
        self.y += self.velocidade * self.direcao.y
        self.rect.topleft = (int(self.x), int(self.y))

    def desenhar(self, surface: pygame.Surface):
        pygame.draw.rect(surface, (255, 255, 0), (int(self.x), int(self.y), 10, 10))