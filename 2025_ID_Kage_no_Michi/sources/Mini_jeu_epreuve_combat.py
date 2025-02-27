#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Créé le Wed Feb  5 15:13:47 2025

@author: ahmed-adamrezkallah
"""

import pygame
import sys
import random
from enum import Enum
from Cinematics import Cinematics
from Audio import Music

class minigm_trial1:
    def __init__(self):
        # On définit ici les différents états que peut prendre notre mini-jeu.
        # On a ajouté l'état INSTRUCTIONS pour présenter les règles au joueur.
        self.GameState = Enum('GameState', 'INSTRUCTIONS INTRO DEMONSTRATION INPUT VICTORY DEFEAT')

        self.playing = False     # Indique si le mini-jeu est lancé.
        self.in_minigm = False   # On est en plein déroulement de la partie.

        # On crée une instance de Cinematics pour gérer l'intro et la fin du jeu.
        self.cin = Cinematics()
        self.music = Music()

        # On charge une police pour afficher certains textes à l'écran.
        self.font_MFMG30 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 30)

        # Quelques paramètres généraux pour le jeu
        self.WIDTH, self.HEIGHT = 1280, 720


        self.demo_interval_idle = 500   # Durée en ms pour l'état "idle"
        self.demo_interval_arrow = 500  # Durée en ms pour l'affichage de la flèche

        # Variables pour animer l'intro avec le texte "Tu es prêt... C'est parti !"
        self.intro_text = "Tu es prêt... C'est parti !"
        self.intro_x = -self.WIDTH
        self.intro_alpha = 0
        self.intro_start_time = pygame.time.get_ticks()

        # Pour créer un effet de flash lors d'une saisie ou d'une erreur
        self.flash_alpha = 0
        # On utilisera un flash blanc pour une touche correcte et rouge en cas d'erreur
        self.flash_color = (255, 255, 255)

        # Variables pour simuler un léger tremblement de la caméra
        self.shake_duration = 0      # Durée restante de l'effet tremblement en ms
        self.shake_magnitude = 5     # Amplitude maximale du tremblement
        self.shake_offset = (0, 0)   # Décalage actuel appliqué à l'écran

        # Pour gérer le temps et les animations
        self.clock = pygame.time.Clock()

        # On prépare les différentes instructions qui expliquent les règles du jeu
        self.instruction_texts = [
            "Le nombre d'étapes représente le nombre de touches que vous devez mémoriser.",
            "Appuyez sur l'une des 4 touches pour enregistrer votre réponse.",
            "Faîtes attention! Vous avez 3 tentatives pour réussir ce mini jeu.",
            "Mémorisez les touches suivantes:"
        ]


        # On utilise une police plus petite pour les instructions et les retours au joueur.
        self.instruction_font = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 20)

        # Variable pour afficher des messages de feedback sur le rectangle noir en bas de l'écran.
        self.feedback_text = ""
        self.feedback_timer = 0
        self.feedback_duration = 1500  # Durée d'affichage du feedback en ms

        self.load_assets()

    ########## Lancement du mini‑jeu ##########
    def load(self):
        self.running = True      # Le jeu continue de tourner tant que cette variable est vraie.
        self.playing = True
        self.state = self.GameState.INSTRUCTIONS  # On commence par afficher les instructions du jeu.
        self.player_input = []

        # Variables pour la phase de démonstration où le joueur doit mémoriser la séquence.
        self.demo_phase = "idle"      # Peut être "idle" ou "arrow" selon ce qu'on affiche
        self.demo_timer = pygame.time.get_ticks()
        self.instruction_index = 0
        # On définit la vitesse d'animation pour l'affichage des instructions (ms par lettre)
        self.instruction_anim_speed = 50  
        self.instruction_char_index = 0
        self.current_instruction = self.instruction_texts[self.instruction_index]
        self.instruction_last_update = pygame.time.get_ticks()
        self.instruction_complete = False
        self.demo_index = 0         # Indice de la touche à montrer
        self.flash_alpha = 0
        # On génère une séquence aléatoire de 10 touches parmi les flèches directionnelles.
        self.sequence = [random.choice([pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])
                         for _ in range(10)]
        
        self.lives = 3
        self.current_step = 0  # Indice actuel dans la séquence à mémoriser
        self.music.play(self.music.menu3)


    def load_assets(self):
        try:
            # Chargement et redimensionnement du fond d'écran
            self.background = pygame.image.load('../data/assets/minigm/Fond_Ine_Dojo_Automne_1.png').convert_alpha()
            self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
            # Chargement du parchemin qui sera affiché au centre
            self.scroll = pygame.image.load('../data/assets/minigm/Parchemin_Affichage_Texte_V1.png').convert_alpha()
            self.scroll = pygame.transform.scale(self.scroll, (600, 400))
            # Chargement de l'image du samouraï (placé à gauche pour laisser de la place au rectangle noir en bas)
            self.samurai = pygame.image.load('../data/assets/minigm/Shikisha_16bit_Gauche_LameBambou_V1.png').convert_alpha()
            self.samurai = pygame.transform.scale(self.samurai, (250, 400))
            # Chargement des images pour les flèches
            arrow_size = (400, 300)
            self.arrows = {}
            self.arrows["idle"] = pygame.image.load('../data/assets/minigm/Fleches_Toutes_Sombres_V1.png').convert_alpha()
            self.arrows["idle"] = pygame.transform.scale(self.arrows["idle"], arrow_size)
            self.arrows[pygame.K_UP] = pygame.image.load('../data/assets/minigm/Fleche_Haute_Claire_V1.png').convert_alpha()
            self.arrows[pygame.K_UP] = pygame.transform.scale(self.arrows[pygame.K_UP], arrow_size)
            self.arrows[pygame.K_DOWN] = pygame.image.load('../data/assets/minigm/Fleche_Bas_Claire_V1.png').convert_alpha()
            self.arrows[pygame.K_DOWN] = pygame.transform.scale(self.arrows[pygame.K_DOWN], arrow_size)
            self.arrows[pygame.K_LEFT] = pygame.image.load('../data/assets/minigm/Fleche_Gauche_Claire_V1.png').convert_alpha()
            self.arrows[pygame.K_LEFT] = pygame.transform.scale(self.arrows[pygame.K_LEFT], arrow_size)
            self.arrows[pygame.K_RIGHT] = pygame.image.load('../data/assets/minigm/Fleche_Droite_Claire_V1.png').convert_alpha()
            self.arrows[pygame.K_RIGHT] = pygame.transform.scale(self.arrows[pygame.K_RIGHT], arrow_size)
            # Chargement des polices pour les textes
            self.font = pygame.font.Font('../data/assets/fonts/MadouFutoMaruGothic.ttf', 32)
            self.title_font = pygame.font.Font('../data/assets/fonts/MadouFutoMaruGothic.ttf', 64)


            # Chargement du son qui se joue en cas d'erreur (click_sound_1)
            self.key_sound = pygame.mixer.Sound("../data/assets/sounds/SFX_ClickSound_1.mp3")

            # Chargement des 4 fichiers audio pour l'effet "swoosh" de la lame de bambou
            self.swoosh_sfx = [
                pygame.mixer.Sound("../data/assets/sounds/SFX_Swoosh_Bamboo_Katana_1.mp3"),
                pygame.mixer.Sound("../data/assets/sounds/SFX_Swoosh_Bamboo_Katana_2.mp3"),
                pygame.mixer.Sound("../data/assets/sounds/SFX_Swoosh_Bamboo_Katana_3.mp3"),
                pygame.mixer.Sound("../data/assets/sounds/SFX_Swoosh_Bamboo_Katana_4.mp3")
            ]

        except Exception as e:
            print(f"Erreur de chargement des ressources: {e}")
            sys.exit()

    ########## Introduction et Fin ##########
    def intro(self, screen, saved):
        if saved=='none':
            self.cin.cinematic_frame(screen, 'ine1', 2, "Bien Musashi. Débutons cette première séance d'entraînement, mon cher élève.", "Vu que tu as les capacités pour devenir un véritable samouraï, nous allons", "améliorer tes compétences physiques.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 2, "Comme d'habitude, sache que ce ne sera pas facile. Il faut que tu sois", "complètement concentré lors de mes instructions pour que tu puisses te", "remémorer de mes cours.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 2, "Compris ?", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 2, "Oui Sensei Hoshida. Je ne vous décevrais pas, et je ferai de mon mieux.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 2, "Très bien. Que l'entraînement commence !", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
        elif saved=='KM':
            self.cin.cinematic_frame(screen, 'ine1', 3, "Cela me rappelle quand tu as décidé de participer à des cours de combats dans", "notre village natal. Tu avais l'air très joyeux et très déterminé à ce", "moment-là, comme aujourd'hui !", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Ha ha, tu lis vraiment dans mes pensées. En effet, ce cours est assez", "similaire à l'entraînement auquel je vais participer.", "C'est une question de s'adapter à son propre environnement.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Bien Musashi. Débutons cette première séance d'entraînement, mon cher élève.", "Vu que tu as les capacités pour devenir un véritable samouraï, nous allons", "améliorer tes compétences physiques.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Comme d'habitude, sache que ce ne sera pas facile. Il faut que tu sois", "complètement concentré lors de mes instructions pour que tu puisses te", "remémorer de mes cours.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Compris ?", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Oui Sensei Hoshida. Je ne vous décevrais pas, et je ferai de mon mieux.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Très bien. Que l'entraînement commence !", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
        elif saved=='KT':
            self.cin.cinematic_frame(screen, 'ine1', 3, "La dernière fois qu'on s'est entraîné, c'était dans notre village natal, où", "l'on prenait des cours de combats. Je me souvenais de la fois où on a détruit", "nos katanas en bois lors de notre duel. Le maître était rouge de colère !", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Mais oui ! Il était prêt à nous trucider l'un et l'autre...", "C'était une expérience terrifiante mais aussi palpitante.", "J'ai en tout cas l'envie d'aller encore plus loin.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Bien sûr, on ne va reculer devant aucun défi.", "Nous nous sacrifierons pour la patrie et nous serons reconnus comme les héros", "du Japon.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Takeshi et Musashi, reprenons. Nous allons commencer cette première séance", "d'entraînement, mes chers élèves.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Puisque vous avez les capacités pour devenir de véritables samouraïs,", "nous allons tout d'abord améliorer vos compétences physiques.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Comme d'habitude, sachez que ce ne sera pas facile. Il faut que vous soyez", "complètement concentré lors de mes instructions pour que tu puisses te", "remémorer de mes cours.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Compris ?", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Oui Sensei Hoshida. Je ne vous décevrais pas, et je ferai de mon mieux.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Pareil pour moi, nous y allons à fond !", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'ine1', 3, "Très bien. Que l'entraînement commence !", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
        self.in_minigm = True

    def end(self, screen, saved):
        if self.state == self.GameState.VICTORY or self.state == self.GameState.DEFEAT :
            if saved=='none':
                self.cin.cinematic_frame(screen, 'ine1', 2, "Bon travail. Continue sur cette voie et tu seras aussitôt devenu un nouveau", "samouraï. Sache qu'il faut devenir patient pour obtenir ce que l'on veut.", "Donc évite de vivre dans un avenir fictif mais plutôt dans un présent réaliste", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 2, "Compris. La patience avant tout comme on le dit.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 2, "Exactement. Nous poursuivrons l'entraînement demain et tu continueras", "à assimiler les bases nécessaires conformes au code Bushido.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 2, "Je ne compte pas baisser les bras.", "La patience et la régularité je pense sont les deux vertus les plus", "importantes pour pouvoir accomplir nos objectifs.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 2, "C'est exactement le genre d'élève que je recherche.", "Il faut rester concentré dans nos progrès actuels avant le résultat.", "Sur ce, je te laisse rentrer pour te reposer, et nous nous reverrons demain.", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 2, "Merci beaucoup Sensei Hoshida. A demain !", kind_info=[["SM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
            elif saved=='KM':
                self.cin.cinematic_frame(screen, 'ine1', 3, "Bon travail. Continue sur cette voie et tu seras aussitôt devenu un nouveau", "samouraï. Sache qu'il faut devenir patient pour obtenir ce que l'on veut.", "Donc évite de vivre dans un avenir fictif mais plutôt dans un présent réaliste", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 3, "Compris. La patience avant tout comme on le dit.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 3, "Exactement. Nous poursuivrons l'entraînement le lendemain et tu continueras", "à assimiler les bases nécessaires conformes au code Bushido.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 3, "Tu as été incroyable Shikisha ! Franchement plus personne ne pourra", "t'arrêter !", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 3, "C'est justement grâce à l'entraînement de Sensei que je vais pouvoir tous vous", "protéger", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 3, "J'admire beaucoup ton intérêt pour les autres Musashi.", "Poursuis tes efforts et je pense que tu pourras aller très très loin.", "Reverrons-nous demain, pour que tu puisses accomplir ta destinée.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 3, "Merci beaucoup Sensei Hoshida. A demain !", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 3, "A demain Sensei Hoshida !", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
            elif saved=='KT':
                self.cin.cinematic_frame(screen, 'ine1', 3, "Bon travail vous deux. Lorsque je vous observe, j'ai l'impression de voir deux", "jumeaux côte à côte. Vous êtes en parfaite coordination. Si vous réussissez", "à unir vos forces, vous serez un duo inarrêtable.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 3, "Bien sûr ! Je connais Musashi depuis mon enfance.", "Donc je sais très bien à quoi il pense actuellement, d'où l'homogénéité de nos", "forces et de notre puissance.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 3, "Personne ne nous arrêtera quoi qu'il en soit.", "Nous protégerons le Japon jusqu'au bout.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 3, "Je ressens du potentiel chez vous deux. Vous avez la capacité d'agir pour le", "bien. Donc n'abandonnez pas si vous vous sentez accablé par le mal du monde", "extérieur. Poursuivons l'entraînement demain.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 3], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 3, "Nous intégrerons vos conseils coûte que coûte, puisque nous deviendrons des","samouraïs.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 1], running=self.running)
                self.cin.cinematic_frame(screen, 'ine1', 3, "Tu as tout compris Musashi. Ensemble, nous faisons la paire.", "A demain, Sensei Hoshida. J'ai hâte de reprendre.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["SH", "no_weapon"], 2], running=self.running)
            
        self.playing= False
            
    ########## Partie 1 : Gestion des événements ##########
    def minigm_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.event.post(event)

            # Si on est dans l'état INSTRUCTIONS et que le joueur clique, on fait avancer l'animation du texte
            if self.state == self.GameState.INSTRUCTIONS and event.type == pygame.MOUSEBUTTONDOWN:
                if not self.instruction_complete:
                    # Si le texte n'est pas encore affiché en entier, on le complète d'un coup
                    self.instruction_char_index = len(self.current_instruction)
                    self.instruction_complete = True
                else:
                    # Sinon, on passe à l'instruction suivante
                    self.instruction_index += 1
                    if self.instruction_index >= len(self.instruction_texts):
                        # Plus d'instructions, on passe à l'intro du jeu
                        self.state = self.GameState.INTRO
                        self.intro_start_time = pygame.time.get_ticks()
                    else:
                        self.current_instruction = self.instruction_texts[self.instruction_index]
                        self.instruction_char_index = 0
                        self.instruction_complete = False
                        self.instruction_last_update = pygame.time.get_ticks()

            # Gestion de la saisie du joueur en phase INPUT
            if self.state == self.GameState.INPUT and event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    # On joue au hasard l'un des sons "swoosh"
                    random.choice(self.swoosh_sfx).play()
                    self.player_input.append(event.key)
                    self.flash_alpha = 255
                    now = pygame.time.get_ticks()
                    # Vérifie si la touche appuyée correspond à celle attendue
                    if self.player_input[-1] != self.sequence[len(self.player_input)-1]:
                        self.flash_color = (200, 0, 0)  # Flash rouge en cas d'erreur
                        self.key_sound.play()
                        self.handle_mistake()
                    else:
                        self.flash_color = (100, 255, 100)  # Flash blanc pour confirmer une bonne touche
                        if len(self.player_input) == (self.current_step + 1):
                            self.current_step += 1
                            self.feedback_text = "Bien joué!"
                            self.feedback_timer = now
                            if self.current_step >= len(self.sequence):
                                self.state = self.GameState.VICTORY
                            else:
                                self.state = self.GameState.DEMONSTRATION
                                self.demo_index = 0
                                self.demo_phase = "idle"
                                self.demo_timer = now
                                self.player_input = []
            # Permet de basculer en plein écran en appuyant sur F11
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_F11]:
                pygame.display.toggle_fullscreen()
                pygame.time.Clock().tick(5)

    def handle_mistake(self):
        # Réduit d'une vie et lance l'effet visuel de flash
        self.lives -= 1
        self.flash_alpha = 255
        self.feedback_text = "Aïe..."
        self.feedback_timer = pygame.time.get_ticks()
        # Démarre l'effet de tremblement de l'écran
        self.shake_duration = 500
        if self.lives <= 0:
            self.state = self.GameState.DEFEAT
        else:
            self.reset_round()

    def reset_round(self):
        # Réinitialise la phase de démonstration pour recommencer la séquence
        self.state = self.GameState.DEMONSTRATION
        self.demo_index = 0
        self.demo_phase = "idle"
        self.demo_timer = pygame.time.get_ticks()
        self.player_input = []

    ########## Partie 2 : Mise à jour de l'état du jeu ##########
    def minigm_update(self):
        dt = self.clock.tick(60)
        now = pygame.time.get_ticks()

        # Mise à jour de l'animation du texte des instructions (seulement en mode INSTRUCTIONS)
        if self.state == self.GameState.INSTRUCTIONS:
            if not self.instruction_complete:
                if now - self.instruction_last_update >= self.instruction_anim_speed:
                    self.instruction_char_index += 1
                    self.instruction_last_update = now
                    if self.instruction_char_index >= len(self.current_instruction):
                        self.instruction_char_index = len(self.current_instruction)
                        self.instruction_complete = True

        # Gestion de l'affichage temporaire du feedback
        if self.feedback_text:
            if now - self.feedback_timer > self.feedback_duration:
                self.feedback_text = ""

        # Animation de l'intro avec le texte "Tu es prêt... C'est parti !"
        if self.state == self.GameState.INTRO:
            elapsed = now - self.intro_start_time
            if elapsed < 3000:
                progress = elapsed / 3000
                self.intro_x = -self.WIDTH + (self.WIDTH * 1.5) * progress
                self.intro_alpha = int(255 * progress)
            else:
                self.state = self.GameState.DEMONSTRATION
                self.demo_timer = now

        # Gestion de la phase de démonstration : alterne entre "idle" et l'affichage de la flèche
        if self.state == self.GameState.DEMONSTRATION:
            if self.demo_phase == "idle" and now - self.demo_timer >= self.demo_interval_idle:
                self.demo_phase = "arrow"
                self.demo_timer = now
            elif self.demo_phase == "arrow" and now - self.demo_timer >= self.demo_interval_arrow:
                self.demo_index += 1
                self.demo_phase = "idle"
                self.demo_timer = now
                if self.demo_index > self.current_step:
                    self.state = self.GameState.INPUT
        if self.state in[self.GameState.VICTORY,self.GameState.DEFEAT]:
            self.in_minigm = False

        # Réduction progressive de l'effet flash
        if self.flash_alpha > 0:
            self.flash_alpha = max(0, self.flash_alpha - 10)

        # Application de l'effet de tremblement de la caméra
        if self.shake_duration > 0:
            self.shake_duration -= dt
            self.shake_offset = (random.randint(-self.shake_magnitude, self.shake_magnitude),
                                 random.randint(-self.shake_magnitude, self.shake_magnitude))
        else:
            self.shake_offset = (0, 0)

    ########## Partie 3 : Affichage ##########
    def minigm_draw(self, screen, saved):
        offset_x, offset_y = self.shake_offset

        # On commence par afficher le fond d'écran
        screen.fill((0, 0, 0))
        screen.blit(self.background, (0 + offset_x, 0 + offset_y))
        # On place le samouraï à gauche, pour libérer de l'espace pour le rectangle noir en bas
        screen.blit(self.samurai, (50 + offset_x, self.HEIGHT - self.samurai.get_height() - 150 + offset_y))
        # Positionnement du parchemin au centre (légèrement remonté)
        scroll_x = (self.WIDTH - self.scroll.get_width()) // 2 + offset_x
        scroll_y = self.HEIGHT - self.scroll.get_height() - 130 + offset_y  # décalé un peu plus bas
        screen.blit(self.scroll, (scroll_x, scroll_y))

        # Affichage de la phase de démonstration
        if self.state == self.GameState.DEMONSTRATION:
            arrow_x = scroll_x + (self.scroll.get_width() - self.arrows["idle"].get_width()) // 2
            arrow_y = scroll_y + (self.scroll.get_height() - self.arrows["idle"].get_height()) // 2
            if self.demo_index <= self.current_step:
                if self.demo_phase == "idle":
                    screen.blit(self.arrows["idle"], (arrow_x, arrow_y))
                else:
                    current_key = self.sequence[self.demo_index]
                    screen.blit(self.arrows[current_key], (arrow_x, arrow_y))
            else:
                screen.blit(self.arrows["idle"], (arrow_x, arrow_y))

        # Pendant la phase INPUT, on affiche la séquence que le joueur a entrée
        if self.state == self.GameState.INPUT:
            touches_fr = {
                pygame.K_UP: "Haut",
                pygame.K_DOWN: "Bas",
                pygame.K_LEFT: "Gauche",
                pygame.K_RIGHT: "Droite"
            }
            input_text = "Répète la séquence : "
            for key in self.player_input:
                input_text += touches_fr.get(key, pygame.key.name(key)) + " "

            max_chars = 30
            words = input_text.split(" ")
            lines = []
            current_line = ""
            for word in words:
                if len(current_line) + len(word) + 1 > max_chars:
                    lines.append(current_line)
                    current_line = word
                else:
                    if current_line:
                        current_line += " " + word
                    else:
                        current_line = word
            if current_line:
                lines.append(current_line)
            final_text = "\n".join(lines)
            text_rect = pygame.Rect(scroll_x + 60, scroll_y + 70, self.scroll.get_width(), self.scroll.get_height())
            self.draw_multiline_text(screen, final_text, (130, 80, 50), text_rect)

        # On affiche le compteur d'étapes et le nombre de vies restantes
        step_display = min(self.current_step + 1, len(self.sequence))
        self.draw_text(screen, f'Vies: {self.lives}', (255, 0, 0), (30 + offset_x, 30 + offset_y))
        self.draw_text(screen, f'Étape: {step_display}/{len(self.sequence)}', (200, 200, 200), (30 + offset_x, 70 + offset_y))

        """ # En cas de victoire ou de défaite, on affiche un message au centre de l'écran
        if self.state == self.GameState.VICTORY:
            self.draw_centered_text(screen, "Épreuve réussie !", (0, 200, 0))
        elif self.state == self.GameState.DEFEAT:
            self.draw_centered_text(screen, "Échec...", (200, 0, 0))"""
            

        # Pendant l'intro, on affiche le texte animé "Tu es prêt... C'est parti !"
        if self.state == self.GameState.INTRO:
            text_surface = self.title_font.render(self.intro_text, True, (255, 255, 255))
            text_surface.set_alpha(self.intro_alpha)
            text_rect = text_surface.get_rect(midleft=(self.intro_x + offset_x, self.HEIGHT // 2 + offset_y))
            screen.blit(text_surface, text_rect)

        # Dessine le rectangle noir en bas de l'écran (taille : 1280 x 100)
        #pygame.draw.rect(screen, (0, 0, 0), (0, self.HEIGHT - 100, self.WIDTH, 100))
        # Sur ce rectangle, on affiche soit les instructions, soit un message de feedback
        if self.state == self.GameState.INSTRUCTIONS:
            # On affiche progressivement les lettres de l'instruction courante
            display_text = self.current_instruction[:self.instruction_char_index]
            self.draw_centered_instruction(screen, display_text, (255, 255, 255))
        elif self.feedback_text:
            self.draw_centered_instruction(screen, self.feedback_text, (255, 255, 255))

        # Enfin, si un flash est en cours, on superpose une surface semi-transparente
        if self.flash_alpha > 0:
            flash_surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
            flash_surface.fill((*self.flash_color, self.flash_alpha))
            screen.blit(flash_surface, (0, 0))

        pygame.display.flip()

    def draw_text(self, screen, text, color, pos):
        surface = self.font.render(text, True, color)
        screen.blit(surface, pos)

    def draw_centered_text(self, screen, text, color):
        surface = self.title_font.render(text, True, color)
        rect = surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
        screen.blit(surface, rect)

    def draw_centered_instruction(self, screen, text, color):
        surface = self.instruction_font.render(text, True, color)
        rect = surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 50))
        screen.blit(surface, rect)

    def draw_multiline_text(self, screen, text, color, rect, line_spacing=5):
        lines = text.split("\n")
        y = rect.top
        for line in lines:
            line_surface = self.font.render(line, True, color)
            screen.blit(line_surface, (rect.left, y))
            y += line_surface.get_height() + line_spacing

    ########## Boucle principale du mini‑jeu ##########
    def run(self, screen, saved,devmode=False):
        # Une fois l'intro terminée, on charge toutes les ressources nécessaires
        self.load()
        # On commence par afficher la cinématique d'intro
        self.intro(screen, saved)
        

        while self.playing and self.running and self.in_minigm:
            self.minigm_events()
            self.minigm_update()
            self.minigm_draw(screen, saved)
            
            
            #if self.state in [self.GameState.VICTORY, self.GameState.DEFEAT]:
            #    pygame.time.delay(2000)
            #    self.playing = False

        if self.playing and self.running:
            self.end(screen, saved)

        return self.running

# Lancement du mini‑jeu
if __name__ == '__main__':
    pygame.init()
    
    icon = pygame.image.load("../data/assets/common/Icone_LOGO_V12.ico")
    pygame.display.set_icon(icon)
    cursor = pygame.image.load("../data/assets/common/Souris_V4.png")
    pygame.mouse.set_cursor((5, 5), cursor)
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Kage no michi")
    
    jeu = minigm_trial1()
    jeu.run(screen, 'KM')
    pygame.quit()
