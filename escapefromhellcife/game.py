import pygame
import random
import sys
import os
import math

LARGURA_TELA = 800
ALTURA_TELA = 450 
FPS = 60
TITULO = "Escape from Hellcife"

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
AMARELO = (255, 215, 0)
AZUL_CEU = (135, 206, 235)
CINZA_CIDADE = (169, 169, 169)
AREIA = (237, 201, 175)
MARROM = (139, 69, 19)
DIRETORIO_JOGO = os.path.dirname(os.path.abspath(__file__))

def carregar_img_segura(nome_arquivo, cor_fallback=(0,0,0), tamanho_fallback=(50,50)):
    caminho_completo = os.path.join(DIRETORIO_JOGO, nome_arquivo)
    try:
        img = pygame.image.load(caminho_completo).convert_alpha()
        return img
    except FileNotFoundError:
        surf = pygame.Surface(tamanho_fallback)
        surf.fill(cor_fallback)
        return surf

def carregar_som_seguro(nome_arquivo):
    caminho_completo = os.path.join(DIRETORIO_JOGO, nome_arquivo)
    try:
        som = pygame.mixer.Sound(caminho_completo)
        return som
    except:
        return None 

class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites_correndo = [
            carregar_img_segura("p1.png", (0, 0, 255)),
            carregar_img_segura("p2.png", (0, 0, 200)),
            carregar_img_segura("p3.png", (0, 0, 150))
        ]
        self.sprites_invencivel = [
            carregar_img_segura("gold1.png", AMARELO),
            carregar_img_segura("gold2.png", (255, 255, 200)),
            carregar_img_segura("gold3.png", (255, 255, 200))
        ]
        
        self.index_atual = 0
        self.image = self.sprites_correndo[self.index_atual]
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.bottom = ALTURA_TELA - 40 
        
        self.gravidade = 0.8
        self.velocidade_y = 0
        self.pulo_forca = -16
        self.no_chao = True
        self.invencivel = False
        self.tempo_inicio_invencivel = 0
        self.duracao_invencibilidade = 5000

    def pular(self):
        if self.no_chao:
            self.velocidade_y = self.pulo_forca
            self.no_chao = False
            return True 
        return False

    def ativar_invencibilidade(self):
        self.invencivel = True
        self.tempo_inicio_invencivel = pygame.time.get_ticks()

    def update(self):
        self.velocidade_animacao = 0.2
        lista_atual = self.sprites_invencivel if self.invencivel else self.sprites_correndo
        self.index_atual += self.velocidade_animacao
        if self.index_atual >= len(lista_atual): self.index_atual = 0
        self.image = lista_atual[int(self.index_atual)]

        self.velocidade_y += self.gravidade
        self.rect.y += self.velocidade_y

        if self.rect.bottom >= ALTURA_TELA - 40:
            self.rect.bottom = ALTURA_TELA - 40
            self.velocidade_y = 0
            self.no_chao = True

        if self.invencivel:
            if pygame.time.get_ticks() - self.tempo_inicio_invencivel > self.duracao_invencibilidade:
                self.invencivel = False

class ObstaculoChao(pygame.sprite.Sprite):
    dados_possiveis = []

    def __init__(self):
        super().__init__()
        if len(ObstaculoChao.dados_possiveis) == 0:
            anim_tubarao = [carregar_img_segura("tuba1.png", (100, 100, 100), (70, 40)),
                            carregar_img_segura("tuba2.png", (120, 120, 120), (70, 40))]
            anim_laursa = [carregar_img_segura("laursa1.png", (255, 20, 147), (40, 70)),
                           carregar_img_segura("laursa2.png", (255, 100, 180), (40, 70))]
            img_santa = carregar_img_segura("santa.png", VERMELHO, (50, 50))
            anim_santa = [img_santa]
            anim_onibus = [carregar_img_segura("onibus.png", (0, 0, 200), (90, 60))]

            ObstaculoChao.dados_possiveis = [
                {'tipo': 'tubarao', 'sprites': anim_tubarao},
                {'tipo': 'laursa',  'sprites': anim_laursa},
                {'tipo': 'santa',   'sprites': anim_santa},
                {'tipo': 'onibus',  'sprites': anim_onibus}
            ]

        escolha = random.choice(ObstaculoChao.dados_possiveis) 
        self.tipo = escolha['tipo']
        self.sprites = escolha['sprites']
        
        self.index_atual = 0
        self.velocidade_animacao = 0.15 
        self.image = self.sprites[self.index_atual]
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA_TELA + random.randint(0, 50)
        self.rect.bottom = ALTURA_TELA - 40 
        self.velocidade_x = -6

    def update(self):
        self.rect.x += self.velocidade_x
        self.index_atual += self.velocidade_animacao
        if self.index_atual >= len(self.sprites): self.index_atual = 0
        self.image = self.sprites[int(self.index_atual)]
        if self.rect.right < 0: self.kill()

class InimigoZigZag(pygame.sprite.Sprite):
    dados_possiveis = []

    def __init__(self):
        super().__init__()
        if len(InimigoZigZag.dados_possiveis) == 0:
            anim_tolete = [carregar_img_segura("tolete1.png", MARROM, (50, 30)),
                           carregar_img_segura("tolete2.png", (160, 82, 45), (50, 30)),
                           carregar_img_segura("tolete3.png", (160, 82, 45), (50, 30))]

            InimigoZigZag.dados_possiveis = [
                {'tipo': 'tolete', 'sprites': anim_tolete}
            ]

        escolha = random.choice(InimigoZigZag.dados_possiveis)
        self.tipo = escolha['tipo']
        self.sprites = escolha['sprites']
        self.index_atual = 0
        self.image = self.sprites[self.index_atual]
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA_TELA + 50
        self.base_y = random.randint(ALTURA_TELA // 2 - 50, ALTURA_TELA // 2 + 50)
        self.rect.centery = self.base_y
        self.velocidade_x = -7
        self.angulo = 0

    def update(self):
        self.rect.x += self.velocidade_x
        self.angulo += 0.1
        self.rect.centery = self.base_y + math.sin(self.angulo) * 60
        self.index_atual += 0.15
        if self.index_atual >= len(self.sprites): self.index_atual = 0
        self.image = self.sprites[int(self.index_atual)]
        if self.rect.right < 0: self.kill()

class ItemInvencibilidade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = [
            carregar_img_segura("pitu1.png", AMARELO, (30, 30)),
            carregar_img_segura("pitu2.png", (255, 255, 200), (30, 30))
        ]
        self.index_atual = 0
        self.image = self.sprites[self.index_atual]
        self.rect = self.image.get_rect()
        self.rect.x = LARGURA_TELA + random.randint(100, 300)
        self.rect.y = random.randint(ALTURA_TELA - 200, ALTURA_TELA - 100)
        self.velocidade_x = -5

    def update(self):
        self.rect.x += self.velocidade_x
        self.index_atual += 0.15
        if self.index_atual >= len(self.sprites): self.index_atual = 0
        self.image = self.sprites[int(self.index_atual)]
        if self.rect.right < 0: self.kill()


class Jogo:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()

        self.tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        pygame.display.set_caption(TITULO)
        self.clock = pygame.time.Clock()
        self.rodando = True
        
        self.jogo_iniciado = False 
        self.game_over = False
        self.fonte = pygame.font.Font(None, 36)

        self.img_titulo = carregar_img_segura("titulo.png", (0, 255, 255), (400, 100))

        self.som_pulo = carregar_som_seguro("jump.wav")
        self.som_santa = carregar_som_seguro("hino_santa.wav")
        self.som_buzina = carregar_som_seguro("buzina.wav")
        self.som_laursa = carregar_som_seguro("dinheiro.wav")
        self.som_tubarao = carregar_som_seguro("jaws.wav")
        self.som_estrela = carregar_som_seguro("star_theme.wav")
        
        self.musica_fundo = carregar_som_seguro("musica_fundo.wav")
        self.canal_fundo = None

        if self.musica_fundo: 
            self.musica_fundo.set_volume(0.5)
            self.canal_fundo = self.musica_fundo.play(-1)
        
        self.tocando_estrela = False
        self.bg_ceu = carregar_img_segura("bg_recife_ceu.png", AZUL_CEU, (LARGURA_TELA, ALTURA_TELA))
        self.bg_ceu = pygame.transform.scale(self.bg_ceu, (LARGURA_TELA, ALTURA_TELA))
        self.bg_ceu_x1 = 0; self.bg_ceu_x2 = LARGURA_TELA
        self.vel_ceu = 1

        self.bg_cidade = carregar_img_segura("bg_recife_cidade.png", CINZA_CIDADE, (LARGURA_TELA, 300))
        self.bg_cidade = pygame.transform.scale(self.bg_cidade, (LARGURA_TELA, 350))
        self.bg_cidade_x1 = 0; self.bg_cidade_x2 = LARGURA_TELA
        self.pos_y_cidade = ALTURA_TELA - 350 - 20
        self.vel_cidade = 3

        self.bg_chao = carregar_img_segura("bg_recife_chao.png", AREIA, (LARGURA_TELA, 40))
        self.bg_chao = pygame.transform.scale(self.bg_chao, (LARGURA_TELA, 40)) 
        self.bg_chao_x1 = 0; self.bg_chao_x2 = LARGURA_TELA
        self.pos_y_chao = ALTURA_TELA - 40
        self.vel_chao = 6 
        
        self.criar_objetos()

    def criar_objetos(self):
        self.todos_sprites = pygame.sprite.Group()
        self.grupo_inimigos = pygame.sprite.Group()
        self.grupo_powerups = pygame.sprite.Group()
        self.jogador = Jogador()
        self.todos_sprites.add(self.jogador)
        self.pontos = 0
        self.inicio_tempo = pygame.time.get_ticks()

        self.EVENTO_OBSTACULO = pygame.USEREVENT + 1
        self.EVENTO_ZIGZAG = pygame.USEREVENT + 2
        self.EVENTO_POWERUP = pygame.USEREVENT + 3
        pygame.time.set_timer(self.EVENTO_OBSTACULO, 2000)
        pygame.time.set_timer(self.EVENTO_ZIGZAG, 5000)
        pygame.time.set_timer(self.EVENTO_POWERUP, 10000)

    def lidar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT: 
                self.rodando = False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if not self.jogo_iniciado:
                        self.jogo_iniciado = True
                        self.inicio_tempo = pygame.time.get_ticks() 
                    
                    elif self.game_over:
                        self.reiniciar_jogo()
                    
                    else:
                        if self.jogador.pular() and self.som_pulo:
                            self.som_pulo.play()

            if self.jogo_iniciado and not self.game_over:
                if evento.type == self.EVENTO_OBSTACULO:
                    obs = ObstaculoChao()
                    self.todos_sprites.add(obs); self.grupo_inimigos.add(obs)
                if evento.type == self.EVENTO_ZIGZAG:
                    zig = InimigoZigZag()
                    self.todos_sprites.add(zig); self.grupo_inimigos.add(zig)
                if evento.type == self.EVENTO_POWERUP:
                    power = ItemInvencibilidade()
                    self.todos_sprites.add(power); self.grupo_powerups.add(power)

    def mover_fundo(self):
        self.bg_ceu_x1 -= self.vel_ceu; self.bg_ceu_x2 -= self.vel_ceu
        if self.bg_ceu_x1 + LARGURA_TELA < 0: self.bg_ceu_x1 = self.bg_ceu_x2 + LARGURA_TELA
        if self.bg_ceu_x2 + LARGURA_TELA < 0: self.bg_ceu_x2 = self.bg_ceu_x1 + LARGURA_TELA

        self.bg_cidade_x1 -= self.vel_cidade; self.bg_cidade_x2 -= self.vel_cidade
        if self.bg_cidade_x1 + LARGURA_TELA < 0: self.bg_cidade_x1 = self.bg_cidade_x2 + LARGURA_TELA
        if self.bg_cidade_x2 + LARGURA_TELA < 0: self.bg_cidade_x2 = self.bg_cidade_x1 + LARGURA_TELA

        self.bg_chao_x1 -= self.vel_chao; self.bg_chao_x2 -= self.vel_chao
        if self.bg_chao_x1 + LARGURA_TELA < 0: self.bg_chao_x1 = self.bg_chao_x2 + LARGURA_TELA
        if self.bg_chao_x2 + LARGURA_TELA < 0: self.bg_chao_x2 = self.bg_chao_x1 + LARGURA_TELA

    def atualizar(self):
        if not self.game_over:
            self.mover_fundo()

        if not self.jogo_iniciado or self.game_over:
            return

        self.todos_sprites.update()
        self.pontos = (pygame.time.get_ticks() - self.inicio_tempo) // 100
        if pygame.sprite.spritecollide(self.jogador, self.grupo_powerups, True):
                self.jogador.ativar_invencibilidade()
                if self.som_estrela and not self.tocando_estrela:
                    if self.canal_fundo: self.canal_fundo.pause()
                    self.som_estrela.play(-1)
                    self.tocando_estrela = True

        if self.tocando_estrela and not self.jogador.invencivel:
            if self.som_estrela: self.som_estrela.stop()
            if self.canal_fundo: self.canal_fundo.unpause()
            self.tocando_estrela = False

        hits = pygame.sprite.spritecollide(self.jogador, self.grupo_inimigos, False, pygame.sprite.collide_rect_ratio(0.7))
        if hits:
            if self.jogador.invencivel:
                for inimigo in hits: inimigo.kill()
            else:
                self.game_over = True
                pygame.mixer.stop()
                
                inimigo = hits[0]
                tipo = getattr(inimigo, 'tipo', '')
                if tipo == 'tubarao' and self.som_tubarao: self.som_tubarao.play()
                elif tipo == 'santa' and self.som_santa: self.som_santa.play()
                elif tipo == 'onibus' and self.som_buzina: self.som_buzina.play()
                elif tipo == 'laursa' and self.som_laursa: self.som_laursa.play()

    def desenhar(self):
        self.tela.blit(self.bg_ceu, (self.bg_ceu_x1, 0))
        self.tela.blit(self.bg_ceu, (self.bg_ceu_x2, 0))
        self.tela.blit(self.bg_cidade, (self.bg_cidade_x1, self.pos_y_cidade))
        self.tela.blit(self.bg_cidade, (self.bg_cidade_x2, self.pos_y_cidade))
        self.tela.blit(self.bg_chao, (self.bg_chao_x1, self.pos_y_chao))
        self.tela.blit(self.bg_chao, (self.bg_chao_x2, self.pos_y_chao))
        
        if self.jogo_iniciado:
            self.todos_sprites.draw(self.tela)
            cor = AMARELO if self.jogador.invencivel else PRETO
            txt = f"Pontos: {self.pontos}" + (" - INVENCÍVEL!" if self.jogador.invencivel else "")
            self.tela.blit(self.fonte.render(txt, True, cor), (10, 10))

        if not self.jogo_iniciado:
            rect_img_titulo = self.img_titulo.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/3))
            self.tela.blit(self.img_titulo, rect_img_titulo)

            if (pygame.time.get_ticks() % 1000) < 500:
                start_txt = self.fonte.render("Pressione ESPAÇO para Começar", True, PRETO)
                rect_start = start_txt.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 + 50))
                self.tela.blit(start_txt, rect_start)
            
            self.tela.blit(self.jogador.image, (100, ALTURA_TELA - 40 - 50))

        if self.game_over:
            overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA), pygame.SRCALPHA); overlay.fill((0,0,0,160))
            self.tela.blit(overlay, (0,0))
            msg_fim = self.fonte.render("Vixe! GAME OVER", True, BRANCO)
            rect_fim = msg_fim.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 - 20))
            self.tela.blit(msg_fim, rect_fim)
            msg_restart = self.fonte.render("Pressione ESPAÇO para tentar de novo", True, AMARELO)
            rect_restart = msg_restart.get_rect(center=(LARGURA_TELA/2, ALTURA_TELA/2 + 30))
            self.tela.blit(msg_restart, rect_restart)

        pygame.display.flip()

    def reiniciar_jogo(self):
        pygame.mixer.stop() 
        if self.musica_fundo: 
            self.canal_fundo = self.musica_fundo.play(-1)
            
        self.tocando_estrela = False
        self.game_over = False
        self.bg_ceu_x1 = 0; self.bg_ceu_x2 = LARGURA_TELA
        self.bg_cidade_x1 = 0; self.bg_cidade_x2 = LARGURA_TELA
        self.bg_chao_x1 = 0; self.bg_chao_x2 = LARGURA_TELA
        self.criar_objetos()

    def executar(self):
        while self.rodando:
            self.clock.tick(FPS)
            self.lidar_eventos()
            self.atualizar()
            self.desenhar()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()