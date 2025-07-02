from animacoes_base import *
import pygame
from os.path import join
from arma import Arma
from raio import Raio
WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720

class Jogador(AnimacoesBase):
    def __init__(self, pos, groups, save=None):
        super().__init__("Virus_sprite.png", pos)
        self.add(groups)

        self._direction = pygame.Vector2()
        self._speed = 300
        self.arma_normal = Arma()
        self.arma_raio = Raio()

        self._vida_maxima = 100
        self._vida = self._vida_maxima
        self._invulneravel = False
        self._invuln_tempo = 1000
        self._ultimo_dano = 0

        self._pode_usar_raio = False
         # garantir que o save funcione corretamente
        if save:
            self.vida_maxima = save.get("vida_maxima", 100)
            self.vida = save.get("vida", self._vida_maxima)
            self.rect.x, self.rect.y = save.get("pos", pos)
            self.arma_normal.dano = save.get("arma_dano", self.arma_normal.dano)
            self.arma_normal.intervalo = save.get("intervalo_arma", self.arma_normal.intervalo)
            self.pode_usar_raio = save.get("pode_usar_raio", False)

    def input(self)-> None:
        keys = pygame.key.get_pressed()
        self._direction.x = int(keys[pygame.K_d]) - int(keys[pygame.K_a])
        self._direction.y = int(keys[pygame.K_s]) - int(keys[pygame.K_w])
        if self._direction.length() != 0:
            self._direction = self._direction.normalize()

    def mover(self, dt)-> None:
        deslocamento = self._direction * self._speed * dt
        self.rect.x += deslocamento.x
        self.rect.y += deslocamento.y

        # Limita dentro da tela
        # Garante que o jogador fique dentro da tela:
        # Se ultrapassar alguma borda (esquerda, direita, topo ou fundo),
        # a posição do retângulo (rect) é ajustada para o limite correspondente.
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT

    def levar_dano(self, dano)-> None:
        agora = pygame.time.get_ticks()
        if not self._invulneravel:
            self._vida -= dano
            self._invulneravel = True
            self._ultimo_dano = agora

        if self._vida <= 0:
            print("Jogador morreu!")  # Substituir por tela de morte

    def update(self, dt)-> None:
        self.input()
        self.mover(dt)
        super().update()  # Atualiza animação da base

        if self._invulneravel:
            agora = pygame.time.get_ticks()
            if agora - self._ultimo_dano >= self._invuln_tempo:
                self._invulneravel = False

    # -------- Getters e setters --------
    @property
    def vida(self)-> int:
        return self._vida

    @vida.setter
    def vida(self, valor)-> None:
        self._vida = max(0, min(valor, self._vida_maxima))

    @property
    def vida_maxima(self)-> int:
        return self._vida_maxima

    @vida_maxima.setter
    def vida_maxima(self, valor)-> None:
        if valor > 0:
            self._vida_maxima = valor
            self._vida = min(self._vida, self._vida_maxima)

    @property
    def pode_usar_raio(self)-> bool:
        return self._pode_usar_raio

    @pode_usar_raio.setter
    def pode_usar_raio(self, valor)-> None:
        self._pode_usar_raio = bool(valor)

    @property
    def speed(self)-> float:
        return self._speed

    @speed.setter
    def speed(self, valor)->None:
        if valor >= 0:
            self._speed = valor

    @property
    def invulneravel(self)-> bool:
        return self._invulneravel
