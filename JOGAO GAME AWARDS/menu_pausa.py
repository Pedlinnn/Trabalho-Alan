from __future__ import annotations
from typing import TYPE_CHECKING
import sys
import pygame
from menu_base import MenuBase
from save_ranking import SaveRanking
from configuracoes import Configuracoes

if TYPE_CHECKING:
    from jogo import Jogo

class MenuPausa(MenuBase):
    def __init__(self, jogo: Jogo) -> None:
        surface = jogo.display_surface
        largura, altura = surface.get_size()
        labels = ["Continuar", "Configurações", "Menu Principal", "Sair do Jogo"]
        botoes = self._create_buttons(largura, altura, labels)
        super().__init__(surface, botoes, pygame.font.Font(None, 50))
        self.jogo = jogo
        self.ativo = True

    def _create_buttons(self, w, h, labels):
        largura_b, altura_b, esp = 300, 60, 30
        y0 = (h - (len(labels)*altura_b + (len(labels)-1)*esp)) // 2
        x0 = (w - largura_b) // 2
        return [{"rect": pygame.Rect(x0, y0 + i*(altura_b+esp), largura_b, altura_b), "texto": labels[i]} for i in range(len(labels))]

    def on_click(self, pos):
        texto = next((b["texto"] for b in self.botoes if b["rect"].collidepoint(pos)), "")
        if texto == "Continuar":
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))  # força sair do loop base
        elif texto == "Configurações":
            Configuracoes(self.jogo.display_surface, self.jogo.config, self.jogo.som).run()
        elif texto == "Menu Principal":
            SaveRanking.salvar(self.jogo)
            self.jogo.voltar_menu = True
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
        elif texto == "Sair do Jogo":
            self.jogo.running = False
            self.jogo.voltar_menu = False
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
