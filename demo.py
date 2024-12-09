import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройка параметров окна
WIDTH, HEIGHT = 800, 600  # Размеры окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создание окна
pygame.display.set_caption("Простое приложение на Pygame")  # Заголовок окна

# Цвета (RGB)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Параметры шара
ball_radius = 20
ball_x, ball_y = WIDTH // 2, HEIGHT // 2  # Начальная позиция
ball_speed_x, ball_speed_y = 5, 5  # Скорость движения

# Игровой цикл
while True:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Проверка на закрытие окна
            pygame.quit()
            sys.exit()

    # Логика обновления игры
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Проверка столкновений с границами окна
    if ball_x - ball_radius < 0 or ball_x + ball_radius > WIDTH:
        ball_speed_x = -ball_speed_x  # Изменение направления по X
    if ball_y - ball_radius < 0 or ball_y + ball_radius > HEIGHT:
        ball_speed_y = -ball_speed_y  # Изменение направления по Y

    # Отрисовка на экране
    screen.fill(WHITE)  # Очистка экрана (фон белый)
    pygame.draw.circle(screen, BLUE, (ball_x, ball_y), ball_radius)  # Отрисовка шара
    pygame.display.flip()  # Обновление экрана

    # Контроль частоты кадров
    pygame.time.Clock().tick(60)
