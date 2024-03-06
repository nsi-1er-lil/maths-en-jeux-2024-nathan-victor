import pygame
import sys
import random

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Mage Battle"
BG_COLOR = (255, 255, 255)  # Blanc

# Paramètres du joueur
PLAYER_COLOR = (0, 0, 255)  # Bleu
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5
PLAYER_START_X = 50
PLAYER_START_Y = WINDOW_HEIGHT // 2 - PLAYER_HEIGHT // 2
PLAYER_PROJECTILE_SPEED = 7
PLAYER_MAX_HEALTH = 3

# Paramètres de l'adversaire (IA)
ENEMY_COLOR = (255, 0, 0)  # Rouge
ENEMY_WIDTH = 50
ENEMY_HEIGHT = 50
ENEMY_SPEED = 4
ENEMY_START_X = WINDOW_WIDTH - 100
ENEMY_START_Y = WINDOW_HEIGHT // 2 - ENEMY_HEIGHT // 2
ENEMY_PROJECTILE_SPEED = 6
ENEMY_MAX_HEALTH = 3

# Paramètres du projectile
PROJECTILE_COLOR = (0, 255, 0)  # Vert
PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 5

# Initialisation de la fenêtre de jeu
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)
clock = pygame.time.Clock()

# Classes du joueur et de l'adversaire
class Mage:
    def __init__(self, x, y, color, speed, max_health):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.color = color
        self.speed = speed
        self.health = max_health
        self.max_health = max_health
        self.projectiles = []

    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def shoot_projectile(self, speed):
        projectile = pygame.Rect(self.rect.x + self.rect.width, self.rect.y + self.rect.height // 2 - PROJECTILE_HEIGHT // 2, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
        self.projectiles.append((projectile, speed))

    def update_projectiles(self):
        for projectile, speed in self.projectiles:
            projectile.x += speed

    def draw_projectiles(self):
        for projectile, _ in self.projectiles:
            pygame.draw.rect(window, PROJECTILE_COLOR, projectile)

    def reset_projectiles(self):
        self.projectiles = []

# Création du joueur et de l'adversaire
player = Mage(PLAYER_START_X, PLAYER_START_Y, PLAYER_COLOR, PLAYER_SPEED, PLAYER_MAX_HEALTH)
enemy = Mage(ENEMY_START_X, ENEMY_START_Y, ENEMY_COLOR, ENEMY_SPEED, ENEMY_MAX_HEALTH)

# Fonction pour détecter les collisions entre projectiles
def handle_collisions():
    for player_projectile, _ in player.projectiles[:]:
        if enemy.rect.colliderect(player_projectile):
            player.projectiles.remove((player_projectile, PLAYER_PROJECTILE_SPEED))
            enemy.health -= 1

    for enemy_projectile, _ in enemy.projectiles[:]:
        if player.rect.colliderect(enemy_projectile):
            enemy.projectiles.remove((enemy_projectile, ENEMY_PROJECTILE_SPEED))
            player.health -= 1

# Fonction pour dessiner les informations de santé
def draw_health_info():
    font = pygame.font.Font(None, 36)
    player_health_text = font.render(f"Player Health: {player.health}", True, (0, 0, 0))
    enemy_health_text = font.render(f"Enemy Health: {enemy.health}", True, (0, 0, 0))
    window.blit(player_health_text, (20, 20))
    window.blit(enemy_health_text, (WINDOW_WIDTH - 200, 20))

# Boucle principale du jeu
running = True
while running:
    window.fill(BG_COLOR)

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot_projectile(PLAYER_PROJECTILE_SPEED)

    # Mouvement du joueur
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.move(0, -player.speed)
    if keys[pygame.K_DOWN]:
        player.move(0, player.speed)

    # Mouvement de l'adversaire (IA)
    if random.randint(0, 30) == 1:
        enemy.shoot_projectile(-ENEMY_PROJECTILE_SPEED)
    if player.rect.y < enemy.rect.y:
        enemy.move(0, -enemy.speed)
    elif player.rect.y > enemy.rect.y:
        enemy.move(0, enemy.speed)

    # Mise à jour des projectiles
    player.update_projectiles()
    enemy.update_projectiles()

    # Gestion des collisions
    handle_collisions()

    # Dessiner les éléments du jeu
    player.draw()
    enemy.draw()
    player.draw_projectiles()
    enemy.draw_projectiles()
    draw_health_info()

    # Vérification de la fin du jeu
    if player.health <= 0 or enemy.health <= 0:
        running = False

    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(60)

# Affichage du gagnant
if player.health <= 0:
    print("Enemy wins!")
elif enemy.health <= 0:
    print("Player wins!")

# Fermeture de Pygame
pygame.quit()
sys.exit()

