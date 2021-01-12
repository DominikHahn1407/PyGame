import pygame


pygame.init()

WIN_HEIGHT = 500
WIN_WIDTH = 500

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Best Game Ever")

rec_width = 40
rec_height = 60
speed = 10

x = int(WIN_WIDTH / 2 - rec_width / 2)
y = int(WIN_HEIGHT / 2 - rec_height / 2)

still_playing = True
jumping = False
jump_height = 10
initial_jump_height = jump_height
min_jump_height = -1 * jump_height

while still_playing:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            still_playing = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > speed:
        x -= speed
    elif keys[pygame.K_RIGHT] and x < WIN_WIDTH - rec_width - speed:
        x += speed
    if not jumping:
        if keys[pygame.K_UP] and y > speed:
            y -= speed
        elif keys[pygame.K_DOWN] and y < WIN_HEIGHT - rec_height - speed:
            y += speed
        elif keys[pygame.K_SPACE]:
            jumping = True
    else:
        if jump_height >= min_jump_height:
            negative = 1
            if jump_height < 0:
                negative = -1
            y -= (jump_height ** 2) / 2 * negative
            jump_height -= 1
        else:
            jumping = False
            jump_height = initial_jump_height

    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255, 255, 255), (x, y, rec_width, rec_height))
    pygame.display.update()


pygame.quit()
