import pygame

class RamObjeto(pygame.sprite.Sprite):
    def __init__(self, caminho_imagem, x, y, largura=None, altura=None) -> None:
        super().__init__()
        self._caminho_imagem = caminho_imagem
        try:
            self.image_original = pygame.image.load(caminho_imagem).convert_alpha()   #carrega imagem e otimiza a imagem
            if largura and altura:   #verifica se foi fornecido largura e altura
                self.image = pygame.transform.scale(self.image_original, (largura, altura))
            else:
                self.image = self.image_original  #se nao usa em altura original
        except pygame.error as e:
            print(f"Erro ao carregar imagem para RamObjeto '{caminho_imagem}': {e}")
            self.image = pygame.Surface((32, 32), pygame.SRCALPHA) # Imagem de placeholde, tem um canal de transparência alfa 
            self.image.fill((255, 0, 255)) # Magenta para indicar erro

        self.rect = self.image.get_rect(topleft=(x, y))

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
   
    def desenhar(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)  #desenha na posição do retangulo