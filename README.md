# TowerDefence

# Налаштування спрайтів та їх побудова в Pygame

Це перший етап розробки гри на основі бібліотеки Pygame, на якому налаштовуються спрайти та визначається їхня початкова побудова. У цьому розділі ми розглянемо, як створити та керувати спрайтами на екрані.

## Клас GameSprite

Щоб почати, створимо базовий клас для спрайтів - `GameSprite`. Це універсальний клас, який допоможе нам створювати об'єкти з базовими властивостями, такими як розмір, колір та початкова позиція.

```python
from pygame import *

init()

class GameSprite:
    def __init__(self, x, y, width, height, color):
        self.rect = Rect(x, y, width, height)
        self.color = color
        self.direction = 'right'

    def reset(self):
        draw.rect(window, self.color, self.rect)
```

- **`__init__`**: Метод-конструктор, який визначає початкові параметри спрайта: координати (`x`, `y`), розмір (`width`, `height`) та колір (`color`).
- **`reset`**: Метод, який дозволяє відобразити спрайт на екрані, використовуючи функцію `draw.rect`.

## Клас Enemy та його метод руху

Далі ми створимо клас `Enemy`, що успадковується від `GameSprite`, щоб додати ворогам можливість рухатися. У цьому класі визначено метод `move()`, який контролює рух в залежності від того, на яку клітинку карти ворог потрапляє.

```python
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
```

Метод `move()` визначає, як саме ворог має рухатись залежно від символу на карті (`map_layout`). Кожен символ (`r`, `d`, `l`, `u`) визначає напрямок руху.

## Побудова карти та відображення елементів

Для відображення карти використовуємо функцію `draw_map()`, яка проходить по кожному елементу та малює відповідний прямокутник в залежності від символу в масиві `map_layout`.

```python
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
```

Ця функція малює різні типи плиток на основі символів карти, де:
- `#` представляє стіну (зелений колір).
- `+`, `l`, `d`, `u`, `r` - траєкторії руху ворогів (коричневий).
- `x` - місця для майбутніх башен (червоний).
- `s` та `e` - початкова та кінцева точки (жовтий) для пересування ворогів.

## Ініціалізація та цикл гри

Основна частина програми складається з налаштування екрана, додавання ворогів на карту та основного циклу гри:

```python
size = 800, 600
window = display.set_mode(size)
clock = time.Clock()

enemies = list()

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
```

Основний цикл гри:
1. Очищає екран (`window.fill`).
2. Викликає `draw_map` для відображення карти.
3. Оновлює стан кожного ворога (`move` та `reset`).
4. Обробляє події (`event.get()`), щоб завершити гру при закритті вікна.
5. Оновлює екран (`display.update()`) та встановлює частоту кадрів (`clock.tick(60)`).

Це був перший етап розробки, де ми визначили базові елементи карти, налаштували ворогів та реалізували їх рух. У наступному розділі розглянемо, як додати більше взаємодії, наприклад, гравця та колізії.

