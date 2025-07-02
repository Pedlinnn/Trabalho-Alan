import pygame
import sys
from typing import List, Dict
from menu_base import MenuBase
from configuracoes import Configuracoes
from sons import Sons
from save_ranking import SaveRanking

class MenuPrincipal(MenuBase):
    def __init__(self, surface: pygame.Surface, som: Sons, config: dict) -> None:
        largura, altura = surface.get_size()
        botoes = self._criar_botoes_padrao(largura, altura)
        fonte = pygame.font.Font(None, 50)
        super().__init__(
            surface,
            botoes,
            fonte,
            titulo="Nao_e_virus.exe",
            fonte_titulo=pygame.font.Font(None, 70)
        )
        self.som = som
        self.config = config
        self.proximo_estado = None
        self._deve_sair = False

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

    def on_click(self, pos: tuple[int, int]) -> None:
        for botao in self.botoes:
            if botao["rect"].collidepoint(pos):
                texto = botao["texto"]
                if texto == "Jogar":
                    self._abrir_submenu_jogar()
                elif texto == "Configurações":
                    self._abrir_configuracoes()
                elif texto == "Rankings":
                    resultado = SaveRanking.mostrar(self.surface)
                    if resultado == "sair":
                        self.proximo_estado = "sair"
                        self._deve_sair = True
                elif texto == "Sair":
                    self.proximo_estado = "sair"
                    self._deve_sair = True

    def _abrir_submenu_jogar(self) -> None:
        from sub_menu_jogar import SubMenuJogar
        submenu = SubMenuJogar(self.surface, self.som, self.config)
        submenu.run()

        if self.config.get("estado_proximo") == "jogar":
            self.proximo_estado = "jogar"
            self._deve_sair = True
            self.config.pop("estado_proximo", None)

    def _abrir_configuracoes(self) -> None:
        configuracoes = Configuracoes(self.surface, self.config, self.som)
        configuracoes.run()

    def run(self) -> None:
        self._deve_sair = False
        while not self._deve_sair:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self._deve_sair = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.on_click(event.pos)

            self.surface.fill((0, 0, 0))
            self.desenhar_fundo_escuro()
            self.desenhar_titulo()
            self.desenhar_botoes()
            pygame.display.flip()
            self.clock.tick(60)
