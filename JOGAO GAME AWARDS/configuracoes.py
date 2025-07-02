import pygame
from typing import Dict, List
from menu_base import MenuBase

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

class Configuracoes(MenuBase):
    def __init__(self, surface: pygame.Surface, config: Dict, sons) -> None:
        self.config = config
        self.sons = sons

        largura, altura = surface.get_size()
        fonte = pygame.font.Font(None, 50)
        botoes = self._criar_botoes(largura, altura)

        super().__init__(surface, botoes, fonte, titulo="Configurações")
        self.fonte = fonte  # necessário para desenhar os sliders

        # Sliders
        self.slider_largura = 300
        self.slider_altura = 10
        self.slider_musica_pos = (WINDOW_WIDTH // 2 - self.slider_largura // 2, 250)
        self.slider_sfx_pos = (WINDOW_WIDTH // 2 - self.slider_largura // 2, 350)

        self.musica_valor = config.get("volume_musica", 0.5)
        self.sfx_valor = config.get("volume_efeitos", 0.5)

        self.arrastando_musica = False
        self.arrastando_sfx = False

        self._deve_voltar = False

    def _criar_botoes(self, largura: int, altura: int) -> List[Dict]:
        largura_b, altura_b, esp = 300, 60, 30
        x = (largura - largura_b) // 2
        y = 500
        return [{"rect": pygame.Rect(x, y, largura_b, altura_b), "texto": "Voltar"}]

    def desenhar_slider(self, pos: tuple[int, int], valor: float, texto: str) -> None:
        pygame.draw.rect(self.surface, (100, 100, 100), (*pos, self.slider_largura, self.slider_altura))
        preenchimento = int(valor * self.slider_largura)
        pygame.draw.rect(self.surface, (0, 200, 0), (*pos, preenchimento, self.slider_altura))
        circulo_x = pos[0] + preenchimento
        circulo_y = pos[1] + self.slider_altura // 2
        pygame.draw.circle(self.surface, (255, 255, 255), (circulo_x, circulo_y), 12)

        label = self.fonte.render(f"{texto}: {int(valor * 100)}%", True, (255, 255, 255))
        self.surface.blit(label, (pos[0], pos[1] - 40))

    def lidar_slider(self, evento: pygame.event.Event, pos_slider: tuple[int, int], arrastando: bool) -> tuple[bool, float | None]:
        if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
            mouse_x, mouse_y = evento.pos
            x, y = pos_slider
            if x <= mouse_x <= x + self.slider_largura and y - 10 <= mouse_y <= y + self.slider_altura + 10:
                return True, (mouse_x - x) / self.slider_largura
        elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
            return False, None
        elif evento.type == pygame.MOUSEMOTION and arrastando:
            mouse_x, _ = evento.pos
            novo_valor = (mouse_x - pos_slider[0]) / self.slider_largura
            novo_valor = max(0.0, min(1.0, novo_valor))
            return True, novo_valor
        return arrastando, None

    def on_click(self, pos: tuple[int, int]) -> None:
        for botao in self.botoes:
            if botao["rect"].collidepoint(pos):
                if botao["texto"] == "Voltar":
                    self.config["volume_musica"] = self.musica_valor
                    self.config["volume_efeitos"] = self.sfx_valor
                    self._deve_voltar = True

    def run(self) -> None:
        self._deve_voltar = False
        while not self._deve_voltar:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    self._deve_voltar = True
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    self.on_click(evento.pos)

                # Sliders
                self.arrastando_musica, novo_musica = self.lidar_slider(evento, self.slider_musica_pos, self.arrastando_musica)
                if novo_musica is not None:
                    self.musica_valor = novo_musica
                    self.sons.set_volume_musica(self.musica_valor)

                self.arrastando_sfx, novo_sfx = self.lidar_slider(evento, self.slider_sfx_pos, self.arrastando_sfx)
                if novo_sfx is not None:
                    self.sfx_valor = novo_sfx
                    self.sons.set_volume_efeitos(self.sfx_valor)

            self.surface.fill((0, 0, 0))
            self.desenhar_fundo_escuro()
            self.desenhar_titulo()
            self.desenhar_slider(self.slider_musica_pos, self.musica_valor, "Música")
            self.desenhar_slider(self.slider_sfx_pos, self.sfx_valor, "SFX")
            self.desenhar_botoes()

            pygame.display.flip()
            self.clock.tick(60)
