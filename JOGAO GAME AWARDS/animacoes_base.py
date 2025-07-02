import pygame
from os.path import join
from typing import Tuple, List

class AnimacoesBase(pygame.sprite.Sprite):
    def __init__(
        self,
        nome_arquivo: str,
        pos: Tuple[int, int],
        tamanho_frame: Tuple[int, int] = (32, 32),
        escala: int = 4,
        tempo_animacao: int = 100
    ) -> None:
        super().__init__()

        self._frame_largura, self._frame_altura = tamanho_frame
        self._escala: int = escala
        self._tempo_animacao: int = tempo_animacao
        self._frame_index: int = 0
        self._ultimo_update: int = pygame.time.get_ticks()

        caminho_sprite: str = join("sprites", nome_arquivo)
        sprite_sheet = pygame.image.load(caminho_sprite).convert_alpha()
        largura_sheet, altura_sheet = sprite_sheet.get_size()

        self._colunas: int = largura_sheet // self._frame_largura
        self._linhas: int = altura_sheet // self._frame_altura
        self._total_frames: int = self._colunas * self._linhas

        self._frames: List[pygame.Surface] = []
        for linha in range(self._linhas):
            for coluna in range(self._colunas):
                x = coluna * self._frame_largura
                y = linha * self._frame_altura
                frame = sprite_sheet.subsurface((x, y, self._frame_largura, self._frame_altura))
                novo_tamanho = (self._frame_largura * self._escala, self._frame_altura * self._escala)
                frame_ampliado = pygame.transform.scale(frame, novo_tamanho)
                self._frames.append(frame_ampliado)

        self.image: pygame.Surface = self._frames[self._frame_index]
        self.rect: pygame.Rect = self.image.get_rect(topleft=pos)
        self.mask: pygame.mask.Mask = pygame.mask.from_surface(self.image)

    def update(self) -> None:
        agora = pygame.time.get_ticks()
        if agora - self._ultimo_update >= self._tempo_animacao:
            self._ultimo_update = agora
            self._frame_index = (self._frame_index + 1) % self._total_frames
            self.image = self._frames[self._frame_index]
            self.mask = pygame.mask.from_surface(self.image)

    # Getters e setters
    @property
    def tempo_animacao(self) -> int:
        return self._tempo_animacao

    @tempo_animacao.setter
    def tempo_animacao(self, novo_tempo: int) -> None:
        if novo_tempo > 0:
            self._tempo_animacao = novo_tempo

    @property
    def escala(self) -> int:
        return self._escala

    @escala.setter
    def escala(self, nova_escala: int) -> None:
        if nova_escala > 0:
            self._escala = nova_escala

    @property
    def frame_atual(self) -> int:
        return self._frame_index

    @property
    def total_frames(self) -> int:
        return self._total_frames
