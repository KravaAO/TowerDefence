from pygame import *

init()


class GameSprite:
    def __init__(self, x, y, width, height, color):
        self.rect = Rect(x, y, width, height)
        self.color = color
        self.direction = 'right'

    def reset(self):
        draw.rect(window, self.color, self.rect)


class Enemy(GameSprite):
    def move(self):
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
            return

        if self.direction == 'right':
            self.rect.x += 5
        elif self.direction == 'down':
            self.rect.y += 5
        elif self.direction == 'left':
            self.rect.x -= 5
        elif self.direction == 'up':
            self.rect.y -= 5


map_layout = [
    "####################",
    "s++++++++++++++d####",
    "###############+####",
    "########x####x#+####",
    "###############+####",
    "########x####x#+####",
    '###############+####',
    '####d++++++++++l####',
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
BROWN = (139,69,19)

TILE_SIZE = 40


def draw_map(screen, map_layout):
    for row_idx, row in enumerate(map_layout):
        for col_idx, cell in enumerate(row):
            x = col_idx * TILE_SIZE
            y = row_idx * TILE_SIZE
            if cell == '#':
                draw.rect(screen, GREEN, (x, y, TILE_SIZE, TILE_SIZE))
            elif cell in ['l', 'd', 'u', 'r', '+']:
                draw.rect(screen, BROWN, (x, y, TILE_SIZE, TILE_SIZE))
            elif cell == 'x':
                draw.rect(screen, RED, (x, y, TILE_SIZE, TILE_SIZE))
            elif cell == 's':
                draw.rect(screen, YELLOW, (x, y, TILE_SIZE, TILE_SIZE))
            elif cell == 'e':
                draw.rect(screen, YELLOW, (x, y, TILE_SIZE, TILE_SIZE))


size = 800, 600
window = display.set_mode(size)
clock = time.Clock()

enemies = list()


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
    enemy = Enemy(x - 10, y - 10, 20, 20, RED)
    enemies.append(enemy)
    x += 25

running = True
while running:
    window.fill((0, 0, 0))

    draw_map(window, map_layout)

    for enemy in enemies[:]:
        enemy.move()
        enemy.reset()

    for e in event.get():
        if e.type == QUIT:
            running = False

    display.update()
    clock.tick(60)

quit()
