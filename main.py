from pygame import *
from random import randint
import math

init()


class GameSprite:
    def __init__(self, x, y, width, height, color):

        self.rect = Rect(x, y, width, height)
        self.color = color
        self.direction = 'right'
        self.speed = randint(2, 6)

    def reset(self):
        draw.rect(window, self.color, self.rect)


class Enemy(GameSprite):
    def move(self):
        global x_start, y_start, lose_enemy
        current_row = (self.rect.centery) // TILE_SIZE
        current_col = (self.rect.centerx) // TILE_SIZE
        current_tile = map_layout[current_row][current_col]
        if current_tile == 'r':
            self.direction = 'right'
            self.rect.centery = current_row * TILE_SIZE + TILE_SIZE // 2
        elif current_tile == 'd':
            self.direction = 'down'
            self.rect.centerx = current_col * TILE_SIZE + TILE_SIZE // 2
        elif current_tile == 'l':
            self.direction = 'left'
            self.rect.centery = current_row * TILE_SIZE + TILE_SIZE // 2
        elif current_tile == 'u':
            self.direction = 'up'
            self.rect.centerx = current_col * TILE_SIZE + TILE_SIZE // 2
        if current_tile == 'e':
            enemies.remove(self)
            enemy = Enemy(x_start, y_start - 10, 20, 20, RED)
            enemies.append(enemy)
            lose_enemy += 1
            return

        if self.direction == 'right':
            self.rect.x += self.speed
        elif self.direction == 'down':
            self.rect.y += self.speed
        elif self.direction == 'left':
            self.rect.x -= self.speed
        elif self.direction == 'up':
            self.rect.y -= self.speed


class Bullet(GameSprite):
    def __init__(self, x, y, width, height, color, target):
        super().__init__(x, y, width, height, color)
        self.target = target
        self.speed = 10

    def move(self):
        dx = self.target.rect.centerx - self.rect.centerx
        dy = self.target.rect.centery - self.rect.centery
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx /= distance
            dy /= distance
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def hit(self):
        if self.rect.colliderect(self.target.rect):
            return True
        return False


class Tower(GameSprite):
    def __init__(self, x, y, width, height, color, radius=200):
        super().__init__(x, y, width, height, color)
        self.images = transform.scale(image.load('4.png'), (60, 80))
        self.radius = radius
        self.fire_delay = 60  # Delay in frames
        self.last_shot = 0
        self.bullets = []

    def fire(self, enemies, current_frame):
        if current_frame - self.last_shot >= self.fire_delay:
            for enemy in enemies:
                distance = math.hypot(enemy.rect.centerx - self.rect.centerx, enemy.rect.centery - self.rect.centery)
                if distance < self.radius:
                    bullet = Bullet(self.rect.centerx, self.rect.centery, 5, 5, (255, 255, 0), enemy)
                    self.bullets.append(bullet)
                    self.last_shot = current_frame
                    break

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.move()
            bullet.reset()
            if bullet.hit():
                if bullet.target in enemies:
                    enemies.remove(bullet.target)
                self.bullets.remove(bullet)

    def reset(self):
        window.blit(self.images, (self.rect.x, self.rect.y))


map_layout = [
    "####################",
    "s++++++++++++++d####",
    "###############+####",
    "########x####x#+####",
    "###############+####",
    "########x####x#+####",
    '###############+####',
    '#x##d++++++++++l####',
    "####+###############",
    '####+#x#############',
    "####+###############",
    '####+#x#############',
    "####+###############",
    '####+###############',
    "####e###############",
]

GREEN = (0, 153, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (250, 200, 0)
BROWN = (139, 69, 19)

TILE_SIZE = 60

field_tower = transform.scale(image.load('1.png'), (60, 60))
field_way = transform.scale(image.load('FieldsTile_01.png'), (60, 60))
field_grass = transform.scale(image.load('grass.png'), (60, 60))

def draw_map(screen, map_layout):
    for row_idx, row in enumerate(map_layout):
        for col_idx, cell in enumerate(row):
            x = col_idx * TILE_SIZE
            y = row_idx * TILE_SIZE
            if cell == '#':
                #draw.rect(screen, GREEN, (x, y, TILE_SIZE, TILE_SIZE))
                window.blit(field_grass, (x, y))
            elif cell in ['l', 'd', 'u', 'r', '+']:
                #draw.rect(screen, BROWN, (x, y, TILE_SIZE, TILE_SIZE))
                window.blit(field_way, (x, y))
            elif cell == 'x':
                #draw.rect(screen, RED, (x, y, TILE_SIZE, TILE_SIZE))
                window.blit(field_tower, (x,y))
            elif cell == 's':
                draw.rect(screen, YELLOW, (x, y, TILE_SIZE, TILE_SIZE))
            elif cell == 'e':
                draw.rect(screen, YELLOW, (x, y, TILE_SIZE, TILE_SIZE))


size = 1200, 800
window = display.set_mode(size)
clock = time.Clock()

enemies = list()
towers = list()

lose_enemy = 0

font1 = font.Font('Half_Bold_Pixel-7.ttf', 20)


def get_start_position(map_layout):
    for row_idx, row in enumerate(map_layout):
        for col_idx, cell in enumerate(row):
            if cell == 's':
                x = col_idx * TILE_SIZE + TILE_SIZE // 2
                y = row_idx * TILE_SIZE + TILE_SIZE // 2
                return (x, y)
    return None


start_position = get_start_position(map_layout)
x, y = start_position
for i in range(5):
    enemy = Enemy(x, y - 10, 20, 20, RED)
    enemies.append(enemy)
    x -= 35
x_start, y_start = start_position

running = True
current_frame = 0
while running:
    for i in range(0, 800, 60):
        for j in range(0, 1200, 60):
            window.blit(field_grass, (j, i))

    draw_map(window, map_layout)

    for enemy in enemies[:]:
        enemy.move()
        enemy.reset()

    for tower in towers:
        tower.reset()
        tower.fire(enemies, current_frame)
        tower.update_bullets()

    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == MOUSEBUTTONDOWN and e.button == 1:
            mouse_x, mouse_y = e.pos
            for row_idx, row in enumerate(map_layout):
                for col_idx, cell in enumerate(row):
                    if cell == 'x':
                        x = col_idx * TILE_SIZE
                        y = row_idx * TILE_SIZE
                        rect = Rect(x, y, TILE_SIZE, TILE_SIZE)
                        if rect.collidepoint(mouse_x, mouse_y):
                            print(f"Клік по квадрату 'x' на позиції ({col_idx}, {row_idx})")
                            map_layout[row_idx] = map_layout[row_idx][:col_idx] + '.' + map_layout[row_idx][
                                                                                        col_idx + 1:]
                            tower = Tower(x, y, 30, 30, BLUE)
                            towers.append(tower)

    lose_enemy_text = font1.render(f'Пропущені: {lose_enemy}', True, (255, 255, 255))
    window.blit(lose_enemy_text, (620, 10))

    if len(enemies) == 0:
        window.fill(GREEN)

    if lose_enemy > 12:
        window.fill(RED)

    display.update()
    clock.tick(60)
    current_frame += 1

quit()
