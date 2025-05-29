import pygame
from intro_screen import IntroScreen

#Rectangle coordinates
x = 400
y = 400

PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20

square_size_x = 100
square_size_y = 50

WIDTH = 800
HEIGHT = 600
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_SPEED = 5
JUMP_POWER = -15
GRAVITY = 0.4
WHITE = (255, 255, 255)
YELLOW = (0, 0, 255)
BLACK = (0, 0, 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() #Инициализатор родительского класса
        try:
            self.image = pygame.image.load('player.png')
            self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        except:
            self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
            self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        # Инициализация float_x и float_y внутри __init__
        self.float_x = float(WIDTH // 2)  # Используем float() для явного преобразования
        self.float_y = float(HEIGHT - PLAYER_HEIGHT // 2 - 20)  # Используем float()

        # Центр rect устанавливаем на основе float_x и float_y
        self.rect.center = (int(self.float_x), int(self.float_y))

        self.vel_y = 0
        self.on_ground = True #Change to False later
        self.vel_x = 0
    def move_left(self):
        self.float_x -= PLAYER_SPEED # Изменяем float позицию
        # В этом месте мы можем добавить проверку столкновений,
        # но лучше делать это централизованно в update()
        # или в отдельном методе столкновений.

    def move_right(self):
        self.float_x += PLAYER_SPEED # Изменяем float позицию
        # Аналогично для движения вправо

    def update(self, platforms):
        # --- Горизонтальное движение и столкновения ---
        # Здесь нет прямого горизонтального движения, так как оно управляется move_left/right
        # Но мы обновляем self.rect.x для проверки столкновений
        self.rect.x = int(self.float_x)

        # Проверка горизонтальных столкновений после обновления rect.x
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Если движемся вправо и столкнулись
                if self.vel_x > 0: # Предполагаем, что у вас есть vel_x для горизонтальной скорости,
                                  # но в вашем коде ее нет, поэтому используем направление движения.
                                  # Если у вас нет vel_x, вам нужно определить, как игрок двигался.
                    # Более надежный способ: проверить, откуда произошло столкновение
                    # Если правый край игрока пересек левый край платформы
                    if self.rect.right > platform.rect.left and self.rect.left < platform.rect.left:
                        self.float_x = platform.rect.left - self.rect.width # Отталкиваем игрока влево
                        self.rect.x = int(self.float_x)
                # Если движемся влево и столкнулись
                elif self.vel_x < 0:
                    # Если левый край игрока пересек правый край платформы
                    if self.rect.left < platform.rect.right and self.rect.right > platform.rect.right:
                        self.float_x = platform.rect.right # Отталкиваем игрока вправо
                        self.rect.x = int(self.float_x)
                # Важно: это очень базовая логика, которая предполагает, что игрок
                # движется либо влево, либо вправо, а не просто "стоит" на месте столкновения.
                # Для более сложных случаев лучше использовать более продвинутые алгоритмы
                # разрешения столкновений.

        # --- Вертикальное движение и столкновения (из предыдущего исправленного кода) ---
        self.vel_y += GRAVITY
        self.float_y += self.vel_y

        self.on_ground = False
        landed_on_platform_this_frame = False

        for platform in platforms:
            if self.vel_y >= 0 and self.rect.colliderect(platform.rect):
                if self.rect.bottom > platform.rect.top and self.rect.top < platform.rect.bottom:
                    if self.rect.bottom - self.vel_y <= platform.rect.top:
                        self.float_y = platform.rect.top - self.rect.height
                        self.vel_y = 0
                        self.on_ground = True
                        landed_on_platform_this_frame = True
                        break

        if self.float_y + self.rect.height >= HEIGHT:
            self.float_y = HEIGHT - self.rect.height
            self.vel_y = 0
            self.on_ground = True
            landed_on_platform_this_frame = True

        if not landed_on_platform_this_frame:
            self.on_ground = False

        # Обновляем rect.y в конце после всех расчетов
        self.rect.y = int(self.float_y)

        # Ограничение горизонтального движения по краям экрана
        if self.rect.left < 0:
            self.rect.left = 0
            self.float_x = float(self.rect.x) # Синхронизируем float_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.float_x = float(self.rect.x) # Синхронизируем float_x

    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False

    # def move_left(self):
    #     self.rect.x -= PLAYER_SPEED
    #
    # def move_right(self):
    #     self.rect.x += PLAYER_SPEED

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, ):
        super().__init__()
        self.image = pygame.Surface([PLATFORM_WIDTH, PLATFORM_HEIGHT])
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
# Создаем объект заставки, передавая ему размеры экрана
game_intro = IntroScreen(WIDTH, HEIGHT)
# Запускаем заставку. Игра продолжится только после ее завершения.
game_intro.run(screen)
# --- КОНЕЦ ЗАСТАВКИ ---


#--- Спрайты и группы
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group() #Группа для платформ

player = Player()
all_sprites.add(player)

platform1 = Platform(WIDTH // 2 - PLATFORM_WIDTH // 2, HEIGHT - 100)
platform2 = Platform(WIDTH // 4, HEIGHT - 250)
platform3 = Platform(WIDTH * 3 // 4 - PLATFORM_WIDTH, HEIGHT - 400)

all_sprites.add(platform1, platform2, platform3)
platforms.add(platform1, platform2, platform3)

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                player.jump()
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                player.move_left()
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                player.move_right()

    all_sprites.update(platforms)

    screen.fill(WHITE)
    all_sprites.draw(screen)
    # pygame.draw.rect(screen, YELLOW, platform)
    # pygame.draw.rect(screen, BLACK, platform2)
    # screen.blit(player_image, (player_x, player_y))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()