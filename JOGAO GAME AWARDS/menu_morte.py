from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import sys
from menu_base import MenuBase
from save_ranking import SaveRanking
from typing import List, Dict

if TYPE_CHECKING:
    from jogo import Jogo

class MenuMorte(MenuBase):
    def __init__(self, jogo: Jogo) -> None:
        surface = jogo.display_surface
        largura, altura = surface.get_size()
        labels = ["Menu Principal", "Sair"]
        botoes = self._create_buttons(largura, altura, labels)
        fonte_botoes = pygame.font.Font(None, 50)
        fonte_titulo = pygame.font.Font(None, 70)  # mesmo do MenuPausa por padrão
        super().__init__(surface, botoes, fonte_botoes, titulo="Vírus Eliminado!", fonte_titulo=fonte_titulo)
        self.jogo = jogo

    def _criar_botoes_padrao(self, largura: int, altura: int) -> List[Dict]:
        largura_b, altura_b, esp = 300, 60, 30
        y0 = (altura - (4 * altura_b + 3 * esp)) // 2
        x0 = (largura - largura_b) // 2
        labels = ["Jogar", "Configurações", "Rankings", "Sair"]
        return [
            {
                "rect": pygame.Rect(x0, y0 + i * (altura_b + esp), largura_b, altura_b),
                "texto": labels[i]
            }
            for i in range(4)
        ]

    def on_click(self, pos):
        texto = next((b["texto"] for b in self.botoes if b["rect"].collidepoint(pos)), "")

        if texto in ["Menu Principal", "Sair"]:
            SaveRanking.pedir_nome_e_salvar(self.jogo.display_surface, self.jogo.inimigos_mortos_contagem * 10)

            if texto == "Menu Principal":
                self.jogo.voltar_menu = True
                pygame.event.post(pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE))
            elif texto == "Sair":
                self.jogo.running = False
                pygame.quit()
                sys.exit()