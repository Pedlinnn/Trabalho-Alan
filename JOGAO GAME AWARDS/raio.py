import pygame
import random
from arma import Arma
import math

class Raio(Arma):
    def __init__(self):
        super().__init__()
        self.sprite_raio = pygame.image.load('sprites/raio.png').convert_alpha()
        self.sprite_raio = pygame.transform.scale(self.sprite_raio, (100, 100))
        self.dano_raio = 60
        self.tempo_ativo = 3000  # Raio dura 3 segundos
        self.cooldown = 10000    # Cooldown de 10 segundosa
        self.ativo = False
        self.ultimo_uso = 0
        self.raio_largura = 8
        self.cor_raio = (0, 100, 255)

        self.origem_x = 0
        self.origem_y = 0
        self.destino_x = 0
        self.destino_y = 0

    def ativar_raio(self, jogador: pygame.sprite.Sprite) -> None:
        tempo_atual = pygame.time.get_ticks()
        if tempo_atual - self.ultimo_uso >= self.cooldown:
            self.ativo = True
            self.ultimo_uso = tempo_atual
            self.origem_x, self.origem_y = jogador.rect.center
            print("Raio Ativado")


    def aplicar_dano(self, inimigos: pygame.sprite.Sprite) -> None:
        if self.ativo:
            area_raio = pygame.Rect(self.origem_x - 100, self.origem_y - 100, 200, 200)
            for inimigo in list(inimigos):
                if inimigo.rect.colliderect(area_raio):
                    inimigo.vida -= 25
                    print(f"O raio atingiu um inimigo HP restante: {inimigo.vida}")

                    # Empurrão baseado na pressão do raio
                    impacto_x = inimigo.rect.centerx - self.origem_x
                    impacto_y = inimigo.rect.centery - self.origem_y
                    vetor = pygame.Vector2(impacto_x, impacto_y)
                    if vetor.length() != 0:
                        direcao_impacto = vetor.normalize() * 20  # Aumenta a força do empurrão
                        inimigo.rect.x += direcao_impacto.x
                        inimigo.rect.y += direcao_impacto.y


    def atualizar(self, jogador: pygame.sprite.Sprite) -> None:
        if self.ativo:
            # Atualiza a origem para a posição atual do jogador
            self.origem_x, self.origem_y = jogador.rect.center
            self.destino_x, self.destino_y = pygame.mouse.get_pos()

            # Checa se o tempo do raio acabou
            if pygame.time.get_ticks() - self.ultimo_uso >= self.tempo_ativo:
                self.ativo = False
                print("Raio desativado após 3 segundos")


    def desenhar(self, surface: pygame.Surface) -> None:
        if self.ativo:
            dx = self.destino_x - self.origem_x     #pega a distancia de x 
            dy = self.destino_y - self.origem_y     #y
            angulo = math.degrees(math.atan2(-dy, dx))  #usa-se - para que quando for calcular acerte independente do quadrante, ele pe util para rotação de sprites e etc

            distancia = math.hypot(dx, dy)    #distancia hipotenusa
            raio_escalado = pygame.transform.scale(
                self.sprite_raio, (int(distancia), self.sprite_raio.get_height())          #redimensiona ajustando a largura
            ) 
            raio_rotacionado = pygame.transform.rotate(raio_escalado, angulo)               #rotaciona ajustando e vendo o angulo

            rect = raio_rotacionado.get_rect(  
                center=(self.origem_x + dx // 2, self.origem_y + dy // 2)    #posiciona o raio corretamente 
            )
            surface.blit(raio_rotacionado, rect)   #desenha definido pelo rect