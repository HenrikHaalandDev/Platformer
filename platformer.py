import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Platformer")

WHITE, BLACK, BLUE, RED, GOLD = (255, 255, 255), (0, 0, 0), (0, 0, 255), (255, 0, 0), (255, 215, 0)

class Player:
    def __init__(self):
        self.width, self.height = 40, 60
        self.x, self.y = 100, HEIGHT - self.height - 10
        self.velocity, self.jump_power, self.gravity, self.dy = 5, 12, 0.5, 0
        self.score = 0

    def move(self, keys):
        if keys[pygame.K_LEFT]: self.x -= self.velocity
        if keys[pygame.K_RIGHT]: self.x += self.velocity

    def jump(self):
        self.dy = -self.jump_power

    def apply_gravity(self, platforms):
        self.dy += self.gravity
        self.y += self.dy
        for platform in platforms:
            if self.y + self.height >= platform.y and platform.x < self.x < platform.x + platform.width:
                self.y, self.dy = platform.y - self.height, 0

    def check_collision(self, enemies):
        for enemy in enemies:
            if self.x < enemy.x + enemy.width and self.x + self.width > enemy.x and self.y < enemy.y + enemy.height and self.y + self.height > enemy.y:
                print("GAME OVER!")
                pygame.quit()
                exit()

    def collect_coins(self, coins):
        for coin in coins[:]:
            if self.x < coin.x + coin.size and self.x + self.width > coin.x and self.y < coin.y + coin.size and self.y + self.height > coin.y:
                self.score += 1
                coins.remove(coin)

class Platform:
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height

    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))

class MovingPlatform(Platform):
    def __init__(self, x, y, width, height, speed):
        super().__init__(x, y, width, height)
        self.speed = speed

    def move(self):
        self.y += self.speed
        if self.y < 100 or self.y > HEIGHT - 100:
            self.speed *= -1

class Enemy:
    def __init__(self, x, y, width, height, speed):
        self.x, self.y, self.width, self.height, self.speed = x, y, width, height, speed

    def move(self):
        self.x += self.speed
        if self.x < 50 or self.x > WIDTH - 50:
            self.speed *= -1

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

class Coin:
    def __init__(self, x, y):
        self.x, self.y, self.size = x, y, 15

    def draw(self):
        pygame.draw.circle(screen, GOLD, (self.x, self.y), self.size)

def draw_score(player):
    font = pygame.font.Font(None, 36)
    screen.blit(font.render(f"Score: {player.score}", True, BLACK), (10, 10))

player = Player()
platforms = [Platform(50, HEIGHT - 20, WIDTH - 100, 20), MovingPlatform(300, 400, 200, 20, 2)]
enemies = [Enemy(300, HEIGHT - 60, 50, 50, 3)]
coins = [Coin(350, 380), Coin(150, 280)]

clock = pygame.time.Clock()
running = True

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: player.jump()

    keys = pygame.key.get_pressed()
    player.move(keys)
    player.apply_gravity(platforms)
    player.check_collision(enemies)
    player.collect_coins(coins)

    for platform in platforms: platform.draw()
    for enemy in enemies: enemy.move(); enemy.draw()
    for coin in coins: coin.draw()
    
    draw_score(player)
    pygame.draw.rect(screen, BLACK, (player.x, player.y, player.width, player.height))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
