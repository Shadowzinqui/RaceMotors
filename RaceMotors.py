import pygame
import random
import sys
import os
import datetime
import json
import re



def resource_path(caminho_relativo):
    """Retorna o caminho absoluto para recursos, compatível com PyInstaller"""
    try:
        # PyInstaller cria a variável _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, caminho_relativo)

# Inicializa o Pygame e o mixer de áudio
pygame.init()
pygame.mixer.init()

# -------------------- CONFIGURAÇÃO DA TELA --------------------
largura = 500
altura = 900
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Race Motors")

# -------------------- CORES --------------------
cinza = (50, 50, 50)
cinza_hover = (200, 200, 200)  # Um cinza mais claro para o hover
branco = (255, 255, 255)
verde = (0, 150, 0)
verde_hover = (0, 200, 0)
vermelho = (150, 0, 0)
vermelho_hover = (200, 0, 0)
laranja = (255, 165, 0)
azul = (0, 90, 200)
azul_hover = (0, 120, 255)
preto = (0, 0, 0)

# -------------------- FONTE --------------------
fonte_titulo = pygame.font.Font(None, 60)
fonte_botao = pygame.font.Font(None, 36)
fonte_pontos = pygame.font.Font(None, 36)
fonte_media = pygame.font.Font(None, 32)
fonte_pequena = pygame.font.Font(None, 26)
fonte_grande = pygame.font.Font(None, 40)

 

# -------------------- JOGADOR --------------------
jogador_largura = 50
jogador_altura = 100
jogador_vel_base = 10

# -------------------- OBSTÁCULOS --------------------
obstaculo_largura = 70
obstaculo_altura = 80

# -------------------- CLOCK --------------------
clock = pygame.time.Clock()
fps = 60


# -------------------- CURSOR GLOBAL --------------------
cursor_atual = "arrow"

def set_cursor(tipo):
    """Define o cursor de forma global, evitando conflitos entre telas"""
    global cursor_atual
    if tipo != cursor_atual:
        if tipo == "hand":
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        cursor_atual = tipo


# -------------------- SONS --------------------
som_colisao = pygame.mixer.Sound(resource_path("musicas/colisao.wav"))


# -------------------- FUNDOS E IMAGENS (carregadas uma vez) --------------------
fundo_audio = pygame.image.load(resource_path("imagens/pontuacaoEinformacao.png"))
fundo_audio = pygame.transform.scale(fundo_audio, (largura, altura))

fundo_menu = pygame.image.load(resource_path("imagens/fundo_menu02.png")).convert()
fundo_menu = pygame.transform.scale(fundo_menu, (largura, altura))


fundo_config = pygame.image.load(resource_path("imagens/pontuacaoEinformacao.png")).convert()
fundo_config = pygame.transform.scale(fundo_config, (largura, altura))

fundo_InfoPonto = pygame.image.load(resource_path("imagens/pontuacaoEinformacao.png")).convert()
fundo_InfoPonto = pygame.transform.scale(fundo_InfoPonto, (largura, altura))

fundo_game_over = pygame.image.load(resource_path("imagens/game_over.png")).convert_alpha()
fundo_game_over = pygame.transform.scale(fundo_game_over, (largura, altura)) # ajusta ao tamanho da tela

fundo_facil = pygame.image.load(resource_path("imagens/rua.png")).convert()
fundo_facil = pygame.transform.scale(fundo_facil, (largura, altura))

fundo_medio = pygame.image.load(resource_path("imagens/rua_medio.png")).convert()
fundo_medio = pygame.transform.scale(fundo_medio, (largura, altura))

fundo_dificil = pygame.image.load(resource_path("imagens/rua_dificil.png")).convert()
fundo_dificil = pygame.transform.scale(fundo_dificil, (largura, altura))

obstaculo_facil_img = pygame.image.load(resource_path("imagens/pedra.png")).convert_alpha()
obstaculo_facil_img = pygame.transform.scale(obstaculo_facil_img, (obstaculo_largura, obstaculo_altura))

obstaculo_medio_img = pygame.image.load(resource_path("imagens/cacto.png")).convert_alpha()
obstaculo_medio_img = pygame.transform.scale(obstaculo_medio_img, (obstaculo_largura, obstaculo_altura))

obstaculo_dificil_img = pygame.image.load(resource_path("imagens/arvore_de_natal.png")).convert_alpha()
obstaculo_dificil_img = pygame.transform.scale(obstaculo_dificil_img, (obstaculo_largura, obstaculo_altura))

# Ícones de dificuldade (estilo Need for Speed)
icone_facil = pygame.image.load(resource_path("imagens/icone_facil.png")).convert_alpha()
icone_medio = pygame.image.load(resource_path("imagens/icone_medio.png")).convert_alpha()
icone_dificil = pygame.image.load(resource_path("imagens/icone_dificil.png")).convert_alpha()

# cria versões de hover (ligeiramente maiores) para os ícones (mantém estilo simples)
icone_facil_hover   = pygame.transform.smoothscale(icone_facil,   (int(64*1.18), int(64*1.18)))
icone_medio_hover   = pygame.transform.smoothscale(icone_medio,   (int(64*1.18), int(64*1.18)))
icone_dificil_hover = pygame.transform.smoothscale(icone_dificil, (int(64*1.18), int(64*1.18)))

 


carro_jogador_atual = "lambo/lambo.png"
jogador_img_base = pygame.image.load(resource_path(f"imagens/{carro_jogador_atual}")).convert_alpha()
jogador_img = pygame.transform.scale(jogador_img_base, (jogador_largura, jogador_altura))


# -------------------- ENGENHAGEM, SETA E OUTRAS IMAGENS --------------------
try:
    engrenagem_orig = pygame.image.load(resource_path("imagens/engrenagem01.png")).convert_alpha()
except:
    # fallback: gere uma superfície simples se imagem faltar (para evitar crash durante teste)
    engrenagem_orig = pygame.Surface((48,48), pygame.SRCALPHA)
    pygame.draw.circle(engrenagem_orig, (200,200,200), (24,24), 22, 3)


ENGRENAGEM_SIZE = 48
ENGRENAGEM_HOVER = 56
engrenagem_img = pygame.transform.smoothscale(engrenagem_orig, (ENGRENAGEM_SIZE, ENGRENAGEM_SIZE))
engrenagem_hover_img = pygame.transform.smoothscale(engrenagem_orig, (ENGRENAGEM_HOVER, ENGRENAGEM_HOVER))


try:
    seta_voltar_orig = pygame.image.load(resource_path("imagens/seta_voltar.png")).convert_alpha()
    seta_voltar_img = pygame.transform.smoothscale(seta_voltar_orig, (40, 40))
    seta_voltar_hover = pygame.transform.smoothscale(seta_voltar_orig, (46, 46))
except:
    seta_voltar_img = pygame.Surface((40,40), pygame.SRCALPHA)
    pygame.draw.polygon(seta_voltar_img, (255,255,255), [(30,10),(10,20),(30,30)])
    seta_voltar_hover = pygame.transform.smoothscale(seta_voltar_img, (46,46))
    
    
try:
    lixo_img_orig = pygame.image.load(resource_path("imagens/lixo.png")).convert_alpha()
    trofeu_img_orig = pygame.image.load(resource_path("imagens/trofeu.png")).convert_alpha()
except:
    # Fallbacks simples caso as imagens não existam
    lixo_img_orig = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.rect(lixo_img_orig, (200, 0, 0), (8, 8, 24, 24), 3)
    pygame.draw.rect(lixo_img_orig, (200, 0, 0), (14, 4, 12, 4))

    trofeu_img_orig = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(trofeu_img_orig, (255, 215, 0), (20, 16), 8)
    pygame.draw.rect(trofeu_img_orig, (255, 215, 0), (15, 22, 10, 10))


LIXO_SIZE = 40
TROFEU_SIZE = 40

lixo_img = pygame.transform.smoothscale(lixo_img_orig, (LIXO_SIZE, LIXO_SIZE))
trofeu_img = pygame.transform.smoothscale(trofeu_img_orig, (TROFEU_SIZE, TROFEU_SIZE)) 


try:
    perfil_img_orig = pygame.image.load(resource_path("imagens/perfil.png")).convert_alpha()
except:
    # Fallback caso a imagem falhe
    perfil_img_orig = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(perfil_img_orig, (200, 200, 200), (20, 12), 8)
    pygame.draw.ellipse(perfil_img_orig, (200, 200, 200), (10, 22, 20, 15))


PERFIL_SIZE = 40
PERFIL_HOVER_SIZE = 46
perfil_img = pygame.transform.smoothscale(perfil_img_orig, (PERFIL_SIZE, PERFIL_SIZE))
perfil_hover_img = pygame.transform.smoothscale(perfil_img_orig, (PERFIL_HOVER_SIZE, PERFIL_HOVER_SIZE))

# -------------------- SETAS (mesmo padrão do perfil) --------------------
SETA_ARROW_SIZE = 60
SETA_ARROW_HOVER = 70

# seta direita
try:
    seta_direita_orig = pygame.image.load(resource_path("imagens/seta_dir.png")).convert_alpha()
except:
    seta_direita_orig = pygame.Surface((SETA_ARROW_SIZE, SETA_ARROW_SIZE), pygame.SRCALPHA)
seta_direita_img = pygame.transform.smoothscale(seta_direita_orig, (SETA_ARROW_SIZE, SETA_ARROW_SIZE))
seta_direita_hover = pygame.transform.smoothscale(seta_direita_orig, (SETA_ARROW_HOVER, SETA_ARROW_HOVER))

# seta esquerda
try:
    seta_esquerda_orig = pygame.image.load(resource_path("imagens/seta_esq.png")).convert_alpha()
except:
    seta_esquerda_orig = pygame.Surface((SETA_ARROW_SIZE, SETA_ARROW_SIZE), pygame.SRCALPHA)
seta_esquerda_img = pygame.transform.smoothscale(seta_esquerda_orig, (SETA_ARROW_SIZE, SETA_ARROW_SIZE))
seta_esquerda_hover = pygame.transform.smoothscale(seta_esquerda_orig, (SETA_ARROW_HOVER, SETA_ARROW_HOVER))

# seta cima
try:
    seta_cima_orig = pygame.image.load(resource_path("imagens/seta_cima.png")).convert_alpha()
except:
    seta_cima_orig = pygame.Surface((SETA_ARROW_SIZE, SETA_ARROW_SIZE), pygame.SRCALPHA)
seta_cima_img = pygame.transform.smoothscale(seta_cima_orig, (SETA_ARROW_SIZE, SETA_ARROW_SIZE))
seta_cima_hover = pygame.transform.smoothscale(seta_cima_orig, (SETA_ARROW_HOVER, SETA_ARROW_HOVER))

# seta baixo
try:
    seta_baixo_orig = pygame.image.load(resource_path("imagens/seta_baixo.png")).convert_alpha()
except:
    seta_baixo_orig = pygame.Surface((SETA_ARROW_SIZE, SETA_ARROW_SIZE), pygame.SRCALPHA)
seta_baixo_img = pygame.transform.smoothscale(seta_baixo_orig, (SETA_ARROW_SIZE, SETA_ARROW_SIZE))
seta_baixo_hover = pygame.transform.smoothscale(seta_baixo_orig, (SETA_ARROW_HOVER, SETA_ARROW_HOVER))



# -------------------- MÚSICAS --------------------
musica_facil = resource_path("musicas/02.mp3")
musica_medio = resource_path("musicas/01.mp3")
musica_dificil = resource_path("musicas/03.mp3")

som_facil = pygame.mixer.Sound(musica_facil)
som_medio = pygame.mixer.Sound(musica_medio)
som_dificil = pygame.mixer.Sound(musica_dificil)


# -------------------- VARIÁVEL DE DIFICULDADE --------------------
dificuldade = "Facil"  # padrão


# -------------------- VARIÁVEIS DE MUTE --------------------
mute_facil = False
mute_medio = False
mute_dificil = False
mute_menu = False


# -------------------- VOLUMES INICIAIS --------------------
vol_facil = 0.3
vol_medio = 0.3
vol_dificil = 0.3
vol_menu = 0.3


# -------------------- FASE ATUAL RODANDO --------------------
fase_rodando = None  # Nenhuma fase está rodando inicialmente


# -------------------- DADOS DO USUÁRIO --------------------
usuario_nome = None
usuario_id = None
dados_usuario = {
    "email": "",
    "senha": "",
    "nome": "",
    "vezes_facil": 0,
    "vezes_medio": 0,
    "vezes_dificil": 0,
    "tempo_total": 0
}



# -------------------- LIMITES DE CARACTERES --------------------
EMAIL_MAX_CHARS = 50
SENHA_MAX_CHARS = 20
NOME_MAX_CHARS = 25


 # -------------------- TELA DE CADASTRO   --------------------
# -------------------- TELA DE CADASTRO   --------------------
def tela_cadastro():
    global usuario_nome, usuario_id, dados_usuario, cursor_atual 
    rodando_cadastro = True
    input_ativo = None
    email_texto = ""
    senha_texto = ""
    nome_texto = ""

    seta_rect = pygame.Rect(10, 10, 40, 40)
    
    fonte_input = pygame.font.Font(None, 36)
    fonte_botao_pequena = pygame.font.Font(None, 28)
    fonte_media_pequena = pygame.font.Font(None, 30)
    
    y_base = 160
    
    campo_email = pygame.Rect(largura//2 - 150, y_base + 20, 300, 40)
    campo_senha = pygame.Rect(largura//2 - 150, y_base + 110, 300, 40)
    campo_nome  = pygame.Rect(largura//2 - 150, y_base + 200, 300, 40)
    
    confirmar_rect = pygame.Rect(largura//2 - 165, y_base + 300, 150, 50)
    login_rect = pygame.Rect(largura//2 + 15, y_base + 300, 150, 50)

    mensagem_erro = ""
    tempo_erro = 0

    # helper: considera "   " como vazio
    def is_blank(s):
        return s is None or s.strip() == ""

    while rodando_cadastro:
        tela.blit(fundo_config, (0, 0))
        
        titulo = fonte_titulo.render("Cadastro", True, branco)
        tela.blit(titulo, (largura//2 - titulo.get_width()//2, 80))

        mouse_pos = pygame.mouse.get_pos()
        hover_any = False

        # cursor blink
        tempo_atual = pygame.time.get_ticks()
        mostrar_cursor = (tempo_atual // 500) % 2 == 0
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if seta_rect.collidepoint(mouse_pos):
                    return 
                
                if campo_email.collidepoint(mouse_pos):
                    input_ativo = "email"
                elif campo_senha.collidepoint(mouse_pos):
                    input_ativo = "senha"
                elif campo_nome.collidepoint(mouse_pos):
                    input_ativo = "nome"
                
                elif confirmar_rect.collidepoint(mouse_pos):
                    # nova verificação: campos não podem ser vazios ou só espaços
                    if is_blank(email_texto) or is_blank(nome_texto) or is_blank(senha_texto):
                        mensagem_erro = "Ainda há campos vazios — preencha-os, por favor!"
                        tempo_erro = pygame.time.get_ticks()
                    else:
                        norm_email = email_texto.strip().lower()
                        norm_nome  = nome_texto.strip().lower()

                        existe = False
                        try:
                            with open("usuarios.txt", "r", encoding="utf-8") as f:
                                conteudo = f.read().split("\n\n")
                                for bloco in conteudo:
                                    if not bloco.strip():
                                        continue
                                    dados = {}
                                    for linha in bloco.split("\n"):
                                        if ":" in linha:
                                            chave, valor = linha.split(":", 1)
                                            dados[chave.strip()] = valor.strip()
                                    if dados:
                                        if dados.get("email","").strip().lower() == norm_email or dados.get("nome","").strip().lower() == norm_nome:
                                            existe = True
                                            break
                        except FileNotFoundError:
                            pass

                        if existe:
                            mensagem_erro = "E-mail ou nome já cadastrado!"
                            tempo_erro = pygame.time.get_ticks()
                        else:
                            try:
                                with open("usuarios.txt", "r", encoding="utf-8") as f:
                                    linhas = f.readlines()
                                    ultimo_id = 0
                                    for linha in linhas:
                                        if linha.startswith("id:"):
                                            try:
                                                ultimo_id = max(ultimo_id, int(linha.split(":")[1].strip()))
                                            except Exception:
                                                pass
                                    novo_id = ultimo_id + 1
                            except FileNotFoundError:
                                novo_id = 1

                            with open("usuarios.txt", "a", encoding="utf-8") as f:
                                f.write(f"id:{novo_id}\n")
                                f.write(f"email:{email_texto.strip()}\n")
                                f.write(f"senha:{senha_texto}\n")
                                f.write(f"nome:{nome_texto.strip()}\n\n")

                            atualizar_usuario_logado(novo_id, nome_texto.strip(), {
                                "email": email_texto.strip(),
                                "senha": senha_texto,
                                "nome": nome_texto.strip(),
                                "vezes_facil": 0,
                                "vezes_medio": 0,
                                "vezes_dificil": 0,
                                "tempo_total": 0
                            })

                            menu()
                            return

                elif login_rect.collidepoint(mouse_pos):
                    tela_login()
                    return

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                
                if input_ativo == "email":
                    if evento.key == pygame.K_BACKSPACE:
                        email_texto = email_texto[:-1]
                    elif len(email_texto) < EMAIL_MAX_CHARS and evento.unicode.isprintable():
                        email_texto += evento.unicode
                elif input_ativo == "senha":
                    if evento.key == pygame.K_BACKSPACE:
                        senha_texto = senha_texto[:-1]
                    elif len(senha_texto) < SENHA_MAX_CHARS and evento.unicode.isprintable():
                        senha_texto += evento.unicode
                elif input_ativo == "nome":
                    if evento.key == pygame.K_BACKSPACE:
                        nome_texto = nome_texto[:-1]
                    elif len(nome_texto) < NOME_MAX_CHARS and evento.unicode.isprintable():
                        nome_texto += evento.unicode

        # --- Desenho dos campos ---
        campos_info = [
            (campo_email, "E-mail", email_texto, "email", y_base + 0),
            (campo_senha, "Senha", "*" * len(senha_texto), "senha", y_base + 90),
            (campo_nome, "Nome de Usuário", nome_texto, "nome", y_base + 180),
        ]

        for campo, label, valor, nome_input, label_y in campos_info:
            # label (sempre desenhado centralizado — não será afetado pelo scroll do texto)
            texto_label_render = fonte_media_pequena.render(label, True, branco)
            tela.blit(texto_label_render, (largura//2 - texto_label_render.get_width()//2, label_y))
            
            cor_caixa = (180, 180, 255) if input_ativo == nome_input else (150, 150, 150)
            pygame.draw.rect(tela, cor_caixa, campo, border_radius=5)
            pygame.draw.rect(tela, branco, campo, 2, border_radius=5) 
            
            # renderiza o texto (já mascarado para senha)
            texto_surface = fonte_input.render(valor, True, branco)

            # calcula scroll lateral se texto maior que a área disponível
            margem = 10
            largura_disponivel = campo.width - 2 * margem
            largura_texto = texto_surface.get_width()
            scroll_x = max(0, largura_texto - largura_disponivel)

            # cria surface máscara com mesmo tamanho da área visível do campo
            mask_surf = pygame.Surface((largura_disponivel, campo.height), pygame.SRCALPHA)
            mask_surf.fill((0, 0, 0, 0))  # transparente

            # posição vertical para centrar o texto dentro da máscara
            y_offset = (campo.height - texto_surface.get_height()) // 2
            # blita o texto na máscara com deslocamento negativo (clip automático)
            mask_surf.blit(texto_surface, (-scroll_x, y_offset))

            # blita a máscara na tela (no local do campo, respeitando margem)
            tela.blit(mask_surf, (campo.x + margem, campo.y))

            # desenha a barra (caret) piscante no final do texto quando o campo está ativo
            if input_ativo == nome_input and mostrar_cursor:
                # posição do cursor relativa ao conteúdo
                cursor_pos_in_mask = largura_texto - scroll_x
                # limita cursor dentro da área visível
                cursor_pos_in_mask = max(0, min(cursor_pos_in_mask, largura_disponivel))
                cursor_x = campo.x + margem + cursor_pos_in_mask
                cursor_y = campo.y + 6
                cursor_h = campo.height - 12
                pygame.draw.rect(tela, branco, (cursor_x, cursor_y, 2, cursor_h))

            if campo.collidepoint(mouse_pos):
                hover_any = True

        # --- Botões CONFIRMAR e LOGIN (iguais à tela de login) ---
        for botao_rect, texto in [(confirmar_rect, "CONFIRMAR"), (login_rect, "LOGIN")]:
            cor_botao = azul_hover if botao_rect.collidepoint(mouse_pos) else azul
            pygame.draw.rect(tela, cor_botao, botao_rect, border_radius=8)
            texto_render = fonte_botao_pequena.render(texto, True, branco)
            tela.blit(texto_render, (botao_rect.centerx - texto_render.get_width()//2,
                                     botao_rect.centery - texto_render.get_height()//2))
            if botao_rect.collidepoint(mouse_pos):
                hover_any = True

        # --- Mensagem de erro ---
        if mensagem_erro and pygame.time.get_ticks() - tempo_erro < 2000:
            erro_render = fonte_botao_pequena.render(mensagem_erro, True, vermelho)
            tela.blit(erro_render, (largura//2 - erro_render.get_width()//2, altura - 100))

        # --- Botão voltar ---
        if seta_rect.collidepoint(mouse_pos):
            center = (seta_rect.x + 20, seta_rect.y + 20)
            hover_w, hover_h = seta_voltar_hover.get_size()
            tela.blit(seta_voltar_hover, (center[0] - hover_w//2, center[1] - hover_h//2))
            hover_any = True
        else:
            tela.blit(seta_voltar_img, (seta_rect.x, seta_rect.y))

        # --- Cursor ---
        if hover_any and cursor_atual != "hand":
            set_cursor("hand")
            cursor_atual = "hand"
        elif not hover_any and cursor_atual != "arrow":
            set_cursor("arrow")
            cursor_atual = "arrow"

        pygame.display.flip()
        clock.tick(fps)


        
# -------------------- TELA DE LOGIN   --------------------
def tela_login():
    global usuario_nome, dados_usuario, cursor_atual
    rodando_login = True
    input_ativo = None
    email_texto = ""
    senha_texto = ""

    seta_rect = pygame.Rect(10, 10, 40, 40)
    
    fonte_input = pygame.font.Font(None, 36)
    fonte_botao_pequena = pygame.font.Font(None, 28)
    fonte_media_pequena = pygame.font.Font(None, 30)
    
    y_base = 180 
    
    # Campos
    campo_email = pygame.Rect(largura//2 - 150, y_base + 20, 300, 40)
    campo_senha = pygame.Rect(largura//2 - 150, y_base + 110, 300, 40)
    
    login_rect = pygame.Rect(largura//2 - 75, y_base + 200, 150, 50)

    while rodando_login:
        tela.blit(fundo_config, (0, 0))
        
        titulo = fonte_titulo.render("Login", True, branco)
        tela.blit(titulo, (largura//2 - titulo.get_width()//2, 80))

        mouse_pos = pygame.mouse.get_pos()
        hover_any = False

        tempo_atual = pygame.time.get_ticks()
        mostrar_cursor = (tempo_atual // 500) % 2 == 0  # pisca a cada meio segundo
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if seta_rect.collidepoint(mouse_pos):
                    return 
                
                if campo_email.collidepoint(mouse_pos):
                    input_ativo = "email"
                elif campo_senha.collidepoint(mouse_pos):
                    input_ativo = "senha"
                
                elif login_rect.collidepoint(mouse_pos):
                    # --- Verifica login ---
                    try:
                        with open("usuarios.txt", "r", encoding="utf-8") as f:
                            conteudo = f.read().split("\n\n")
                            usuarios = []
                            for bloco in conteudo:
                                if bloco.strip() == "":
                                    continue
                                dados = {}
                                for linha in bloco.split("\n"):
                                    linha = linha.strip()
                                    if linha == "" or ":" not in linha:
                                        continue
                                    chave, valor = linha.split(":", 1)
                                    dados[chave.strip()] = valor.strip()
                                if dados:
                                    usuarios.append(dados)
                    except FileNotFoundError:
                        usuarios = []

                    # Procura usuário
                    encontrado = False
                    for u in usuarios:
                        if u.get("email") == email_texto and u.get("senha") == senha_texto:
                            atualizar_usuario_logado(int(u.get("id")), u.get("nome"), {
                                "email": u.get("email"),
                                "senha": u.get("senha"),
                                "nome": u.get("nome"),
                                "vezes_facil": int(u.get("vezes_facil",0)),
                                "vezes_medio": int(u.get("vezes_medio",0)),
                                "vezes_dificil": int(u.get("vezes_dificil",0)),
                                "tempo_total": int(u.get("tempo_total",0))
                            })
                            rodando_login = False
                            encontrado = True
                            break

                    if not encontrado:
                        erro_texto = fonte_media_pequena.render("Email ou senha incorretos!", True, vermelho)
                        tela.blit(erro_texto, (largura//2 - erro_texto.get_width()//2, login_rect.y - 40))
                        pygame.display.flip()
                        pygame.time.delay(1200)

                else:
                    input_ativo = None

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    return
                
                if input_ativo == "email":
                    if evento.key == pygame.K_BACKSPACE:
                        email_texto = email_texto[:-1]
                    elif len(email_texto) < EMAIL_MAX_CHARS and evento.unicode.isprintable():
                        email_texto += evento.unicode
                elif input_ativo == "senha":
                    if evento.key == pygame.K_BACKSPACE:
                        senha_texto = senha_texto[:-1]
                    elif len(senha_texto) < SENHA_MAX_CHARS and evento.unicode.isprintable():
                        senha_texto += evento.unicode

        # --- Desenho dos campos ---
        campos_info = [
            (campo_email, "E-mail", email_texto, "email", y_base + 0),
            (campo_senha, "Senha", "*" * len(senha_texto), "senha", y_base + 90),
        ]

        for campo, label, valor, nome_input, label_y in campos_info:
            texto_label_render = fonte_media_pequena.render(label, True, branco)
            tela.blit(texto_label_render, (largura//2 - texto_label_render.get_width()//2, label_y))
            
            cor_caixa = (180, 180, 255) if input_ativo == nome_input else (150, 150, 150)
            pygame.draw.rect(tela, cor_caixa, campo, border_radius=5)
            pygame.draw.rect(tela, branco, campo, 2, border_radius=5) 
            
            max_largura = campo.width - 20
            texto_surface = fonte_input.render(valor, True, branco)
            if texto_surface.get_width() > max_largura:
                for i in range(len(valor)):
                    sub_surface = fonte_input.render(valor[i:], True, branco)
                    if sub_surface.get_width() <= max_largura:
                        texto_surface = sub_surface
                        break
            tela.blit(texto_surface, (campo.x + 10, campo.y + 5))

            # --- CARET (barra) PISCANTE ---
            if input_ativo == nome_input and mostrar_cursor:
                cursor_x = campo.x + 10 + texto_surface.get_width() + 2
                cursor_y = campo.y + 6
                cursor_h = campo.height - 12
                # garante que o cursor fique dentro do campo
                cursor_x = min(cursor_x, campo.x + campo.width - 6)
                pygame.draw.rect(tela, branco, (cursor_x, cursor_y, 2, cursor_h))

            if campo.collidepoint(mouse_pos):
                hover_any = True

        # --- Botão LOGIN ---
        cor_login = azul_hover if login_rect.collidepoint(mouse_pos) else azul
        pygame.draw.rect(tela, cor_login, login_rect, border_radius=8)
        texto_render = fonte_botao_pequena.render("LOGIN", True, branco)
        tela.blit(texto_render, (login_rect.centerx - texto_render.get_width()//2,
                                  login_rect.centery - texto_render.get_height()//2))
        if login_rect.collidepoint(mouse_pos):
            hover_any = True

        # --- Botão voltar ---
        if seta_rect.collidepoint(mouse_pos):
            center = (seta_rect.x + 20, seta_rect.y + 20)
            hover_w, hover_h = seta_voltar_hover.get_size()
            tela.blit(seta_voltar_hover, (center[0] - hover_w//2, center[1] - hover_h//2))
            hover_any = True
        else:
            tela.blit(seta_voltar_img, (seta_rect.x, seta_rect.y))

        # --- Cursor do mouse ---
        if 'cursor_atual' not in globals():
            cursor_atual = "arrow"

        if hover_any and cursor_atual != "hand":
            set_cursor("hand")
            cursor_atual = "hand"
        elif not hover_any and cursor_atual != "arrow":
            set_cursor("arrow")
            cursor_atual = "arrow"

        pygame.display.flip()
        clock.tick(fps)


        
# -------------------- FUNÇÕES DE USUÁRIO LOGADO --------------------      
def atualizar_usuario_logado(novo_id, novo_nome, dados=None):
    global usuario_id, usuario_nome, dados_usuario
    # Se antes não tinha usuário logado, deleta arquivo padrão
    if usuario_id is None and os.path.exists("pontuacoes.txt"):
        try:
            os.remove("pontuacoes.txt")
        except Exception:
            pass

    usuario_id = novo_id
    usuario_nome = novo_nome

    # atualiza dados básicos (email/nome/contadores se fornecidos)
    if dados:
        # cópia protege o original
        dados_usuario = dados.copy()
    else:
        # garante que o dicionário exista
        if not isinstance(dados_usuario, dict):
            dados_usuario = {}

    # Garante que exista o arquivo de pontuações do usuário (vazio se não existir)
    arquivo_usuario = get_arquivo_pontuacoes()
    if not os.path.exists(arquivo_usuario):
        open(arquivo_usuario, "w", encoding="utf-8").close()

    # Agora recarrega resumo das pontuações do arquivo e atualiza dados_usuario
    resumo = carregar_resumo_pontuacoes()
    # garante chaves
    dados_usuario.setdefault("email", dados_usuario.get("email", ""))
    dados_usuario.setdefault("senha", dados_usuario.get("senha", ""))
    dados_usuario.setdefault("nome", dados_usuario.get("nome", usuario_nome or ""))
    dados_usuario["tempo_total"] = resumo.get("tempo_total", 0)
    dados_usuario["vezes_facil"] = resumo.get("vezes_facil", 0)
    dados_usuario["vezes_medio"] = resumo.get("vezes_medio", 0)
    dados_usuario["vezes_dificil"] = resumo.get("vezes_dificil", 0)
    
    
# -------------------- TELA DE PERFIL  --------------------
def tela_perfil():
    global usuario_nome, dados_usuario, cursor_atual, usuario_id
    rodando_perfil = True
    fonte_perfil = pygame.font.Font(None, 40)
    fonte_media_pequena = pygame.font.Font(None, 30)

    pedindo_confirmacao = False
    box_alterar_ativo = False
    scroll_offset = 0

    seta_rect = pygame.Rect(10, 10, 40, 40)
    lixo_rect = lixo_img.get_rect(topright=(largura - 10, 10))
    alterar_usuario_rect = pygame.Rect(10, altura - 60, 220, 50)

    confirm_box_rect = pygame.Rect(largura//2 - 175, altura//2 - 100, 350, 200)
    btn_sim_rect = pygame.Rect(largura//2 - 100, altura//2 + 20, 80, 40)
    btn_nao_rect = pygame.Rect(largura//2 + 20, altura//2 + 20, 80, 40)

    altura_box = 350
    linha_altura = 40

    lista_usuarios = []

    # ----- Primeira sincronização (quando abrir a tela) -----
    if not isinstance(dados_usuario, dict):
        dados_usuario = {}
    dados_usuario.setdefault("email", "")
    dados_usuario.setdefault("senha", "")
    dados_usuario.setdefault("nome", usuario_nome or "")
    dados_usuario.setdefault("tempo_total", 0)
    dados_usuario.setdefault("vezes_facil", 0)
    dados_usuario.setdefault("vezes_medio", 0)
    dados_usuario.setdefault("vezes_dificil", 0)

    if usuario_nome:
        resumo_inicial = carregar_resumo_pontuacoes()
        dados_usuario["tempo_total"] = resumo_inicial.get("tempo_total", dados_usuario.get("tempo_total", 0))
        dados_usuario["vezes_facil"] = resumo_inicial.get("vezes_facil", dados_usuario.get("vezes_facil", 0))
        dados_usuario["vezes_medio"] = resumo_inicial.get("vezes_medio", dados_usuario.get("vezes_medio", 0))
        dados_usuario["vezes_dificil"] = resumo_inicial.get("vezes_dificil", dados_usuario.get("vezes_dificil", 0))

    while rodando_perfil:
        mouse_pos = pygame.mouse.get_pos()
        hover_any = False

        # Se a box estiver ativa, calcule já o rect e posições (garante que não seja None)
        alterar_box_rect = None
        if box_alterar_ativo:
            box_width = 350
            box_height = altura_box
            box_x = int(largura) // 2 - box_width // 2
            box_y = int(altura) // 2 - box_height // 2
            alterar_box_rect = pygame.Rect(box_x, box_y, box_width, box_height)

            # layout dos 3 botões abaixo da box (recalcula para uso em eventos e desenho)
            btn_largura = 110
            btn_altura = 40
            espacamento = 20
            total_largura = btn_largura * 3 + espacamento * 2
            inicio_x = largura//2 - total_largura//2
            btn_y = box_y + box_height + 15

            cadastrar_rect = pygame.Rect(inicio_x, btn_y, btn_largura, btn_altura)
            logout_rect = pygame.Rect(inicio_x + btn_largura + espacamento, btn_y, btn_largura, btn_altura)
            fechar_rect = pygame.Rect(inicio_x + 2*(btn_largura + espacamento), btn_y, btn_largura, btn_altura)
        else:
            cadastrar_rect = logout_rect = fechar_rect = None

        # -------------------- EVENTOS --------------------
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                return

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # --- 1) Se estamos na confirmação de delete: tratar SIM/NÃO exclusivamente ---
                if pedindo_confirmacao:
                    if btn_sim_rect.collidepoint(mouse_pos):
                        # ==== AÇÃO DE DELETAR (mantive seu fluxo original) ====
                        try:
                            with open("usuarios.txt", "r", encoding="utf-8") as f:
                                conteudo = [b for b in f.read().split("\n\n") if b.strip() != ""]
                        except FileNotFoundError:
                            conteudo = []

                        usuarios_orig = []
                        id_para_deletar = None
                        for bloco in conteudo:
                            dados = {}
                            for linha in bloco.split("\n"):
                                if ":" not in linha:
                                    continue
                                chave, valor = linha.split(":", 1)
                                dados[chave.strip()] = valor.strip()
                            if dados:
                                usuarios_orig.append(dados)
                                if dados.get("nome") == usuario_nome:
                                    try:
                                        id_para_deletar = int(dados.get("id"))
                                    except:
                                        id_para_deletar = None

                        if id_para_deletar is None and usuario_id is not None:
                            try:
                                id_para_deletar = int(usuario_id)
                            except:
                                id_para_deletar = None

                        nova_lista = []
                        for u in usuarios_orig:
                            try:
                                uid = int(u.get("id")) if u.get("id") not in (None, "") else None
                            except:
                                uid = None

                            if id_para_deletar is not None:
                                if uid == id_para_deletar:
                                    continue
                                else:
                                    nova_lista.append(u)
                            else:
                                if u.get("nome") == usuario_nome:
                                    continue
                                else:
                                    nova_lista.append(u)

                        try:
                            with open("usuarios.txt", "w", encoding="utf-8") as f:
                                for u in nova_lista:
                                    uid = u.get("id", "")
                                    if uid != "":
                                        f.write(f"id:{uid}\n")
                                    else:
                                        f.write("id:0\n")
                                    f.write(f"email:{u.get('email','')}\n")
                                    f.write(f"senha:{u.get('senha','')}\n")
                                    f.write(f"nome:{u.get('nome','')}\n\n")
                        except Exception as e:
                            print("Erro ao regravar usuarios.txt:", e)

                        if id_para_deletar is not None:
                            arquivo_del = f"pontuacoes_id{id_para_deletar}.txt"
                            try:
                                if os.path.exists(arquivo_del):
                                    os.remove(arquivo_del)
                            except:
                                pass

                        # decide novo login automático
                        novo_login_id = None
                        novo_login_dados = None
                        ids_existentes = []
                        mapa_por_id = {}
                        for u in nova_lista:
                            try:
                                iu = int(u.get("id"))
                                ids_existentes.append(iu)
                                mapa_por_id[iu] = u
                            except:
                                continue
                        ids_existentes = sorted(set(ids_existentes))

                        if id_para_deletar is not None and ids_existentes:
                            menores = [i for i in ids_existentes if i < id_para_deletar]
                            if menores:
                                novo_login_id = max(menores)
                                novo_login_dados = mapa_por_id.get(novo_login_id)
                            else:
                                maiores = [i for i in ids_existentes if i > id_para_deletar]
                                if maiores:
                                    novo_login_id = min(maiores)
                                    novo_login_dados = mapa_por_id.get(novo_login_id)

                        if novo_login_id is None and nova_lista:
                            ultimo = nova_lista[-1]
                            try:
                                cand = int(ultimo.get("id"))
                                novo_login_id = cand
                                novo_login_dados = ultimo
                            except:
                                novo_login_id = None
                                novo_login_dados = None

                        if novo_login_id is None:
                            usuario_nome = None
                            usuario_id = None
                            dados_usuario = {"email":"", "senha":"", "nome":"", "vezes_facil":0, "vezes_medio":0, "vezes_dificil":0, "tempo_total":0}
                            pedindo_confirmacao = False
                            tela_cadastro()
                            return
                        else:
                            try:
                                atualizar_usuario_logado(novo_login_id, novo_login_dados.get("nome",""), novo_login_dados)
                            except Exception:
                                usuario_id = novo_login_id
                                usuario_nome = novo_login_dados.get("nome","")
                            pedindo_confirmacao = False
                            box_alterar_ativo = False
                            scroll_offset = 0
                            continue  # IMPORTANTÍSSIMO: não processe mais este clique

                    elif btn_nao_rect.collidepoint(mouse_pos):
                        # Fecha a caixa de confirmação e ignora o resto do clique
                        pedindo_confirmacao = False
                        continue
                    else:
                        # Se clicou fora do Sim/Não enquanto a caixa está aberta, ignore o clique
                        continue

                # --- 2) Se a caixa de alteração está aberta, tratar somente os cliques da box (evita None) ---
                if box_alterar_ativo:
                    # Prioridade: Cadastrar -> Logout -> Fechar -> Lista
                    if cadastrar_rect and cadastrar_rect.collidepoint(mouse_pos):
                        box_alterar_ativo = False
                        tela_cadastro()
                        continue

                    if logout_rect and logout_rect.collidepoint(mouse_pos):
                        usuario_nome = None
                        usuario_id = None
                        dados_usuario = {"email": "", "senha": "", "nome": "", "vezes_facil":0, "vezes_medio":0, "vezes_dificil":0, "tempo_total":0}
                        try:
                            open("pontuacoes.txt", "a", encoding="utf-8").close()
                        except Exception:
                            pass
                        box_alterar_ativo = False
                        pedindo_confirmacao = False
                        scroll_offset = 0
                        try:
                            tela_cadastro()
                        except Exception as e:
                            print("Erro ao chamar tela_cadastro:", e)
                        return

                    if fechar_rect and fechar_rect.collidepoint(mouse_pos):
                        box_alterar_ativo = False
                        continue

                    # clique nas linhas da lista de usuários (consistência: largura 330)
                    if alterar_box_rect:
                        for i, usuario in enumerate(lista_usuarios):
                            y_line = alterar_box_rect.y + 60 + i * linha_altura - scroll_offset
                            linha_rect = pygame.Rect(alterar_box_rect.x + 10, y_line, 330, linha_altura)
                            if linha_rect.collidepoint(mouse_pos):
                                uid = usuario.get("id")
                                try:
                                    novo_id = int(uid) if uid is not None else None
                                except:
                                    novo_id = None
                                atualizar_usuario_logado(novo_id, usuario.get("nome",""), usuario)
                                box_alterar_ativo = False
                                break
                        continue

                # --- 3) fluxo normal quando nenhuma caixa está ativa ---
                # Botão voltar
                if seta_rect.collidepoint(mouse_pos):
                    return

                # Lixo → abre confirmação para deletar conta atual
                if lixo_rect.collidepoint(mouse_pos):
                    if usuario_nome:
                        pedindo_confirmacao = True
                        continue

                # Abrir/fechar box alterar usuário (toggle)
                if alterar_usuario_rect.collidepoint(mouse_pos):
                    box_alterar_ativo = not box_alterar_ativo
                    scroll_offset = 0
                    lista_usuarios = []
                    if box_alterar_ativo:
                        try:
                            with open("usuarios.txt", "r", encoding="utf-8") as f:
                                conteudo = f.read().split("\n\n")
                                for bloco in conteudo:
                                    if bloco.strip() == "":
                                        continue
                                    dados = {}
                                    for linha in bloco.split("\n"):
                                        if ":" not in linha:
                                            continue
                                        chave, valor = linha.split(":",1)
                                        dados[chave.strip()] = valor.strip()
                                    if dados:
                                        lista_usuarios.append(dados)
                        except FileNotFoundError:
                            lista_usuarios = []
                    continue

            # Scroll via roda (quando box ativa)
            if evento.type == pygame.MOUSEWHEEL:
                if box_alterar_ativo:
                    visiveis = altura_box - 100
                    conteudo_total = len(lista_usuarios) * linha_altura
                    max_scroll = max(0, conteudo_total - visiveis)
                    scroll_offset = max(0, scroll_offset - int(evento.y * 20))
                    scroll_offset = min(scroll_offset, max_scroll)

        # -------------------- SINCRONIZAÇÃO ANTES DE DESENHAR --------------------
        if usuario_nome:
            resumo_atual = carregar_resumo_pontuacoes()
            dados_usuario.setdefault("email", dados_usuario.get("email",""))
            dados_usuario.setdefault("senha", dados_usuario.get("senha",""))
            dados_usuario.setdefault("nome", dados_usuario.get("nome", usuario_nome))
            dados_usuario["tempo_total"] = resumo_atual.get("tempo_total", dados_usuario.get("tempo_total", 0))
            dados_usuario["vezes_facil"] = resumo_atual.get("vezes_facil", dados_usuario.get("vezes_facil", 0))
            dados_usuario["vezes_medio"] = resumo_atual.get("vezes_medio", dados_usuario.get("vezes_medio", 0))
            dados_usuario["vezes_dificil"] = resumo_atual.get("vezes_dificil", dados_usuario.get("vezes_dificil", 0))

        # -------------------- DESENHO --------------------
        tela.blit(fundo_config, (0,0))
        texto_titulo = fonte_perfil.render("Perfil", True, branco)
        tela.blit(texto_titulo, (largura//2 - texto_titulo.get_width()//2, 80))

        # Informações do usuário (posicionadas mais à esquerda)
        y = 180
        info_x = largura//2 - 220

        infos = {
            "E-mail": dados_usuario.get("email",""),
            "Usuário": dados_usuario.get("nome",""),
            "Tempo total": f"{dados_usuario.get('tempo_total',0)}s",
            "Fácil jogado": f"{dados_usuario.get('vezes_facil',0)}x",
            "Médio jogado": f"{dados_usuario.get('vezes_medio',0)}x",
            "Difícil jogado": f"{dados_usuario.get('vezes_dificil',0)}x"
        }
        for label, valor in infos.items():
            texto_info = fonte_media_pequena.render(f"{label}: {valor}", True, branco)
            tela.blit(texto_info, (info_x, y))
            y += 40

        # Botões voltar e lixo
        if seta_rect.collidepoint(mouse_pos):
            tela.blit(seta_voltar_hover, (seta_rect.x-5, seta_rect.y-5))
            hover_any = True
        else:
            tela.blit(seta_voltar_img, (seta_rect.x, seta_rect.y))

        if lixo_rect.collidepoint(mouse_pos):
            hover_any = True
        tela.blit(lixo_img, lixo_rect)

        # Botão Alterar Usuário
        cor_alt = azul_hover if alterar_usuario_rect.collidepoint(mouse_pos) else azul
        pygame.draw.rect(tela, cor_alt, alterar_usuario_rect, border_radius=10)
        texto_alt = fonte_botao.render("Alterar Usuário", True, branco)
        tela.blit(texto_alt, (alterar_usuario_rect.centerx - texto_alt.get_width()//2,
                              alterar_usuario_rect.centery - texto_alt.get_height()//2))
        if alterar_usuario_rect.collidepoint(mouse_pos):
            hover_any = True

        # Box de alterar usuário (quando ativo)
        if box_alterar_ativo and alterar_box_rect:
            pygame.draw.rect(tela, cinza, alterar_box_rect, border_radius=10)
            pygame.draw.rect(tela, branco, alterar_box_rect, 2, border_radius=10)

            titulo = fonte_media_pequena.render("Selecionar Usuário", True, branco)
            tela.blit(titulo, (alterar_box_rect.centerx - titulo.get_width()//2, alterar_box_rect.y + 10))

            visiveis = altura_box - 100
            conteudo_total = len(lista_usuarios) * linha_altura
            max_scroll = max(0, conteudo_total - visiveis)
            scroll_offset = max(0, min(scroll_offset, max_scroll))

            for i, usuario in enumerate(lista_usuarios):
                y_line = alterar_box_rect.y + 60 + i * linha_altura - scroll_offset
                if alterar_box_rect.y + 50 <= y_line <= alterar_box_rect.y + alterar_box_rect.height - 40:
                    linha_rect = pygame.Rect(alterar_box_rect.x + 10, y_line, alterar_box_rect.width - 20, linha_altura)
                    cor_linha = azul_hover if linha_rect.collidepoint(mouse_pos) else azul
                    pygame.draw.rect(tela, cor_linha, linha_rect, border_radius=5)
                    texto_usuario = usuario.get('nome', '')
                    tela.blit(fonte_media_pequena.render(texto_usuario, True, branco),
                              (linha_rect.x + 10, linha_rect.y + 5))
                    if linha_rect.collidepoint(mouse_pos):
                        hover_any = True

            # Scrollbar da box (se precisar)
            if conteudo_total > visiveis:
                barra_altura = max(40, int((visiveis / conteudo_total) * (altura_box - 60)))
                if max_scroll > 0:
                    barra_y = int(alterar_box_rect.y + 60 + (scroll_offset / max_scroll) * (altura_box - 60 - barra_altura))
                else:
                    barra_y = alterar_box_rect.y + 60
                trilho_rect = pygame.Rect(alterar_box_rect.right - 15, alterar_box_rect.y + 60, 8, altura_box - 60)
                barra_rect_vis = pygame.Rect(alterar_box_rect.right - 15, barra_y, 8, barra_altura)
                pygame.draw.rect(tela, (100,100,100), trilho_rect, border_radius=5)
                pygame.draw.rect(tela, (200,200,200), barra_rect_vis, border_radius=5)

            # Botões Cadastrar | Logout | Fechar (centralizados abaixo da box)
            pygame.draw.rect(tela, azul_hover if cadastrar_rect.collidepoint(mouse_pos) else azul, cadastrar_rect, border_radius=10)
            pygame.draw.rect(tela, (200, 120, 40) if logout_rect.collidepoint(mouse_pos) else (160, 100, 30), logout_rect, border_radius=10)
            pygame.draw.rect(tela, vermelho if fechar_rect.collidepoint(mouse_pos) else (200,60,60), fechar_rect, border_radius=10)

            tela.blit(fonte_media_pequena.render("Cadastrar", True, branco), (cadastrar_rect.centerx - 55, cadastrar_rect.centery - 12))
            tela.blit(fonte_media_pequena.render("Logout", True, branco), (logout_rect.centerx - 35, logout_rect.centery - 12))
            tela.blit(fonte_media_pequena.render("Fechar", True, branco), (fechar_rect.centerx - 25, fechar_rect.centery - 12))

            if cadastrar_rect.collidepoint(mouse_pos) or logout_rect.collidepoint(mouse_pos) or fechar_rect.collidepoint(mouse_pos):
                hover_any = True

        # Cursor
        if hover_any and cursor_atual != "hand":
            set_cursor("hand")
            cursor_atual = "hand"
        elif not hover_any and cursor_atual != "arrow":
            set_cursor("arrow")
            cursor_atual = "arrow"

        # Confirmação deletar (desenho)
        if pedindo_confirmacao:
            s = pygame.Surface((largura, altura), pygame.SRCALPHA)
            s.fill((0, 0, 0, 150))
            tela.blit(s, (0, 0))

            pygame.draw.rect(tela, cinza, confirm_box_rect, border_radius=10)
            pygame.draw.rect(tela, branco, confirm_box_rect, 2, border_radius=10)

            texto_conf = fonte_perfil.render("Deletar conta?", True, branco)
            tela.blit(texto_conf, (confirm_box_rect.centerx - texto_conf.get_width()//2, confirm_box_rect.y + 30))

            cor_sim = vermelho if btn_sim_rect.collidepoint(mouse_pos) else (200, 60, 60)
            cor_nao = azul if btn_nao_rect.collidepoint(mouse_pos) else (60, 60, 200)
            pygame.draw.rect(tela, cor_sim, btn_sim_rect, border_radius=8)
            pygame.draw.rect(tela, cor_nao, btn_nao_rect, border_radius=8)

            tela.blit(fonte_media_pequena.render("Sim", True, branco), (btn_sim_rect.centerx - 15, btn_sim_rect.centery - 10))
            tela.blit(fonte_media_pequena.render("Não", True, branco), (btn_nao_rect.centerx - 15, btn_nao_rect.centery - 10))

        pygame.display.flip()
        clock.tick(fps)




# -------------------- FUNÇÃO PARA OBTER NOME DO ARQUIVO DE PONTUAÇÕES --------------------
def get_arquivo_pontuacoes():
    global usuario_id
    if usuario_id:
        return f"pontuacoes_id{usuario_id}.txt"
    else:
        return "pontuacoes.txt"


# -------------------- FUNÇÃO PARA SALVAR PONTUAÇÕES --------------------
def salvar_pontuacao(dificuldade, tempo, pontos):
    arquivo_nome = get_arquivo_pontuacoes()
    tempo_formatado = str(datetime.timedelta(seconds=tempo))
    with open(arquivo_nome, "a", encoding="utf-8") as f:
        f.write(f"{dificuldade};{tempo_formatado};{pontos}\n")



# -------------------- RESUMO DE PONTUAÇÕES (total de tempo + counts por fase) --------------------
def carregar_resumo_pontuacoes():
    """
    Lê o arquivo retornado por get_arquivo_pontuacoes() e devolve
    um dicionário com tempo_total (em segundos) e contagens por fase.
    """
    arquivo = get_arquivo_pontuacoes()
    resumo = {
        "tempo_total": 0,
        "vezes_facil": 0,
        "vezes_medio": 0,
        "vezes_dificil": 0
    }

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                partes = linha.strip().split(";")
                if len(partes) != 3:
                    continue
                fase, tempo_str, _ = partes
                # aceita formats como H:M:S ou HH:MM:SS
                try:
                    h, m, s = map(int, tempo_str.split(":"))
                except Exception:
                    # se algo anômalo, ignora a linha
                    continue
                segundos = h*3600 + m*60 + s
                resumo["tempo_total"] += segundos

                f_lower = fase.strip().lower()
                # aceitamos "facil", "fácil", "medio", "médio", "dificil", "difícil"
                if "fac" in f_lower:   # cobre 'facil' e 'fácil'
                    resumo["vezes_facil"] += 1
                elif "med" in f_lower: # 'medio' / 'médio'
                    resumo["vezes_medio"] += 1
                elif "dif" in f_lower: # 'dificil' / 'difícil'
                    resumo["vezes_dificil"] += 1
    except FileNotFoundError:
        # arquivo ainda não existe -> zeros
        pass
    except PermissionError:
        pass

    return resumo



# -------------------- FUNÇÃO PARA CARREGAR PONTUAÇÕES --------------------        
def carregar_pontuacoes():
    pontuacoes = {"Facil": [], "Medio": [], "Dificil": []}
    arquivo_caminho = get_arquivo_pontuacoes()

    try:
        with open(arquivo_caminho, "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                partes = linha.strip().split(";")
                if len(partes) == 3:
                    fase, tempo_str, pontos_str = partes
                    h, m, s = map(int, tempo_str.split(":"))
                    tempo_seg = h*3600 + m*60 + s
                    pontuacoes[fase].append({"tempo": tempo_seg, "pontos": int(pontos_str)})
    except (FileNotFoundError, PermissionError):
        pass  # ignora erro e continua com lista vazia

    return pontuacoes



# -------------------- FUNÇÃO PARA LIMPAR PONTUAÇÕES --------------------
def limpar_pontuacoes():
    pontuacoes = carregar_pontuacoes()
    novas_linhas = []

    for fase in pontuacoes:
        ordenadas = sorted(pontuacoes[fase], key=lambda x: (-x["pontos"], x["tempo"]))
        melhores = ordenadas[:3]  # mantém só as 3 melhores

        for p in melhores:
            tempo_formatado = str(datetime.timedelta(seconds=p["tempo"]))
            novas_linhas.append(f"{fase};{tempo_formatado};{p['pontos']}\n")

    arquivo_caminho = get_arquivo_pontuacoes()
    with open(arquivo_caminho, "w", encoding="utf-8") as arquivo:
        arquivo.writelines(novas_linhas)
        


# -------------------- TELA DE PONTUAÇÕES --------------------        
def tela_pontuacoes():
    global usuario_nome, usuario_id

    rodando_pontuacao = True
    cursor_atual = "arrow"
    mostrar_top3 = False  # botão troféu para top 3

    # Retângulo dos botões
    seta_rect = pygame.Rect(10, 10, 40, 40)
    lixo_rect = pygame.Rect(largura - 50, 10, 40, 40)
    trofeu_rect = pygame.Rect(largura - 100, 10, 40, 40)

    # Define arquivo do usuário ou padrão
    if usuario_id is None:
        arquivo_pontuacao = "pontuacoes.txt"
        deletar_arquivo_no_sair = True  # será apagado se fechar sem usuário
    else:
        arquivo_pontuacao = f"pontuacoes_id{usuario_id}.txt"
        deletar_arquivo_no_sair = False

    # Garante que o arquivo existe
    if not os.path.exists(arquivo_pontuacao):
        open(arquivo_pontuacao, "w", encoding="utf-8").close()

    # Função para carregar pontuações por fase
    def carregar_pontuacoes():
        pontuacoes = {"Facil": [], "Medio": [], "Dificil": []}
        try:
            with open(arquivo_pontuacao, "r", encoding="utf-8") as f:
                for linha in f:
                    partes = linha.strip().split(";")
                    if len(partes) == 3:
                        fase, tempo_str, pontos_str = partes
                        h, m, s = map(int, tempo_str.split(":"))
                        tempo_seg = h*3600 + m*60 + s
                        pontuacoes[fase].append({"tempo": tempo_seg, "pontos": int(pontos_str)})
        except:
            pass
        return pontuacoes

    # Função para salvar apenas os top 3 de cada fase
    def salvar_top3(pontuacoes):
        novas_linhas = []
        for fase in pontuacoes:
            ordenadas = sorted(pontuacoes[fase], key=lambda x: (-x["pontos"], x["tempo"]))[:3]
            for p in ordenadas:
                tempo_formatado = str(datetime.timedelta(seconds=p["tempo"]))
                novas_linhas.append(f"{fase};{tempo_formatado};{p['pontos']}\n")
        with open(arquivo_pontuacao, "w", encoding="utf-8") as f:
            f.writelines(novas_linhas)

    # scroll state
    scroll_offset = 0
    scroll_speed = 30
    dragging_thumb = False
    drag_offset_y = 0

    # área de conteúdo (onde as pontuações aparecem)
    content_left = 50
    content_top = 100
    content_width = largura - 100
    content_height = altura - 150  # ajusta conforme layout

    while rodando_pontuacao:
        tela.blit(fundo_InfoPonto, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        hover_any = False

        # --- Ícones ---
        # Voltar
        tela.blit(seta_voltar_img, (seta_rect.x, seta_rect.y))
        # Lixo
        tela.blit(lixo_img, lixo_rect)
        # Troféu
        tela.blit(trofeu_img, trofeu_rect)

        # Cursor hover para ícones
        if seta_rect.collidepoint(mouse_pos) or lixo_rect.collidepoint(mouse_pos) or trofeu_rect.collidepoint(mouse_pos):
            hover_any = True
            set_cursor("hand")
        else:
            # cursor atualizado mais abaixo dependendo de hover_any
            pass

        # --- Prepara conteúdo em memória (calcula altura total) ---
        pontuacoes = carregar_pontuacoes()
        lines = []  # cada item: (text_surface, x, y_absolute)
        y = content_top
        line_gap = 8

        for fase in ["Facil", "Medio", "Dificil"]:
            texto_fase = fonte_media.render(f"{fase}", True, branco)
            lines.append((texto_fase, content_left, y))
            y += texto_fase.get_height() + 6

            if pontuacoes[fase]:
                ordenadas = sorted(pontuacoes[fase], key=lambda x: (-x["pontos"], x["tempo"]))
                if mostrar_top3:
                    ordenadas = ordenadas[:3]

                for p in ordenadas:
                    tempo_formatado = str(datetime.timedelta(seconds=p['tempo']))
                    texto = fonte_pequena.render(f"tempo: {tempo_formatado}   pontuação: {p['pontos']}", True, branco)
                    lines.append((texto, content_left + 30, y))
                    y += texto.get_height() + 4
            else:
                texto = fonte_pequena.render("sem registros", True, branco)
                lines.append((texto, content_left + 30, y))
                y += texto.get_height() + 4

            y += 20  # espaço entre fases

        total_content_height = max(0, y - content_top)
        max_scroll = max(0, total_content_height - content_height)
        # clamp scroll_offset
        if scroll_offset < 0:
            scroll_offset = 0
        if scroll_offset > max_scroll:
            scroll_offset = max_scroll

        # --- Desenha somente linhas visíveis (aplica scroll_offset) ---
        for surf, x_pos, y_abs in lines:
            y_on_screen = y_abs - scroll_offset
            # desenha se dentro da área visível (com pequena margem)
            if y_on_screen + surf.get_height() >= content_top and y_on_screen <= content_top + content_height:
                tela.blit(surf, (x_pos, y_on_screen))

        # --- Desenha scrollbar se necessário ---
        thumb_rect = None
        if max_scroll > 0:
            # track background
            track_x = content_left + content_width - 14
            track_rect = pygame.Rect(track_x, content_top, 10, content_height)
            pygame.draw.rect(tela, (50,50,50), track_rect, border_radius=5)

            # thumb size proporcional
            thumb_h = max(30, int((content_height * content_height) / total_content_height))
            # avoid division by zero:
            if max_scroll > 0:
                thumb_y = content_top + int((scroll_offset / max_scroll) * (content_height - thumb_h))
            else:
                thumb_y = content_top
            thumb_rect = pygame.Rect(track_x, thumb_y, 10, thumb_h)
            pygame.draw.rect(tela, (180,180,180), thumb_rect, border_radius=5)

            # hover detection on thumb
            if thumb_rect.collidepoint(mouse_pos):
                hover_any = True

        # atualiza cursor se não for ícone
        if hover_any and cursor_atual != "hand":
            set_cursor("hand")
            cursor_atual = "hand"
        elif not hover_any and cursor_atual != "arrow":
            set_cursor("arrow")
            cursor_atual = "arrow"

        pygame.display.update()

        # --- Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                if deletar_arquivo_no_sair:
                    try:
                        os.remove(arquivo_pontuacao)
                    except Exception:
                        pass
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando_pontuacao = False

            # Compatibilidade roda antiga (botões 4/5)
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button in (4, 5):
                if evento.button == 4:  # up
                    scroll_offset = max(0, scroll_offset - scroll_speed)
                else:  # 5 down
                    scroll_offset = min(max_scroll, scroll_offset + scroll_speed)

            elif evento.type == pygame.MOUSEWHEEL:
                # negativo -> down (em algumas plataformas), em outras y>0 up
                # usamos y to move opposite: wheel up (y>0) -> scroll up (decrease offset)
                scroll_offset = max(0, min(max_scroll, scroll_offset - int(evento.y * scroll_speed)))

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # clique esquerdo

                # Voltar
                if seta_rect.collidepoint(mouse_pos):
                    rodando_pontuacao = False
                    break

                # Lixo → apaga pontuações
                if lixo_rect.collidepoint(mouse_pos):
                    open(arquivo_pontuacao, "w", encoding="utf-8").close()
                    # recarregar conteúdo e resetar scroll
                    scroll_offset = 0
                    pontuacoes = carregar_pontuacoes()
                    continue

                # Troféu → alterna exibição top3
                if trofeu_rect.collidepoint(mouse_pos):
                    mostrar_top3 = not mostrar_top3
                    scroll_offset = 0
                    continue

                # clique no thumb para arrastar
                if thumb_rect and thumb_rect.collidepoint(mouse_pos):
                    dragging_thumb = True
                    drag_offset_y = mouse_pos[1] - thumb_rect.y
                    continue

            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                # solta arraste do thumb
                dragging_thumb = False

            elif evento.type == pygame.MOUSEMOTION:
                if dragging_thumb and thumb_rect is not None and max_scroll > 0:
                    # calcula nova posição do thumb baseado no mouse
                    new_thumb_y = mouse_pos[1] - drag_offset_y
                    new_thumb_y = max(content_top, min(content_top + content_height - thumb_rect.height, new_thumb_y))
                    # converte para scroll_offset
                    ratio = (new_thumb_y - content_top) / (content_height - thumb_rect.height) if (content_height - thumb_rect.height) > 0 else 0
                    scroll_offset = int(ratio * max_scroll)

        clock.tick(fps)
        
        


# -------------------- FUNÇÃO PARA DELETAR PONTUAÇÕES TEMPORÁRIAS --------------------
def deletar_pontuacoes_temp():
    if 'usuario_id' not in globals() or not usuario_id:
        try:
            os.remove("pontuacoes.txt")
        except FileNotFoundError:
            pass
        
        


# -------------------- TELA DE CONFIGURAÇÕES --------------------
def tela_configuracoes():
    rodando = True
    cursor_atual = "arrow"

    # Aumentamos o botão para caber o texto
    voltar_rect = pygame.Rect(largura//2 - 120, altura - 80, 240, 55)
    seta_rect = pygame.Rect(10, 10, 40, 40)

    while rodando:
        tela.blit(fundo_config, (0, 0))  # usa o fundo próprio da tela de configurações
        titulo = fonte_titulo.render("Configurações", True, branco)
        tela.blit(titulo, (largura//2 - titulo.get_width()//2, 50))

        mouse_pos = pygame.mouse.get_pos()
        hover_any = False

        # seta voltar
        if seta_rect.collidepoint(mouse_pos):
            tela.blit(seta_voltar_hover, (seta_rect.x - 3, seta_rect.y - 3))
            hover_any = True
        else:
            tela.blit(seta_voltar_img, (seta_rect.x, seta_rect.y))

           

        if hover_any and cursor_atual != "hand":
            set_cursor("hand")

        elif not hover_any and cursor_atual != "arrow":
            set_cursor("arrow")
            
        audio_rect = pygame.Rect(largura//2 - 100, 200, 200, 50)  # exemplo de posição
        # Botão Áudio
        if audio_rect.collidepoint(mouse_pos):
            pygame.draw.rect(tela, azul_hover, audio_rect)
            hover_any = True
        else:
            pygame.draw.rect(tela, azul, audio_rect)
        texto_audio = fonte_botao.render("Áudio", True, branco)
        tela.blit(texto_audio, (
            audio_rect.centerx - texto_audio.get_width()//2,
            audio_rect.centery - texto_audio.get_height()//2
        ))

        pygame.display.update()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if seta_rect.collidepoint(mouse_pos) or voltar_rect.collidepoint(mouse_pos):
                    rodando = False
                    return
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if audio_rect.collidepoint(mouse_pos):
                    tela_audio()  # chama a tela de áudio
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_a:  # tecla A abre áudio
                    tela_audio()
                elif evento.key == pygame.K_ESCAPE:  # tecla Esc volta para o menu
                    rodando = False
                    return
                
                


# -------------------- TELA DE ÁUDIO --------------------
def tela_audio():
    global mute_facil, mute_medio, mute_dificil, mute_menu
    global vol_facil, vol_medio, vol_dificil, vol_menu
    rodando_audio = True
    cursor_atual = "arrow"


    seta_rect = pygame.Rect(10, 10, 40, 40)

    botoes = [
        ("Fase Fácil", "facil"),
        ("Fase Média", "medio"),
        ("Fase Difícil", "dificil"),
        ("Musica do Menu", "menu")
    ]

    while rodando_audio:
        tela.blit(fundo_audio, (0, 0))   
        titulo = fonte_titulo.render("Áudio", True, branco)
        tela.blit(titulo, (largura//2 - titulo.get_width()//2, 50))

        mouse_pos = pygame.mouse.get_pos()
        hover_any = False

        # Botão voltar
        if seta_rect.collidepoint(mouse_pos):
            center = (seta_rect.x + 20, seta_rect.y + 20)
            hover_w, hover_h = seta_voltar_hover.get_size()
            tela.blit(seta_voltar_hover, (center[0] - hover_w//2, center[1] - hover_h//2))
            hover_any = True
        else:
            tela.blit(seta_voltar_img, (seta_rect.x, seta_rect.y))

        botoes_rects = []

        for i, (texto, chave) in enumerate(botoes):
            rect = pygame.Rect(50, 150 + i*100, 300, 50)
            botoes_rects.append(rect)

            cor = vermelho_hover if rect.collidepoint(mouse_pos) else vermelho
            pygame.draw.rect(tela, cor, rect)

            # Estado mute/desmute
            estado = mute_facil if chave=="facil" else mute_medio if chave=="medio" else mute_dificil if chave=="dificil" else mute_menu
            estado_texto = "mutado" if estado else "desmutado"
            tela.blit(fonte_pequena.render(f"{texto} - {estado_texto}", True, branco), (rect.x + 10, rect.y + 5))

            # Volume atual
            vol_atual = vol_facil if chave=="facil" else vol_medio if chave=="medio" else vol_dificil if chave=="dificil" else vol_menu
            vol_perc = int(vol_atual * 100)
            tela.blit(fonte_pequena.render(f"{vol_perc}%", True, branco), (rect.right + 10, rect.y + 15))

            # Botões + e -
            btn_aumentar = pygame.Rect(rect.right + 60, rect.y + 10, 30, 30)
            btn_diminuir = pygame.Rect(rect.right + 100, rect.y + 10, 30, 30)
            botoes_rects.extend([btn_aumentar, btn_diminuir])

            for btn, sinal in [(btn_aumentar, "+"), (btn_diminuir, "-")]:
                pygame.draw.rect(tela, laranja, btn)
                pygame.draw.rect(tela, branco, btn, 1)
                texto_sinal = fonte_pequena.render(sinal, True, branco)
                tela.blit(texto_sinal, (btn.x + 8, btn.y + 5))

                if btn.collidepoint(mouse_pos):
                    hover_any = True

        # Ajuste do cursor (apenas uma vez por frame)
        if hover_any and cursor_atual != "hand":
            set_cursor("hand")

        elif not hover_any and cursor_atual != "arrow":
            set_cursor("arrow")

        pygame.display.update()

                # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:  # Esc volta para configurações
                    rodando_audio = False
                    return    

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if seta_rect.collidepoint(mouse_pos):
                    rodando_audio = False
                    return

                # Verifica clique nos botões
                for i, (texto, chave) in enumerate(botoes):
                    rect = pygame.Rect(50, 150 + i*100, 300, 50)
                    btn_aumentar = pygame.Rect(rect.right + 60, rect.y + 10, 30, 30)
                    btn_diminuir = pygame.Rect(rect.right + 100, rect.y + 10, 30, 30)

                    # --- Mute/Desmute ---
                    if rect.collidepoint(mouse_pos):
                        if chave == "facil":
                            mute_facil = not mute_facil
                            if mute_facil:
                                som_facil.stop()
                            # NÃO tocar música aqui!

                        elif chave == "medio":
                            mute_medio = not mute_medio
                            if mute_medio:
                                som_medio.stop()

                        elif chave == "dificil":
                            mute_dificil = not mute_dificil
                            if mute_dificil:
                                som_dificil.stop()

                        elif chave == "menu":
                            mute_menu = not mute_menu
                            if mute_menu:
                                pygame.mixer.music.stop()
                            else:
                                if not pygame.mixer.music.get_busy():
                                    pygame.mixer.music.load(resource_path("musicas/musica_fundo.mp3"))
                                    pygame.mixer.music.set_volume(vol_menu)
                                    pygame.mixer.music.play(-1)

                    # --- Aumentar volume ---
                    if btn_aumentar.collidepoint(mouse_pos):
                        if chave == "facil":
                            vol_facil = min(vol_facil + 0.1, 1.0)
                            som_facil.set_volume(vol_facil)
                        elif chave == "medio":
                            vol_medio = min(vol_medio + 0.1, 1.0)
                            som_medio.set_volume(vol_medio)
                        elif chave == "dificil":
                            vol_dificil = min(vol_dificil + 0.1, 1.0)
                            som_dificil.set_volume(vol_dificil)
                        elif chave == "menu":
                            vol_menu = min(vol_menu + 0.1, 1.0)
                            pygame.mixer.music.set_volume(vol_menu)

                    # --- Diminuir volume ---
                    if btn_diminuir.collidepoint(mouse_pos):
                        if chave == "facil":
                            vol_facil = max(vol_facil - 0.1, 0.0)
                            som_facil.set_volume(vol_facil)
                        elif chave == "medio":
                            vol_medio = max(vol_medio - 0.1, 0.0)
                            som_medio.set_volume(vol_medio)
                        elif chave == "dificil":
                            vol_dificil = max(vol_dificil - 0.1, 0.0)
                            som_dificil.set_volume(vol_dificil)
                        elif chave == "menu":
                            vol_menu = max(vol_menu - 0.1, 0.0)
                            pygame.mixer.music.set_volume(vol_menu)




# -------------------- FUNÇÃO PARA PARAR MÚSICAS DAS FASES --------------------
def parar_musicas_fase():
    som_facil.stop()
    som_medio.stop()
    som_dificil.stop()

                                
# -------------------- TELA DE INFORMAÇÕES --------------------
def tela_informacoes():
    global cursor_atual
    rodando_info = True

    voltar_rect = pygame.Rect(10, 10, 40, 40)
    fonte_info = pygame.font.Font(None, 24)

    # Controle da rolagem
    scroll_offset = 0
    scroll_speed = 30  # quanto a roda/arraste move por passo
    dragging_thumb = False
    drag_offset_y = 0

    # Texto de informações
    linhas_texto = [
        "            ====*====  INFORMAÇÕES  ====*====",
        "",
        "",
        "IMPORTANTE:",
        "- Caso não crie uma conta e jogue ",
        "  como convidado, ",
        "  suas pontuações serão salvas apenas  ",
        "  temporariamente e serão",
        "  apagadas ao fechar o jogo.",
        "- Recomenda-se criar uma conta para  ",
        "  salvar suas pontuações permanentemente.",
        "",
        "MENU PRINCIPAL:",
        "- ESC: Fecha o jogo",
        "",
         "TELA DE CADASTRO/LOGIN:",
        "- Clicar nos campos de texto para digitar",
        "- Email e nomes de usuário são únicos",
        "  (não podem ser repetidos)",
        "- Senhas são sensíveis a maiúsculas/minúsculas",
        "",
        "PERFIL:",
        "- Lixo no canto superior direito: Deleta a conta",
        "  (apaga também as pontuações associadas)",
        "- Alterar Usuario: Você consegue acessar contas",
        "  das quais você já logou anteriormente",
        "  e você pode criar novas contas",
        "",
        "PERSONALIZAÇÃO:",
        "- SETAS DA TELA: Navega entre as opções",
        "- Seta para cima/baixo: Muda a cor do carro",
        "- Seta para esquerda/direita: ",
        "  Muda o modelo do carro",
        "-Total de 3 modelos de carro e 8 cores diferentes",
        " sendo preto, laranja, vermelho, azul, verde,",
        " amarelo, roxo e rosa ",
        "",
        "JOGO:",
        "- ESC: Volta para o menu principal",
        "- R: Reinicia a fase atual",
        "- Espaço: Pausa/Despausa o jogo",
        "- Usar setas para mover o carro para os lados",
        "",
        "SELECAO DE FASES:",
        "- 1 (ou teclado numerico 1): Inicia fase fácil",
        "- 2 (ou teclado numerico 2): Inicia fase média",
        "- 3 (ou teclado numerico 3): Inicia fase difícil",
        "",
        "PONTUAÇÃO:",
        "- Lixo: Limpa todas as pontuações salvas",
        "- Troféu: alterna mostrando as 3 ",
        "  melhores pontuações",
        "- SCROLL: Rola a tela para cima/baixo",
       "",
        "INFORMAÇÕES:",
        "- SCROLL: Rola a tela para cima/baixo",
        "",
    ]

    # Layout do conteúdo (mesma ideia da tela_pontuacoes)
    content_left = 50
    content_top = 60
    content_width = largura - 100
    content_height = altura - 140  # ajuste visual (pode mudar se quiser)

    # calcula altura total do conteúdo
    altura_conteudo = len(linhas_texto) * 28 + 60
    max_scroll = max(0, altura_conteudo - content_height)

    while rodando_info:
        tela.blit(fundo_InfoPonto, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        hover_any = False

        # --- Desenha conteúdo (aplica scroll_offset) ---
        y = content_top - scroll_offset
        for linha in linhas_texto:
            surf = fonte_info.render(linha, True, branco)
            # desenha somente se visível
            if surf is not None and (y + surf.get_height() >= content_top) and (y <= content_top + content_height):
                tela.blit(surf, (content_left, y))
            y += 28

        # --- Scrollbar (igual à tela_pontuacoes) ---
        thumb_rect = None
        if altura_conteudo > content_height:
            track_x = content_left + content_width - 14
            track_rect = pygame.Rect(track_x, content_top, 10, content_height)
            pygame.draw.rect(tela, (50,50,50), track_rect, border_radius=5)

            thumb_h = max(30, int((content_height * content_height) / altura_conteudo))
            if max_scroll > 0:
                thumb_y = content_top + int((scroll_offset / max_scroll) * (content_height - thumb_h))
            else:
                thumb_y = content_top
            thumb_rect = pygame.Rect(track_x, thumb_y, 10, thumb_h)
            pygame.draw.rect(tela, (180,180,180), thumb_rect, border_radius=5)

            # highlight quando hover no thumb
            if thumb_rect.collidepoint(mouse_pos):
                hover_any = True

        # --- Botão voltar (seta) ---
        if voltar_rect.collidepoint(mouse_pos):
            center = (voltar_rect.x + 20, voltar_rect.y + 20)
            tela.blit(seta_voltar_hover, (center[0] - seta_voltar_hover.get_width()//2,
                                          center[1] - seta_voltar_hover.get_height()//2))
            hover_any = True
        else:
            tela.blit(seta_voltar_img, (voltar_rect.x, voltar_rect.y))

        # cursor
        if hover_any and cursor_atual != "hand":
            set_cursor("hand")
            cursor_atual = "hand"
        elif not hover_any and cursor_atual != "arrow":
            set_cursor("arrow")
            cursor_atual = "arrow"

        pygame.display.update()

        # --- Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # roda do mouse (compatível)
            elif evento.type == pygame.MOUSEWHEEL:
                # roda: y>0 = up, y<0 = down -> diminuímos offset para subir
                scroll_offset = max(0, min(max_scroll, scroll_offset - int(evento.y * scroll_speed)))

            # compatibilidade com botões 4/5 (algumas plataformas)
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button in (4, 5):
                if evento.button == 4:
                    scroll_offset = max(0, scroll_offset - scroll_speed)
                else:
                    scroll_offset = min(max_scroll, scroll_offset + scroll_speed)

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # clique esquerdo

                # voltar
                if voltar_rect.collidepoint(mouse_pos):
                    rodando_info = False
                    return

                # clicar no track para pular (se existir track)
                if altura_conteudo > content_height:
                    track_x = content_left + content_width - 14
                    track_rect = pygame.Rect(track_x, content_top, 10, content_height)
                    if track_rect.collidepoint(mouse_pos) and (thumb_rect is not None):
                        # se clicou acima do thumb, pula uma página
                        if mouse_pos[1] < thumb_rect.y:
                            scroll_offset = max(0, scroll_offset - content_height + 20)
                        elif mouse_pos[1] > thumb_rect.bottom:
                            scroll_offset = min(max_scroll, scroll_offset + content_height - 20)
                        else:
                            # clicou no thumb -> inicia drag
                            dragging_thumb = True
                            drag_offset_y = mouse_pos[1] - thumb_rect.y

                # outros cliques podem ficar aqui...

            elif evento.type == pygame.MOUSEBUTTONUP and evento.button == 1:
                dragging_thumb = False

            elif evento.type == pygame.MOUSEMOTION:
                if dragging_thumb and thumb_rect is not None and max_scroll > 0:
                    # move o thumb junto com o mouse
                    new_thumb_y = mouse_pos[1] - drag_offset_y
                    new_thumb_y = max(content_top, min(content_top + content_height - thumb_rect.height, new_thumb_y))
                    ratio = (new_thumb_y - content_top) / (content_height - thumb_rect.height) if (content_height - thumb_rect.height) > 0 else 0
                    scroll_offset = int(ratio * max_scroll)

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                rodando_info = False
                return

        clock.tick(fps)




# --- Ícones do MENU (64px) ---
def load_icon64(path):
    img = pygame.image.load(resource_path(path)).convert_alpha()
    return pygame.transform.smoothscale(img, (64, 64))

iniciar_icon      = load_icon64("imagens/botao-play.png")
informacoes_icon  = load_icon64("imagens/informacoes.png")
pontuacoes_icon   = load_icon64("imagens/pontuacao-maxima.png")
personalizar_icon = load_icon64("imagens/extra.png")

# Versões hover (move 3px igual seta)
iniciar_icon_hover      = iniciar_icon
informacoes_icon_hover  = informacoes_icon
pontuacoes_icon_hover   = pontuacoes_icon
personalizar_icon_hover = personalizar_icon




# -------------------- MENU PRINCIPAL (ÍCONES) --------------------
def menu():
    global vol_menu, mute_menu, fase_rodando
    rodando_menu = True
    cursor_atual = "arrow"

    fonte_legenda = fonte_botao  # usa legenda igual a da seleção de dificuldade
 

    BASE_Y = 350  # posição inicial mais baixa
    OFFSET = 130   # distância entre ícones

    iniciar_rect      = iniciar_icon.get_rect(center=(largura//2, BASE_Y))
    informacoes_rect  = informacoes_icon.get_rect(center=(largura//2, BASE_Y + OFFSET))
    pontuacoes_rect   = pontuacoes_icon.get_rect(center=(largura//2, BASE_Y + OFFSET*2))
    personalizar_rect = personalizar_icon.get_rect(center=(largura//2, BASE_Y + OFFSET*3))
    # Ícones do topo
    engr_rect   = pygame.Rect(10, 10, ENGRENAGEM_SIZE, ENGRENAGEM_SIZE)
    perfil_rect = pygame.Rect(largura - PERFIL_SIZE - 15, 10, PERFIL_SIZE, PERFIL_SIZE)

    sair_rect = pygame.Rect(largura - 120, altura - 70, 110, 55)

    while rodando_menu:

        if not mute_menu and not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(resource_path("musicas/musica_fundo.mp3"))
            pygame.mixer.music.set_volume(vol_menu)
            pygame.mixer.music.play(-1)

        tela.blit(fundo_menu, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        hover_any = False

        # ----------- FUNÇÃO PADRÃO PARA DESENHAR ÍCONES -----------
        def draw_icon(img, hover_img, rect, texto):
            nonlocal hover_any

            if rect.collidepoint(mouse_pos):
                new_rect = hover_img.get_rect(center=rect.center)
                tela.blit(hover_img, (new_rect.x - 3, new_rect.y - 3))
                hover_any = True
            else:
                tela.blit(img, rect)

            # legenda
            txt = fonte_legenda.render(texto, True, branco)
            tela.blit(txt, (rect.centerx - txt.get_width()//2, rect.bottom + 6))

        # ----------- DESENHAR ÍCONES DO MENU -----------
        draw_icon(iniciar_icon,      iniciar_icon_hover,      iniciar_rect,      "Iniciar")
        draw_icon(informacoes_icon,  informacoes_icon_hover,  informacoes_rect,  "Informações")
        draw_icon(pontuacoes_icon,   pontuacoes_icon_hover,   pontuacoes_rect,   "Pontuações")
        draw_icon(personalizar_icon, personalizar_icon_hover, personalizar_rect, "Personalizar")

        # ----------- ÍCONE DE CONFIGURAÇÃO -----------
        if engr_rect.collidepoint(mouse_pos):
            center = (engr_rect.x + ENGRENAGEM_SIZE//2, engr_rect.y + ENGRENAGEM_SIZE//2)
            w, h = engrenagem_hover_img.get_size()
            tela.blit(engrenagem_hover_img, (center[0] - w//2 - 3, center[1] - h//2 - 3))
            hover_any = True
        else:
            tela.blit(engrenagem_img, (engr_rect.x, engr_rect.y))

        # ----------- ÍCONE DE PERFIL -----------
        if perfil_rect.collidepoint(mouse_pos):
            center = (perfil_rect.x + PERFIL_SIZE//2, perfil_rect.y + PERFIL_SIZE//2)
            w, h = perfil_hover_img.get_size()
            tela.blit(perfil_hover_img, (center[0] - w//2 - 3, center[1] - h//2 - 3))
            hover_any = True
        else:
            tela.blit(perfil_img, (perfil_rect.x, perfil_rect.y))

        # Nome de usuário
        if usuario_nome:
            txt_user = fonte_botao.render(usuario_nome, True, branco)
            tela.blit(txt_user, (perfil_rect.x - txt_user.get_width() - 10, perfil_rect.y + 5))

        # ----------- BOTÃO SAIR (único retangular) -----------
        if sair_rect.collidepoint(mouse_pos):
            pygame.draw.rect(tela, vermelho_hover, sair_rect)
            hover_any = True
        else:
            pygame.draw.rect(tela, vermelho, sair_rect)
        txt_sair = fonte_botao.render("SAIR", True, branco)
        tela.blit(txt_sair, (sair_rect.centerx - txt_sair.get_width()//2,
                             sair_rect.centery - txt_sair.get_height()//2))

        # Cursor
        set_cursor("hand" if hover_any else "arrow")

        pygame.display.update()

        # ----------- EVENTOS -----------
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                if iniciar_rect.collidepoint(mouse_pos):
                    rodando_menu = False
                    selecionar_dificuldade()
                    jogar()

                elif informacoes_rect.collidepoint(mouse_pos):
                    tela_informacoes()

                elif pontuacoes_rect.collidepoint(mouse_pos):
                    tela_pontuacoes()

                elif personalizar_rect.collidepoint(mouse_pos):
                    tela_personalizacao()

                elif engr_rect.collidepoint(mouse_pos):
                    tela_configuracoes()

                elif perfil_rect.collidepoint(mouse_pos):
                    tela_perfil() if usuario_nome else tela_cadastro()

                elif sair_rect.collidepoint(mouse_pos):
                    deletar_pontuacoes_temp()
                    pygame.quit(); sys.exit()

            # Teclas rápidas
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    rodando_menu = False
                    selecionar_dificuldade()
                    jogar()
                elif evento.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                elif evento.key == pygame.K_c:
                    tela_configuracoes()
                elif evento.key == pygame.K_i:
                    tela_informacoes()
                elif evento.key == pygame.K_p:
                    tela_pontuacoes()
                    
                    



 # -------------------- TELA DE PERSONALIZAÇÃO --------------------
def tela_personalizacao():
    global cursor_atual, carro_jogador_atual
    rodando = True

    # --- Configuração inicial ---
    modelos = ["lambo","gtr", "camaro" ]
    modelo_atual_idx = 0

    cores_por_modelo = {}
    for modelo in modelos:
        pasta = resource_path(f"imagens/{modelo}")
        arquivos = os.listdir(pasta)
        pngs = [f for f in arquivos if f.lower().endswith(".png")]

        inicial = [f for f in pngs if all(cor not in f for cor in 
            ["Amarelo","Azul","Verde","Vermelho","Roxo","Rosa","Laranja"])]
        variantes = [f for f in pngs if f not in inicial]

        cores_por_modelo[modelo] = inicial + sorted(variantes)

    cor_atual_idx = 0

    def carrega_imagem(modelo, cor_idx):
        arquivo = cores_por_modelo[modelo][cor_idx]
        caminho = resource_path(f"imagens/{modelo}/{arquivo}")
        img = pygame.image.load(caminho).convert_alpha()

        largura_carro = 180
        altura_carro = int(largura_carro * 1.5)

        return pygame.transform.smoothscale(img, (largura_carro, altura_carro)), arquivo

    carro_img, arquivo_selecionado = carrega_imagem(modelos[modelo_atual_idx], cor_atual_idx)

    # --- Seta de voltar ---
    seta_rect = pygame.Rect(10, 10, 40, 40)

    # --- Botão confirmar ---
    confirmar_rect = pygame.Rect(largura // 2 - 120, altura - 100, 240, 60)

    # Controle de alerta
    alerta_timer = 0
    alerta_texto = fonte_media.render("Carro selecionado!", True, branco)

    while rodando:
        tela.blit(fundo_config, (0, 0))

        # --- Título ---
        titulo = fonte_titulo.render("Personalização", True, branco)
        tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, 50))

        mouse_pos = pygame.mouse.get_pos()
        hover_any = False

        # --- Seta de voltar ---
        if seta_rect.collidepoint(mouse_pos):
            tela.blit(seta_voltar_hover, (seta_rect.x - 3, seta_rect.y - 3))
            hover_any = True
        else:
            tela.blit(seta_voltar_img, (seta_rect.x, seta_rect.y))

        # --- Carro central ---
        carro_rect = carro_img.get_rect(center=(largura // 2, altura // 2))
        tela.blit(carro_img, carro_rect)

        # --- Posiciona setas ---
        seta_gap = 80
        esq_center = (carro_rect.left - seta_gap, carro_rect.centery)
        dir_center = (carro_rect.right + seta_gap, carro_rect.centery)
        cima_center = (carro_rect.centerx, carro_rect.top - seta_gap)
        baixo_center = (carro_rect.centerx, carro_rect.bottom + seta_gap)

        # --- Função de hover das setas ---
        def desenha_seta(img, hover_img, center):
            rect = img.get_rect(center=center)
            if rect.collidepoint(mouse_pos):
                tela.blit(hover_img, hover_img.get_rect(center=center))
                return True
            else:
                tela.blit(img, rect)
                return False

        if desenha_seta(seta_esquerda_img, seta_esquerda_hover, esq_center): hover_any = True
        if desenha_seta(seta_direita_img, seta_direita_hover, dir_center): hover_any = True
        if desenha_seta(seta_cima_img, seta_cima_hover, cima_center): hover_any = True
        if desenha_seta(seta_baixo_img, seta_baixo_hover, baixo_center): hover_any = True

        # --- Botão CONFIRMAR ---
        if confirmar_rect.collidepoint(mouse_pos):
            pygame.draw.rect(tela, verde_hover, confirmar_rect, border_radius=10)
            hover_any = True
        else:
            pygame.draw.rect(tela, verde, confirmar_rect, border_radius=10)

        texto_conf = fonte_botao.render("CONFIRMAR", True, branco)
        tela.blit(texto_conf, (confirmar_rect.centerx - texto_conf.get_width() // 2,
                               confirmar_rect.centery - texto_conf.get_height() // 2))

        # --- Mostra alerta (por 1.2 segundos) ---
        if alerta_timer > 0:
            alerta_timer -= 1
            tela.blit(alerta_texto, (largura // 2 - alerta_texto.get_width() // 2, altura - 160))

        # --- Cursor ---
        if hover_any: set_cursor("hand")
        else: set_cursor("arrow")

        pygame.display.update()

        # --- Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                # voltar
                if seta_rect.collidepoint(mouse_pos):
                    rodando = False
                    return

                # trocar modelo
                if desenha_seta(seta_esquerda_img, seta_esquerda_hover, esq_center):
                    modelo_atual_idx = (modelo_atual_idx - 1) % len(modelos)
                    cor_atual_idx = 0
                    carro_img, arquivo_selecionado = carrega_imagem(modelos[modelo_atual_idx], cor_atual_idx)

                if desenha_seta(seta_direita_img, seta_direita_hover, dir_center):
                    modelo_atual_idx = (modelo_atual_idx + 1) % len(modelos)
                    cor_atual_idx = 0
                    carro_img, arquivo_selecionado = carrega_imagem(modelos[modelo_atual_idx], cor_atual_idx)

                # trocar cor
                if desenha_seta(seta_cima_img, seta_cima_hover, cima_center):
                    cor_atual_idx = (cor_atual_idx + 1) % len(cores_por_modelo[modelos[modelo_atual_idx]])
                    carro_img, arquivo_selecionado = carrega_imagem(modelos[modelo_atual_idx], cor_atual_idx)

                if desenha_seta(seta_baixo_img, seta_baixo_hover, baixo_center):
                    cor_atual_idx = (cor_atual_idx - 1) % len(cores_por_modelo[modelos[modelo_atual_idx]])
                    carro_img, arquivo_selecionado = carrega_imagem(modelos[modelo_atual_idx], cor_atual_idx)

                 # --- CONFIRMAR SELEÇÃO ---
                if confirmar_rect.collidepoint(mouse_pos):

                    # salva caminho (modelo/arquivo.png)
                    carro_jogador_atual = f"{modelos[modelo_atual_idx]}/{arquivo_selecionado}"

                    # atualiza a imagem do jogador globalmente
                    global jogador_img_base, jogador_img

                    nova_base = pygame.image.load(resource_path(f"imagens/{carro_jogador_atual}")).convert_alpha()
                    jogador_img_base = nova_base
                    jogador_img = pygame.transform.scale(jogador_img_base, (jogador_largura, jogador_altura))

                    # alerta
                    alerta_timer = 1200


            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                    return



 
#    # --- Ícones DE DIFICULDADE (64px) ---
def load_icon64(path):
    img = pygame.image.load(resource_path(path)).convert_alpha()
    return pygame.transform.smoothscale(img, (64, 64))

icone_facil   = load_icon64("imagens/icone_facil.png")
icone_medio   = load_icon64("imagens/icone_medio.png")
icone_dificil = load_icon64("imagens/icone_dificil.png")
 
 
 
 # -------------------- SELEÇÃO DE DIFICULDADE --------------------
def selecionar_dificuldade():
    global dificuldade, cursor_atual
    rodando = True
    cursor_atual = "arrow"

    # Botão Seta Voltar (padrão)
    seta_rect = pygame.Rect(10, 10, 40, 40)

    # Ícones no centro
    facil_rect   = icone_facil.get_rect(center=(largura//2, 240))
    medio_rect   = icone_medio.get_rect(center=(largura//2, 360))
    dificil_rect = icone_dificil.get_rect(center=(largura//2, 480))

    fonte_legenda = fonte_pequena if "fonte_pequena" in globals() else fonte_botao

    while rodando:
        tela.blit(fundo_InfoPonto, (0, 0))

        titulo = fonte_titulo.render("Selecione a Dificuldade", True, branco)
        tela.blit(titulo, (largura//2 - titulo.get_width()//2, 80))

        mouse_pos = pygame.mouse.get_pos()
        hover_any = False

        # ------------------- SETA VOLTAR (estilo antigo) -------------------
        if seta_rect.collidepoint(mouse_pos):
            tela.blit(seta_voltar_hover, (seta_rect.x - 3, seta_rect.y - 3))
            hover_any = True
        else:
            tela.blit(seta_voltar_img, seta_rect)


        # ------------------- FUNÇÃO ÍCONES (estilo seta) -------------------
        def draw_icon(base_img, hover_img, rect, texto):
            nonlocal hover_any

            # hover estilo seta (move -3px)
            if rect.collidepoint(mouse_pos):
                img = hover_img
                new_rect = img.get_rect(center=rect.center)
                tela.blit(img, (new_rect.x - 3, new_rect.y - 3))
                hover_any = True
            else:
                tela.blit(base_img, rect)

            # legenda
            txt = fonte_legenda.render(texto, True, branco)
            tela.blit(txt, (rect.centerx - txt.get_width()//2, rect.bottom + 8))


        # Ícones
        draw_icon(icone_facil,   icone_facil_hover,   facil_rect,   "Fácil")
        draw_icon(icone_medio,   icone_medio_hover,   medio_rect,   "Médio")
        draw_icon(icone_dificil, icone_dificil_hover, dificil_rect, "Difícil")


        # Cursor
        set_cursor("hand" if hover_any else "arrow")

        pygame.display.update()

        # ---------------------- EVENTOS ----------------------
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:

                # Voltar (usando exatamente o seu sistema antigo)
                if seta_rect.collidepoint(mouse_pos):
                    rodando = False
                    menu()
                    return

                # Seleção da dificuldade
                if facil_rect.collidepoint(mouse_pos):
                    dificuldade = "Facil"; return
                if medio_rect.collidepoint(mouse_pos):
                    dificuldade = "Medio"; return
                if dificil_rect.collidepoint(mouse_pos):
                    dificuldade = "Dificil"; return

            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_ESCAPE, pygame.K_BACKSPACE):
                    rodando = False
                    menu()
                    return
                if evento.key in (pygame.K_1, pygame.K_KP1):
                    dificuldade = "Facil"; return
                if evento.key in (pygame.K_2, pygame.K_KP2):
                    dificuldade = "Medio"; return
                if evento.key in (pygame.K_3, pygame.K_KP3):
                    dificuldade = "Dificil"; return
                    
                    

# -------------------- FUNÇÃO DO JOGO --------------------
def jogar():
    global fase_rodando
    fase_rodando = dificuldade.lower()  # "facil", "medio" ou "dificil"

    pausado = False  # estado de pausa
    mostrar_hitbox = False  # Hitbox inicialmente invisível

    # Parar qualquer música anterior
    pygame.mixer.music.stop()
    som_facil.stop()
    som_medio.stop()
    som_dificil.stop()

    # Posição inicial do jogador
    jogador_x = largura // 2 - jogador_largura // 2
    jogador_y = altura - jogador_altura - 60
    jogador = pygame.Rect(jogador_x, jogador_y, jogador_largura, jogador_altura)

    # Lista de obstáculos e pontuação
    obstaculos = []
    pontos = 0
    contador_gerar = 0

    # Ajusta conforme a dificuldade
    if dificuldade == "Facil":
        fundo_jogo_atual = fundo_facil
        obstaculo_img_atual = obstaculo_facil_img
        velocidade_obstaculo = 4
        tempo_gerar_obstaculo = 40
        if not mute_facil:
            som_facil.play(-1)
    elif dificuldade == "Medio":
        fundo_jogo_atual = fundo_medio
        obstaculo_img_atual = obstaculo_medio_img
        velocidade_obstaculo = 6
        tempo_gerar_obstaculo = 30
        if not mute_medio:
            som_medio.play(-1)
    else:  # Dificil
        fundo_jogo_atual = fundo_dificil
        obstaculo_img_atual = obstaculo_dificil_img
        velocidade_obstaculo = 8
        tempo_gerar_obstaculo = 25
        if not mute_dificil:
            som_dificil.play(-1)

    # Timer
    tempo_inicial = pygame.time.get_ticks()
    tempo_pausado = 0  # tempo acumulado enquanto pausado
    ultimo_tick = tempo_inicial

    rodando = True

    while rodando:
        clock.tick(fps)
        tela.blit(fundo_jogo_atual, (0, 0))

        tick_atual = pygame.time.get_ticks()
        if pausado:
            tempo_pausado += tick_atual - ultimo_tick
        ultimo_tick = tick_atual

        tempo_decorrido = (tick_atual - tempo_inicial - tempo_pausado) // 1000

        # --- EVENTOS ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_F3:
                    mostrar_hitbox = not mostrar_hitbox  # alterna visibilidade
                elif evento.key == pygame.K_ESCAPE:
                    parar_musicas_fase()
                    pygame.mixer.music.stop()  # para qualquer música da fase

                    return menu()  # volta para o menu
                elif evento.key == pygame.K_r:  # reinicia a fase
                    return jogar()
                elif evento.key == pygame.K_SPACE:  # pausa/despausa
                    pausado = not pausado
                

        # --- LÓGICA DE MOVIMENTO E OBSTÁCULOS ---
        if not pausado:
            # Movimento do jogador
            jogador_vel = jogador_vel_base + pontos * 0.05
            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT] and jogador.x > 0:
                jogador.x -= jogador_vel
            if teclas[pygame.K_RIGHT] and jogador.x < largura - jogador_largura:
                jogador.x += jogador_vel

            # Gerar obstáculos
            contador_gerar += 1
            if contador_gerar >= tempo_gerar_obstaculo:
                obstaculo_x = random.randint(0, largura - obstaculo_largura)
                obstaculo_y = -obstaculo_altura
                obstaculos.append(pygame.Rect(obstaculo_x, obstaculo_y, obstaculo_largura, obstaculo_altura))
                contador_gerar = 0

            # Atualizar obstáculos
            for obstaculo in obstaculos[:]:
                obstaculo.y += velocidade_obstaculo

                # Hitboxes reduzidas para colisão
                hitbox_jogador = pygame.Rect(jogador.x + 5, jogador.y + 5, jogador_largura - 10, jogador_altura - 10)
                hitbox_obstaculo = pygame.Rect(obstaculo.x + 5, obstaculo.y + 5, obstaculo_largura - 10, obstaculo_altura - 10)

                # Colisão
                if hitbox_jogador.colliderect(hitbox_obstaculo):
                    som_colisao.play()
                    # salva pontuação (mantém sua função)
                    salvar_pontuacao(dificuldade, tempo_decorrido, pontos)
 

                    game_over(pontos)
                    return


                # Remover obstáculo que saiu da tela
                if obstaculo.y > altura:
                    obstaculos.remove(obstaculo)
                    pontos += 1
                    velocidade_obstaculo += 0.2
            

        # --- DESENHAR TUDO ---
        for obstaculo in obstaculos:
            tela.blit(obstaculo_img_atual, (obstaculo.x, obstaculo.y))
            if mostrar_hitbox:
                pygame.draw.rect(tela, (255, 0, 0), pygame.Rect(obstaculo.x + 5, obstaculo.y + 5, obstaculo_largura - 10, obstaculo_altura - 10), 2)
            

        tela.blit(jogador_img, (jogador.x, jogador.y))
        if mostrar_hitbox:
            pygame.draw.rect(tela, (0, 255, 0), pygame.Rect(jogador.x + 5, jogador.y + 5, jogador_largura - 10, jogador_altura - 10), 2)

        # Texto de pause
        if pausado:
            texto_pause = fonte_titulo.render("PAUSE", True, branco)
            tela.blit(texto_pause, (largura//2 - texto_pause.get_width()//2, altura//2 - texto_pause.get_height()//2))

        if dificuldade == "Dificil":
            cor_texto = preto
        else:
            cor_texto = branco
        # Pontos e tempo

        # Pontos e tempo
        texto_pontos = fonte_pontos.render(f"Pontos: {pontos}", True, cor_texto)
        texto_timer = fonte_pontos.render(f"Tempo: {tempo_decorrido}s", True, cor_texto)
        tela.blit(texto_pontos, (10, 10))
        tela.blit(texto_timer, (10, 40))

        pygame.display.update()




# -------------------- GAME OVER --------------------
def game_over(pontos):
    parar_musicas_fase()

    global fase_rodando  # para poder alterar a variável global
    fase_rodando = None   # resetar a fase atual
    pygame.mixer.music.stop()  # para qualquer música da fase
    rodando_gameover = True
    
    


    
    while rodando_gameover:
        tela.blit(fundo_game_over, (0, 0))  # desenha o fundo

        # Texto Game Over
        texto = fonte_titulo.render(f"Game Over! Pontos: {pontos}", True, vermelho)
        tela.blit(texto, (largura//2 - texto.get_width()//2, altura//2 - 150))

        # Botão Tentar Novamente
        tentar_rect = pygame.Rect(largura//2 - 150, altura//2 - 50, 300, 50)
        pygame.draw.rect(tela, verde, tentar_rect)
        texto_tentar = fonte_botao.render("Tentar Novamente", True, branco)
        tela.blit(texto_tentar, (
            tentar_rect.x + tentar_rect.width//2 - texto_tentar.get_width()//2,
            tentar_rect.y + tentar_rect.height//2 - texto_tentar.get_height()//2))

        # Botão Voltar ao Menu
        menu_rect = pygame.Rect(largura//2 - 100, altura//2 + 30, 200, 50)
        pygame.draw.rect(tela, vermelho, menu_rect)
        texto_menu = fonte_botao.render("Voltar ao Menu", True, branco)
        tela.blit(texto_menu, (menu_rect.x + menu_rect.width//2 - texto_menu.get_width()//2,
                                menu_rect.y + menu_rect.height//2 - texto_menu.get_height()//2))

        pygame.display.update()

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                if tentar_rect.collidepoint(mouse_pos):
                    rodando_gameover = False
                    jogar()
                    return
                if menu_rect.collidepoint(mouse_pos):
                    rodando_gameover = False
                    menu()
                    return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN or evento.key == pygame.K_KP_ENTER:
                    rodando_gameover = False
                    jogar()
                    return
                if evento.key == pygame.K_ESCAPE:
                    rodando_gameover = False
                    menu()
                    return
                
                
                


  # -------------------- INÍCIO DO PROGRAMA --------------------
if __name__ == "__main__":
    # Loop principal do programa: nunca fecha sozinho, sempre volta ao menu
    while True:
        menu()  # sempre retorna ao menu após jogar ou sair de config
        
        
        
        