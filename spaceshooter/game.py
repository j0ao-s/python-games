import pygame
import sys

# Inicialização
pygame.init()
LARGURA = 600
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Space Defender")

# Cores
BRANCO = (255, 255, 255)
# Fonte para pontuação
fonte = pygame.font.Font(None, 36)  # None usa a fonte padrão

# Player
player_img = pygame.image.load("spaceshooter/player.png")
player_rect = player_img.get_rect(center=(LARGURA // 2, ALTURA - 50))
velocidade_player = 5

#Enemy
enemy_img = pygame.image.load("spaceshooter/enemy.png")
enemy_img = pygame.transform.scale(enemy_img, (50, 50)) 

# Tiros
tiros = []
velocidade_tiro = 9
ULTIMO_TIRO = 0  # Controla o intervalo entre tiros
INTERVALO_TIROS = 500  # Milissegundos (0.5 segundos)

# Configurações de dificuldade
VELOCIDADE_INIMIGO_BASE = 3
INTERVALO_INIMIGOS_BASE = 2000  # 2 segundos
AUMENTO_VELOCIDADE_POR_PONTO = 0.003  # Reduzido para 0.3% por ponto
AUMENTO_TAXA_POR_PONTO = 3  # Reduzido para 3ms por ponto
INTERVALO_INIMIGOS_MINIMO = 800  # Limite mínimo de 0.8 segundos

# Inimigos
inimigos = []
velocidade_inimigo = VELOCIDADE_INIMIGO_BASE
ULTIMO_INIMIGO = 0
intervalo_inimigos = INTERVALO_INIMIGOS_BASE

# Pontuação
pontos = 0

# Loop principal
relogio = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimento do Player
    teclas = pygame.key.get_pressed()
    if (teclas[pygame.K_a] and player_rect.left) or (teclas[pygame.K_LEFT] and player_rect.left> 0):
        player_rect.x -= velocidade_player
    if (teclas[pygame.K_d] and player_rect.right < LARGURA) or (teclas[pygame.K_RIGHT] and player_rect.right < LARGURA):
        player_rect.x += velocidade_player

    # Disparar tiros (automático)
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ULTIMO_TIRO > INTERVALO_TIROS:
        tiro_rect = pygame.Rect(
            player_rect.centerx - 2,  # Posição X centralizada
            player_rect.top - 20,      # Posição Y acima da nave
            4, 16                      # Largura e altura do tiro
        )
        tiros.append(tiro_rect)
        ULTIMO_TIRO = tempo_atual  # Atualiza o último tempo de tiro

    # Movimento dos tiros
    for tiro in tiros[:]:
        tiro.y -= velocidade_tiro
        if tiro.bottom < 0:
            tiros.remove(tiro)

    # --- ATUALIZA DIFICULDADE COM BASE NOS PONTOS ---
    velocidade_inimigo = VELOCIDADE_INIMIGO_BASE * (1 + pontos * AUMENTO_VELOCIDADE_POR_PONTO)
    intervalo_inimigos = max(
        INTERVALO_INIMIGOS_MINIMO,  # Limite mínimo
        INTERVALO_INIMIGOS_BASE - pontos * AUMENTO_TAXA_POR_PONTO
    )

    # Gerar inimigos
    # Gerar inimigos (com controle de tempo)
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ULTIMO_INIMIGO > intervalo_inimigos:
        enemy_rect = enemy_img.get_rect()
        enemy_rect.x = pygame.time.get_ticks() % (LARGURA - enemy_rect.width)
        enemy_rect.y = -enemy_rect.height
        inimigos.append(enemy_rect)
        ULTIMO_INIMIGO = tempo_atual

    # Movimento dos inimigos
    for inimigo in inimigos[:]:
        inimigo.y += velocidade_inimigo
        if inimigo.top > ALTURA:
            inimigos.remove(inimigo)

    if len(inimigos) > 10:
        del inimigos[0]  # Remove o inimigo mais antigo

     # Colisão tiro-inimigo
    for tiro in tiros[:]:  # Iterar em uma cópia da lista
        for inimigo in inimigos[:]:
            if tiro.colliderect(inimigo):
                tiros.remove(tiro)
                inimigos.remove(inimigo)
                pontos += 10  # Adiciona pontos
    
    # Colisão player-inimigo (Game Over)
    for inimigo in inimigos:
        if inimigo.colliderect(player_rect):
            running = False  # Encerra o jogo

    # Desenhar
    tela.fill((0, 0, 0))
    tela.blit(player_img, player_rect)
    
    for tiro in tiros:
        pygame.draw.rect(tela, BRANCO, tiro)

    # Desenhar inimigos
    for inimigo in inimigos:
        pygame.draw.rect(tela, (255, 0, 0), inimigo)  # Cor vermelha
        tela.blit(enemy_img, inimigo)

    # Mostrar pontuação
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, BRANCO)
    tela.blit(texto_pontos, (10, 10))

    pygame.display.flip()
    relogio.tick(60)  # 60 FPS

pygame.quit()
sys.exit()