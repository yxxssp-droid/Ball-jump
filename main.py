import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
WIDTH, HEIGHT = 800, 450
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Red Ball Clone")

# Colores
WHITE = (255, 255, 255)
BLUE = (100, 150, 255)
RED = (255, 50, 50)
GREEN = (60, 200, 60)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Física
GRAVITY = 0.8
JUMP_FORCE = -15
MOVE_SPEED = 6

# Clase del jugador (bola)
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (20, 20), 20)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_y = 0
        self.on_ground = False

    def update(self, keys, platforms):
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            dx = MOVE_SPEED

        # Gravedad
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10

        dy = self.vel_y

        # Colisiones
        self.on_ground = False
        for platform in platforms:
            # Movimiento horizontal
            if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            # Movimiento vertical
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y > 0:
                    dy = platform.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    dy = platform.rect.bottom - self.rect.top
                    self.vel_y = 0

        # Aplicar movimiento
        self.rect.x += dx
        self.rect.y += dy

        # Saltar
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_FORCE

        # Reiniciar si cae
        if self.rect.top > HEIGHT:
            self.rect.center = (100, 300)
            self.vel_y = 0

# Clase de plataformas
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

# Crear objetos
player = Ball(100, 300)
platforms = pygame.sprite.Group()
platforms.add(Platform(0, 400, 800, 50))
platforms.add(Platform(300, 320, 200, 20))
platforms.add(Platform(600, 250, 150, 20))

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(platforms)

# Bucle principal
running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(keys, platforms)

    # Dibujar
    WINDOW.fill(BLUE)
    all_sprites.draw(WINDOW)
    pygame.display.flip()

pygame.quit()
sys.exit()

import pygame
import sys
import random

pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 800, 450
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Red Ball Clone - Scroll y Obstáculos")

# Colores
BLUE = (120, 180, 255)
GREEN = (60, 200, 60)
RED = (255, 50, 50)
BROWN = (120, 80, 40)
BLACK = (30, 30, 30)
WHITE = (255, 255, 255)

# Constantes de física
GRAVITY = 0.8
JUMP_FORCE = -15
MOVE_SPEED = 6
SCROLL_SPEED = 4

clock = pygame.time.Clock()
FPS = 60

# Clase jugador
class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (20, 20), 20)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel_y = 0
        self.on_ground = False

    def update(self, keys, platforms):
        dx = 0
        if keys[pygame.K_LEFT]:
            dx = -MOVE_SPEED
        if keys[pygame.K_RIGHT]:
            dx = MOVE_SPEED

        # Gravedad
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy = self.vel_y

        # Colisiones con plataformas
        self.on_ground = False
        for p in platforms:
            # Horizontal
            if p.rect.colliderect(self.rect.x + dx, self.rect.y, self.rect.width, self.rect.height):
                dx = 0
            # Vertical
            if p.rect.colliderect(self.rect.x, self.rect.y + dy, self.rect.width, self.rect.height):
                if self.vel_y > 0:
                    dy = p.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    dy = p.rect.bottom - self.rect.top
                    self.vel_y = 0

        # Movimiento
        self.rect.x += dx
        self.rect.y += dy

        # Saltar
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = JUMP_FORCE

        # Si cae fuera
        if self.rect.top > HEIGHT:
            self.reset()

    def reset(self):
        self.rect.center = (100, 300)
        self.vel_y = 0

# Clase plataforma
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, scroll):
        self.rect.x -= scroll
        if self.rect.right < 0:
            self.kill()

# Clase obstáculo
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, size=40):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(BROWN)
        pygame.draw.rect(self.image, BLACK, (0, 0, size, size), 2)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, scroll):
        self.rect.x -= scroll
        if self.rect.right < 0:
            self.kill()

# Grupos
player = Ball(100, 300)
platforms = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
all_sprites = pygame.sprite.Group(player)

# Crear plataformas iniciales
for i in range(3):
    p = Platform(i * 400, 400, 400, 50)
    platforms.add(p)
    all_sprites.add(p)

# Variables de juego
scroll = 0
level_distance = 0
score = 0

font = pygame.font.SysFont("Arial", 24)

def spawn_platform():
    """Genera nuevas plataformas y obstáculos aleatoriamente"""
    global level_distance
    x = WIDTH + random.randint(100, 200)
    y = random.choice([300, 350, 400])
    w = random.randint(250, 400)
    p = Platform(x, y, w, 50)
    platforms.add(p)
    all_sprites.add(p)

    # A veces agrega un obstáculo
    if random.random() < 0.6:
        o = Obstacle(x + random.randint(50, w - 50), y - 40)
        obstacles.add(o)
        all_sprites.add(o)

    level_distance += 1

# Bucle principal
running = True
while running:
    clock.tick(FPS)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(keys, platforms)

    # Scroll del nivel
    scroll = SCROLL_SPEED
    for p in platforms:
        p.update(scroll)
    for o in obstacles:
        o.update(scroll)

    # Generar nuevas plataformas
    if len(platforms) < 5:
        spawn_platform()

    # Colisión con obstáculos
    if pygame.sprite.spritecollide(player, obstacles, False):
        player.reset()
        score = 0
        obstacles.empty()
        platforms.empty()
        for i in range(3):
            p = Platform(i * 400, 400, 400, 50)
            platforms.add(p)
            all_sprites.add(p)
        continue

    # Dibujar
    WINDOW.fill(BLUE)
    all_sprites.draw(WINDOW)

    # Puntaje
    score += 0.1
    text = font.render(f"Puntaje: {int(score)}", True, WHITE)
    WINDOW.blit(text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
