import pygame
# from intro_screen import IntroScreen # Закомментировано, так как IntroScreen не предоставлен

# Rectangle coordinates (эти переменные не используются, можно удалить)
# x = 400
# y = 400

PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20

# square_size_x = 100 # Эти переменные не используются, можно удалить
# square_size_y = 50

WIDTH = 800
HEIGHT = 600
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
JUMP_POWER = -15
GRAVITY = 0.4 # Хорошее значение для гравитации
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0) # Исправлен цвет на настоящий желтый
BLACK = (0, 0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Инициализатор родительского класса
        try:
            self.image = pygame.image.load('player.png')
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        except:
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            self.image.fill(BLACK)
        self.rect = self.image.get_rect()

        # Инициализация float_x и float_y для точной позиции
        self.float_x = float(WIDTH // 2)
        self.float_y = float(HEIGHT - PLAYER_HEIGHT // 2 - 20)

        # Устанавливаем rect на основе float-позиции
        self.rect.center = (int(self.float_x), int(self.float_y))

        self.vel_y = 0
        self.vel_x = 0 # Инициализируем горизонтальную скорость
        self.on_ground = False # Лучше начинать с False, если игрок не точно на платформе

    # Методы move_left и move_right теперь просто устанавливают vel_x
    def move_left(self):
        self.vel_x = -PLAYER_SPEED

    def move_right(self):
        self.vel_x = PLAYER_SPEED

    def jump(self):
        if self.on_ground: # Прыжок возможен только если игрок на земле
            self.vel_y = JUMP_POWER
            self.on_ground = False # Игрок больше не на земле после прыжка

    def update(self, platforms):
        # --- Горизонтальное движение ---
        self.float_x += self.vel_x # Применяем горизонтальную скорость
        self.rect.x = int(self.float_x) # Обновляем rect для проверки столкновений

        # Проверка горизонтальных столкновений
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Если игрок движется вправо
                if self.vel_x > 0:
                    # Отталкиваем игрока влево, к левому краю платформы
                    self.float_x = float(platform.rect.left - self.rect.width)
                    self.rect.x = int(self.float_x)
                    self.vel_x = 0 # Останавливаем горизонтальное движение
                # Если игрок движется влево
                elif self.vel_x < 0:
                    # Отталкиваем игрока вправо, к правому краю платформы
                    self.float_x = float(platform.rect.right)
                    self.rect.x = int(self.float_x)
                    self.vel_x = 0 # Останавливаем горизонтальное движение

        # Ограничение горизонтального движения по краям экрана
        if self.rect.left < 0:
            self.rect.left = 0
            self.float_x = float(self.rect.x)
            self.vel_x = 0 # Остановка при касании края
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.float_x = float(self.rect.x)
            self.vel_x = 0 # Остановка при касании края


        # --- Вертикальное движение и столкновения ---
        self.vel_y += GRAVITY
        self.float_y += self.vel_y
        self.rect.y = int(self.float_y) # Обновляем rect для проверки столкновений

        self.on_ground = False # Предполагаем, что игрок не на земле

        # Флаг для отслеживания, приземлился ли игрок на платформу в этом кадре
        landed_on_platform_this_frame = False

        for platform in platforms:
            # Проверяем столкновение только если игрок падает (vel_y >= 0)
            if self.vel_y >= 0 and self.rect.colliderect(platform.rect):
                # Проверяем, что игрок приземлился сверху на платформу
                # (т.е. нижний край игрока был выше верхнего края платформы в предыдущем кадре)
                if self.rect.bottom - self.vel_y <= platform.rect.top:
                    self.float_y = float(platform.rect.top - self.rect.height) # Устанавливаем игрока ровно на платформу
                    self.vel_y = 0 # Обнуляем вертикальную скорость
                    self.on_ground = True # Игрок на земле
                    landed_on_platform_this_frame = True
                    break # Нашли платформу, можно выйти из цикла

        # Проверка столкновения с нижней границей экрана
        if self.float_y + self.rect.height >= HEIGHT:
            self.float_y = float(HEIGHT - self.rect.height)
            self.vel_y = 0
            self.on_ground = True
            landed_on_platform_this_frame = True

        # Если после всех проверок мы не приземлились ни на что, то мы в воздухе
        if not landed_on_platform_this_frame:
            self.on_ground = False

        # Важно: В конце update() убедитесь, что self.rect.x и self.rect.y
        # всегда синхронизированы с self.float_x и self.float_y.
        # Это уже сделано в начале и середине метода.

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y): # Убрана лишняя запятая
        super().__init__()
        self.image = pygame.Surface([PLATFORM_WIDTH, PLATFORM_HEIGHT])
        # Создаем простой узор для платформы, чтобы ее было видно
        for i in range(PLATFORM_WIDTH // 10):
            for j in range(PLATFORM_HEIGHT // 5):
                pygame.draw.rect(self.image, YELLOW, (i * 10, j * 5, 9, 4))
                pygame.draw.rect(self.image, BLACK, (i * 10 + 9, j * 5, 1, 4))
                pygame.draw.rect(self.image, BLACK, (i * 10, j * 5 + 4, 9, 1))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Платформер")
clock = pygame.time.Clock()

# --- ЗАСТАВКА ---
# Если у вас есть файл intro_screen.py, раскомментируйте эти строки.
# Если нет, удалите импорт и эти строки.
# try:
#     game_intro = IntroScreen(WIDTH, HEIGHT)
#     game_intro.run(screen)
# except NameError:
#     print("Предупреждение: Класс IntroScreen не найден. Пропускаем заставку.")
# --- КОНЕЦ ЗАСТАВКИ ---


# --- Спрайты и группы ---
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group() # Группа для платформ

player = Player() # Создание игрока без аргументов, как мы исправили __init__
all_sprites.add(player)

# Создаем платформы
platform1 = Platform(WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - 100)
platform2 = Platform(WIDTH // 4, HEIGHT - 250)
platform3 = Platform(WIDTH * 3 // 4 - PLATFORM_WIDTH, HEIGHT - 400)
platform4 = Platform(50, HEIGHT - 180) # Дополнительные платформы
platform5 = Platform(WIDTH - 150, HEIGHT - 320)

all_sprites.add(platform1, platform2, platform3, platform4, platform5)
platforms.add(platform1, platform2, platform3, platform4, platform5)

run = True

while run:
    # --- 1. Обработка событий (для однократных действий) ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # Прыжок по нажатию пробела
                player.jump()

    # --- 2. Обработка непрерывного движения (вне цикла событий) ---
    keys = pygame.key.get_pressed()

    # **ВАЖНОЕ ИСПРАВЛЕНИЕ**: Сбрасываем горизонтальную скорость игрока до 0
    # если никакие клавиши движения не нажаты. Это позволяет игроку останавливаться.
    player.vel_x = 0 # Сброс скорости перед проверкой нажатий

    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player.move_right()

    # --- 3. Обновление состояния игры ---
    # Передаем группу платформ в метод update каждого спрайта (в нашем случае, Player)
    all_sprites.update(platforms)

    # --- 4. Отрисовка ---
    screen.fill(WHITE) # Фон
    all_sprites.draw(screen) # Отрисовываем все спрайты
    pygame.display.flip() # Обновляем экран
    clock.tick(60) # Ограничиваем FPS до 60

pygame.quit()