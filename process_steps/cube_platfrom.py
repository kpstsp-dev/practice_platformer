import pygame



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
GRAVITY = 0.2
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
        self.rect.center = (WIDTH // 2, HEIGHT - PLAYER_HEIGHT // 2 - 20)
        self.vel_y = 0
        self.on_ground = True #Change to False later
    def update(self):
        self.vel_y = self.vel_y + GRAVITY
        self.rect.y = self.rect.y + self.vel_y #check int/float

        self.on_ground = False

        #Kick to bottom line
        if self.rect.bottom >= HEIGHT:
            self.rect_bottom = HEIGHT
            self.vel_y = 0
            self.on_ground = True
        #Restrict horizontal moving
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


    def jump(self):
        if self.on_ground:
            self.vel_y = JUMP_POWER
            self.on_ground = False

    def move_left(self):
        self.rect.x -= PLAYER_SPEED

    def move_right(self):
        self.rect.x += PLAYER_SPEED

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, ):
        super().__init__()
        self.image = pygame.Surface([PLATFORM_WIDTH, PLATFORM_HEIGHT])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Платформер")
clock = pygame.time.Clock()


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
# try:
#     player_image = pygame.image.load('player.png')
#     player_image = pygame.transform.scale(player_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
# except:
#     player_image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
#     player_image.fill(YELLOW)
# player_x = WIDTH // 2 - PLAYER_WIDTH // 2 #transfered
# player_y = HEIGHT - PLAYER_HEIGHT - 5 #transfered
# player_y_vel = 0 #transfered
# on_ground = True
# platform = pygame.Rect(x, y, square_size_x, square_size_y)
# platform2 = pygame.Rect(300, 150, square_size_x, square_size_y)



run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: # Прыжок срабатывает только один раз при нажатии
                player.jump()

        # if event.type == pygame.KEYDOWN:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.move_right()



    # player_y += player_y_vel
    # player_rect.y = player_y

    # if player_rect.colliderect(platform):
    #     if player_y_vel > 0:
    #         player_y = platform.top - PLAYER_HEIGHT
    #         player_y_vel = 0
    #         on_ground = True
    #     elif player_y_vel < 0:
    #         player_y = platform.bottom
    #         player_y_vel = 0
    #
    # player_y_vel += GRAVITY  #transfered to update
    #
    # if player_y >= HEIGHT - PLAYER_HEIGHT - 5:
    #     player_y = HEIGHT - PLAYER_HEIGHT - 5
    #     player_y_vel = 0
    #     on_ground = True
    #
    # if player_x < 0:
    #     player_x = 0
    # elif player_x > WIDTH - PLAYER_WIDTH:
    #     player_x = WIDTH - PLAYER_WIDTH
    all_sprites.update()

    screen.fill(WHITE)
    all_sprites.draw(screen)
    # pygame.draw.rect(screen, YELLOW, platform)
    # pygame.draw.rect(screen, BLACK, platform2)
    # screen.blit(player_image, (player_x, player_y))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()