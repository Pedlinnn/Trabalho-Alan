import json
import os
import pygame
import sys

ARQUIVO_SAVE = "save_jogo.json"
ARQUIVO_RANKING = "ranking.json"

class SaveRanking:

    @staticmethod
    def salvar(jogo, modo="completo") -> None:
        """
        Salva o estado do jogo em arquivo JSON.
        Modo "completo" salva tudo; modo "buffs" salva apenas dados essenciais.
        """
        if modo == "completo":
            dados = {
                "player": {
                    "vida": jogo.player.vida,
                    "vida_maxima": jogo.player.vida_maxima,
                    "pos": (jogo.player.rect.x, jogo.player.rect.y),
                    "arma_dano": jogo.player.arma_normal.dano,
                    "intervalo_arma": jogo.player.arma_normal.intervalo,
                    "pode_usar_raio": jogo.player.pode_usar_raio
                },
                "wave": jogo.spawn_wave,
                "inimigos_mortos": jogo.inimigos_mortos_contagem,
                "buff_contagem": jogo.buff_contagem
            }
        elif modo == "buffs":
            dados = {
                "player": {
                    "vida": jogo.player.vida,
                    "vida_maxima": jogo.player.vida_maxima,
                    "arma_dano": jogo.player.arma_normal.dano,
                    "intervalo_arma": jogo.player.arma_normal.intervalo,
                    "pode_usar_raio": jogo.player.pode_usar_raio
                },
                "inimigos_mortos": jogo.inimigos_mortos_contagem,
                "buff_contagem": jogo.buff_contagem
            }
        else:
            print(f"[ERRO] Modo '{modo}' inválido para salvar.")
            return

        with open(ARQUIVO_SAVE, "w") as arquivo:
            json.dump(dados, arquivo)
        print(f"Jogo salvo com sucesso! (modo: {modo})")

    @staticmethod
    def carregar() -> dict:
        try:
            with open(ARQUIVO_SAVE, "r") as arquivo:
                dados = json.load(arquivo)
                print("Save carregado com sucesso!")
                return dados
        except FileNotFoundError:
            print("Nenhum save encontrado.")
            return {}
        except json.JSONDecodeError:
            print("Erro ao decodificar o save.")
            return {}

    @staticmethod
    def apagar()->None:
        if os.path.exists(ARQUIVO_SAVE):
            os.remove(ARQUIVO_SAVE)

    @staticmethod
    def pedir_nome_e_salvar(screen, score)-> None:
        fonte_titulo = pygame.font.Font(None, 70)
        fonte_input = pygame.font.Font(None, 50)
        nome = ""
        digitando = True

        while digitando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(nome) > 0:
                        SaveRanking.salvar_no_ranking(nome, score)
                        SaveRanking.apagar()
                        digitando = False
                    elif event.key == pygame.K_BACKSPACE:
                        nome = nome[:-1]
                    elif len(nome) < 6 and event.unicode.isalnum():
                        nome += event.unicode.upper()

            screen.fill((0, 0, 0))
            texto = fonte_titulo.render("Digite seu nome (max 6 letras):", True, (255, 255, 255))
            nome_texto = fonte_input.render(nome, True, (0, 255, 0))
            screen.blit(texto, texto.get_rect(center=(screen.get_width() // 2, screen.get_height() // 3)))
            screen.blit(nome_texto, nome_texto.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)))
            pygame.display.flip()

    @staticmethod
    def salvar_no_ranking(nome, score) -> None:
        dados = []
        if os.path.exists(ARQUIVO_RANKING):
            with open(ARQUIVO_RANKING, "r") as f:
                dados = json.load(f)

        dados.append({"nome": nome, "score": score})
        dados = sorted(dados, key=lambda x: x["score"], reverse=True)[:10]

        with open(ARQUIVO_RANKING, "w") as f:
            json.dump(dados, f, indent=4)

    @staticmethod
    def mostrar(screen)-> None:
        fonte_titulo = pygame.font.Font(None, 70)
        fonte_ranking = pygame.font.Font(None, 40)
        fonte_voltar = pygame.font.Font(None, 50)

        largura_tela = screen.get_width()
        altura_tela = screen.get_height()
        botao_voltar = pygame.Rect((largura_tela - 250) // 2, altura_tela - 100, 250, 60)

        ranking = []
        if os.path.exists(ARQUIVO_RANKING):
            with open(ARQUIVO_RANKING, "r") as f:
                ranking = json.load(f)

        mostrar = True
        while mostrar:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "sair"
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return "voltar"
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if botao_voltar.collidepoint(event.pos):
                        return "voltar"

            screen.fill((20, 20, 20))
            titulo = fonte_titulo.render("Top 25 Ranking", True, (255, 255, 0))
            screen.blit(titulo, titulo.get_rect(center=(largura_tela // 2, 50)))

            for i, entrada in enumerate(ranking[:25]):
                texto = f"{i+1:02d}. {entrada['nome']} - {entrada['score']}"
                render = fonte_ranking.render(texto, True, (255, 255, 255))
                screen.blit(render, (100, 120 + i * 30))

            cor = (200, 200, 200) if botao_voltar.collidepoint(pygame.mouse.get_pos()) else (170, 170, 170)
            pygame.draw.rect(screen, cor, botao_voltar, border_radius=10)
            texto_voltar = fonte_voltar.render("Voltar", True, (0, 0, 0))
            screen.blit(texto_voltar, texto_voltar.get_rect(center=botao_voltar.center))

            pygame.display.flip()