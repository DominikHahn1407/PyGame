import pygame

pygame.init()

WIN_HEIGHT = 480
WIN_WIDTH = 852

win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Best Game Ever")

walk_right_list = []
walk_left_list = []

enemy_walk_right_list = []
enemy_walk_left_list = []

background = pygame.image.load("./images/bg.jpg")
character = pygame.image.load("./images/standing.png")
bullets_img = pygame.image.load("./images/bullet.png")

score = 0

for i in range(1, 10):
    walk_right_list.append(pygame.image.load(f"./images/R{i}.png"))
    walk_left_list.append(pygame.image.load(f"./images/L{i}.png"))

for i in range(1, 12):
    enemy_walk_left_list.append(pygame.image.load(f"./images/L{i}E.png"))
    enemy_walk_right_list.append(pygame.image.load(f"./images/R{i}E.png"))

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
        self.right_movement = True
        self.standing_still = True

        self.walk_count = 0
        self.hit_box = (self.x + 20, self.y + 10, 28, 52)

    def window_draw(self, win):
        if self.walk_count + 1 >= 27:
            self.walk_count = 0

        if not self.standing_still:
            if self.left_movement:
                win.blit(walk_left_list[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
            elif self.right_movement:
                win.blit(walk_right_list[self.walk_count//3], (self.x, self.y))
                self.walk_count += 1
        elif self.standing_still:
            if self.left_movement:
                win.blit(walk_left_list[0], (self.x, self.y))
            elif self.right_movement:
                win.blit(walk_right_list[0], (self.x, self.y))
        self.hit_box = (self.x + 20, self.y + 10, 28, 52)
        pygame.draw.rect(win, (255, 0, 0), self.hit_box, 2)


class Attack:
    def __init__(self, x, y, width, height, speed, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.direction = speed * direction

    def draw_bullet(self, win):
        win.blit(bullets_img, (self.x, self.y))


class Enemy:
    def __init__(self, width, height, speed):
        self.width = width
        self.height = height
        self.speed = speed

        self.x = 0
        self.y = WIN_HEIGHT - self.height
        self.end = WIN_WIDTH - self.width

        self.walk_count = 0
        self.path = [self.x, self.end]

        self.hit_box = (self.x + 10, self.y + 2, 28, 55)
        self.health = 10
        self.visible = True


    def enemy_move(self):
        if self.speed > 0:
            if self.x + self.speed < self.path[1]:
                self.x += self.speed
            else:
                self.speed *= -1
                self.walk_count = 0
        else:
            if self.x - self.speed > self.path[0]:
                self.x += self.speed
            else:
                self.speed *= -1
                self.walk_count = 0

    def enemy_draw(self, win):
        if self.visible:
            self.enemy_move()
            if self.walk_count + 1 >= 33:
                self.walk_count = 0

            if self.speed > 0:
                win.blit(enemy_walk_right_list[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
                self.hit_box = (self.x + 10, self.y + 2, 28, 55)
            elif self.speed < 0:
                win.blit(enemy_walk_left_list[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
                self.hit_box = (self.x + 22, self.y + 2, 28, 55)
            pygame.draw.rect(win, (255, 0, 0), (self.hit_box[0] - 6, self.hit_box[1] - 20, 40, 10))
            pygame.draw.rect(win, (0, 255, 0), (self.hit_box[0] - 6,
                                                self.hit_box[1] - 20, 40 - 4 * (10 - self.health), 10))
            pygame.draw.rect(win, (255, 0, 0), self.hit_box, 2)

    def hit(self):
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False
        print("hit")


awesome_character = CharacterObject(64, 64, 10, 10)
ugly_guy = Enemy(64, 64, 5)
bullet_speed = 10
bullets = []
shoots = 0
font = pygame.font.SysFont('comicsans', 30, True)


def draw_window():
    win.blit(background, (0, 0))

    text = font.render(f"Score: {score}", 1, (40, 40, 40))
    win.blit(text, (700, 20))

    awesome_character.window_draw(win)
    ugly_guy.enemy_draw(win)

    for bullet in bullets:
        bullet.draw_bullet(win)

    pygame.display.update()


while still_playing:
    pygame.time.delay(int(1000/27))

    if shoots > 0:
        shoots += 1
    if shoots > 3:
        shoots = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            still_playing = False

    for bullet in bullets:
        if bullet.y > ugly_guy.hit_box[1] and bullet.y + bullet.height < ugly_guy.hit_box[1] + ugly_guy.hit_box[3]:
            if bullet.x + bullet.width > ugly_guy.hit_box[0] and bullet.x < ugly_guy.hit_box[0] + ugly_guy.hit_box[2]:
                ugly_guy.hit()
                score += 10
                bullets.remove(bullet)
        if 0 < bullet.x < WIN_WIDTH:
            bullet.x += bullet.direction
        else:
            bullets.remove(bullet)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and awesome_character.x > awesome_character.speed:
        awesome_character.x -= awesome_character.speed
        awesome_character.left_movement = True
        awesome_character.right_movement = False
        awesome_character.standing_still = False
    elif keys[pygame.K_RIGHT] and awesome_character.x < WIN_WIDTH - awesome_character.width - awesome_character.speed:
        awesome_character.x += awesome_character.speed
        awesome_character.left_movement = False
        awesome_character.right_movement = True
        awesome_character.standing_still = False
    else:
        awesome_character.standing_still = True
        awesome_character.walk_count = 0

    if keys[pygame.K_SPACE] and shoots == 0:
        bullet_start_x = int(awesome_character.x + awesome_character.width // 2)
        bullet_start_y = int(awesome_character.y + awesome_character.height // 2)
        bullet_direction = 0
        if awesome_character.left_movement:
            bullet_direction = -1
        elif awesome_character.right_movement:
            bullet_direction = 1
        if len(bullets) < 5:
            bullets.append(Attack(bullet_start_x, bullet_start_y, 12, 8, bullet_speed, bullet_direction))
        shoots = 1

    if not awesome_character.jumping:
        if keys[pygame.K_UP]:
            awesome_character.jumping = True
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

    draw_window()

pygame.quit()
