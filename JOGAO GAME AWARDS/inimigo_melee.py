from inimigo_base import InimigoBase
import math
import pygame
from typing import Tuple

class InimigoMelee(InimigoBase):
    def __init__(
        self,
        pos: Tuple[int, int],
        vida: int,
        velocidade: float,
        dano: int,
        cooldown: int,
        jogador,
        groups: pygame.sprite.Group
    ) -> None:
        super().__init__("Melee_sprite.png", pos, vida, velocidade, dano, cooldown, jogador, groups)

    def update(self, dt: float) -> None:
        dx = self.jogador.rect.centerx - self.rect.centerx
        dy = self.jogador.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            dx /= distancia
            dy /= distancia
            self.rect.x += dx * self.velocidade
            self.rect.y += dy * self.velocidade

        if self.rect.colliderect(self.jogador.rect):
            self.atacar()

        super().update(dt)

    @property
    def velocidade(self) -> float:
        return self._velocidade

    @velocidade.setter
    def velocidade(self, valor: float) -> None:
        if valor >= 0:
            self._velocidade = valor
