import pygame

class Objeto2(pygame.sprite.Sprite):
    def __init__(self, caminho_imagem, x, y, largura=None, altura=None) -> None:
        super().__init__()
        try:
            imagem_original = pygame.image.load(caminho_imagem).convert_alpha()
            if largura and altura:
                self.image = pygame.transform.scale(imagem_original, (largura, altura))
            else:
                self.image = imagem_original
        except pygame.error as e:
            print(f"Erro ao carregar imagem do ObjetoEspecial '{caminho_imagem}': {e}")
            self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
            self.image.fill((255, 0, 0))  # Vermelho em caso de erro

        self.rect = self.image.get_rect(topleft=(x, y))

    def atualizar(self, tela: pygame.Surface) -> None:
        tela.blit(self.image, self.rect)
        
#get e setters

    @property
    def caminho_imagem(self) -> None:
        return self._caminho_imagem
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, valor: x) -> None:
        self._x = valor

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, valor):
        self._y = valor