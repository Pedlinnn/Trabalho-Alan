from projetil import *

class Arma:
    def __init__(self):  
        self.dano = 25
        self.intervalo = 500
        self.projeteis = pygame.sprite.Group()   #armazena os tiros (bem intuitivo grupo de sprites)
        self.ultimo_tiro = pygame.time.get_ticks()    #tempo do ultimo disparo

    def atirar(self, x: int, y: int, grupo_projeteis: pygame.sprite.Sprite) -> None:
        tempo_atual = pygame.time.get_ticks()   #pega o momento (pygame é um pai com essas funções)
        if tempo_atual - self.ultimo_tiro >= self.intervalo:  #basicamente pega o atual e tira o tick do ultimo se der > ou = pode atirar
            self.ultimo_tiro = tempo_atual #atualiza o ultimo tiro
            destino_x, destino_y = pygame.mouse.get_pos()    #pega onde o mouse esta olhando
            novo_projetil = Projetil(x, y, destino_x, destino_y, self.dano)  # Agora passa o dano corretamente #cria um projetil com a direção do mouse 
            grupo_projeteis.add(novo_projetil)#adiciona no grupo correspondente a disparos ativos
            print(" Projetil disparado")

    def atualizar(self, inimigos: pygame.sprite.Sprite, grupo_projeteis: pygame.sprite.Sprite):
        for projetil in grupo_projeteis:  # Itera sobre cada projétil corretamente
            projetil.atualizar()  # Move o projétil

            for inimigo in inimigos:  # Itera sobre cada inimigo
                if projetil.rect.colliderect(inimigo.rect):  # Agora a colisão é verificada corretamente
                    inimigo.vida -= self.dano  
                    print(f" Tiro acertou o inimigo HP restante: {inimigo.vida}")

                    projetil.kill()  # Remove o projétil após acertar
            
                    break #garantindo q acerta so um

    
    def desenhar(self, surface: pygame.Surface, grupo_projeteis: pygame.sprite.Sprite):
        # Desenha cada projétil na tela usando o sprite definido na classe Projetil
        for projetil in grupo_projeteis:
            surface.blit(projetil.image, projetil.rect)
