from inimigo_base import InimigoBase
from projetil_inimigo import ProjetilInimigo
import pygame
import random
import math
from typing import Tuple

class InimigoRanged(InimigoBase):
    def __init__(
        self,
        pos: Tuple[int, int],
        vida: int,
        velocidade: float,
        dano: int,
        cooldown: int,
        jogador,
        groups: pygame.sprite.Group,
        grupo_projeteis_jogador: pygame.sprite.Group,
        distancia_ideal: int = 400
    ) -> None:
        super().__init__("Ranged_sprite.png", pos, vida, velocidade, dano, cooldown, jogador, groups)

        self._distancia_ideal = distancia_ideal
        self._grupo_projeteis_jogador = grupo_projeteis_jogador
        self._projeteis = pygame.sprite.Group()

        self._ultimo_teleporte = 0
        self._cooldown_teleporte = 3000

    def atacar(self) -> None:
        if self.pode_atacar():
            origem_x, origem_y = self.rect.center
            destino_x, destino_y = self.jogador.rect.center
            novo_proj = ProjetilInimigo(origem_x, origem_y, destino_x, destino_y, self.dano)
            self._projeteis.add(novo_proj)
            self.ultimo_ataque = pygame.time.get_ticks()

    def update(self, dt: float) -> None:
        agora = pygame.time.get_ticks()

        for proj in self._grupo_projeteis_jogador:
            proj.update(dt)

        self.tentar_teleportar()
        self._projeteis.update(dt)

        dx = self.jogador.rect.centerx - self.rect.centerx
        dy = self.jogador.rect.centery - self.rect.centery
        distancia = math.hypot(dx, dy)

        if distancia > 0:
            dx /= distancia
            dy /= distancia

            if distancia < self._distancia_ideal - 10:
                self.rect.x -= dx * self.velocidade
                self.rect.y -= dy * self.velocidade
            elif distancia > self._distancia_ideal + 10:
                self.rect.x += dx * self.velocidade
                self.rect.y += dy * self.velocidade

        if self.pode_atacar():
            self.atacar()

        super().update(dt)

    def tentar_teleportar(self) -> None:
        agora = pygame.time.get_ticks()
        if agora - self._ultimo_teleporte < self._cooldown_teleporte:
            return

        for proj in self._grupo_projeteis_jogador:
            if self.rect.colliderect(proj.rect.inflate(20, 20)):
                print("    >> PROJETIL PERTO! Tentando teleportar...")

                direcao = -1 if proj.rect.centerx > self.rect.centerx else 1
                distancia_teleporte = 120
                novo_x = self.rect.centerx + direcao * distancia_teleporte
                novo_x = max(0, min(1280 - self.rect.width, novo_x))

                self.rect.centerx = novo_x
                self._ultimo_teleporte = agora
                print(f"    >> TELEPORTOU para {self.rect.centerx}")
                break

    def desenhar_projeteis(self, surface: pygame.Surface) -> None:
        self._projeteis.draw(surface)

    @property
    def distancia_ideal(self) -> int:
        return self._distancia_ideal

    @distancia_ideal.setter
    def distancia_ideal(self, valor: int) -> None:
        if valor > 0:
            self._distancia_ideal = valor

    @property
    def cooldown_teleporte(self) -> int:
        return self._cooldown_teleporte

    @cooldown_teleporte.setter
    def cooldown_teleporte(self, valor: int) -> None:
        if valor >= 0:
            self._cooldown_teleporte = valor

    @property
    def projeteis(self) -> pygame.sprite.Group:
        return self._projeteis

    @property
    def grupo_projeteis_jogador(self) -> pygame.sprite.Group:
        return self._grupo_projeteis_jogador
