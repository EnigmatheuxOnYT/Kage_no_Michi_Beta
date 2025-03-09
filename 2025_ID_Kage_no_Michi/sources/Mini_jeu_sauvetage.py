import pygame
import sys
import time
import random
import math
from Cinematics import Cinematics
from Audio import Music, Sound

class minigm_MashingGame:
    
    def __init__(self):
        ### Etats du mini-jeu ###
        self.running = True           # Le jeu tourne
        self.playing = False          # Le mini-jeu est en cours
        self.in_minigm = False        # La phase de gameplay est active
        
        ### Appel de la classe cinématique
        self.cin = Cinematics()
        
        ### Appel des classes pour l'audio
        self.music, self.sound = Music(), Sound()
        
        # Flag pour jouer le SFX d'erreur une seule fois
        self.error_played = False
        
    ########## Démarrage du mini-jeu ##########
    def load(self):
        self.playing = True
        self.load_assets()
     
    def load_assets(self):
        # Initialisation des variables principales
        self.width, self.height = 1280, 720
        self.clock = pygame.time.Clock()
        
        # Définition des niveaux avec leurs paramètres
        self.levels = [
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
        self.num_levels = len(self.levels)
        self.current_level = 0
        self.force = 0
        self.level_complete = False
        self.level_failed = False
        # On ne démarre pas le timer ici : il sera lancé après la cinématique d'intro.
        self.debris_removed = [False] * self.num_levels
        
        # Variables pour l'effet screen shake
        self.shake_timer = 0
        self.shake_magnitude = 0
        
        # Liste des particules pour l'explosion visuelle
        self.particles = []
        
        # Chargement des polices
        self.font = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 24)
        self.font_MFMG30 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 30)
        
        # Chargement des sprites pour les pierres
        self.stone_images = []
        for i in range(1, 6):
            try:
                image = pygame.image.load(f"../data/assets/minigm/Pierre_{i}.png").convert_alpha()
            except Exception as e:
                image = pygame.Surface((self.levels[i-1]["width"], self.levels[i-1]["height"]), pygame.SRCALPHA)
                image.fill(self.levels[i-1]["color"])
            self.stone_images.append(image)
        
        # Chargement du fond
        try:
            self.background = pygame.image.load("../data/assets/bgs/Fond_Aizuwakamatsu_Détruit_Herbe_1.png").convert()
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
        except Exception as e:
            self.background = None
        
        # Position de base pour les pierres
        self.debris_base_y = 150
        
        # Le villageois est affiché en arrière-plan
        self.villager_rect = pygame.Rect((self.width - 150) // 2, 800, 150, 200)
     
    ########## Intro/Fin ##########
    def intro(self, screen, saved):
        self.screen = screen
        self.music.play(self.music.exploration)
        if saved=='none':
            self.cin.cinematic_frame(screen, 'azw2', 2, "Très bien, je vais la retrouver pour vous. Restez en sécurité.", kind_info=[["SM","no_weapon"],["VL1", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'azw2', 2, "Merci infiniment ! Cette pierre est tout ce qu’il me reste de mes ancêtres...", kind_info=[["SM","no_weapon"],["VL1", "no_weapon"], 2], running=self.running)
        elif saved=='KM':
            self.cin.cinematic_frame(screen, 'azw2', 3, "Très bien, je vais la retrouver pour vous. Restez en sécurité.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL1", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'azw2', 3, "Merci infiniment ! Cette pierre est tout ce qu’il me reste de mes ancêtres...", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL1", "no_weapon"], 3], running=self.running)
        elif saved=='KT':
            self.cin.cinematic_frame(screen, 'azw2', 3, "Très bien, je vais la retrouver pour vous. Restez en sécurité.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL1", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'azw2', 3, "Merci infiniment ! Cette pierre est tout ce qu’il me reste de mes ancêtres...", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL1", "no_weapon"], 3], running=self.running)
        self.music.play(self.music.intro)
        self.cin.cinematic_frame(screen, 'azw2', 0, "Appuyez rapidement sur la touche indiquée pour accumuler de la force et", "soulever les débris avant la fin du temps imparti !", kind_info=[[], 0], running=self.running)   
        self.in_minigm = True

    def end(self, screen, saved):
        self.music.play(self.music.exploration)
        # Lancement de la cinématique de fin en fonction de la réussite ou de l'échec
        if self.current_level >= self.num_levels:
            if saved=='none':
                self.cin.cinematic_frame(screen, 'azw2', 2, "Vous l’avez trouvée ! Oh, mille mercis ! Je ne sais comment vous remercier...", "Prenez ceci, ce n’est pas grand-chose, mais c’est tout ce que je peux offrir.", kind_info=[["SM","no_weapon"],["VL1", "no_weapon"], 2], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 2, "Ce n’était pas nécessaire, mais je vous remercie.", "Gardez bien cette pierre, elle est précieuse. Prenez soin de vous.", kind_info=[["SM","no_weapon"],["VL1", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 2, "Que les esprits veillent sur vous ! Bonne chance à vous, noble samouraï !", kind_info=[["SM","no_weapon"],["VL1", "no_weapon"], 2], running=self.running)
            elif saved=='KM':
                self.cin.cinematic_frame(screen, 'azw2', 3, "Vous l’avez trouvée ! Oh, mille mercis ! Je ne sais comment vous remercier...", "Prenez ceci, ce n’est pas grand-chose, mais c’est tout ce que je peux offrir.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL1", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "Ce n’était pas nécessaire, mais je vous remercie.", "Gardez bien cette pierre, elle est précieuse. Prenez soin de vous.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL1", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "Que les esprits veillent sur vous ! Bonne chance à vous, noble samouraï !", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL1", "no_weapon"], 3], running=self.running)
            elif saved=='KT':
                self.cin.cinematic_frame(screen, 'azw2', 3, "Vous l’avez trouvée ! Oh, mille mercis ! Je ne sais comment vous remercier...", "Prenez ceci, ce n’est pas grand-chose, mais c’est tout ce que je peux offrir.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL1", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "Ce n’était pas nécessaire, mais je vous remercie.", "Gardez bien cette pierre, elle est précieuse. Prenez soin de vous.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL1", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "Que les esprits veillent sur vous ! Bonne chance à vous, noble samouraï !", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL1", "no_weapon"], 3], running=self.running)
        else:
            if saved=='none':
                self.cin.cinematic_frame(screen, 'azw2', 2, "Je.. Je suis désolé. J’ai fouillé partout mais je ne parviens pas à", "retrouver votre pierre précieuse...", kind_info=[["SM","no_weapon"],["VL1", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 2, "Non... C’est impossible... Cette pierre représentait des générations entières", "d’histoire familiale...", kind_info=[["SM","no_weapon"],["VL1", "no_weapon"], 2], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 2, "Peut-être qu’avec le temps, les débris seront plus faciles à déplacer.", "Je reviendrai essayer plus tard.", kind_info=[["SM","no_weapon"],["VL1", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 2, "...D’accord. Je vais attendre ici.", kind_info=[["SM","no_weapon"],["VL1", "no_weapon"], 2], running=self.running)
            elif saved=='KM':
                self.cin.cinematic_frame(screen, 'azw2', 3, "Je.. Je suis désolé. J’ai fouillé partout mais je ne parviens pas à", "retrouver votre pierre précieuse...", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL1", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "Non... C’est impossible... Cette pierre représentait des générations entières", "d’histoire familiale...", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL1", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "Peut-être qu’avec le temps, les débris seront plus faciles à déplacer.", "Je reviendrai essayer plus tard.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL1", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "...D’accord. Je vais attendre ici.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL1", "no_weapon"], 3], running=self.running)
            elif saved=='KT':
                self.cin.cinematic_frame(screen, 'azw2', 3, "Je.. Je suis désolé. J’ai fouillé partout mais je ne parviens pas à", "retrouver votre pierre précieuse...", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL1", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "Non... C’est impossible... Cette pierre représentait des générations entières", "d’histoire familiale...", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL1", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "Peut-être qu’avec le temps, les débris seront plus faciles à déplacer.", "Je reviendrai essayer plus tard.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL1", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "...D’accord. Je vais attendre ici.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL1", "no_weapon"], 3], running=self.running)
        self.playing = False
     
    ########## Partie 1 : évènements ##########
    def minigm_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.event.post(event)
            # Gestion de la force avec les touches et la souris
            if event.type == pygame.KEYDOWN and not self.level_complete and not self.level_failed:
                if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    self.force += 5
                    self.shake_timer = 0.2
                    self.shake_magnitude = 5
            if event.type == pygame.MOUSEBUTTONDOWN and not self.level_complete and not self.level_failed:
                self.force += 5
                self.shake_timer = 0.2
                self.shake_magnitude = 5
        
        # Gestion du plein écran avec F11
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_F11]:
            pygame.display.toggle_fullscreen()
            self.clock.tick(5)
        
    ########## Partie 2 : Mise à jour ##########
    def minigm_update(self):
        config = self.levels[self.current_level]
        threshold = config["threshold"]
        time_limit = config["time_limit"]
        max_offset = config["max_offset"]
        
        elapsed_time = time.time() - self.start_time
        self.remaining_time = max(0, time_limit - elapsed_time)
        
        if self.remaining_time < 3:
            self.shake_timer = max(self.shake_timer, 0.05)
            self.shake_magnitude = 7
        
        if self.force >= threshold:
            self.level_complete = True
        if self.remaining_time <= 0 and self.force < threshold:
            self.level_failed = True
        
        for particle in self.particles[:]:
            particle["x"] += particle["dx"]
            particle["y"] += particle["dy"]
            particle["lifetime"] -= 1/60
            if particle["lifetime"] <= 0:
                self.particles.remove(particle)
                
        if self.shake_timer > 0:
            self.shake_timer -= 1/60
        
    ########## Partie 3 : Affichage ##########
    def minigm_draw(self, screen):
        game_surface = pygame.Surface((self.width, self.height))
        if self.background:
            game_surface.blit(self.background, (0, 0))
        else:
            game_surface.fill((30, 30, 30))
        
        for i in reversed(range(self.num_levels)):
            if self.debris_removed[i]:
                continue
            stone = self.stone_images[i]
            stone_rect = stone.get_rect()
            stone_rect.x = (self.width - stone_rect.width) // 2
            stone_rect.y = self.debris_base_y
            
            if i == self.current_level:
                progress = min(self.force / self.levels[self.current_level]["threshold"], 1)
                offset = int(progress * self.levels[self.current_level]["max_offset"] * 1.5)
                angle = progress * 20
                stone_rect.x -= offset
                if angle != 0:
                    rotated_stone = pygame.transform.rotate(stone, angle)
                    rotated_rect = rotated_stone.get_rect(center=stone_rect.center)
                    game_surface.blit(rotated_stone, rotated_rect)
                else:
                    game_surface.blit(stone, stone_rect)
            else:
                game_surface.blit(stone, stone_rect)
        
        gauge_width, gauge_height = 400, 40
        gauge_x = (self.width - gauge_width) // 2
        gauge_y = 600
        pygame.draw.rect(game_surface, (255, 255, 255), (gauge_x, gauge_y, gauge_width, gauge_height), 2)
        fill_width = int((self.force / self.levels[self.current_level]["threshold"]) * gauge_width)
        fill_width = min(fill_width, gauge_width)
        pygame.draw.rect(game_surface, (0, 200, 0), (gauge_x, gauge_y, fill_width, gauge_height))
        if self.force / self.levels[self.current_level]["threshold"] > 0.8:
            pulsate = 128 + 127 * math.sin(time.time() * 10)
            pygame.draw.rect(game_surface, (pulsate, pulsate, 0), (gauge_x, gauge_y, gauge_width, gauge_height), 4)
        
        for particle in self.particles:
            alpha = int(255 * (particle["lifetime"] / 1.0))
            color = (255, 255, 255, alpha)
            pygame.draw.circle(game_surface, color, (int(particle["x"]), int(particle["y"])), 3)
        
        if self.remaining_time < 3:
            flash = abs(math.sin(time.time() * 10)) * 100
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((255, 0, 0, int(flash)))
            game_surface.blit(overlay, (0, 0))
        
        shake_offset_x, shake_offset_y = 0, 0
        if self.shake_timer > 0:
            shake_offset_x = random.randint(-self.shake_magnitude, self.shake_magnitude)
            shake_offset_y = random.randint(-self.shake_magnitude, self.shake_magnitude)
        
        screen.fill((0, 0, 0))
        screen.blit(game_surface, (shake_offset_x, shake_offset_y))
        
        # Affichage des textes d'information
        text_level = self.font.render(f"Niveau {self.current_level+1} / {self.num_levels}", True, (255, 255, 255))
        text_force = self.font.render(f"Force : {self.force} / {self.levels[self.current_level]['threshold']}", True, (255, 255, 255))
        text_time = self.font.render(f"Temps restant : {self.remaining_time:.1f} s", True, (255, 255, 255))
        screen.blit(text_level, (gauge_x + 50, gauge_y - 90))
        screen.blit(text_force, (gauge_x + 50, gauge_y - 60))
        screen.blit(text_time, (gauge_x + 50, gauge_y - 30))
        
        pygame.display.flip()
        self.clock.tick(60)
        
    ########## Boucle mini-jeu ##########
    def run(self, screen, saved):
        self.screen = screen
        self.load()
        self.intro(screen, saved)
        # Démarrage du timer après la cinématique d'intro
        self.start_time = time.time()
        
        while self.playing and self.running and self.in_minigm:
            self.minigm_events()
            self.minigm_update()
            self.minigm_draw(screen)
            
            # Transition entre niveaux
            if self.level_complete:
                # Mise à jour de l'affichage et vidage de la file d'événements
                pygame.display.flip()
                pygame.event.clear()
                pygame.time.wait(1000)
                self.debris_removed[self.current_level] = True
                self.current_level += 1
                if self.current_level < self.num_levels:
                    self.force = 0
                    self.level_complete = False
                    self.level_failed = False
                    # Démarrage du timer pour le niveau suivant
                    self.start_time = time.time()
                else:
                    self.playing = False  # Fin du mini-jeu (succès)
                    
            if self.level_failed:
                if not self.error_played:
                    self.sound.play(self.sound.error)
                    self.error_played = True
                pygame.display.flip()
                pygame.time.wait(1000)
                self.playing = False  # Fin du mini-jeu (échec)
                
        # Lancement de la cinématique de fin pour tous les cas
        self.end(screen, saved)
            
        return self.running

# Lancement du mini-jeu
if __name__ == '__main__':
    pygame.init()
    
    icon = pygame.image.load("../data/assets/common/Icone_LOGO_V12.ico")
    pygame.display.set_icon(icon)
    cursor = pygame.image.load("../data/assets/common/Souris_V4.png")
    pygame.mouse.set_cursor((5, 5), cursor)
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Kage no michi")
    
    minigm = minigm_MashingGame()
    minigm.run(screen, 'KM')
    pygame.quit()
    sys.exit()
