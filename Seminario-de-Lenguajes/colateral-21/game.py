# SEMINARIO DE LENGUAJES — 2021
# Proyecto de Videojuego en Pygame
# ————————————INTEGRANTES————————————
# Cruz, Denis Liam
# Fernandez, Nahuel
# Guevara, Agustín Ezequiel
# Luoni, Brian Ezequiel
# Moro, Enzo Sebastián
# Suarez Arnaldi, Leonel

#region Imports
import pygame
import sys
import random

from pygame.constants import K_w
#endregion

pygame.init()
pygame.display.set_caption('COLATERAL-21') # Título del juego
clock = pygame.time.Clock()

#region Constantes
WIDTH = 800
HEIGHT = 600

BLACK = (15, 15, 25)
GREY = (65,65,65)
WHITE = (255, 255, 255)
GREEN = (0, 180, 0)
RED = (180, 0, 0)
SCORE_COLOR = (random.randint(0,20), random.randint(180,255), random.randint(180,200))
KILLS_COLOR = (random.randint(170,255), random.randint(0,50), 0)

LIFEBAR_WIDTH = 3
MISSILE_SPEED = 6
MISSILE_DMG = 3
PLAYER_SPEED = 3.5

SFX_VOLUME = 0.5
BGM_VOLUME = 0.2

# Dificultad
ENEMY_AMOUNT = 3
#endregion

#region Pantalla
## Crea la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))

## Icono del juego
icon = pygame.image.load('assets/icon.png').convert_alpha()
icon = pygame.transform.scale(icon , (64, 64))
pygame.display.set_icon(icon)
#endregion

#region Player
class Player():
    def __init__(self):
        self.speed = PLAYER_SPEED
        self.x = 0
        self.y = HEIGHT//2
        self.dy = 0
        self.dx = 0
        self.image = pygame.image.load('assets/player.png').convert_alpha()
        self.image.set_colorkey(BLACK)
        self.score = 0
        self.max_health = 20
        self.health = self.max_health
        self.kills = 0
        
    def up(self):
        self.dy = -self.speed
        
    def down(self):
        self.dy = self.speed
    
    def left(self):
        self.dx = -self.speed
    
    def right(self):
        self.dx = self.speed
    
    def move(self):
        # Calibra el movimiento diagonal
        self.y = self.y + self.dy/1.2
        self.x = self.x + self.dx/1.2 
        
        # Chequeo de colisión
        if self.y < 0:
            self.y = 0
            self.dy = 0
            
        elif self.y > 550 :
            self.y = 550    
            self.dy = 0
            
        if self.x < 0:
            self.x = 0
            self.dx = 0
        
        elif self.x > 200:
            self.x = 200
            self.dx = 0

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
            
    def render(self):
        screen.blit(self.image, (int(self.x), int(self.y)))
        
        # Randeriza la barra de vida
        pygame.draw.line(screen, GREEN, (int(self.x), int(self.y)), (int(self.x + (40 * (self.health/self.max_health))), int(self.y)), LIFEBAR_WIDTH)
#endregion

#region Missile
class Missile():
    def __init__(self):
        self.x = 0
        self.y = 1000
        self.dx = 0
        self.image = pygame.image.load('assets/missile.png').convert_alpha()
        self.state = 'ready'
    
    def fire(self):
        self.state = 'firing'
        self.x = player.x + 25
        self.y = player.y + 16
        self.dx = MISSILE_SPEED
    
    def move(self):
        if self.state == 'firing':
            self.x = self.x + self.dx 
            
        if self.x > 800:
            self.state = 'ready'
            self.y = 1000

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def render(self):
        screen.blit(self.image, (int(self.x), int(self.y)))
#endregion

#region Enemy
class Enemy():
    def __init__(self):
        self.x = 800
        self.y = random.randint(0, 550)
        self.dx = random.randint(10, 50) / -10
        self.dy = 0
        self.surface = pygame.image.load('assets/enemy.png').convert_alpha()
        self.rect = self.surface.get_rect()
        self.max_health = random.randint(5, 15)
        self.health = self.max_health
        self.type = 'enemy'

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        
        # Chequeo de bordes
        if self.x < -30:
            self.x = random.randint(800, 900)
            self.y = random.randint(0, 550) 
            
        # Chequeo de colisión
        if self.y < 0:
            self.y = 0
            self.dy *= -1
            
        elif self.y > 550 :
            self.y = 550    
            self.dy *= -1
            
    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def render(self):
        screen.blit(self.surface, (int(self.x), int(self.y)))

        # Randeriza barra de vida
        pygame.draw.line(screen, RED, (int(self.x), int(self.y)), (int(self.x + (30 * (self.health/self.max_health))), int(self.y)), LIFEBAR_WIDTH)
#endregion

#region Star
class Star():
    def __init__(self):
        self.x = random.randint(0, 1000)
        self.y = random.randint(0, 550)
        self.dx = random.randint(10, 50) / -30
        images = ['assets/yellow_star.png', 'assets/red_star.png', 'assets/white_star.png']
        self.surface = pygame.image.load(random.choice(images))

    def move(self):
        self.x = self.x + self.dx
        
        # Chequeo de bordes
        if self.x < 0:
            self.x = random.randint(800, 900)
            self.y = random.randint(0, 550)        

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def render(self):
        screen.blit(self.surface, (int(self.x), int(self.y)))
#endregion

#region Menu

def draw_text(surface, text, size, x, y, color):
	font = pygame.font.Font('assets/font/kenvector_future_thin.ttf', size)
	text_surface = font.render(text, True, color)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surface.blit(text_surface, text_rect)

def show_menu():
    screen.blit(screen, [0,0])
    screen.fill(BLACK)
    draw_text(screen, "COLATERAL-21", 65, WIDTH//2, HEIGHT//4, RED)
    draw_text(screen, "CONTROLES", 28, WIDTH // 2, HEIGHT // 2.3, WHITE)
    draw_text(screen, "Movimiento: FLECHAS", 18, WIDTH // 2, HEIGHT // 1.9, WHITE)
    draw_text(screen, "Disparo:   BARRA ESP.", 18, WIDTH // 2, HEIGHT // 1.8, WHITE)
    draw_text(screen, "Presione ENTER para jugar", 12, WIDTH // 2, HEIGHT * 3/4, WHITE)
    draw_text(screen, "Hecho por", 10, WIDTH // 2, HEIGHT * 3.5/4, WHITE)
    draw_text(screen, "Suarez Arnaldi, Leonel", 10, WIDTH // 2, HEIGHT * 3.56/4, GREY)
    draw_text(screen, "Moro, Enzo Sebastian", 10, WIDTH // 2, HEIGHT * 3.62/4, GREY)
    draw_text(screen, "Luoni, Brian Sebastian", 10, WIDTH // 2, HEIGHT * 3.68/4, GREY)
    draw_text(screen, "Guevara, Agustin Ezequiel", 10, WIDTH // 2, HEIGHT * 3.74/4, GREY)
    draw_text(screen, "Fernandez, Nahuel", 10, WIDTH // 2, HEIGHT * 3.8/4, GREY)
    draw_text(screen, "Cruz, Denis Liam", 10, WIDTH // 2, HEIGHT * 3.86/4, GREY)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    waiting = False
#endregion

#region SFX & VFX
# Crea sonidos
bgm = pygame.mixer.Sound('assets/bgm.wav')
bgm.set_volume(BGM_VOLUME)

missile_sound = pygame.mixer.Sound('assets/missile.ogg')
explosion_sound = pygame.mixer.Sound('assets/explosion.wav')
kill_sound = pygame.mixer.Sound('assets/kill.wav')
crash_sound = pygame.mixer.Sound('assets/crash.wav')
explosion_sound.set_volume(SFX_VOLUME - 0.3)
missile_sound.set_volume(SFX_VOLUME + 0.4)
kill_sound.set_volume(SFX_VOLUME)
crash_sound.set_volume(SFX_VOLUME - 0.2)

# Crea fuente
#font = pygame.font.SysFont("agencyfb", 24)
font = pygame.font.Font('assets/font/kenvector_future.ttf', 16)
#endregion

####LOOP PRINCIPAL###
#region Main
game_over = True
running = True
debug = False
while running:
    if game_over:
        show_menu()
        game_over = False
        #region Objetos
        # Crea objetos
        player = Player()
        # Resetea variables
        BLACK = (15, 15, 25)
        MISSILE_SPEED = 6
        MISSILE_DMG = 3
        ENEMY_AMOUNT = 3
        PLAYER_SPEED = 3.5
        player.score = 0
        player.kills = 0

        missiles = [Missile(), Missile(), Missile()]

        enemies = []
        for _ in range(ENEMY_AMOUNT):
            enemies.append(Enemy())
            
        stars = []
        for _ in range(30):
            stars.append(Star())

        def fire_missile():
            # Misiles listos
            for missile in missiles:
                if missile.state == "ready":
                    missile.fire()
                    pygame.mixer.Channel(1).play(missile_sound)
                    break
        #endregion
        
    
    bgm.play(-1)
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
            sys.exit()
            
        # Controles
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                player.up()
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                player.down()
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                player.left()
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                player.right()
            elif event.key == pygame.K_SPACE:
                fire_missile()
            elif event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_TAB:
                debug = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_TAB:
                debug = False

    # Actualiza objetos
    player.move()
    for missile in missiles:
        missile.move()
    
    for star in stars:
        star.move()
    
    for enemy in enemies:
        enemy.move()

        # Chequeo de colisión
        for missile in missiles:
            if enemy.distance(missile) < 20:
                pygame.mixer.Channel(0).play(explosion_sound)
                enemy.health -= MISSILE_DMG
                if enemy.health <= 0:
                    pygame.mixer.Channel(3).play(kill_sound)
                    enemy.x = random.randint(800, 900)
                    enemy.y = random.randint(0, 550)
                    
                    player.kills += 1
                    KILLS_COLOR = (random.randint(170,255), random.randint(0,50), 0)
                    # Experimento/Concepto para items de mejora
                    if player.kills >= 50:
                        BLACK = (25, 10, 25)
                        y_missile = pygame.image.load('assets/missileM.png').convert_alpha()
                        missile.image = y_missile
                        MISSILE_SPEED = 16
                        MISSILE_DMG = 5
                        PLAYER_SPEED = 5
                    if player.kills % 10 == 0:
                        enemies.append(Enemy())
                        ENEMY_AMOUNT += 1
                        enemy.surface = pygame.image.load('assets/boss.png').convert_alpha()
                        enemy.max_health = 50
                        enemy.health = enemy.max_health
                        enemy.dy = random.randint(-5, 5)
                        enemy.type = "boss"
                    else:
                        enemy.type = "enemy"
                        enemy.dy = 0
                        enemy.surface = pygame.image.load('assets/enemy.png').convert_alpha()
                        enemy.max_health = random.randint(5, 15)
                        enemy.health = enemy.max_health
                else:
                    enemy.x += 20

                # Resetear munición
                missile.dx = 0
                missile.x = 0
                missile.y = 1000
                missile.state = "ready"
                
                # Añadir al contador
                player.score += 10
                SCORE_COLOR = (random.randint(0,20), random.randint(180,255), random.randint(180,255))
        
        # Chequeo de colisión
        if enemy.distance(player) < 20:
            pygame.mixer.Channel(2).play(crash_sound)
            
            player.health -= random.randint(5, 10)
            enemy.health -= random.randint(5, 10)
            enemy.x = random.randint(800, 900)
            enemy.y = random.randint(0, 550)
            
            if player.health <= 0:
                print("GAME OVER")
                bgm.stop()
                game_over = True

    # Randerizar
    # Llena el fondo de color
    screen.fill(BLACK)
    
    # Randeriza estrellas
    for star in stars:
        star.render()
    
    # Randerizar objetos
    player.render()
    
    for missile in missiles: 
        missile.render()
    
    for enemy in enemies:
        enemy.render()  

    # Contador de munición
    ammo = 0
    for missile in missiles:
        if missile.state == "ready":
            ammo += 1
    
    for x in range(ammo):
        screen.blit(missile.image, (665 + 30 * x, 60))
    
    # Randerizar contador
    # SCORE
    draw_text(screen, f"SCORE", 14, 680, 20, WHITE)
    draw_text(screen, f"{player.score}", 14, 680, 35, SCORE_COLOR)
    # KILLS 
    draw_text(screen, f"KILLS", 14, 740, 20, WHITE)
    draw_text(screen, f"{player.kills}", 14, 740, 35, KILLS_COLOR)
    
    # Randerizar debug 
    if debug:
        draw_text(screen, f"ATT.DAMAGE: {MISSILE_DMG}", 10, 650, 550, GREY)
        draw_text(screen, f"ATT.SPEED: {MISSILE_SPEED}", 10, 650, 558, GREY)
        draw_text(screen, f"VELOCITY: {PLAYER_SPEED}", 10, 650, 566, GREY)
        draw_text(screen, f"HEALTH: {player.health}", 10, 650, 574, GREY)
        draw_text(screen, f"ENEMIES: {ENEMY_AMOUNT}", 10, 650, 574+8, GREY)

    pygame.display.flip()
    
    clock.tick(60)

#endregion
