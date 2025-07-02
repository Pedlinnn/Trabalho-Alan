import sys
import pygame
from typing import List, Dict
from menu_base import MenuBase
from sons import Sons
from save_ranking import SaveRanking

class SubMenuJogar(MenuBase):
    def __init__(self, surface: pygame.Surface, som: Sons, config: dict) -> None:
        largura, altura = surface.get_size()
        labels = ["Novo Jogo", "Continuar", "Voltar"]
        botoes = self._criar_botoes(largura, altura, labels)
        super().__init__(surface, botoes, pygame.font.Font(None, 50), titulo="Jogar")
        self.som = som
        self.config = config
        self._deve_voltar = False

    def _criar_botoes(self, largura: int, altura: int, labels: List[str]) -> List[Dict]:
        largura_b, altura_b, esp = 300, 60, 30
        y0 = (altura - (len(labels) * altura_b + (len(labels) - 1) * esp)) // 2
        x0 = (largura - largura_b) // 2
        return [
            {"rect": pygame.Rect(x0, y0 + i*(altura_b+esp), largura_b, altura_b), 
             "texto": labels[i]} 
            for i in range(len(labels))
        ]

    def on_click(self, pos: tuple[int, int]) -> None:
        """Lida com cliques nos botões do submenu"""
        for botao in self.botoes:
            if botao["rect"].collidepoint(pos):
                texto = botao["texto"]
                if texto == "Novo Jogo":
                    self._iniciar_novo_jogo()
                elif texto == "Continuar":
                    self._continuar_jogo()
                elif texto == "Voltar":
                    self._deve_voltar = True

    def _iniciar_novo_jogo(self) -> None:
        self.config["continuar"] = {}
        self._deve_voltar = True
        self.config["estado_proximo"] = "jogar"

    def _continuar_jogo(self) -> None:
        dados = SaveRanking.carregar()
        if isinstance(dados, dict) and all(k in dados for k in ("player", "wave", "inimigos_mortos")):
            self.config["continuar"] = dados
            self.config["estado_proximo"] = "jogar"
            self._deve_voltar = True
        else:
            print("Nenhum jogo salvo encontrado ou arquivo corrompido.")

    def run(self) -> None:
        """Executa o loop do submenu"""
        self._deve_voltar = False
        while not self._deve_voltar:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self._deve_voltar = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.on_click(event.pos)
            
            # Renderização
            self.surface.fill((0, 0, 0))
            self.desenhar_fundo_escuro()
            self.desenhar_titulo()
            self.desenhar_botoes()
            pygame.display.flip()
            self.clock.tick(60)