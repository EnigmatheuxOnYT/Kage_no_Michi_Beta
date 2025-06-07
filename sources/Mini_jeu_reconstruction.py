#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao

# -*- coding: utf-8 -*-
"""
Created on Mon Jan 20 17:38:15 2025

@author: ahmed-adamrezkallah & maximerousseaux
"""

#############
"""Placer le fichier dans le même dossier que le reste des fichiers python"""
#############

import sys
import random
import math
import pygame
from Cinematics import Cinematics
from Audio import Music, Sound

class minigm_mastermind:
    def __init__(self):
        ### États du mini-jeu ###
        self.running = True      # Le jeu tourne
        self.playing = False     # Le mini-jeu est en cours
        self.in_minigm = False   # La phase de gameplay est active

        ### Appel de la classe cinématique
        self.cin = Cinematics()

        ### Appel des classes pour l'audio
        self.music, self.sound = Music(), Sound()

        # Paramètres généraux
        self.width, self.height = 1280, 720
        self.clock = pygame.time.Clock()

    ########## Démarrage du mini-jeu ##########
    def load(self):
        self.playing = True
        self.load_assets()

    def load_assets(self):
        # Configuration audio
        pygame.mixer.set_num_channels(16)

        # Thème visuel
        self.theme = {
            'background': (30, 30, 45),
            'accent': (98, 210, 162),
            'text': (0, 0, 0),
            'highlight': (255, 255, 255, 50),
            'panel': (45, 45, 60)
        }

        # Note : les sfx seront désormais lancés via self.sound
        # et la musique via self.music (ex. self.music.play(self.music.intro))

        # Variables pour les effets visuels
        self.shake_time = 0
        self.shake_duration = 0
        self.shake_magnitude = 0
        self.flash_time = 0
        self.flash_duration = 0
        self.flash_color = (0, 255, 0)

        # Chargement des polices
        self.font = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 24)
        self.font_bold = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 30)
        
        # Tailles des briques et de la grille
        self.brick_size = 70
        self.grid_square_size = self.brick_size + 20

        # Chargement des images des briques
        self.brick_images = {}
        color_names = ["rouge", "vert", "bleu", "jaune", "gris", "rose"]
        color_values = {
            "rouge": (255, 99, 132),
            "vert": (120, 224, 143),
            "bleu": (100, 181, 246),
            "jaune": (255, 236, 153),
            "gris": (50, 50, 50),
            "rose": (255, 161, 224)
        }
        for color in color_names:
            try:
                img = pygame.image.load(f"../data/assets/minigm/brique_{color}.png").convert_alpha()
                img = pygame.transform.scale(img, (self.brick_size, self.brick_size))
                self.brick_images[color] = img
            except Exception as e:
                print(f"Erreur de chargement de l'image pour {color}: {e}. Utilisation de la couleur par défaut.")
                surf = pygame.Surface((self.brick_size, self.brick_size), pygame.SRCALPHA)
                pygame.draw.rect(surf, color_values[color], (0, 0, self.brick_size, self.brick_size), border_radius=12)
                self.brick_images[color] = surf

        # Chargement du sprite de fond (terre)
        try:
            terre_img = pygame.image.load("../data/assets/minigm/terre.png").convert_alpha()
            bg_width = 4 * self.grid_square_size + 3 * 20 + 92
            bg_height = self.grid_square_size + 21
            self.terre_sprite = pygame.transform.scale(terre_img, (bg_width, bg_height))
        except Exception as e:
            print(f"Erreur de chargement du sprite de terre: {e}. Utilisation d'un fond uni.")
            self.terre_sprite = None

        # Chargement du sprite du panneau d'information
        try:
            info_panel_img = pygame.image.load("../data/assets/minigm/Parchemin_Reponses.png").convert_alpha()
            self.info_panel_sprite = pygame.transform.scale(info_panel_img, (360, 650))
        except Exception as e:
            print(f"Erreur de chargement du sprite du panneau info: {e}. Utilisation d'un fond uni.")
            self.info_panel_sprite = None
        
        # Chargement du fond pour le mini-jeu
        try:
            self.background_sprite = pygame.image.load("../data/assets/bgs/Fond_Aizuwakamatsu_Détruit_3.png").convert_alpha()
            self.background_sprite = pygame.transform.scale(self.background_sprite, (self.width, self.height))
        except Exception as e:
            print("Erreur de chargement du sprite de fond :", e)
            self.background_sprite = None


        # Chargement des sprites pour le feedback
        try:
            self.feedback_images = {
                "correct": pygame.transform.scale(
                    pygame.image.load("../data/assets/minigm/rond_vert.png").convert_alpha(), (24, 24)),
                "misplaced": pygame.transform.scale(
                    pygame.image.load("../data/assets/minigm/rond_jaune.png").convert_alpha(), (24, 24)),
                "wrong": pygame.transform.scale(
                    pygame.image.load("../data/assets/minigm/rond_rouge.png").convert_alpha(), (24, 24))
            }
        except Exception as e:
            print("Erreur lors du chargement des sprites de feedback:", e)
            self.feedback_images = {
                "correct": self.create_feedback_circle((98, 210, 162)),
                "misplaced": self.create_feedback_circle((255, 236, 153)),
                "wrong": self.create_feedback_circle((255, 99, 132, 50))
            }

        # Initialisation de l'état du jeu
        self.reset_game()

    def create_feedback_circle(self, color):
        surf = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(surf, color, (12, 12), 10)
        return surf

    def reset_game(self):
        self.solution = [random.choice(list(self.brick_images.keys())) for _ in range(4)]
        if self.devmode:
            print("Sequence à trouver :", self.solution)
        
        self.max_tries = 6  # Nombre d'essais autorisés
        self.current_try = 0
        self.game_over = False
        self.win = False
        self.board = [[None] * 4 for _ in range(self.max_tries)]
        self.feedback = [[] for _ in range(self.max_tries)]
        self.selected_color = None
        
        # Décalages pour l'affichage de la grille
        self.grid_offset = (80, 10)
        self.grid_spacing = 20
        self.feedback_offset = (self.grid_offset[0] + 4 * (self.grid_square_size + self.grid_spacing) + 40, 0)
        
        # Création des zones interactives et du bouton de suppression
        self.create_interactive_areas()

        # Réinitialisation des effets visuels
        self.shake_time = 0
        self.flash_time = 0
        self.confetti_particles = []  # Confettis en cas de victoire
        self.particles = []           # Particules lors du placement d'une brique

        self.game_over_restart_rect = None
        self.game_over_continue_rect = None

    def create_interactive_areas(self):
        # Zones de la grille d'essai
        self.grid_rects = []
        for row in range(self.max_tries):
            row_rects = []
            for col in range(4):
                x = self.grid_offset[0] + col * (self.grid_square_size + self.grid_spacing)
                y = self.grid_offset[1] + row * (self.grid_square_size + self.grid_spacing)
                row_rects.append(pygame.Rect(x, y, self.grid_square_size, self.grid_square_size))
            self.grid_rects.append(row_rects)

        # Boutons de sélection des briques
        self.color_buttons = {}
        color_names = list(self.brick_images.keys())
        start_x = self.width - 450
        start_y = 250
        for i, color in enumerate(color_names):
            x = start_x + (i % 2) * 90 + 26
            y = start_y + (i // 2) * 90 + 70
            self.color_buttons[color] = pygame.Rect(x, y, self.brick_size, self.brick_size)

        # Bouton "Supprimer"
        self.reset_button = pygame.Rect(self.width - 450, self.height - 130, 200, 50)

    ########## Intro / Fin ##########
    def intro(self, screen, saved):
        self.screen = screen
        # Lancement de la musique d'intro via self.music
        self.music.play(self.music.intro)
        
        # Appel de la cinématique d'intro (finir toujours par running=self.running)
        if saved=='none':
            self.cin.cinematic_frame(screen, 'azw2', 2, "Pourquoi pas. C'est le mieux que je puisse faire pour pouvoir aider", "Aizuwakamatsu.", kind_info=[["SM","no_weapon"],["VL3", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'azw2', 2, "Merci de vos efforts, monsieur le samouraï.", "Ce que vous devez faire, c'est suivre le plan de ce parchemin.", kind_info=[["SM","no_weapon"],["VL3", "no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'azw2', 2, "Elle contient toutes les étapes nécessaires à la reconstruction de ce mur.", "Trouvez la bonne combinaison de briques pour le reconstruire !", "A vous de jouer !", kind_info=[["SM","no_weapon"],["VL3", "no_weapon"], 2], running=self.running)
        elif saved=='KM':
            self.cin.cinematic_frame(screen, 'azw2', 3, "Pourquoi pas. C'est le mieux que je puisse faire pour pouvoir aider", "Aizuwakamatsu.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL3", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'azw2', 3, "Merci de vos efforts, monsieur le samouraï.", "Ce que vous devez faire, c'est suivre le plan de ce parchemin.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL3", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'azw2', 3, "Elle contient toutes les étapes nécessaires à la reconstruction de ce mur.", "Trouvez la bonne combinaison de briques pour le reconstruire !", "A vous de jouer !", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL3", "no_weapon"], 3], running=self.running)
        elif saved=='KT':
            self.cin.cinematic_frame(screen, 'azw2', 3, "Pourquoi pas. C'est le mieux que je puisse faire pour pouvoir aider", "Aizuwakamatsu.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL3", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'azw2', 3, "Merci de vos efforts, monsieur le samouraï.", "Ce que vous devez faire, c'est suivre le plan de ce parchemin.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL3", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'azw2', 3, "Elle contient toutes les étapes nécessaires à la reconstruction de ce mur.", "Trouvez la bonne combinaison de briques pour le reconstruire !", "A vous de jouer !", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL3", "no_weapon"], 3], running=self.running)
        
        self.in_minigm = True

    def end(self, screen, saved):
        
        if self.win:
            if saved=='none':
                self.cin.cinematic_frame(screen, 'azw2', 2, "Splendide ! Vous avez un très bon travail. Je vous félicite.", kind_info=[["SM","no_weapon"],["VL3", "no_weapon"], 2], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 2, "L'honneur est pour moi madame.", "Je me suis contenté du nécessaire, c'est tout simplement du bon sens.", kind_info=[["SM","no_weapon"],["VL3", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 2, "C'est formidable !", "N'hésitez-pas à aller voir les autres habitants dans le coin qui auront", "peut-être besoin de votre aide.", kind_info=[["SM","no_weapon"],["VL3", "no_weapon"], 2], running=self.running)
            elif saved=='KM':
                self.cin.cinematic_frame(screen, 'azw2', 3, "Splendide ! Vous avez un très bon travail. Je vous félicite.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL3", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "L'honneur est pour moi madame.", "Je me suis contenté du nécessaire, c'est tout simplement du bon sens.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL3", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "C'est formidable !", "N'hésitez-pas à aller voir les autres habitants dans le coin qui auront", "peut-être besoin de votre aide.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL3", "no_weapon"], 3], running=self.running)
            elif saved=='KT':
                self.cin.cinematic_frame(screen, 'azw2', 3, "Splendide ! Vous avez un très bon travail. Je vous félicite.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL3", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "L'honneur est pour moi madame.", "Je me suis contenté du nécessaire, c'est tout simplement du bon sens.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL3", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "Elle contient toutes les étapes nécessaires à la reconstruction de ce mur", "N'hésitez-pas à aller voir les autres habitants dans le coin qui auront", "peut-être besoin de votre aide.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL3", "no_weapon"], 3], running=self.running)
        else :
            if saved=='none':
                self.cin.cinematic_frame(screen, 'azw2', 2, "Dommage... Ce n'est pas ce que j'attendais de vous.", kind_info=[["SM","no_weapon"],["VL3", "no_weapon"], 2], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 2, "Je suis désolé, madame.", "J'ai fait de mon mieux, mais cela n'a pas suffi.", kind_info=[["SM","no_weapon"],["VL3", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 2, "Ce n'est pas très brillant.", "D'autres auraient sûrement fait mieux à votre place.", kind_info=[["SM","no_weapon"],["VL3", "no_weapon"], 2], running=self.running)
            elif saved=='KM':
                self.cin.cinematic_frame(screen, 'azw2', 3, "Dommage... Ce n'est pas ce que j'attendais de vous.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL3", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "Je suis désolé, madame.", "J'ai fait de mon mieux, mais cela n'a pas suffi.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL3", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "Ce n'est pas très brillant.", "D'autres auraient sûrement fait mieux à votre place.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["VL3", "no_weapon"], 3], running=self.running)
            elif saved=='KT':
                self.cin.cinematic_frame(screen, 'azw2', 3, "Dommage... Ce n'est pas ce que j'attendais de vous.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL3", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "Je suis désolé, madame.", "J'ai fait de mon mieux, mais cela n'a pas suffi.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL3", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'azw2', 3, "Ce n'est pas très brillant.", "D'autres auraient sûrement fait mieux à votre place.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["VL3", "no_weapon"], 3], running=self.running)
                
        self.playing = False

    ########## Partie 1 : Évènements ##########
    def minigm_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.event.post(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over:
                        self.playing = False
                    else:
                        self.validate_row()

    def handle_click(self, pos):
        if self.game_over and self.game_over_continue_rect and self.game_over_continue_rect.collidepoint(pos):
            self.playing = False
            self.play_sound('click')
            return
        
        if self.reset_button.collidepoint(pos):
            # Supprime la combinaison en cours (la ligne active)
            self.board[self.current_try] = [None] * 4
            self.play_sound('click')
            self.start_flash(0.2, (255, 50, 50))
            return

        for color, rect in self.color_buttons.items():
            if rect.collidepoint(pos):
                self.selected_color = color
                self.play_sound('click')
                return

        if not self.game_over and self.current_try < self.max_tries:
            for col, rect in enumerate(self.grid_rects[self.current_try]):
                if rect.collidepoint(pos) and self.selected_color:
                    self.board[self.current_try][col] = self.selected_color
                    self.play_sound('click')
                    # Lancement d'un effet particulaire lors du placement
                    center_x = rect.x + rect.width // 2
                    center_y = rect.y + rect.height // 2
                    self.spawn_particles(center_x, center_y)

    def spawn_particles(self, x, y):
        brown = (139, 69, 19)
        for _ in range(10):
            particle = {
                'x': x,
                'y': y,
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(-2, 0),
                'color': brown,
                'lifetime': random.uniform(0.5, 1.0)
            }
            self.particles.append(particle)

    def validate_row(self):
        if self.game_over:
            return

        if not all(color is not None for color in self.board[self.current_try]):
            self.sound.play(self.sound.error)
            self.start_flash(0.2, (255, 50, 50))
            return

        guess = self.board[self.current_try]
        temp_solution = self.solution.copy()
        feedback = []

        # Vérification des positions correctes
        for i in range(4):
            if guess[i] == temp_solution[i]:
                feedback.append("correct")
                temp_solution[i] = None
            else:
                feedback.append(None)

        # Vérification des couleurs mal placées
        for i in range(4):
            if feedback[i] is None and guess[i] in temp_solution:
                feedback[i] = "misplaced"
                temp_solution[temp_solution.index(guess[i])] = None
            elif feedback[i] is None:
                feedback[i] = "wrong"

        self.feedback[self.current_try] = feedback

        if all(fb == "correct" for fb in feedback):
            self.game_over = True
            self.win = True
            self.play_sound('win')
            self.start_flash(0.5, (50, 205, 50))
            self.start_confetti()
        else:
            self.start_shake(0.3, 10)
            self.current_try += 1
            if self.current_try >= self.max_tries:
                self.game_over = True
                self.sound.play(self.sound.lose)
                self.start_flash(0.5, (139, 0, 0))

    ########## Partie 2 : Mise à jour ##########
    def minigm_update(self):
        dt = self.clock.get_time() / 1000.0
        self.clock.tick(60)
        self.update_effects(dt)

    def update_effects(self, dt):
        if self.shake_time > 0:
            self.shake_time -= dt
            if self.shake_time < 0:
                self.shake_time = 0
        if self.flash_time > 0:
            self.flash_time -= dt
            if self.flash_time < 0:
                self.flash_time = 0

        # Mise à jour des confettis
        for particle in self.confetti_particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['lifetime'] -= dt
        self.confetti_particles = [p for p in self.confetti_particles if p['lifetime'] > 0]

        # Mise à jour des particules
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['lifetime'] -= dt
        self.particles = [p for p in self.particles if p['lifetime'] > 0]

    def start_shake(self, duration, magnitude):
        self.shake_duration = duration
        self.shake_time = duration
        self.shake_magnitude = magnitude

    def start_flash(self, duration, color):
        self.flash_duration = duration
        self.flash_time = duration
        self.flash_color = color

    def start_confetti(self):
        self.confetti_particles = []
        for _ in range(100):
            particle = {
                'x': random.uniform(0, self.width),
                'y': random.uniform(-50, 0),
                'vx': random.uniform(-2, 2),
                'vy': random.uniform(1, 4),
                'color': random.choice([(139, 69, 19), (160, 82, 45), (101, 67, 33)]),
                'lifetime': random.uniform(2, 4)
            }
            self.confetti_particles.append(particle)

    ########## Partie 3 : Affichage ##########
    def minigm_draw(self, screen):
        canvas = pygame.Surface((self.width, self.height))
        if self.background_sprite:
            canvas.blit(self.background_sprite, (0, 0))
        else:
            canvas.fill(self.theme['background'])

        self.draw_grid(canvas)
        self.draw_info_panel(canvas)
        self.draw_color_picker(canvas)
        self.draw_game_over(canvas)

        # Dessin des particules
        for particle in self.particles:
            alpha = max(0, min(255, int(255 * (particle['lifetime'] / 1.0))))
            particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*particle['color'], alpha), (2, 2), 2)
            canvas.blit(particle_surface, (particle['x'], particle['y']))

        # Dessin des confettis
        for particle in self.confetti_particles:
            alpha = max(0, min(255, int(255 * (particle['lifetime'] / 4))))
            particle_surface = pygame.Surface((4, 4), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*particle['color'], alpha), (2, 2), 2)
            canvas.blit(particle_surface, (particle['x'], particle['y']))

        if self.flash_time > 0:
            flash_alpha = int(255 * (self.flash_time / self.flash_duration))
            flash_overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            flash_overlay.fill((*self.flash_color, flash_alpha))
            canvas.blit(flash_overlay, (0, 0))

        if self.shake_time > 0:
            shake_progress = self.shake_time / self.shake_duration
            magnitude = self.shake_magnitude * shake_progress
            shake_offset = (random.randint(-int(magnitude), int(magnitude)),
                            random.randint(-int(magnitude), int(magnitude)))
        else:
            shake_offset = (0, 0)

        screen.blit(canvas, shake_offset)
        pygame.display.flip()

    def draw_grid(self, surface):
        for row_idx, row in enumerate(self.grid_rects):
            # Fond d'essai avec le sprite de terre si disponible
            first_cell = row[0]
            bg_x = first_cell.x - 46
            bg_y = first_cell.y - 10
            bg_width = 4 * self.grid_square_size + 3 * self.grid_spacing + 20
            bg_height = self.grid_square_size + 20
            if self.terre_sprite:
                surface.blit(self.terre_sprite, (bg_x, bg_y))
            else:
                pygame.draw.rect(surface, self.theme['panel'], (bg_x, bg_y, bg_width, bg_height), border_radius=12)
            
            for col_idx, rect in enumerate(row):
                color = self.board[row_idx][col_idx]
                alpha = 150 if row_idx != self.current_try or self.game_over else 255
                if color:
                    brick_img = self.brick_images[color].copy()
                    brick_x = rect.x + (self.grid_square_size - self.brick_size) // 2
                    brick_y = rect.y + (self.grid_square_size - self.brick_size) // 2
                    surface.blit(brick_img, (brick_x, brick_y))
                else:
                    pygame.draw.rect(surface, (70, 70, 90), rect, 2, border_radius=12)
                    
                if row_idx == self.current_try and not self.game_over:
                    pygame.draw.rect(surface, self.theme['highlight'], rect, 3, border_radius=12)
                    
                if row_idx < self.current_try:
                    fb_pos = (
                        self.feedback_offset[0] + (col_idx % 2) * 30,
                        rect.centery - 12 + (col_idx // 2) * 30
                    )
                    feedback_type = self.feedback[row_idx][col_idx]
                    surface.blit(self.feedback_images[feedback_type], fb_pos)

    def draw_color_picker(self, surface):
        text = self.font_bold.render("CHOISIS TA BRIQUE", True, self.theme['text'])
        surface.blit(text, (self.width - 480, 275))
        
        mouse_pos = pygame.mouse.get_pos()
        for color, rect in self.color_buttons.items():
            if rect.collidepoint(mouse_pos):
                pygame.draw.rect(surface, self.theme['highlight'], rect.inflate(10, 10), border_radius=16)
            if color == self.selected_color:
                scale_factor = 1.0 + 0.1 * math.sin(pygame.time.get_ticks() * 0.005)
                scaled_size = int(self.brick_size * scale_factor)
                scaled_brick = pygame.transform.smoothscale(self.brick_images[color], (scaled_size, scaled_size))
                new_rect = scaled_brick.get_rect(center=rect.center)
                surface.blit(scaled_brick, new_rect)
            else:
                surface.blit(self.brick_images[color], rect)

    def draw_info_panel(self, surface):
        panel_rect = pygame.Rect(self.width - 530, 40, 360, 650)
    
        if self.info_panel_sprite:
            surface.blit(self.info_panel_sprite, (panel_rect.x, panel_rect.y))
        else:
            pygame.draw.rect(surface, self.theme['panel'], panel_rect, border_radius=12)

        # Affichage des essais restants
        essais_text = self.font_bold.render(f"ESSAIS RESTANTS: {self.max_tries - self.current_try}", True, (0, 0, 0))
        essais_rect = essais_text.get_rect(center=(panel_rect.centerx, panel_rect.y + 75))
        surface.blit(essais_text, essais_rect)
        
        # Légende du feedback
        legend_items = [
            ("correct", "Correct"),
            ("misplaced", "Mal placé"),
            ("wrong", "Incorrect")
        ]

        start_y = panel_rect.y + 120
        spacing = 40
        for i, (key, label_text) in enumerate(legend_items):
            sprite = self.feedback_images.get(key)
            if sprite:
                sprite_rect = sprite.get_rect(center=(panel_rect.x + 50, start_y + i * spacing))
                surface.blit(sprite, sprite_rect)
                label = self.font.render(label_text, True, (0, 0, 0))
                label_rect = label.get_rect(midleft=(sprite_rect.right + 10, sprite_rect.centery))
                surface.blit(label, label_rect)
            else:
                circle_x = panel_rect.x + 50
                circle_y = start_y + i * spacing
                default_color = self.theme['accent'] if key == "correct" else ((255, 236, 153) if key == "misplaced" else (255, 99, 132))
                pygame.draw.circle(surface, default_color, (circle_x, circle_y), 8)
                label = self.font.render(label_text, True, (0, 0, 0))
                label_rect = label.get_rect(midleft=(circle_x + 20, circle_y))
                surface.blit(label, label_rect)

        # Bouton Supprimer
        self.reset_button.x = panel_rect.centerx - 100
        self.reset_button.y = panel_rect.y + 540

        pygame.draw.rect(surface, (255, 210, 230), self.reset_button, border_radius=8)
        reset_text = self.font.render("Supprimer", True, (240, 120, 175))
        reset_text_rect = reset_text.get_rect(center=self.reset_button.center)
        surface.blit(reset_text, reset_text_rect)

    def draw_game_over(self, surface):
        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (*self.theme['panel'], 255), (0, 0, self.width, self.height))
            surface.blit(overlay, (0, 0))
            
            if self.win:
                text = "COMBINAISON TROUVÉE !"
                color = self.theme['accent']
            else:
                text = "ECHEC !"
                color = (255, 99, 132)
            text_surf = self.font_bold.render(text, True, color)
            rect = text_surf.get_rect(center=(self.width // 2, self.height // 2 - 100))
            surface.blit(text_surf, rect)
            
            # Affichage de la combinaison solution
            solution_text = self.font.render("La combinaison était :", True, (255, 255, 255))
            solution_rect = solution_text.get_rect(center=(self.width // 2 + 20, self.height // 2))
            surface.blit(solution_text, solution_rect)
            for i, color in enumerate(self.solution):
                brick_rect = self.brick_images[color].get_rect()
                brick_rect.center = (self.width // 2 - 100 + i * 80, self.height // 2 + 60)
                surface.blit(self.brick_images[color], brick_rect)
            
            continue_btn = pygame.Rect(self.width//2 - 100, self.height//2 + 150, 200, 50)
            pygame.draw.rect(surface, (130, 220, 170), continue_btn, border_radius=8)
            text = self.font.render("Continuer", True, (0, 140, 70))
            text_rect = text.get_rect(center=continue_btn.center)
            surface.blit(text, text_rect)
            self.game_over_continue_rect = continue_btn

    def play_sound(self, sound_type):
        try:
            sfx = getattr(self.sound, sound_type)
            self.sound.play(sfx)
        except AttributeError:
            print("Sound effect not found:", sound_type)

    ########## Boucle mini-jeu ##########
    def run(self, screen, saved,devmode=False):
        self.devmode=devmode
        self.load()
        self.intro(screen, saved)
        while self.playing and self.running and self.in_minigm:
            self.minigm_events()
            self.minigm_update()
            self.minigm_draw(screen)
        # Appeler end() si le jeu est terminé
        if self.running and self.game_over:
            self.end(screen, saved)
            return self.running,self.win

if __name__ == '__main__':
    pygame.init()
    
    icon = pygame.image.load("../data/assets/common/Icone_LOGO_V12.ico")
    pygame.display.set_icon(icon)
    cursor = pygame.image.load("../data/assets/common/Souris_V4.png")
    pygame.mouse.set_cursor((5, 5), cursor)
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Kage no michi")
    
    minigm = minigm_mastermind()
    minigm.run(screen, 'KM')
    pygame.quit()
