import pygame
import math
from typing import Union

class ProjetilInimigo(pygame.sprite.Sprite):
    def __init__(
        self,
        origem_x: int,
        origem_y: int,
        destino_x: int,
        destino_y: int,
        dano: int = 10,
        velocidade: Union[int, float] = 200
    ) -> None:
        super().__init__()

        imagem_original: pygame.Surface = pygame.image.load("sprites/bullet_enemy.png").convert_alpha()
        novo_tamanho = (60, 60)
        self.image: pygame.Surface = pygame.transform.scale(imagem_original, novo_tamanho)
        self.rect: pygame.Rect = self.image.get_rect(center=(origem_x, origem_y))
        self.mask: pygame.mask.Mask = pygame.mask.from_surface(self.image)

        self._dano: int = dano
        self._velocidade: float = velocidade

        dx: float = destino_x - origem_x
        dy: float = destino_y - origem_y
        distancia: float = math.hypot(dx, dy)

        if distancia == 0:
            self._direcao: pygame.Vector2 = pygame.Vector2(0, 0)
        else:
            self._direcao = pygame.Vector2(dx / distancia, dy / distancia)

    def update(self, dt: float) -> None:
        deslocamento = self._direcao * self._velocidade * dt
        self.rect.x += deslocamento.x
        self.rect.y += deslocamento.y

        if not pygame.display.get_surface().get_rect().colliderect(self.rect):
            self.kill()

    # Getters e Setters
    @property
    def dano(self) -> int:
        return self._dano

    @dano.setter
    def dano(self, valor: int) -> None:
        self._dano = max(0, valor)

    @property
    def velocidade(self) -> float:
        return self._velocidade

    @velocidade.setter
    def velocidade(self, valor: float) -> None:
        if valor >= 0:
            self._velocidade = valor

    @property
    def direcao(self) -> pygame.Vector2:
        return self._direcao

    @direcao.setter
    def direcao(self, vetor: pygame.Vector2) -> None:
        if isinstance(vetor, pygame.Vector2):
            self._direcao = vetor
