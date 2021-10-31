# SEMINARIO DE LENGUAJES — 2021
# Proyecto de Videojuego en Pygame
# ————————————INTEGRANTES————————————
# Cruz, Denis            —
# Fernandez, Nahuel      —
# Guevara, Agustín       —
# Luoni, Brian           —
# Moro, Enzo             —
# Suarez Arnaldi, Leonel — 39.810.113

import pygame
import sys
import random

pygame.init()
pygame.display.set_caption("COLATERAL-21")
clock = pygame.time.Clock()

WIDTH = 800
HEIGHT = 600

BLACK = (15, 15, 15)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (200, 0, 0)

# Crea la pantalla
screen = pygame.display.set_mode((WIDTH, HEIGHT))

icon = pygame.image.load('assets/icon.png').convert_alpha()
icon = pygame.transform.scale(icon , (64, 64))
pygame.display.set_icon(icon)

# Crea clase Player
class Player():
    def __init__(self):
        self.speed = 3.5
        self.x = 0
        self.y = 0
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
        self.y = self.y + self.dy
        self.x = self.x + self.dx/1.5 # Calibra el movimiento diagonal
        
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
        pygame.draw.line(screen, GREEN, (int(self.x), int(self.y)), (int(self.x + (40 * (self.health/self.max_health))), int(self.y)), 2)

class Missile():
    def __init__(self):
        self.x = 0
        self.y = 1000
        self.dx = 0
        self.image = pygame.image.load('assets/missile.png').convert_alpha()
        self.state = "ready"
    
    def fire(self):
        self.state = "firing"
        self.x = player.x + 25
        self.y = player.y + 16
        self.dx = 7
    
    def move(self):
        if self.state == "firing":
            self.x = self.x + self.dx 
            
        if self.x > 800:
            self.state = "ready"
            self.y = 1000

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def render(self):
        screen.blit(self.image, (int(self.x), int(self.y)))

class Enemy():
    def __init__(self):
        self.x = 800
        self.y = random.randint(0, 550)
        self.dx = random.randint(10, 50) / -10
        self.dy = 0
        self.surface = pygame.image.load('assets/enemy.png').convert_alpha()
        self.max_health = random.randint(5, 15)
        self.health = self.max_health
        self.type = "enemy"
        

    def move(self):
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        
        # Border check
        if self.x < -30:
            self.x = random.randint(800, 900)
            self.y = random.randint(0, 550) 
            
        # Check for border collision
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
        
        # Draw health meter
        pygame.draw.line(screen, RED, (int(self.x), int(self.y)), (int(self.x + (30 * (self.health/self.max_health))), int(self.y)), 2)

class Star():
    def __init__(self):
        self.x = random.randint(0, 1000)
        self.y = random.randint(0, 550)
        self.dx = random.randint(10, 50) / -30
        images = ["assets/yellow_star.png", "assets/red_star.png", "assets/white_star.png"]
        self.surface = pygame.image.load(random.choice(images))

    def move(self):
        self.x = self.x + self.dx
        
        # Border check
        if self.x < 0:
            self.x = random.randint(800, 900)
            self.y = random.randint(0, 550)        

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def render(self):
        screen.blit(self.surface, (int(self.x), int(self.y)))


# Create sounds
missile_sound = pygame.mixer.Sound("assets/missile.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")

# Create font
font = pygame.font.SysFont("agencyfb", 24)

# Create objects
player = Player()
missiles = [Missile(), Missile(), Missile()]

enemies = []
for _ in range(5):
    enemies.append(Enemy())
    
stars = []
for _ in range(30):
    stars.append(Star())

def fire_missile():
    # Is the missile ready
    for missile in missiles:
        if missile.state == "ready":
            missile.fire()
            missile_sound.play()
            break

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
            
        # Controles
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player.up()
            elif event.key == pygame.K_DOWN:
                player.down()
            elif event.key == pygame.K_LEFT:
                player.left()
            elif event.key == pygame.K_RIGHT:
                player.right()
            elif event.key == pygame.K_SPACE:
                fire_missile()

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
                explosion_sound.play()
                enemy.health -= 4
                if enemy.health <= 0:
                    enemy.x = random.randint(800, 900)
                    enemy.y = random.randint(0, 550)
                    
                    player.kills += 1
                    if player.kills % 10 == 0:
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
        
        # Chequeo de colisión
        if enemy.distance(player) < 20:
            explosion_sound.play()
            
            player.health -= random.randint(5, 10)
            enemy.health -= random.randint(5, 10)
            enemy.x = random.randint(800, 900)
            enemy.y = random.randint(0, 550)
            
            if player.health <= 0:
                print("Game over!")
                pygame.quit()
                exit()    

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
        screen.blit(missile.image, (700 + 30 * x, 20))
    
    # Randerizar contador
    score_surface = font.render(f"Score: {player.score} Kills: {player.kills}", True, WHITE)
    screen.blit(score_surface, (500, 5))
    
    pygame.display.flip()
    
    clock.tick(60)
