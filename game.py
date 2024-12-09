import pygame
import random

# Инициализация Pygame
pygame.init()

# Задание цветов
COLORS = {
    "white": (255, 255, 255),
    "yellow": (255, 255, 102),
    "black": (0, 0, 0),
    "purple": (128, 0, 128),
    "green": (0, 255, 0),
    "blue": (50, 153, 213),
    "red": (213, 50, 80),
}

# Установка размеров окна
WIDTH, HEIGHT = 360, 640
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Размер змейки и скорость
SNAKE_BLOCK = 20
INITIAL_SPEED = 5
OBSTACLE_SPEED_DIVISOR = 4
clock = pygame.time.Clock()

# Шрифты
font_main = pygame.font.SysFont("comicsansms", 20)
font_small = pygame.font.SysFont("comicsansms", 15)

# Размер игрового поля
GAME_WIDTH, GAME_HEIGHT = 250, 500
GAME_X, GAME_Y = (WIDTH - GAME_WIDTH) // 2, (HEIGHT - GAME_HEIGHT) // 2

# Генерация случайных барьеров
def generate_obstacles(count, snake_list):
    """Создает случайные препятствия, избегая пересечения со змейкой."""
    obstacles = []
    while len(obstacles) < count:
        x = random.randrange(GAME_X, GAME_X + GAME_WIDTH, SNAKE_BLOCK)
        y = random.randrange(GAME_Y, GAME_Y + GAME_HEIGHT, SNAKE_BLOCK)
        if (x, y) not in obstacles and [x, y] not in snake_list:
            obstacles.append(pygame.Rect(x, y, SNAKE_BLOCK, SNAKE_BLOCK))
    return obstacles

# Генерация случайных направлений и скоростей препятствий
def generate_obstacle_movements(count):
    """Создает случайные направления и скорости для препятствий."""
    movements = []
    for _ in range(count):
        dx = random.choice([-SNAKE_BLOCK // OBSTACLE_SPEED_DIVISOR, SNAKE_BLOCK // OBSTACLE_SPEED_DIVISOR])
        dy = random.choice([-SNAKE_BLOCK // OBSTACLE_SPEED_DIVISOR, SNAKE_BLOCK // OBSTACLE_SPEED_DIVISOR])
        movements.append([dx, dy])
    return movements


def draw_snake(snake_list):
    """Рисует тело змейки."""
    for block in snake_list:
        pygame.draw.rect(display, COLORS["black"], [block[0], block[1], SNAKE_BLOCK, SNAKE_BLOCK])


def show_score_during_game(score):
    """Показывает текущий счёт во время игры."""
    text = font_small.render(f"Счёт: {score}", True, COLORS["black"])
    display.blit(text, (150, 30))


def show_score_after_game(score, y_offset=0):
    """Показывает текущий счёт после игры."""
    text = font_main.render(f"Счёт: {score}", True, COLORS["black"])
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + y_offset))
    display.blit(text, text_rect)


def show_message(msg, color, y_offset=0):
    """Выводит сообщение в центр экрана."""
    text = font_main.render(msg, True, color)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + y_offset))
    display.blit(text, text_rect)


def draw_obstacles(obstacles):
    """Рисует препятствия."""
    for obs in obstacles:
        pygame.draw.rect(display, COLORS["red"], obs)


def display_menu():
    """Главное меню игры."""
    display.fill(COLORS["blue"])
    show_message("Змейка", COLORS["white"])
    show_message("1: Легко  2: Средне  3: Сложно", COLORS["yellow"], y_offset=30)
    show_message("Нажмите Q для выхода", COLORS["white"], y_offset=60)
    pygame.display.update()


def create_food(obstacles, snake_list):
    """Создаёт координаты для еды, избегая пересечения с препятствиями и телом змейки."""
    while True:
        food_x = round(random.randrange(GAME_X, GAME_X + GAME_WIDTH - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
        food_y = round(random.randrange(GAME_Y, GAME_Y + GAME_HEIGHT - SNAKE_BLOCK) / SNAKE_BLOCK) * SNAKE_BLOCK
        food_rect = pygame.Rect(food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK)
        if not any(obs.colliderect(food_rect) for obs in obstacles) and [food_x, food_y] not in snake_list:
            return food_x, food_y


def game_loop(level):
    """Основной игровой цикл."""
    game_over = False
    game_close = False

    # Начальная позиция змейки
    x, y = GAME_X + GAME_WIDTH // 2, GAME_Y + GAME_HEIGHT // 2
    dx, dy = 0, 0

    snake_list = [[x, y]]
    snake_length = 1

    # Генерация препятствий
    obstacle_count = 3 + (level - 1) * 2  # Уровень определяет количество препятствий
    obstacles = generate_obstacles(obstacle_count, snake_list)
    movements = generate_obstacle_movements(obstacle_count)

    # Координаты еды
    food_x, food_y = create_food(obstacles, snake_list)

    # Скорость змейки
    snake_speed = INITIAL_SPEED + (level - 1) * 5

    while not game_over:
        while game_close:
            display.fill(COLORS["blue"])
            show_message("Игра окончена!", COLORS["red"], y_offset=-30)
            show_score_after_game(snake_length - 1, y_offset=0)
            show_message("C: Играть снова  Q: Выход", COLORS["yellow"], y_offset=30)
            show_message("Нажмите M для возврата в меню", COLORS["white"], y_offset=60)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    elif event.key == pygame.K_c:
                        main()
                    elif event.key == pygame.K_m:
                        main()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx == 0:
                    dx = -SNAKE_BLOCK
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx = SNAKE_BLOCK
                    dy = 0
                elif event.key == pygame.K_UP and dy == 0:
                    dy = -SNAKE_BLOCK
                    dx = 0
                elif event.key == pygame.K_DOWN and dy == 0:
                    dy = SNAKE_BLOCK
                    dx = 0

        # Проверка на столкновения с краями ограниченной области
        if x >= GAME_X + GAME_WIDTH or x < GAME_X or y >= GAME_Y + GAME_HEIGHT or y < GAME_Y:
            game_close = True

        x += dx
        y += dy

        # Обновление экрана
        display.fill(COLORS["blue"])

        # Рисуем ограничивающий прямоугольник
        pygame.draw.rect(display, COLORS["black"], [GAME_X, GAME_Y, GAME_WIDTH, GAME_HEIGHT], 4)

        # Рисуем еду
        pygame.draw.rect(display, COLORS["green"], [food_x, food_y, SNAKE_BLOCK, SNAKE_BLOCK])
        draw_obstacles(obstacles)

        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Проверка на столкновение с препятствиями
        snake_rect = pygame.Rect(x, y, SNAKE_BLOCK, SNAKE_BLOCK)
        if any(obs.colliderect(snake_rect) for obs in obstacles):
            game_close = True

        # Проверка на столкновение с собой
        if snake_head in snake_list[:-1]:
            game_close = True

        draw_snake(snake_list)
        show_score_during_game(snake_length - 1)

        # Проверка на съедание еды
        if x == food_x and y == food_y:
            food_x, food_y = create_food(obstacles, snake_list)
            snake_length += 1

        # Движение препятствий
        for i in range(len(obstacles)):
            obs = obstacles[i]
            mov_dx, mov_dy = movements[i]
            obs.x += mov_dx
            obs.y += mov_dy

            # Проверка на столкновение с краями ограниченной области и изменение направления
            if obs.left < GAME_X or obs.right > GAME_X + GAME_WIDTH:
                movements[i][0] = -mov_dx
            if obs.top < GAME_Y or obs.bottom > GAME_Y + GAME_HEIGHT:
                movements[i][1] = -mov_dy

        pygame.display.update()
        clock.tick(snake_speed)

    pygame.quit()
    quit()


def main():
    while True:
        display_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_2, pygame.K_3]:
                    level = int(event.unicode)
                    game_loop(level)
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()


if __name__ == "__main__":
    main()
