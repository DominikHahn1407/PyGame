import pygame

pygame.init()

WIN_HEIGHT = 480
WIN_WIDTH = 852

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Best Game Ever")


rec_width = 64
rec_height = 64
speed = 10

x = int(WIN_WIDTH / 2 - rec_width / 2)
y = WIN_HEIGHT - rec_height

still_playing = True
jumping = False
jump_height = 10
initial_jump_height = jump_height
min_jump_height = -1 * jump_height

left_movement = False
right_movement = False

walk_count = 0

walk_right_list = []
walk_left_list = []

background = pygame.image.load("./images/bg.jpg")
character = pygame.image.load("./images/standing.png")

for i in range(1, 10):
    walk_right_list.append(pygame.image.load(f"./images/R{i}.png"))
    walk_left_list.append(pygame.image.load(f"./images/L{i}.png"))


def window_draw():
    global walk_count

    win.blit(background, (0, 0))

    if walk_count + 1 >= 27:
        walk_count = 0

    if left_movement:
        win.blit(walk_left_list[walk_count//3], (x, y))
        walk_count += 1
    elif right_movement:
        win.blit(walk_right_list[walk_count//3], (x, y))
        walk_count += 1
    else:
        win.blit(character, (x, y))

    pygame.display.update()


while still_playing:
    pygame.time.delay(int(1000/27))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            still_playing = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and x > speed:
        x -= speed
        left_movement = True
        right_movement = False
    elif keys[pygame.K_RIGHT] and x < WIN_WIDTH - rec_width - speed:
        x += speed
        left_movement = False
        right_movement = True
    else:
        left_movement = False
        right_movement = False
        walk_count = 0

    if not jumping:
        if keys[pygame.K_SPACE]:
            jumping = True
            left_movement = False
            right_movement = False
            walk_count = 0
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

    window_draw()

pygame.quit()
