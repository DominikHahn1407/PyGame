import pygame

pygame.init()

WIN_HEIGHT = 480
WIN_WIDTH = 852

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Best Game Ever")

walk_right_list = []
walk_left_list = []

background = pygame.image.load("./images/bg.jpg")
character = pygame.image.load("./images/standing.png")

for i in range(1, 10):
    walk_right_list.append(pygame.image.load(f"./images/R{i}.png"))
    walk_left_list.append(pygame.image.load(f"./images/L{i}.png"))

still_playing = True


class CharacterObject:
    def __init__(self, height, width, speed, jump_height):

        self.width = width
        self.height = height
        self.speed = speed

        self.x = int(WIN_WIDTH / 2 - self.width / 2)
        self.y = WIN_HEIGHT - self.height

        self.jumping = False
        self.jump_height = jump_height
        self.initial_jump_height = jump_height
        self.min_jump_height = -1 * jump_height

        self.left_movement = False
        self.right_movement = False

        self.walk_count = 0

    def window_draw(self):

        win.blit(background, (0, 0))

        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if self.left_movement:
            win.blit(walk_left_list[self.walk_count//3], (self.x, self.y))
            self.walk_count += 1
        elif self.right_movement:
            win.blit(walk_right_list[self.walk_count//3], (self.x, self.y))
            self.walk_count += 1
        else:
            win.blit(character, (self.x, self.y))

        pygame.display.update()


awesome_character = CharacterObject(64, 64, 10, 10)


while still_playing:
    pygame.time.delay(int(1000/27))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            still_playing = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and awesome_character.x > awesome_character.speed:
        awesome_character.x -= awesome_character.speed
        awesome_character.left_movement = True
        awesome_character.right_movement = False
    elif keys[pygame.K_RIGHT] and awesome_character.x < WIN_WIDTH - awesome_character.width - awesome_character.speed:
        awesome_character.x += awesome_character.speed
        awesome_character.left_movement = False
        awesome_character.right_movement = True
    else:
        awesome_character.left_movement = False
        awesome_character.right_movement = False
        awesome_character.walk_count = 0

    if not awesome_character.jumping:
        if keys[pygame.K_SPACE]:
            awesome_character.jumping = True
            awesome_character.left_movement = False
            awesome_character.right_movement = False
            awesome_character.walk_count = 0
    else:
        if awesome_character.jump_height >= awesome_character.min_jump_height:
            negative = 1
            if awesome_character.jump_height < 0:
                negative = -1
            awesome_character.y -= (awesome_character.jump_height ** 2) / 2 * negative
            awesome_character.jump_height -= 1
        else:
            awesome_character.jumping = False
            awesome_character.jump_height = awesome_character.initial_jump_height

    awesome_character.window_draw()

pygame.quit()
