import pygame
import sys
from typing import List, Optional, Tuple, Dict

class MenuBase:
    def __init__(
        self,
        surface: pygame.Surface,
        botoes: List[Dict[str, pygame.Rect]],
        fonte_botoes: pygame.font.Font,
        titulo: Optional[str] = None,
        fonte_titulo: Optional[pygame.font.Font] = None,
        alpha_fundo: int = 180
    ) -> None:
        self.surface = surface
        self.botoes = botoes
        self.fonte_botoes = fonte_botoes
        self.titulo = titulo
        self.fonte_titulo = fonte_titulo or pygame.font.Font(None, 70)
        self.alpha_fundo = alpha_fundo
        self.clock = pygame.time.Clock()

    def desenhar_fundo_escuro(self) -> None:
        overlay = pygame.Surface(self.surface.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, self.alpha_fundo))
        self.surface.blit(overlay, (0, 0))

    def desenhar_titulo(self) -> None:
        if self.titulo:
            texto = self.fonte_titulo.render(self.titulo, True, (255, 0, 0))
            rect = texto.get_rect(center=(self.surface.get_width()//2, self.surface.get_height()//5))
            self.surface.blit(texto, rect)

    def desenhar_botoes(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        for botao in self.botoes:
            rect = botao["rect"]
            texto = botao["texto"]
            cor = (170, 170, 170) if rect.collidepoint(mouse_pos) else (200, 200, 200)
            pygame.draw.rect(self.surface, cor, rect, border_radius=10)
            txt_surf = self.fonte_botoes.render(texto, True, (0, 0, 0))
            txt_rect = txt_surf.get_rect(center=rect.center)
            self.surface.blit(txt_surf, txt_rect)

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.on_click(event.pos)
            self.surface.fill((0, 0, 0))
            self.desenhar_fundo_escuro()
            self.desenhar_titulo()
            self.desenhar_botoes()
            pygame.display.flip()
            self.clock.tick(60)

    def on_click(self, pos: Tuple[int, int]) -> None:
        """Implementar nas subclasses"""
        pass