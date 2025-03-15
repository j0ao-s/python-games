import pygame

BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((640, 480))

pygame.display.set_caption('Pong')

# Carrega a imagem da bolinha
ball_image = pygame.image.load("pong_game/pizza_pixel.gif") 
ball_image = pygame.transform.scale(ball_image, (30, 30))  # Redimensiona a imagem para 20x20 pixels

# Posição inicial da bolinha
position_x = 300
position_y = 230

# Cria o Rect para a bolinha
ball = pygame.Rect(position_x, position_y, 20, 20)

# Cria o Rect para os pads
left_pad = pygame.Rect(20, 210, 20, 100)
right_pad = pygame.Rect(600, 210, 20, 100)

pads = [left_pad, right_pad]

velocity_x = 0.2  # Velocidade da bolinha em pixels por milissegundo
velocity_y = 0.2

# Cria a instância de um relógio
clock = pygame.time.Clock()

acrescimoBall = 1.05
acrescimoPad = 10

# Game loop
while True:
    # Chamamos o tick para 30fps para o delta
    dt = clock.tick(30)

    event = pygame.event.poll()
    if event.type == pygame.QUIT:  # Verificador para fechar o jogo
        break

    # Usa a função move inplace
    ball.move_ip(velocity_x * dt, velocity_y * dt)

    # Verifica se a bolinha colide com as paredes superior e inferior
    if ball.top <= 0 or ball.bottom >= 480:
        velocity_y = -velocity_y * acrescimoBall

    # Verifica se a bolinha colide com os pads
    if ball.collidelist(pads) >= 0:
        velocity_x = -velocity_x * acrescimoBall
        if acrescimoPad < 15:
            acrescimoPad += 0.1

    # Verifica se a bolinha sai da tela (Game Over)
    if ball.left <= 0 or ball.right >= 640:
        print("Game Over")
        break

    # Movimentação dos pads
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_pad.top > 0:
        left_pad.move_ip(0, -acrescimoPad)
    if keys[pygame.K_s] and left_pad.bottom < 480:
        left_pad.move_ip(0, acrescimoPad)
    if keys[pygame.K_UP] and right_pad.top > 0:
        right_pad.move_ip(0, -acrescimoPad)
    if keys[pygame.K_DOWN] and right_pad.bottom < 480:
        right_pad.move_ip(0, acrescimoPad)

    # Preenche a tela com a cor preta
    screen.fill(BLACK)

    # Desenha a imagem da bolinha na tela
    screen.blit(ball_image, ball.topleft)

    # Desenha os pads
    for pad in pads:
        pygame.draw.rect(screen, WHITE, pad)

    # Atualiza a tela
    pygame.display.flip()

pygame.quit()
