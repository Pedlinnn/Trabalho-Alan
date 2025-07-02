import pygame

class Sons:
    def __init__(self, config: dict) -> None:
        pygame.mixer.init()

        # Volumes iniciais puxados da config
        self.volume_musica = config.get('volume_musica', 0.5)
        self.volume_efeitos = config.get('volume_efeitos', 0.5)

        # Dicionario de efeitos sonoros
        self.sons = {
            'tiro_jogador': pygame.mixer.Sound('audios/TiroJogador.mp3'),
            'morre_inimigo': pygame.mixer.Sound('audios/MorreInimigo.mp3'),
            'raio_jogador': pygame.mixer.Sound('audios/RaioJogador.mp3')
        }

        # Define volume inicial dos efeitos
        for som in self.sons.values():
            som.set_volume(self.volume_efeitos)

        self.musica_atual = None  # Para controle da musica atual

    # Musica
    def tocar_musica(self, nome):
        if nome == self.musica_atual:
            return  # Ja esta tocando essa musica
        if nome == 'menu':
            caminho = 'audios/MusicaMenu.mp3'
        elif nome == 'jogo':
            caminho = 'audios/MusicaJogo.mp3'
        else:
            print(f'Musica "{nome}" nao encontrada!')
            return

        pygame.mixer.music.load(caminho)
        pygame.mixer.music.set_volume(self.volume_musica)
        pygame.mixer.music.play(-1)
        self.musica_atual = nome

    def parar_musica(self):
        pygame.mixer.music.stop()
        self.musica_atual = None

    # Efeitos sonoros SFX
    def tocar_som(self, nome):
        som = self.sons.get(nome)
        if som:
            som.play()
        else:
            print(f"Som '{nome}' nao encontrado!")

    # Getters
    def get_volume_musica(self):
        return self.volume_musica

    def get_volume_efeitos(self):
        return self.volume_efeitos

    # Setters
    def set_volume_musica(self, volume):
        self.volume_musica = max(0, min(volume, 1))
        pygame.mixer.music.set_volume(self.volume_musica)

    def set_volume_efeitos(self, volume):
        self.volume_efeitos = max(0, min(volume, 1))
        for som in self.sons.values():
            som.set_volume(self.volume_efeitos)