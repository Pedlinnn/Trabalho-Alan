
import pygame
from ram_objeto import RamObjeto 

class Mapa():
    def __init__(self, caminho_imagem_fundo: str, largura_janela: int, altura_janela: int) -> None:
        self._largura_janela = largura_janela
        self._altura_janela = altura_janela    #tamanho da tela

        self._caminho_imagem_fundo = caminho_imagem_fundo   
        try:
            self.imagem_original_fundo = pygame.image.load(caminho_imagem_fundo).convert()  #carregar
        except pygame.error as e:
            print(f"Erro ao carregar a imagem de fundo '{caminho_imagem_fundo}': {e}")   #nao carregou cria imagem preta
            self.imagem_original_fundo = pygame.Surface((largura_janela, altura_janela))
            self.imagem_original_fundo.fill((0, 0, 0))   

        self.objetos_do_mapa = pygame.sprite.Group() 

    @property
    def caminho_imagem_fundo(self) -> None:
        return self._caminho_imagem_fundo
    
    @caminho_imagem_fundo.setter
    def caminho_imagem_fundo(self, novo_caminho: str) -> None:
        if self._caminho_imagem_fundo != novo_caminho:
            self._caminho_imagem_fundo = novo_caminho

    @property
    def largura_janela(self):
        return self._largura_janela
    
    @largura_janela.setter
    def largura_janela(self, valor):
        self._largura_janela = valor

    @property
    def altura_janela(self):
        return self._altura_janela
    
    @altura_janela.setter
    def altura_janela(self, valor):
        self._altura_janela = valor


    def adicionar_objeto(self, objeto: pygame.sprite.Sprite) -> None:  #add sprite
        self.objetos_do_mapa.add(objeto)
    
    def remover_objeto(self, objeto: pygame.sprite.Sprite) -> None:   #remove
        if objeto in self.objetos_do_mapa:
            self.objetos_do_mapa.remove(objeto)

    def desenhar(self, tela, deslocamento_x = 0, deslocamento_y = 0) -> None:  #desenha o fundo e todos os objetos
        area_visivel = pygame.Rect(deslocamento_x, deslocamento_y, self._largura_janela, self._altura_janela)
        tela.blit(self.imagem_original_fundo, (0, 0), area_visivel)
        for sprite in self.objetos_do_mapa:
            tela.blit(sprite.image, (sprite.rect.x - deslocamento_x, sprite.rect.y - deslocamento_y))

    def atualizar_dimensoes_janela(self, nova_largura: int, nova_altura: int) -> None:   #atualiza a largura e altura e redimensiona o fundo
        self.largura_janela = nova_largura
        self.altura_janela = nova_altura
