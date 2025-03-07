import pygame
import sys
import time
import random
import math

def main():
    pygame.init()
    width, height = 1280, 720
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Mashing Game - tkt toi même tu sais")
    clock = pygame.time.Clock()

    # Définition de 5 niveaux avec leurs paramètres
    # Les paramètres "width" et "height" servent uniquement à la logique du jeu (force, offset, etc.)
    levels = [
        {"threshold": 100, "time_limit": 10, "max_offset": 150,
         "width": 200, "height": 40, "color": (180, 180, 180)},
        {"threshold": 120, "time_limit": 9, "max_offset": 150,
         "width": 220, "height": 45, "color": (160, 160, 160)},
        {"threshold": 140, "time_limit": 8, "max_offset": 150,
         "width": 240, "height": 50, "color": (140, 140, 140)},
        {"threshold": 160, "time_limit": 7, "max_offset": 150,
         "width": 260, "height": 55, "color": (120, 120, 120)},
        {"threshold": 180, "time_limit": 6, "max_offset": 150,
         "width": 280, "height": 60, "color": (100, 100, 100)}
    ]
    num_levels = len(levels)
    current_level = 0
    force = 0
    level_complete = False
    level_failed = False
    start_time = time.time()
    debris_removed = [False] * num_levels

    # Variables pour l'effet screen shake
    shake_timer = 0
    shake_magnitude = 0

    # Liste des particules pour l'explosion visuelle
    particles = []

    # Chargement des polices
    font = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 24)

    # Chargement des sprites pour les pierres ("Pierre_1.png" à "Pierre_5.png")
    stone_images = []
    for i in range(1, 6):
        try:
            image = pygame.image.load(f"../data/assets/minigm/Pierre_{i}.png").convert_alpha()
        except Exception as e:
            # En cas d'erreur de chargement, on crée une surface de secours
            image = pygame.Surface((levels[i-1]["width"], levels[i-1]["height"]), pygame.SRCALPHA)
            image.fill(levels[i-1]["color"])
        stone_images.append(image)

    # Chargement du fond
    try:
        background = pygame.image.load("../data/assets/bgs/Fond_Aizuwakamatsu_Détruit_Herbe_1.png").convert()
        background = pygame.transform.scale(background, (width, height))
    except Exception as e:
        background = None


    # Position de base pour les pierres (les sprites seront centrés horizontalement et affichés à la même hauteur)
    debris_base_y = 150

    # Le villageois est toujours en arrière-plan (dessiné avant les pierres)
    villager_rect = pygame.Rect((width - 150) // 2, 800, 150, 200)

    running = True
    while running:
        # Récupérer les paramètres du niveau actif
        config = levels[current_level]
        threshold = config["threshold"]
        time_limit = config["time_limit"]
        max_offset = config["max_offset"]

        elapsed_time = time.time() - start_time
        remaining_time = max(0, time_limit - elapsed_time)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.KEYDOWN and not level_complete and not level_failed:
                if event.key == pygame.K_SPACE:
                    force += 5
                    # Déclencher un screen shake à chaque pression
                    shake_timer = 0.2
                    shake_magnitude = 5

        # Intensifie le shake si le temps est presque écoulé
        if remaining_time < 3:
            shake_timer = max(shake_timer, 0.05)
            shake_magnitude = 7

        # Vérifie la réussite ou l'échec du niveau
        if force >= threshold:
            level_complete = True
        if remaining_time <= 0 and force < threshold:
            level_failed = True

        # Mise à jour des particules
        for particle in particles[:]:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["lifetime"] -= 1/60
            if particle["lifetime"] <= 0:
                particles.remove(particle)

        # Surface intermédiaire pour le jeu (les éléments visuels qui subiront le shake)
        game_surface = pygame.Surface((width, height))
        if background:
            game_surface.blit(background, (0, 0))
        else:
            game_surface.fill((30, 30, 30))

        # Dessine le villageois en arrière-plan
        pygame.draw.rect(game_surface, (255, 255, 0), villager_rect)

        # Affichage des pierres (les sprites) en respectant l'ordre de calque (du plus grand en bas au plus petit en haut)
        for i in reversed(range(num_levels)):
            if debris_removed[i]:
                continue

            # Récupérer l'image de la pierre sans modification de taille
            stone = stone_images[i]
            stone_rect = stone.get_rect()
            # Calculer la position pour centrer horizontalement
            stone_rect.x = (width - stone_rect.width) // 2
            stone_rect.y = debris_base_y

            # Pour le niveau actif, appliquer un offset et une rotation selon la progression
            if i == current_level:
                progress = min(force / threshold, 1)
                offset = int(progress * max_offset)
                angle = progress * 15  # rotation maximale de 15°
                # Décaler la pierre vers la gauche (comme dans le code original)
                stone_rect.x -= offset
                if angle != 0:
                    rotated_stone = pygame.transform.rotate(stone, angle)
                    # Centrer la rotation sur la position d'origine
                    rotated_rect = rotated_stone.get_rect(center=stone_rect.center)
                    game_surface.blit(rotated_stone, rotated_rect)
                else:
                    game_surface.blit(stone, stone_rect)
            else:
                game_surface.blit(stone, stone_rect)

        # Dessiner la jauge de force (seulement la barre, sans texte)
        gauge_width, gauge_height = 400, 40
        gauge_x = (width - gauge_width) // 2
        gauge_y = 600
        pygame.draw.rect(game_surface, (255, 255, 255), (gauge_x, gauge_y, gauge_width, gauge_height), 2)
        fill_width = int((force / threshold) * gauge_width)
        fill_width = min(fill_width, gauge_width)
        pygame.draw.rect(game_surface, (0, 200, 0), (gauge_x, gauge_y, fill_width, gauge_height))
        # Effet pulsant sur la bordure de la jauge si l'on est proche du seuil
        if force / threshold > 0.8:
            pulsate = 128 + 127 * math.sin(time.time() * 10)
            pygame.draw.rect(game_surface, (pulsate, pulsate, 0), (gauge_x, gauge_y, gauge_width, gauge_height), 4)

        # Dessiner les particules sur la surface de jeu
        for particle in particles:
            alpha = int(255 * (particle["lifetime"] / 1.0))
            color = (255, 255, 255, alpha)
            pygame.draw.circle(game_surface, color, (int(particle["x"]), int(particle["y"])), 3)

        # Overlay rouge clignotant quand le temps est très court
        if remaining_time < 3:
            flash = abs(math.sin(time.time() * 10)) * 100
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, int(flash)))
            game_surface.blit(overlay, (0, 0))

        # Calcul de l'offset de screen shake
        shake_offset_x, shake_offset_y = 0, 0
        if shake_timer > 0:
            shake_offset_x = random.randint(-shake_magnitude, shake_magnitude)
            shake_offset_y = random.randint(-shake_magnitude, shake_magnitude)
            shake_timer -= 1 / 60

        # Afficher le jeu avec l'effet de shake
        screen.fill((0, 0, 0))
        screen.blit(game_surface, (shake_offset_x, shake_offset_y))

        # Dessiner les textes (positions fixes, non affectées par le shake)
        text_level = font.render(f"Niveau {current_level+1} / {num_levels}", True, (255, 255, 255))
        text_force = font.render(f"Force : {force} / {threshold}", True, (255, 255, 255))
        text_time = font.render(f"Temps restant : {remaining_time:.1f} s", True, (255, 255, 255))
        screen.blit(text_level, (gauge_x + 50, gauge_y - 90))
        screen.blit(text_force, (gauge_x + 50, gauge_y - 60))
        screen.blit(text_time, (gauge_x + 50, gauge_y - 30))

        # Afficher le message de fin de niveau le cas échéant
        if level_complete:
            msg = font.render("Niveau terminé !", True, (0, 255, 0))
            screen.blit(msg, ((width - msg.get_width()) // 2, gauge_y - 120))
        if level_failed:
            msg = font.render("Échec du niveau !", True, (255, 0, 0))
            screen.blit(msg, ((width - msg.get_width()) // 2, gauge_y - 120))

        pygame.display.flip()
        clock.tick(60)

        # Gestion des transitions de niveau
        if level_complete:
            pygame.display.flip()
            pygame.time.wait(1000)
            debris_removed[current_level] = True
            current_level += 1
            if current_level >= num_levels:
                final_msg = font.render("Villageois Sauvé !", True, (0, 255, 0))
                screen.blit(final_msg, ((width - final_msg.get_width()) // 2, 50))
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False
            else:
                force = 0
                level_complete = False
                level_failed = False
                start_time = time.time()
        if level_failed:
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
