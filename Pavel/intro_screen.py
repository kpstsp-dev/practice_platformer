import pygame
import os


class IntroScreen:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Загрузка шрифтов
        # Используем стандартный шрифт Pygame или укажите путь к файлу .ttf
        self.title_font = pygame.font.Font(None, 100)  # Очень крупный для названия
        self.creator_font = pygame.font.Font(None, 40)  # Средний для создателя
        self.instruction_font = pygame.font.Font(None, 30)  # Мелкий для инструкции

        # Цвета
        self.text_color = (0, 0, 0)  # Черный
        self.background_color = (200, 200, 255)  # Светло-голубой фон заставки

        # Текст заставки
        self.game_title = "ПЛАТФОРМЕР ПАШИ"
        self.creator_name = "Создатель: Павел"
        self.instruction_text = "Нажмите ПРОБЕЛ, чтобы начать"

        # Место для спрайта из PNG
        self.sprite_image = None
        self.load_sprite_image()

    def load_sprite_image(self):
        # Получаем текущий путь к файлу скрипта intro_screen.py
        script_dir = os.path.dirname(__file__)
        # Объединяем путь к скрипту с именем файла изображения
        # Предполагается, что 'intro_sprite.png' находится в той же папке
        sprite_path = os.path.join(script_dir, 'intro_sprite.png')

        try:
            self.sprite_image = pygame.image.load(sprite_path).convert_alpha()
            # Масштабируем изображение, если нужно (например, до 150x150)
            self.sprite_image = pygame.transform.scale(self.sprite_image, (110, 110))
        except pygame.error as e:
            print(f"Ошибка загрузки изображения для заставки: {e}")
            print(f"Убедитесь, что файл 'intro_sprite.png' находится в той же папке, что и скрипт.")
            # Если изображение не загрузилось, создадим запасной прямоугольник
            temp_surface = pygame.Surface((150, 150))
            temp_surface.fill((100, 100, 100))  # Серый запасной квадрат
            pygame.draw.rect(temp_surface, (255, 0, 0), (0, 0, 150, 150), 5)  # Красная рамка
            self.sprite_image = temp_surface
            print("Используется запасной серый квадрат для заставки.")

    def draw(self, screen):
        # Заливаем фон заставки
        screen.fill(self.background_color)

        # Рендерим и размещаем название игры
        title_surface = self.title_font.render(self.game_title, True, self.text_color)
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 4))
        screen.blit(title_surface, title_rect)

        # Рендерим и размещаем имя создателя
        creator_surface = self.creator_font.render(self.creator_name, True, self.text_color)
        creator_rect = creator_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 4 + 80))
        screen.blit(creator_surface, creator_rect)

        # Рисуем спрайт (если загружен)
        if self.sprite_image:
            sprite_rect = self.sprite_image.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
            screen.blit(self.sprite_image, sprite_rect)

        # Рендерим и размещаем инструкцию
        instruction_surface = self.instruction_font.render(self.instruction_text, True, self.text_color)
        instruction_rect = instruction_surface.get_rect(center=(self.screen_width // 2, self.screen_height * 3 // 4))
        screen.blit(instruction_surface, instruction_rect)

    def run(self, screen):
        intro_active = True
        while intro_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()  # Выходим из игры полностью
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        intro_active = False  # Выходим из заставки по пробелу

            self.draw(screen)  # Рисуем заставку
            pygame.display.flip()  # Обновляем экран
            # Не используем clock.tick() здесь, так как заставка статична
            # Но если добавите анимацию, он понадобится


# Пример использования (для тестирования модуля отдельно)
if __name__ == '__main__':
    pygame.init()
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Тестовая Заставка")

    # Создайте 'intro_sprite.png' в этой же папке для тестирования
    # Или закомментируйте строку self.load_sprite_image() в __init__ если не нужен спрайт

    intro = IntroScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
    intro.run(screen)

    pygame.quit()
    print("Заставка завершена.")