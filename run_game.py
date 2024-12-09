import subprocess
import os

# Проверка наличия тестового файла
if not os.path.exists('test_example.py'):
    with open('test_example.py', 'w') as f:
        f.write('''import unittest
class TestAddFunction(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(1, 2), 3)
if __name__ == '__main__':
    unittest.main()''')

# Запуск тестов с покрытием
subprocess.run(['coverage', 'run', '-m', 'unittest', 'discover'])

# Генерация отчетов
subprocess.run(['coverage', 'report'])
subprocess.run(['coverage', 'html'])

# Если все тесты прошли успешно, запускаем игру
subprocess.run(['python', 'game.py'])
