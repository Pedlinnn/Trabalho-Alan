import sys
from turtle import Screen
from jogador import Jogador
from sprites import *
from inimigo_melee import *
from inimigo_ranged import *
from raio import Raio
from projetil import Projetil
from mapa import *
from save_ranking import *
from tipo_buff import TipoBuff
from sons import Sons
from menu_principal import MenuPrincipal
from menu_pausa import MenuPausa
from menu_morte import MenuMorte
from objeto2 import Objeto2

WINDOW_WIDTH, WINDOW_HEIGHT = 1280,720

class Jogo:
    def __init__(self, config: dict, som: 'Sons', save: dict = None) -> None:
        # setup
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # pega a screen
        self.config = config      # pega as configurações
        self.som = som # pega o gerenciador de sons
        self._estado = {
        'executando': True,
        'voltar_menu': True,
        'pausado': False
        }

        if not pygame.font.get_init():  # Verifica se já está inicializado
            pygame.font.init()          # Inicializa o módulo de fontes

        pygame.display.set_caption('Nao_e_virus.exe(teste)')  # título
        self.clock = pygame.time.Clock()  # fps
        self.running = True  # tá rodando

        self.mapa_fundo = Mapa("sprites/mapa.png", WINDOW_WIDTH, WINDOW_HEIGHT)  # pega o mapa

        # Grupos
        self.all_sprites = pygame.sprite.Group()  # todos os sprites
        self.projeteis = pygame.sprite.Group()  # guarda os projéteis
        self.projeteis_do_jogador = pygame.sprite.Group()  # guarda os projéteis do jogador
        self.inimigos = pygame.sprite.Group()  # guarda enemys
        self.objeto2 = Objeto2("sprites/placa.png", 50, 50, 200, 150)
        print("SAVE:", save)
        # Dados do save (ou padrão)
        player_save = save.get("player") if save else None
        pos_inicial = tuple(player_save.get("pos", (400, 300))) if player_save else (400, 300)
        self.player = Jogador(pos_inicial, self.all_sprites, save=player_save)  # instancia e add ao grupo de sprites

        # timer wave
        # TESTE: spawnar inimigos logo no início
        self.spawn_wave = save.get("wave", 1) if save else 1  # começa na wave do save ou 1
        self.spawnar_inimigos()  # começa o jogo já com a wave
        self.spawn_timer = pygame.time.get_ticks()  # inicializa o tempo corretamente
        self.spawn_interval = 20000  # Tempo entre as waves (20 segundos)

        self.spawnar_ram_objetos(3)  # add o ram

        self.inimigos_mortos_contagem = save.get("inimigos_mortos", 0) if save else 0
        self.buff_contagem = save.get("buff_contagem", 0) if save else 0
        self.escolhendo_buff = False
        self.opcoes_buff_tela = []
        self.fonte_buff = pygame.font.Font(None, 40)

    @property
    def running(self) -> bool:
        return self._estado['executando']
    
    @running.setter
    def running(self, valor: bool):
        self._estado['executando'] = valor

    @property
    def voltar_menu(self) -> bool:
        return self._estado['voltar_menu']
    
    @voltar_menu.setter
    def voltar_menu(self, valor: bool):
        self._estado['voltar_menu'] = valor

    @property
    def pausado(self) -> bool:
        return self._estado['pausado']

    def pausar(self):
        self._estado['pausado'] = True
        MenuPausa(self).run()
        self._estado['pausado'] = False


    def spawnar_ram_objetos(self, quantidade):  #função para adicionar o ram aleatoriamente no mapa
        for _ in range(quantidade):
            x_aleatorio = random.randint(0, WINDOW_WIDTH - 50)   #largura menos 50
            y_aleatorio = random.randint(0, WINDOW_HEIGHT - 50)   #altura menos 50

            novo_ram = RamObjeto("sprites/ram.png", x_aleatorio, y_aleatorio, 100, 100)   #cria o objeto
            self.mapa_fundo.adicionar_objeto(novo_ram)   #adiciona o objeto

    def run(self) -> None:
        self._estado['voltar_menu'] = False
        while self.running and not self.voltar_menu:  #loop
            dt = self.clock.tick(60) / 1000  # Limita a 60 FPS e dt em segundos

            #loop evento
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #se tiver quitando
                    SaveRanking.salvar(self, modo="saida")
                    self.running = False
                    self.voltar_menu = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.escolhendo_buff: #se o jogo estiver escolhendo buff
                        print(">> Tentando escolher um buff...")
                        mouse_x, mouse_y = event.pos
                        for rect_buff, tipo_buff_selecionado in self.opcoes_buff_tela:
                            if rect_buff.collidepoint(mouse_x, mouse_y):
                                self.aplicar_buff(tipo_buff_selecionado)  #aplica o buff escolhido
                                self.escolhendo_buff = False   #saida do modolho escolha
                                self.opcoes_buff_tela = []    #limpa as opções
                                break

                elif event.type == pygame.KEYDOWN:   #apertar tal tecla ativa o raiozao louco
                    if event.key == pygame.K_SPACE:
                        if self.player.pode_usar_raio:
                            tempo_atual = pygame.time.get_ticks()
                            if tempo_atual - self.player.arma_raio.ultimo_uso >= self.player.arma_raio.cooldown:
                                self.player.arma_raio.ativar_raio(self.player)
                                self.som.tocar_som('raio_jogador')
                    elif event.key == pygame.K_ESCAPE:
                        MenuPausa(self).run()
            
            # ataque contínuo com mouse pressionado

            mouse_pressionado = pygame.mouse.get_pressed()[0]
            if mouse_pressionado and not self.escolhendo_buff:
                tempo_atual = pygame.time.get_ticks()
                if tempo_atual - self.player.arma_normal.ultimo_tiro >= self.player.arma_normal.intervalo:
                    self.player.arma_normal.atirar(self.player.rect.centerx,self.player.rect.centery,self.projeteis)
                    self.som.tocar_som('tiro_jogador')

            #update
            if not self.escolhendo_buff:
                self.all_sprites.update(dt)   #atualiza all sprites
                self.projeteis.update(dt)  # Atualiza a posição dos projéteis
                self.player.arma_normal.atualizar(self.inimigos, self.projeteis)  #Atualiza a lógica da arma
                self.player.arma_raio.aplicar_dano(self.inimigos)   #Aplica o dano
                self.player.arma_raio.atualizar(self.player)  #Atualiza o raio


                for inimigo in self.inimigos:
                    if inimigo.vida <= 0 and not inimigo.contabilizado:
                        self.inimigos_mortos_contagem += 1
                        inimigo.contabilizado = True
                        self.som.tocar_som('morre_inimigo')
                        print("Inimigo morto! Total:", self.inimigos_mortos_contagem)

                if self.inimigos_mortos_contagem >= 2* (self.buff_contagem+1) ** 1.3:
                    self.preparar_buffs()
                    self.buff_contagem +=1


                for inimigo in self.inimigos:
                    if isinstance(inimigo, InimigoRanged):
                        for proj in inimigo.projeteis:  # ← Aqui começa o laço do projétil
                            offset = (
                                self.player.rect.x - proj.rect.x,
                                self.player.rect.y - proj.rect.y
                            )
                            if proj.mask.overlap(self.player.mask, offset):
                                self.player.levar_dano(proj.dano)
                                proj.kill()

                if self.player.vida <= 0:
                    menu_morte = MenuMorte(self)
                    menu_morte.run()

            #imagens
            self.display_surface.fill('black')  # Preenche a tela antes de desenhar

            self.mapa_fundo.desenhar(self.display_surface)   #desenha o mapa

            self.objeto2.atualizar(self.display_surface) 

            self.all_sprites.draw(self.display_surface)  # Desenha personagens/inimigos
            self.projeteis.draw(self.display_surface)  #desenha os projéteis 

            self.player.arma_normal.desenhar(self.display_surface, self.projeteis)  #desenha arma
            self.player.arma_raio.desenhar(self.display_surface)  #desenha arma
            self.display_surface.blit(pygame.font.SysFont('arial', 30).render(f"vida: {self.player.vida}/{self.player.vida_maxima}", True, (255, 0,0)),(10,10))

            # DESENHA PROJÉTEIS DOS INIMIGOS RANGED
            for inimigo in self.inimigos:
                if isinstance(inimigo, InimigoRanged):
                    inimigo.desenhar_projeteis(self.display_surface)
            
            if self.escolhendo_buff:
                self.desenhar_menu_buffs()
            pygame.display.update()  #atualiza a tela

            # Checa se já passou o tempo
            agora = pygame.time.get_ticks()
            if agora - self.spawn_timer >= self.spawn_interval:
                self.spawn_timer = agora
                self.spawn_wave += 1
                self.spawnar_inimigos()

    def spawnar_inimigos(self):
        valor_honesto = max(self.spawn_wave + 1, int(math.log(self.spawn_wave + 1)) * 10)
        if self.spawn_wave == 1:
            quantidade = 2
        else:
            quantidade = random.randint(self.spawn_wave, valor_honesto)  # quantidade de inimigos
        print(quantidade)

        for _ in range(quantidade):  # gera inimigos na quantidade definida
            angulo = random.uniform(0, 2 * math.pi)  # define um angulo aleatorio para spawnar
            raio = random.randint(1000, 1200)  # longe do jogador, mas aleatorio
            offset_x = math.cos(angulo) * raio  # x com base no angulo e raio
            offset_y = math.sin(angulo) * raio  # y

            spawn_x = self.player.rect.centerx + offset_x  # x relativa ao jogador
            spawn_y = self.player.rect.centery + offset_y  # y

            tipo = random.choice(["melee", "ranged"])  # escolhe aleatoriamente

            # Buffs progressivos por wave
            vida_bonus = 1 + self.spawn_wave * 0.05       # +5% por wave
            velocidade_bonus = 1 + self.spawn_wave * 0.01  # +1% por wave
            dano_bonus = 1 + self.spawn_wave * 0.02       # +2% por wave
            cooldown_bonus = 1 - self.spawn_wave * 0.01   # -1% de cooldown por wave

            if tipo == "melee":
                vida = int(100 * vida_bonus)
                velocidade = 2 * velocidade_bonus
                dano = int(10 * dano_bonus)
                cooldown = max(300, int(1000 * cooldown_bonus))  # cooldown mínimo de 300ms

                InimigoMelee((spawn_x, spawn_y),vida,velocidade,dano,cooldown,self.player,[self.all_sprites, self.inimigos])
            else:
                vida = int(80 * vida_bonus)
                velocidade = 2 * velocidade_bonus
                dano = int(5 * dano_bonus)
                cooldown = max(500, int(2000 * cooldown_bonus))  # cooldown mínimo de 500ms

                InimigoRanged((spawn_x, spawn_y),vida,velocidade,dano,cooldown,self.player,[self.all_sprites, self.inimigos],self.projeteis)


    def preparar_buffs(self):
        print(">> Entrou em preparar_buffs()")
        self.escolhendo_buff = True
        todas_opcoes = [TipoBuff.VIDA, TipoBuff.DANO, TipoBuff.VELOCIDADE_ATAQUE, TipoBuff.RAIO]
        if self.player.pode_usar_raio and TipoBuff.RAIO in todas_opcoes:
            todas_opcoes.remove(TipoBuff.RAIO)
        buffs_escolhidos =  random.sample(todas_opcoes, min(3, len(todas_opcoes)))
        print("Buffs escolhidos:", buffs_escolhidos)
        self.opcoes_buff_tela = [(None, tipo) for tipo in buffs_escolhidos]
    
    def desenhar_menu_buffs(self):
        print(">> Desenhando menu de buffs")
        largura_tela = self.display_surface.get_width()
        altura_tela = self.display_surface.get_height()

        largura_caixa = 250
        altura_caixa = 120
        espacamento = 60

        num_caixas = len(self.opcoes_buff_tela)
        largura_total = num_caixas * largura_caixa + (num_caixas - 1) * espacamento
        x_inicial = (largura_tela - largura_total)  // 2
        y_inicial = (altura_tela - altura_caixa) // 2

        temp_opcoes = []
        for i, (_, tipo_buff) in enumerate(self.opcoes_buff_tela):
            x = x_inicial + i * (largura_caixa + espacamento)
            y = y_inicial
            rect = pygame.Rect(x, y, largura_caixa, altura_caixa)

            pygame.draw.rect(self.display_surface, (70,70,70), rect)
            pygame.draw.rect(self.display_surface, (255,255,255), rect, 4)

            texto_buff = ""
            if tipo_buff == TipoBuff.VIDA:
                texto_buff = "Vida Máxima (+25)"
            
            elif tipo_buff == TipoBuff.DANO:
                texto_buff = "Dano (+10)"

            elif tipo_buff == TipoBuff.VELOCIDADE_ATAQUE:
                texto_buff = "Disparo efetivado"

            elif tipo_buff == TipoBuff.RAIO:
                texto_buff = "Arma Secreta"

            texto_renderizado = self.fonte_buff.render(texto_buff, True, (255,255,255))
            texto_rect = texto_renderizado.get_rect(center = rect.center)
            self.display_surface.blit(texto_renderizado, texto_rect)

            temp_opcoes.append((rect, tipo_buff))

        self.opcoes_buff_tela = temp_opcoes

    def aplicar_buff(self, tipo_buff):
        if tipo_buff == TipoBuff.VIDA:
            self.player.vida_maxima += 25
            # Aumenta a vida atual, mas não ultrapassa a nova vida máxima
            self.player.vida = min(self.player.vida + 25, self.player.vida_maxima) 
            print(f"Buff de Vida aplicado! Vida atual: {self.player.vida}/{self.player.vida_maxima}")
        elif tipo_buff == TipoBuff.DANO:
            self.player.arma_normal.dano += 10
            print(f"Buff de Dano aplicado! Dano da arma: {self.player.arma_normal.dano}")
        elif tipo_buff == TipoBuff.VELOCIDADE_ATAQUE:
            # Reduz o intervalo entre ataques (deixa o ataque mais rápido)
            # Garante que não fique abaixo de 0.1 segundos para evitar ataques instantâneos
            self.player.arma_normal.intervalo = max(100, self.player.arma_normal.intervalo - 100)
            print(f"Buff de Velocidade de Ataque aplicado! Novo intervalo: {self.player.arma_normal.intervalo:.1f}ms")
        elif tipo_buff == TipoBuff.RAIO:
            self.player.pode_usar_raio = True # Habilita o uso da arma de raio
            print("Raio habilitado! Use a barra de espaço!")
        
        SaveRanking.salvar(self, modo="buffs")  # modo só buffs

    def carregar_do_save(self):
        """
        Aplica os dados do self.save (carregados do JSON) nos atributos do jogo.
        Deve ser chamado no início do jogo, após set_save().
        """
        if not self.save:
            print("Nenhum save para carregar.")
            return

        dados_player = self.save.get("player", {})
        self.player.vida = dados_player.get("vida", self.player.vida)
        self.player.vida_maxima = dados_player.get("vida_maxima", self.player.vida_maxima)

        # Reposiciona o jogador, se a posição foi salva
        pos = dados_player.get("pos")
        if pos and isinstance(pos, (list, tuple)) and len(pos) == 2:
            self.player.rect.x, self.player.rect.y = pos

        # Restaura dados da arma
        self.player.arma_normal.dano = dados_player.get("arma_dano", self.player.arma_normal.dano)
        self.player.arma_normal.intervalo = dados_player.get("intervalo_arma", self.player.arma_normal.intervalo)

        # Poder especial (raio)
        self.player.pode_usar_raio = dados_player.get("pode_usar_raio", self.player.pode_usar_raio)

        # Outros dados do jogo
        self.spawn_wave = self.save.get("wave", self.spawn_wave)
        self.inimigos_mortos_contagem = self.save.get("inimigos_mortos", self.inimigos_mortos_contagem)
        self.buff_contagem = self.save.get("buff_contagem", self.buff_contagem)

        print("[INFO] Jogo restaurado com sucesso a partir do save!")

    # -------- Getters e setters --------

    def get_save(self):
        return self.save

    def set_save(self, novo_save):
        if isinstance(novo_save, dict):
            self.save = novo_save
        else:
            raise ValueError("Save deve ser um dicionário carregado de um JSON.")
        
def Sair():
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    try:
        pygame.init()
        config = {'volume_musica': 0.5, 'volume_efeitos': 0.5}
        screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption('Nao_e_virus.exe')

        som = Sons(config)
        som.tocar_musica('menu')

        while True:
            menu = MenuPrincipal(screen, som, config)
            menu.run()

            if menu.proximo_estado == "jogar":
                som.parar_musica()
                som.tocar_musica('jogo')

                # carrega o save corretamente do arquivo JSON
                save = SaveRanking.carregar()

                jogo = Jogo(config, som, save=save)  # usa o dicionário carregado
                jogo.run()

                # se o jogador fechou a janela (jogo.running == False), sai de vez
                if not jogo.running:
                    break

                # se ele voltou para o menu, volta
                if jogo.voltar_menu:
                    som.parar_musica()
                    som.tocar_musica('menu')
                    continue
                else:
                    break

            elif menu.proximo_estado == "sair":
                break

    except Exception as e:
        print(f"Erro no jogo: {e}")
    finally:
        pygame.quit()
        sys.exit()