import pygame
import random
from intro_screen import IntroScreen

# --- Константы ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_WIDTH = 85
PLAYER_HEIGHT = 70
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
LAVA_HEIGHT = 50
GRAVITY = 0.5
PLAYER_JUMP_POWER = -12
PLAYER_MOVE_SPEED = 5  # Скорость горизонтального движения игрока
PLATFORM_SPEED = 2
MAX_PLATFORMS = 8  # Максимальное количество платформ на экране
PLATFORM_SPAWN_INTERVAL = 100  # Интервал появления платформ по высоте

# --- Цвета ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BROWN = (139, 69, 19)  # Цвет кирпича
ORANGE = (255, 165, 0)  # Цвет лавы


# --- Класс Игрока ---
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load('gggg.jpg')
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        except:
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            self.image.fill(BLACK)
        # self.image = pygame.Surface([PLAYER_WIDTH, PLAYER_HEIGHT])
        # self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - LAVA_HEIGHT - PLAYER_HEIGHT // 2 - 10)
        self.vel_y = 0
        self.vel_x = 0  # Добавляем горизонтальную скорость игрока
        self.on_ground = False
        self.current_platform = None  # Добавляем ссылку на платформу, на которой стоит игрок
        self.lives = 3

    def update(self, platforms):
        # Обнуляем горизонтальную скорость от движения игрока
        self.vel_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -PLAYER_MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = PLAYER_MOVE_SPEED

        # Добавляем горизонтальную скорость платформы, если игрок на ней
        if self.on_ground and self.current_platform:
            self.rect.x += self.current_platform.direction * PLATFORM_SPEED

        # Применяем горизонтальную скорость игрока
        self.rect.x += self.vel_x

        # Применение гравитации
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Проверка столкновений с платформами
        self.on_ground = False
        self.current_platform = None  # Сбрасываем текущую платформу перед проверкой
        for platform in platforms:
            if self.vel_y >= 0 and self.rect.colliderect(platform.rect):
                # Если игрок приземляется на платформу
                # Проверяем, что нижняя часть игрока находится выше верхней части платформы
                # и что его предыдущая позиция была выше платформы
                if self.rect.bottom > platform.rect.top and self.rect.top < platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.current_platform = platform  # Запоминаем платформу
                    break  # Останавливаем проверку, нашли платформу

        # Столкновение с нижней границей (лавой)
        if self.rect.bottom >= SCREEN_HEIGHT - LAVA_HEIGHT:
            self.lives -= 1
            if self.lives == 0:
                return "game_over"  # Сигнал о конце игры
            else:
                self.reset_position()  # Возвращаем игрока на стартовую позицию

        # Столкновение с верхней границей
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0

        # Ограничение движения по горизонтали
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def jump(self):
        if self.on_ground:
            self.vel_y = PLAYER_JUMP_POWER
            self.on_ground = False  # Игрок больше не на земле после прыжка
            self.current_platform = None  # Больше не на платформе после прыжка

    # Методы move_left/right теперь не нужны, так как движение обрабатывается в update
    # def move_left(self):
    #     self.vel_x = -PLAYER_MOVE_SPEED
    #
    # def move_right(self):
    #     self.vel_x = PLAYER_MOVE_SPEED

    def reset_position(self):
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - LAVA_HEIGHT - PLAYER_HEIGHT // 2 - 10)
        self.vel_y = 0
        self.vel_x = 0
        self.on_ground = False
        self.current_platform = None


# --- Класс Платформы ---
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([PLATFORM_WIDTH, PLATFORM_HEIGHT])
        # Визуализация кирпичной платформы
        for i in range(PLATFORM_WIDTH // 10):
            for j in range(PLATFORM_HEIGHT // 5):
                pygame.draw.rect(self.image, BROWN, (i * 10, j * 5, 9, 4))
                pygame.draw.rect(self.image, BLACK, (i * 10 + 9, j * 5, 1, 4))  # Вертикальные швы
                pygame.draw.rect(self.image, BLACK, (i * 10, j * 5 + 4, 9, 1))  # Горизонтальные швы
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1  # 1 для движения вправо, -1 для движения влево
        # Случайное начальное направление
        if random.random() < 0.5:
            self.direction *= -1

    def update(self):
        self.rect.x += self.direction * PLATFORM_SPEED
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.direction *= -1  # Меняем направление, если платформа достигла края


# --- Инициализация Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Платформер с лавой")
clock = pygame.time.Clock()


# --- ЗАСТАВКА ---
# Если у вас есть файл intro_screen.py, раскомментируйте эти строки.
# Если нет, удалите импорт и эти строки.
try:
    game_intro = IntroScreen(SCREEN_WIDTH, SCREEN_HEIGHT)
    game_intro.run(screen)
except NameError:
    print("Предупреждение: Класс IntroScreen не найден. Пропускаем заставку.")
# --- КОНЕЦ ЗАСТАВКИ ---

# --- Спрайты ---
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()

player = Player()
all_sprites.add(player)


# Создание начальных платформ, обеспечивающих стартовую площадку и путь вверх
def generate_initial_platforms():
    # Создаем стартовую платформу прямо под игроком
    start_platform_x = player.rect.centerx - PLATFORM_WIDTH // 2
    start_platform_y = SCREEN_HEIGHT - LAVA_HEIGHT - 30  # Чуть выше лавы
    start_platform = Platform(start_platform_x, start_platform_y)
    all_sprites.add(start_platform)
    platforms.add(start_platform)

    # Генерируем несколько платформ выше
    for i in range(1, MAX_PLATFORMS):
        platform_x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
        # Располагаем платформы выше предыдущих
        platform_y = start_platform_y - i * PLATFORM_SPAWN_INTERVAL
        if platform_y < 0:  # Не даем платформам уходить за верхний край при старте
            break
        platform = Platform(platform_x, platform_y)
        all_sprites.add(platform)
        platforms.add(platform)


generate_initial_platforms()

# --- Игровой цикл ---
running = True
game_over = False
score = 0
font = pygame.font.Font(None, 36)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                player.jump()
            # Убрал обработку K_LEFT/RIGHT здесь, теперь они в player.update()

    if not game_over:
        # Обновление спрайтов
        player_status = player.update(platforms)
        if player_status == "game_over":
            game_over = True

        platforms.update()

        # Удаление платформ, которые ушли за верхний край экрана
        for platform in platforms:
            if platform.rect.bottom < 0:
                platform.kill()  # Удаляем платформу
                # Если игрок был на удаленной платформе, сбросить current_platform
                if player.current_platform == platform:
                    player.current_platform = None

        # Генерация новых платформ по мере подъема игрока
        # Проверяем, есть ли платформы, чтобы избежать ошибок с пустыми списками
        if platforms:
            highest_platform_y = min(p.rect.y for p in platforms)
        else:  # Если платформ нет, создаем одну на старте
            highest_platform_y = SCREEN_HEIGHT - LAVA_HEIGHT - 50  # Задаем условную "высоту"

        # Если игрок поднялся выше самой высокой платформы или платформ мало
        # или если самая высокая платформа слишком близко к нижней границе, генерируем новую
        if player.rect.y < highest_platform_y + SCREEN_HEIGHT / 3 or len(
                platforms) < MAX_PLATFORMS / 2 or highest_platform_y > SCREEN_HEIGHT / 2:
            new_platform_y = highest_platform_y - PLATFORM_SPAWN_INTERVAL - random.randint(0, 50)  # Разброс
            if new_platform_y > 0:  # Не генерируем платформы слишком высоко за экраном
                new_platform_x = random.randint(0, SCREEN_WIDTH - PLATFORM_WIDTH)
                new_platform = Platform(new_platform_x, new_platform_y)
                all_sprites.add(new_platform)
                platforms.add(new_platform)

        # Обновление счета (можно сделать по максимальной высоте игрока)
        score = max(score, (SCREEN_HEIGHT - LAVA_HEIGHT - player.rect.y) // 10)  # Примерный расчет очков

    # Отрисовка
    screen.fill(WHITE)

    # Отрисовка лавы
    pygame.draw.rect(screen, ORANGE, (0, SCREEN_HEIGHT - LAVA_HEIGHT, SCREEN_WIDTH, LAVA_HEIGHT))

    # Отрисовка спрайтов
    all_sprites.draw(screen)

    # Отображение жизней и счета
    lives_text = font.render(f"Жизни: {player.lives}", True, BLACK)
    screen.blit(lives_text, (10, 10))
    score_text = font.render(f"Очки: {score}", True, BLACK)
    screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

    if game_over:
        game_over_text = font.render("ИГРА ОКОНЧЕНА! Нажмите R для рестарта", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(game_over_text, text_rect)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Перезапуск игры
            game_over = False
            player.lives = 3
            player.reset_position()
            score = 0
            # Очищаем все платформы и создаем новые
            for p in platforms:
                p.kill()
            generate_initial_platforms()

    pygame.display.flip()

    # Ограничение FPS
    clock.tick(60)

pygame.quit()