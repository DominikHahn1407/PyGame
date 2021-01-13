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

while still_playing:
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            still_playing = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= speed
    elif keys[pygame.K_RIGHT]:
        x += speed
    elif keys[pygame.K_UP]:
        y -= speed
    elif keys[pygame.K_DOWN]:
        y += speed

    win.fill((0, 0, 0))
    pygame.draw.rect(win, (255, 255, 255), (x, y, rec_width, rec_height))
    pygame.display.update()


pygame.quit()
