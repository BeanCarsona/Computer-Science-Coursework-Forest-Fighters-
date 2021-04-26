import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 600
HEIGHT = 480
FPS = 60
time = 30
score = 0
health = 10

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 140))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        #self.rect.centerx or self.rect.centery is the spawn coordinate
        self.rect.centerx = 0
        self.rect.centery = HEIGHT / 2
        self.speedy = 0

    def update(self):
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speedy = -14
        if keystate[pygame.K_DOWN]:
            self.speedy = 14
        self.rect.y += self.speedy
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(enemy_img, (30, 40))
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        #self.rect.x is the spawn coordinate
        self.rect.centerx = random.randrange(WIDTH, 700)
        self.rect.centery = random.randrange(0, HEIGHT)
        self.speedy = random.randrange(-4, 4)
        self.speedx = random.randrange(-7, -4)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > 0 or self.rect.bottom > HEIGHT:
            self.speedy = 0
        if self.rect.left < -10:
            global health
            health-=1
            self.rect.centerx = random.randrange(WIDTH, 700)
            self.rect.centery = random.randrange(0, HEIGHT)
            self.speedy = random.randrange(-4, 4)
            self.speedx = random.randrange(-7, -4)

#loading graphics
background = pygame.image.load("forest_background1.png").convert()
background_rect = background.get_rect()
player_img = pygame.image.load("shield_player.png").convert()
enemy_img = pygame.image.load("axe_enemy1.png").convert()

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(4):
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

# Game loop
running = True
while running:
    if health <= 0:
        running = False
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()

    # check to see if player hits mob
    hits = pygame.sprite.spritecollide(player, mobs, True)
    if hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)
        score+=1
        time-=1/FPS


    # Drawing and rendering
    screen.fill(BLACK)
    screen.blit(background,background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_text(screen, str(health), 18, WIDTH - 580, 10)
    # flip the display after drawing
    pygame.display.flip()

pygame.quit()
