from animacoes_base import *
from jogador import Jogador
import pygame
from typing import Tuple

class InimigoBase(AnimacoesBase):
    def __init__(
        self,
        sprite_path: str,
        pos: Tuple[int, int],
        vida: int,
        velocidade: float,
        dano: int,
        cooldown: int,
        jogador: Jogador,
        groups: pygame.sprite.Group
    ) -> None:
        super().__init__(sprite_path, pos)
        self.add(groups)

        self._vida = vida
        self._velocidade = velocidade
        self._dano = dano
        self._cooldown = cooldown
        self.ultimo_ataque = 0
        self._jogador = jogador
        self._contabilizado = False

    # -------- Getters e Setters --------
    @property
    def vida(self) -> int:
        return self._vida

    @vida.setter
    def vida(self, valor: int) -> None:
        self._vida = max(0, valor)

    @property
    def velocidade(self) -> float:
        return self._velocidade

    @velocidade.setter
    def velocidade(self, valor: float) -> None:
        self._velocidade = max(0, valor)

    @property
    def dano(self) -> int:
        return self._dano

    @dano.setter
    def dano(self, valor: int) -> None:
        self._dano = max(0, valor)

    @property
    def cooldown(self) -> int:
        return self._cooldown

    @cooldown.setter
    def cooldown(self, valor: int) -> None:
        self._cooldown = max(0, valor)

    @property
    def posicao(self) -> Tuple[int, int]:
        return self.rect.topleft

    @posicao.setter
    def posicao(self, valor: Tuple[int, int]) -> None:
        self.rect.topleft = valor

    @property
    def jogador(self) -> Jogador:
        return self._jogador

    @property
    def contabilizado(self) -> bool:
        return self._contabilizado

    @contabilizado.setter
    def contabilizado(self, valor: bool) -> None:
        self._contabilizado = bool(valor)

    def pode_atacar(self) -> bool:
        agora = pygame.time.get_ticks()
        return agora - self.ultimo_ataque >= self.cooldown

    def atacar(self) -> None:
        if self.pode_atacar():
            self._jogador.levar_dano(self.dano)
            self.ultimo_ataque = pygame.time.get_ticks()

    def update(self, dt: float) -> None:
        if self.vida <= 0 and self.alive():
            print(f"{self.__class__.__name__} morreu!")
            self.kill()
            return

        super().update()
