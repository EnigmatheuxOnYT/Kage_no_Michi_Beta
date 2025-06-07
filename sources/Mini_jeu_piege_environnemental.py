#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao

import pygame
import random
import sys
import os
import math
from Cinematics import Cinematics
from Audio import Music, Sound

#########################################
# Classe minigm_minesweeper
#########################################
class minigm_minesweeper:
    """
    Mini-jeu Démineur de 'Kage no Michi' avec effets spéciaux avancés :
      - Flash coloré sur case (vert pour case vide, rouge pour pic)
      - Shake rapide et intense lors d'une explosion
      - Heartbeat smooth sur le timer (avec interpolation de couleur et scale)
      - Confettis et overlay dynamique en cas de victoire
      - Gestion soignée du hover
      - Système de vie : le joueur démarre avec 3 vies. À chaque pic découvert, il perd une vie et le mini-jeu se termine (sauf si des vies restent, auquel cas une nouvelle carte est générée).
    """
    
    def __init__(self):
        # États généraux
        self.running = True      
        self.playing = False     
        self.in_minigm = False   
        self.lives = 3  # Système de vie : 3 vies initiales
        
        self.cin = Cinematics()
        self.music, self.sound = Music(), Sound()
        
        self.font_MFMG30 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 30)
        self.font_MFMG25 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 25)
        
        ##### Paramètres du jeu #####
        self.TAILLE = 15  # Nombre de cases par côté
        self.TAILLE_CASE = 30  # Taille de chaque case en pixels
        self.FREQUENCE_PICS = 0.15  # Fréquence des pics
        self.LARGEUR_ECRAN = 1280
        self.HAUTEUR_ECRAN = 720
        self.NOMBRE_PICS = int(self.TAILLE * self.TAILLE * self.FREQUENCE_PICS)  # Calcul du nb de pics
        self.LIMITE_TIMER = int(self.TAILLE * 15)  # Temps à disposition en fonction du nb de cases
        
        # Effets spéciaux
        self.flash_effect = None       # {"time": ..., "cell": (x,y), "color": (R,G,B)}
        self.flash_duration = 150      # ms
        
        self.shake_start = None
        self.shake_duration = 250      # ms en cas d'explosion
        self.shake_intensity = 20      # pixels pour explosion
        
        # Heartbeat pour le timer
        self.heartbeat = False  
        self.heartbeat_period = 800    # ms pour une pulsation complète
        
        # Hover sur une case
        self.hover_cell = None
        
        # Effet victoire
        self.victory_confetti = []
        self.victory_effect_start = None
        
        # SFX et musique
        self.sfx_pic = self.sound.click1
        self.sfx_pic.set_volume(1)
        self.sfx_reveal = self.sound.impact1
        self.sfx_reveal.set_volume(1)
        
        
    ########## INITIALISATION / CHARGEMENT DES ASSETS ##########
    def load(self):
        self.playing = True
        self.load_assets()
        
    def load_assets(self):
        self.images = self._charger_images()
        self._init_game()
        
    def _init_game(self):
        """Réinitialise l'état du plateau et des variables d'effets, sans réinitialiser les vies."""
        self.plateau = [[0 for _ in range(self.TAILLE)] for _ in range(self.TAILLE)]
        self.revele = [[False for _ in range(self.TAILLE)] for _ in range(self.TAILLE)]
        self.drapeaux = [[False for _ in range(self.TAILLE)] for _ in range(self.TAILLE)]
        self.pics_restants = self.NOMBRE_PICS
        self.premier_clic = False
        self.game_over = False
        self.victoire = False
        self.temps_debut = pygame.time.get_ticks()
        self.temps_ecoule = 0
        self.temps_clic_pic = 0
        self.afficher_pics = False
        
        # Réinitialiser les effets
        self.flash_effect = None
        self.shake_start = None
        self.hover_cell = None
        self.heartbeat = False
        self.victory_confetti = []
        self.victory_effect_start = None
        
        # Calcul des offsets pour centrer le plateau
        self.offset_x = (self.LARGEUR_ECRAN - self.TAILLE * self.TAILLE_CASE) // 2
        self.offset_y = (self.HAUTEUR_ECRAN - self.TAILLE * self.TAILLE_CASE) // 2
    
    def _charger_images(self):
        """Charge et redimensionne les images du jeu."""
        images = {}
        try:
            images["case_cachee"] = pygame.image.load("../data/assets/minigm/case_cachee.png").convert_alpha()
            images["case_vide"]   = pygame.image.load("../data/assets/minigm/case_vide.png").convert()
            images["pic"]         = pygame.image.load("../data/assets/minigm/pic.png").convert_alpha()
            images["drapeau"]     = pygame.image.load("../data/assets/minigm/drapeau.png").convert_alpha()
            images["fond"]        = pygame.image.load("../data/assets/bgs/Fond_Forêt_Bambou_3.png").convert()
            
            taille_case = (self.TAILLE_CASE, self.TAILLE_CASE)
            for key in ["case_cachee", "case_vide", "pic", "drapeau"]:
                images[key] = pygame.transform.scale(images[key], taille_case)
            
            for i in range(1, 9):
                key = f"chiffre_{i}1"
                images[key] = pygame.image.load(f"../data/assets/minigm/chiffre_{i}.png").convert_alpha()
                images[key] = pygame.transform.scale(images[key], taille_case)
            
            taille_ecran = (self.LARGEUR_ECRAN, self.HAUTEUR_ECRAN)
            images["fond"] = pygame.transform.scale(images["fond"], taille_ecran)
        
        except pygame.error as e:
            print(f"Erreur lors du chargement des images : {e}")
            sys.exit()
        return images
    
    ########## INTRO / FIN ##########
    def intro(self, screen, saved):
        self.music.play(self.music.theme_tkh1)
        
        if saved == 'none':
            self.cin.switch_lowercase(True)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Mieux vaut économiser mon énergie contre ces deux-là.", kind_info=[["TW", "no_weapon"], ["TW_H", "no_weapon"], ["SM", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Essayons une autre méthode...", kind_info=[["TW", "no_weapon"], ["TW_H", "no_weapon"], ["SM", "no_weapon"], 3], running=self.running)
            self.cin.switch_lowercase(False)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Si vous souhaitez me combattre, essayez de me rattraper.", kind_info=[["TW", "no_weapon"], ["TW_H", "no_weapon"], ["SM", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Ce vaurien... Il se fout complètement de nous !", kind_info=[["TW", "no_weapon"], ["TW_H", "no_weapon"], ["SM", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Tu nous sous-estimes largement mon garçon !", kind_info=[["TW_H", "no_weapon"], ["TW", "no_weapon"], ["SM", "no_weapon"], 1, True], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Hors de question de le laisser courir ! Attrapons-le !", kind_info=[["TW", "no_weapon"], ["TW_H", "no_weapon"], ["SM", "no_weapon"], 1, True], running=self.running)
            self.cin.switch_lowercase(True)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Bien. Tirons parti de l'environnement. Je vais les faire tomber un à un !", kind_info=[["TW", "no_weapon"], ["TW_H", "no_weapon"], ["SM", "no_weapon"], 3], running=self.running)
            self.cin.switch_lowercase(False)
        elif saved == 'KM':
            self.cin.switch_lowercase(True)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Mieux vaut économiser mon énergie contre ces deux-là.", kind_info=[["SM", "no_weapon"], ["KM", "no_weapon"], ["TW", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Essayons une autre méthode...", kind_info=[["SM", "no_weapon"], ["KM", "no_weapon"], ["TW", "no_weapon"], 1], running=self.running)
            self.cin.switch_lowercase(False)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Keiko, j'ai un plan pour pouvoir les battre sans avoir forcément recours à la", "violence.", kind_info=[["SM", "no_weapon"], ["KM", "no_weapon"], ["TW", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Nous allons devoir utiliser l'environnement à notre avantage. Tu me suis ?", kind_info=[["SM", "no_weapon"], ["KM", "no_weapon"], ["TW", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Très bien grand frère, je te suis.", kind_info=[["KM", "no_weapon"], ["SM", "no_weapon"], ["TW", "no_weapon"], 1, True], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Bien. Dans ce cas là...", kind_info=[["SM", "no_weapon"], ["KM", "no_weapon"], ["TW", "no_weapon"], 1, True], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Si vous souhaitez m'affronter , essayez de me rattraper.", kind_info=[["SM", "no_weapon"], ["KM", "no_weapon"], ["TW", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Ce vaurien... Il se fout complètement de nous !", kind_info=[["SM", "no_weapon"], ["KM", "no_weapon"], ["TW", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Tu nous sous-estimes largement mon garçon !", kind_info=[["SM", "no_weapon"], ["KM", "no_weapon"], ["TW_H", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Hors de question de le laisser courir ! Attrapons-le !", kind_info=[["SM", "no_weapon"], ["KM", "no_weapon"], ["TW", "no_weapon"], 3], running=self.running)
            self.cin.switch_lowercase(True)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Bien. Tirons parti de l'environnement. Je vais les faire tomber un à un !", kind_info=[["SM", "no_weapon"], ["KM", "no_weapon"], ["TW", "no_weapon"], 1], running=self.running)
            self.cin.switch_lowercase(False)
        elif saved == 'KT':
            self.cin.switch_lowercase(True)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Mieux vaut économiser mon énergie contre ces deux-là.", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Essayons une autre méthode..", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW", "no_weapon"], 1], running=self.running)
            self.cin.switch_lowercase(False)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Takeshi ! j'ai un plan pour pouvoir les battre sans avoir forcément recours", "à la violence.", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Je t'écoute.", kind_info=[["KT", "no_weapon"], ["SM", "no_weapon"], ["TW", "no_weapon"], 1, True], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Nous allons devoir utiliser l'environnement à notre avantage. Tu me suis ?", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW", "no_weapon"], 1, True], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Pourquoi pas, on pourra se faire un petit jogging.", kind_info=[["KT", "no_weapon"], ["SM", "no_weapon"], ["TW", "no_weapon"], 1, True], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Bien. Dans ce cas là...", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW", "no_weapon"], 1, True], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Si vous souhaitez m'affronter , essayez de me rattraper.", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Ce vaurien... Il se fout complètement de nous !", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Tu nous sous-estimes largement mon garçon !", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW_H", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Hors de question de le laisser courir ! Attrapons-le !", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW", "no_weapon"], 3], running=self.running)
            self.cin.switch_lowercase(True)
            self.cin.cinematic_frame(screen, 'forest2', 3, "Bien. Tirons parti de l'environnement. Je vais les faire tomber un à un !", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW", "no_weapon"], 1], running=self.running)
            self.cin.switch_lowercase(False)
            
        self.in_minigm = True
        
    def end(self, screen, saved):
        
        self.music.play(self.music.theme_tkh1)
        
        # Les dialogues de fin ne se lancent que si le joueur n'a pas réussi parfaitement (c'est-à-dire s'il a perdu au moins 1 vie)
        if self.lives < 3:
            if saved == 'none':
                self.cin.cinematic_frame(screen, 'forest2', 2, "Maraud... Tu vas le payer...", kind_info=[["SM", "no_weapon"], ["TW_H", "no_weapon"], 2], running=self.running)
                self.cin.switch_lowercase(True)
                self.cin.cinematic_frame(screen, 'forest2', 2, "Bon, j'ai réussi à en faire tomber un des deux.", kind_info=[["SM", "no_weapon"], ["TW_H", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'forest2', 2, "Je vais avoir une meilleure chance de battre le deuxième.", kind_info=[["SM", "no_weapon"], ["TW_H", "no_weapon"], 1], running=self.running)
                self.cin.switch_lowercase(False)
                self.cin.cinematic_frame(screen, 'forest2', 2, "Allez, montre-toi. Je vais finir le travail.", kind_info=[["SM", "no_weapon"], ["TW_H", "no_weapon"], 1], running=self.running)
            elif saved == 'KM':
                self.cin.cinematic_frame(screen, 'forest2', 3, "Maraud... Tu vas le payer...", kind_info=[["SM", "no_weapon"], ["KM", "no_weapon"], ["TW_H", "no_weapon"], 3], running=self.running)
                self.cin.switch_lowercase(True)
                self.cin.cinematic_frame(screen, 'forest2', 3, "Bon, j'ai réussi à en faire tomber un des deux.", kind_info=[["SM", "no_weapon"], ["KM", "no_weapon"], ["TW_H", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'forest2', 3, "Je vais avoir une meilleure chance de battre le deuxième.", kind_info=[["SM", "no_weapon"], ["KM", "no_weapon"], ["TW_H", "no_weapon"], 1], running=self.running)
                self.cin.switch_lowercase(False)
                self.cin.cinematic_frame(screen, 'forest2', 3, "Keiko, replie toi. Je vais me le faire.", kind_info=[["SM", "no_weapon"], ["KM", "no_weapon"], ["TW_H", "no_weapon"], 1], running=self.running)
            elif saved == 'KT':
                self.cin.cinematic_frame(screen, 'forest2', 3, "Maraud... Tu vas le payer...", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW_H", "no_weapon"], 3], running=self.running)
                self.cin.switch_lowercase(True)
                self.cin.cinematic_frame(screen, 'forest2', 3, "Bon, j'ai réussi à en faire tomber un des deux.", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW_H", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'forest2', 3, "Je vais avoir une meilleure chance de battre le deuxième.", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW_H", "no_weapon"], 1], running=self.running)
                self.cin.switch_lowercase(False)
                self.cin.cinematic_frame(screen, 'forest2', 3, "Bon Takeshi. Tu connais la chanson.", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW_H", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'forest2', 3, "Oui. C'est l'heure de gagner.", kind_info=[["SM", "no_weapon"], ["KT", "no_weapon"], ["TW_H", "no_weapon"], 2], running=self.running)
        self.playing = False

    ########## GESTION DES ÉVÈNEMENTS ##########
    def minigm_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.event.post(event)
                return
            if event.type == pygame.MOUSEMOTION:
                mx, my = event.pos
                board_x = (my - self.offset_y) // self.TAILLE_CASE
                board_y = (mx - self.offset_x) // self.TAILLE_CASE
                if 0 <= board_x < self.TAILLE and 0 <= board_y < self.TAILLE:
                    if not self.revele[board_x][board_y]:
                        self.hover_cell = (board_x, board_y)
                    else:
                        self.hover_cell = None
                else:
                    self.hover_cell = None
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_over:
                    mx, my = event.pos
                    board_x = (my - self.offset_y) // self.TAILLE_CASE
                    board_y = (mx - self.offset_x) // self.TAILLE_CASE
                    if 0 <= board_x < self.TAILLE and 0 <= board_y < self.TAILLE:
                        if event.button == 1:
                            if not self.revele[board_x][board_y] and not self.drapeaux[board_x][board_y]:
                                if not self.premier_clic:
                                    self.plateau = self._creer_plateau_premier_clic(board_x, board_y)
                                    self.premier_clic = True
                                if self.plateau[board_x][board_y] == -1:
                                    self.lives -= 1
                                    self.shake_start = pygame.time.get_ticks()
                                    self.shake_duration = 250
                                    self.shake_intensity = 20
                                    self.temps_clic_pic = pygame.time.get_ticks()
                                    self.afficher_pics = True
                                    self.flash_effect = {"time": pygame.time.get_ticks(), "cell": (board_x, board_y), "color": (255, 50, 50)}
                                    self.sfx_pic.play()
                                    if self.lives <= 0:  # Si plus de vies, le jeu sera terminé
                                        self.game_over = True
                                else:
                                    if self.plateau[board_x][board_y] == 0:
                                        self.flash_effect = {"time": pygame.time.get_ticks(), "cell": (board_x, board_y), "color": (50, 255, 50)}
                                    self.pics_restants = self._reveler(board_x, board_y, self.pics_restants)
                                    self.sfx_reveal.play()
                        elif event.button == 3:
                            if not self.revele[board_x][board_y]:
                                if not self.drapeaux[board_x][board_y] and self.pics_restants > 0:
                                    self.drapeaux[board_x][board_y] = True
                                    self.pics_restants -= 1
                                elif self.drapeaux[board_x][board_y]:
                                    self.drapeaux[board_x][board_y] = False
                                    self.pics_restants += 1
    
    ########## MISE À JOUR DU JEU ##########
    def minigm_update(self):
        if not self.game_over and not self.victoire:
            self.temps_ecoule = (pygame.time.get_ticks() - self.temps_debut) // 1000
            remaining = self.LIMITE_TIMER - self.temps_ecoule
            percent = remaining / self.LIMITE_TIMER
            self.heartbeat = (percent < 0.6)
        
            if self.temps_ecoule >= self.LIMITE_TIMER:
                self.game_over = True
                self.temps_ecoule = self.LIMITE_TIMER
                print("Temps écoulé, Game Over")
    
        if not self.victoire and not self.game_over:
            if self._verifier_victoire() and self.lives > 0:
                self.victory_effect_start = pygame.time.get_ticks()
                self._init_confetti()
                self.victoire = True
    
        if self.afficher_pics:
            # Pendant 1500 ms, les pics sont affichés ; ensuite, si des vies restent, on réinitialise le plateau, sinon le jeu est terminé.
            if pygame.time.get_ticks() - self.temps_clic_pic < 1500:
                pass
            else:
                self.afficher_pics = False
                if self.lives > 0:
                    self._init_game()
                else:
                    self.game_over = True
    
    ########## AFFICHAGE ##########
    def minigm_draw(self, screen, saved):
        offset_shake_x, offset_shake_y = 0, 0
        if self.shake_start is not None:
            elapsed = pygame.time.get_ticks() - self.shake_start
            if elapsed < self.shake_duration:
                offset_shake_x = random.randint(-self.shake_intensity, self.shake_intensity)
                offset_shake_y = random.randint(-self.shake_intensity, self.shake_intensity)
            else:
                self.shake_start = None
                self.shake_duration = 350
                self.shake_intensity = 10
        
        render_surface = pygame.Surface((self.LARGEUR_ECRAN, self.HAUTEUR_ECRAN))
        render_surface.fill((0, 0, 0))
        
        self._dessiner_plateau(render_surface)
        if self.victoire:
            remaining = self.temps_ecoule
        else:
            remaining = max(self.LIMITE_TIMER - self.temps_ecoule, 0)
        percent = remaining / self.LIMITE_TIMER
        
        if percent >= 0.6:
            base_color = (255, 255, 255)
            amplitude = 0.0
        elif percent >= 0.4:
            t = (0.6 - percent) / 0.2
            base_color = (255, 255, int(255 * (1 - t)))
            amplitude = 0.03 * t
        elif percent >= 0.2:
            t = (0.4 - percent) / 0.2
            base_color = (255, int(255 - t * 90), 0)
            amplitude = 0.06 * t
        else:
            t = (0.2 - percent) / 0.2
            base_color = (255, int(165 * (1 - t)), 0)
            amplitude = 0.1 * t
        
        pulse = math.sin(2 * math.pi * (pygame.time.get_ticks() % self.heartbeat_period) / self.heartbeat_period)
        scale_factor = 1 + amplitude * pulse
        
        timer_text = self.font_MFMG30.render(f"Temps: {remaining}", True, base_color)
        tw, th = timer_text.get_size()
        scaled_timer = pygame.transform.smoothscale(timer_text, (int(tw * scale_factor), int(th * scale_factor)))
        pos_x = self.LARGEUR_ECRAN - 200 - (scaled_timer.get_width() - tw) // 2
        pos_y = 20 - (scaled_timer.get_height() - th) // 2
        render_surface.blit(scaled_timer, (pos_x, pos_y))
        
        pics_text = self.font_MFMG25.render(f"Pics restants: {self.pics_restants}", True, base_color)
        pics_pos_x = self.LARGEUR_ECRAN - 180 - pics_text.get_width() // 2
        pics_pos_y = pos_y + scaled_timer.get_height() + 5
        render_surface.blit(pics_text, (pics_pos_x, pics_pos_y))
        
        vies_text = self.font_MFMG25.render(f"Vies restantes: {self.lives}", True, base_color)
        vies_pos_x = self.LARGEUR_ECRAN - 180 - vies_text.get_width() // 2
        vies_pos_y = pics_pos_y + pics_text.get_height() + 5
        render_surface.blit(vies_text, (vies_pos_x, vies_pos_y))
        
        if self.afficher_pics:
            if pygame.time.get_ticks() - self.temps_clic_pic < 1500:
                for x in range(self.TAILLE):
                    for y in range(self.TAILLE):
                        if self.plateau[x][y] == -1:
                            rect = pygame.Rect(self.offset_x + y * self.TAILLE_CASE,
                                               self.offset_y + x * self.TAILLE_CASE,
                                               self.TAILLE_CASE, self.TAILLE_CASE)
                            render_surface.blit(self.images["pic"], rect.topleft)
            # La réinitialisation du plateau se fait dans minigm_update une fois le délai écoulé
        
        if self.devmode:
            for x in range(self.TAILLE):
                for y in range(self.TAILLE):
                    if self.plateau[x][y] == -1:
                        rect = pygame.Rect(self.offset_x + y * self.TAILLE_CASE,
                                           self.offset_y + x * self.TAILLE_CASE,
                                           self.TAILLE_CASE, self.TAILLE_CASE)
                        render_surface.blit(self.images["pic"], rect.topleft)
        
        if self.hover_cell is not None and not self.game_over:
            hx, hy = self.hover_cell
            hover_rect = pygame.Rect(self.offset_x + hy * self.TAILLE_CASE,
                                     self.offset_y + hx * self.TAILLE_CASE,
                                     self.TAILLE_CASE, self.TAILLE_CASE)
            pygame.draw.rect(render_surface, (255, 170, 210), hover_rect, 3)
        
        screen.blit(render_surface, (offset_shake_x, offset_shake_y))
        pygame.display.flip()
    
    ########## MÉTHODES INTERNES DU JEU ##########
    def _creer_plateau_premier_clic(self, premier_x, premier_y):
        plateau = [[0 for _ in range(self.TAILLE)] for _ in range(self.TAILLE)]
        mines_placees = 0
        cases_interdites = set()
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= premier_x + i < self.TAILLE and 0 <= premier_y + j < self.TAILLE:
                    cases_interdites.add((premier_x + i, premier_y + j))
        while mines_placees < self.NOMBRE_PICS:
            x = random.randint(0, self.TAILLE - 1)
            y = random.randint(0, self.TAILLE - 1)
            if (x, y) not in cases_interdites and plateau[x][y] != -1:
                plateau[x][y] = -1
                mines_placees += 1
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if 0 <= x + i < self.TAILLE and 0 <= y + j < self.TAILLE and plateau[x + i][y + j] != -1:
                            plateau[x + i][y + j] += 1
        return plateau
    
    def _reveler(self, x, y, pics_restants):
        pile = [(x, y)]
        while pile:
            cx, cy = pile.pop()
            if self.revele[cx][cy]:
                continue
            self.revele[cx][cy] = True
            if self.drapeaux[cx][cy]:
                self.drapeaux[cx][cy] = False
                pics_restants += 1
            if self.plateau[cx][cy] == 0:
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        nx, ny = cx + i, cy + j
                        if 0 <= nx < self.TAILLE and 0 <= ny < self.TAILLE and not self.revele[nx][ny]:
                            pile.append((nx, ny))
        return pics_restants
    
    def _verifier_victoire(self):
        for x in range(self.TAILLE):
            for y in range(self.TAILLE):
                if self.plateau[x][y] != -1 and not self.revele[x][y]:
                    return False
        return True
    
    def _dessiner_plateau(self, screen):
        screen.blit(self.images["fond"], (0, 0))
        for x in range(self.TAILLE):
            for y in range(self.TAILLE):
                rect = pygame.Rect(self.offset_x + y * self.TAILLE_CASE,
                                   self.offset_y + x * self.TAILLE_CASE,
                                   self.TAILLE_CASE, self.TAILLE_CASE)
                if self.revele[x][y]:
                    if self.plateau[x][y] == -1:
                        screen.blit(self.images["pic"], rect.topleft)
                    elif self.plateau[x][y] > 0:
                        screen.blit(self.images[f"chiffre_{self.plateau[x][y]}1"], rect.topleft)
                    else:
                        screen.blit(self.images["case_vide"], rect.topleft)
                else:
                    screen.blit(self.images["case_cachee"], rect.topleft)
                    if self.drapeaux[x][y]:
                        screen.blit(self.images["drapeau"], rect.topleft)
    
    def _init_confetti(self):
        self.victory_confetti = []
        for _ in range(100):
            x = random.randint(0, self.LARGEUR_ECRAN)
            y = random.randint(0, self.HAUTEUR_ECRAN)
            size = random.randint(2, 6)
            color = (random.randint(200, 255), random.randint(0, 100), random.randint(0, 100))
            speed = random.uniform(0.5, 2)
            self.victory_confetti.append({"x": x, "y": y, "size": size, "color": color, "speed": speed})
    
    def _draw_victory_effect(self, surface):
        if self.victory_effect_start is None:
            self.victory_effect_start = pygame.time.get_ticks()
        pulse = int(127 + 128 * abs((pygame.time.get_ticks() - self.victory_effect_start) % 1000 - 500) / 500)
        overlay = pygame.Surface((self.LARGEUR_ECRAN, self.HAUTEUR_ECRAN))
        overlay.set_alpha(pulse // 2)
        overlay.fill((255, 255, 255))
        surface.blit(overlay, (0, 0))
        for conf in self.victory_confetti:
            pygame.draw.circle(surface, conf["color"], (int(conf["x"]), int(conf["y"])), conf["size"])
            conf["y"] += conf["speed"]
            if conf["y"] > self.HAUTEUR_ECRAN:
                conf["y"] = 0
                conf["x"] = random.randint(0, self.LARGEUR_ECRAN)
    
    ########## BOUCLE DU MINI-JEU ##########
    def run(self, screen, saved, devmode=False):
        self.devmode = devmode
        self.load()
        self.intro(screen, saved)
        
        while self.playing and self.running and self.in_minigm and not self.victoire and not self.game_over:
            self.minigm_events()
            self.minigm_update()
            self.minigm_draw(screen, saved)
            if self.victoire:
                pygame.time.delay(1000)
                break

        if self.running and (self.victoire or self.lives <= 0):
            self.end(screen, saved)
        
        return self.running, ("win" if self.victoire else "loose")

#########################################
# Lancement du mini-jeu
#########################################
if __name__ == '__main__':
    pygame.init()
    
    icon = pygame.image.load("../data/assets/common/Icone_LOGO_V12.ico")
    pygame.display.set_icon(icon)
    cursor = pygame.image.load("../data/assets/common/Souris_V4.png")
    pygame.mouse.set_cursor((5, 5), cursor)
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Kage no Michi")
    
    mini_game = minigm_minesweeper()
    mini_game.run(screen, 'KT', devmode=False)
    pygame.quit()
