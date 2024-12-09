import unittest
import pygame
from game import (
    generate_obstacles,
    create_food,
    generate_obstacle_movements,
    draw_snake,
    show_score_during_game,
    show_score_after_game,
    draw_obstacles,
    display_menu
)

class TestGame(unittest.TestCase):
    def setUp(self):
        """Настройка начальных условий для тестов."""
        self.snake_list = [[100, 100], [120, 100], [140, 100]]
        self.GAME_X, self.GAME_Y = 55, 75
        self.GAME_WIDTH, self.GAME_HEIGHT = 250, 500
        self.SNAKE_BLOCK = 20
        self.OBSTACLE_SPEED_DIVISOR = 4
        pygame.init()
        self.display = pygame.display.set_mode((360, 640))

    def test_generate_obstacles(self):
        """Тест для функции generate_obstacles."""
        obstacles = generate_obstacles(5, self.snake_list)
        self.assertEqual(len(obstacles), 5, "Количество препятствий должно быть равно запрошенному числу.")
        for obs in obstacles:
            # Проверяем, что координаты кратны размеру блока
            self.assertTrue(
                obs.x % self.SNAKE_BLOCK == 0 and obs.y % self.SNAKE_BLOCK == 0,
                "Координаты препятствия должны быть кратны размеру блока."
            )
            # Проверяем, что препятствия не пересекаются со змейкой
            self.assertFalse(
                any(obs.x == part[0] and obs.y == part[1] for part in self.snake_list),
                "Препятствие не должно пересекаться с телом змейки."
            )

    def test_generate_obstacle_movements(self):
        """Тест для функции generate_obstacle_movements."""
        movements = generate_obstacle_movements(3)
        self.assertEqual(len(movements), 3, "Должно быть сгенерировано движение для каждого препятствия.")
        for dx, dy in movements:
            self.assertIn(
                dx, [-self.SNAKE_BLOCK // self.OBSTACLE_SPEED_DIVISOR, self.SNAKE_BLOCK // self.OBSTACLE_SPEED_DIVISOR],
                "Горизонтальное движение должно соответствовать заданной скорости."
            )
            self.assertIn(
                dy, [-self.SNAKE_BLOCK // self.OBSTACLE_SPEED_DIVISOR, self.SNAKE_BLOCK // self.OBSTACLE_SPEED_DIVISOR],
                "Вертикальное движение должно соответствовать заданной скорости."
            )

    def test_create_food(self):
        """Тест для функции create_food."""
        obstacles = generate_obstacles(3, self.snake_list)
        food_x, food_y = create_food(obstacles, self.snake_list)
        food_rect = pygame.Rect(food_x, food_y, self.SNAKE_BLOCK, self.SNAKE_BLOCK)
        
        self.assertFalse(
            any(obs.colliderect(food_rect) for obs in obstacles),
            "Еда не должна пересекаться с препятствиями."
        )
        self.assertFalse(
            any(food_x == part[0] and food_y == part[1] for part in self.snake_list),
            "Еда не должна генерироваться на теле змейки."
        )

    def test_draw_snake(self):
        """Тест для функции draw_snake."""
        try:
            draw_snake(self.snake_list)  # Проверяем, что функция выполняется без ошибок
        except Exception as e:
            self.fail(f"draw_snake вызвала исключение: {e}")

    def test_show_score_during_game(self):
        """Тест для функции show_score_during_game."""
        try:
            show_score_during_game(10)  # Проверяем, что функция выполняется без ошибок
        except Exception as e:
            self.fail(f"show_score_during_game вызвала исключение: {e}")

    def test_show_score_after_game(self):
        """Тест для функции show_score_after_game."""
        try:
            show_score_after_game(15)  # Проверяем, что функция выполняется без ошибок
        except Exception as e:
            self.fail(f"show_score_after_game вызвала исключение: {e}")

    def test_draw_obstacles(self):
        """Тест для функции draw_obstacles."""
        obstacles = generate_obstacles(3, self.snake_list)
        try:
            draw_obstacles(obstacles)  # Проверяем, что функция выполняется без ошибок
        except Exception as e:
            self.fail(f"draw_obstacles вызвала исключение: {e}")

    def test_display_menu(self):
        """Тест для функции display_menu."""
        try:
            display_menu()  # Проверяем, что функция выполняется без ошибок
        except Exception as e:
            self.fail(f"display_menu вызвала исключение: {e}")

if __name__ == "__main__":
    unittest.main()
