#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao

# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 18:12:05 2025

@author: ahmed-adamrezkallah & cyrilzhao
"""

import pygame
import random
import math
from Cinematics import Cinematics
from Audio import Music,Sound

#########################################
# Classe Particle (pour les effets visuels)
#########################################
class Particle:
    def __init__(self, pos):
        self.x, self.y = pos
        self.radius = random.randint(2, 4)
        self.color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255), 255)
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.lifetime = random.randint(20, 40)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        alpha = max(0, int(255 * (self.lifetime / 40)))
        self.color = (self.color[0], self.color[1], self.color[2], alpha)
        
    def draw(self, surface):
        if self.lifetime > 0:
            s = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
            pygame.draw.circle(s, self.color, (self.radius, self.radius), self.radius)
            surface.blit(s, (int(self.x - self.radius), int(self.y - self.radius)))

#########################################
# Classe minigm
#########################################
class minigm_trade:
    
    def __init__(self):
        ### Etats du mini-jeu ###
        self.running = True       # Le jeu tourne
        self.playing = False      # Le mini-jeu est lancé
        self.in_minigm = False    # La phase de gameplay est active
        self.timer_active = False  # Nouveau flag pour contrôler le timer
        
        # Instance de la classe Cinematics
        self.cin = Cinematics()
        self.music,self.sound = Music(),Sound()
        
        # Police pour les symboles yen dans l'animation
        self.font_yen = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 30)
        
        # --- Variables qui seront chargées dans load_assets() ---
        self.correct_sound = None
        self.wrong_sound = None
        
        self.fond = None
        self.police = None
        self.police_conseils = None
        self.police_conseil_bande_noir = None
        self.police_description = None
        self.police_description_gong = None
        self.police_chiffre = None
        self.input_inbox = None
        self.fond_du_produit = None
        self.fond_detail_du_produit = None
        self.bande_conseil_keiko = None
        self.potion_de_soin = None
        self.cerise_sato_nishiki = None
        self.kg_de_riz_blanc_extra_premium = None
        self.talisman_de_revanche = None
        self.gong_ceremonial_en_bronze = None
        self.fleche_haut_img = None
        self.fleche_bas_img = None
        self.shikisha = None
        self.juzo = None
        
        # --- Variables de jeu ---
        self.reponse = ""
        self.liste_chiffre = [str(i) for i in range(10)]
        self.compteur_de_point = 0
        self.manche = 0
        self.fin_du_jeu = False
        self.fin_phase_jeu = False
        self.fleche = None  # Sera soit fleche_bas_img ou fleche_haut_img
        
        self.start_ticks = 0  # Pour le timer
        
        # --- Variables Flash, Yen et Shake ---
        self.flash_start_time = 0
        self.flash_duration = 750  # Durée du flash (ms)
        self.flash_color = None    # (r,g,b) : rouge pour faux, vert pour correct
        self.flash_yen = []        # Liste des symboles yen (dictionnaires)
        self.flash_yen_duration = 8000  # Durée de l'animation yen (ms)
        
        # Effet de zoom sur le produit
        self.object_scale = 1.0  
        
        # Effet de shake (tremblement) en cas de réponse erronée
        self.shake_start_time = 0
        self.shake_duration = 300  # Durée du shake (ms)
        self.shake_magnitude = 5   # Amplitude en pixels
        
        # Particules (confettis)
        self.particles = []
        
        # --- Paramètres pour le balancier des flèches ---
        self.arrow_amplitude = 10       # Amplitude en pixels
        self.arrow_frequency = 2.0      # Oscillations par seconde
        self.arrow_bas_base_pos = (280, 275)  # Position de base de la flèche basse
        self.arrow_haut_base_pos = (1000, 305)  # Position de base de la flèche haute
        
        # Zones et positions
        self.product_bg_pos = (320, 150)         # Zone du fond du produit
        self.description_bg_pos = (730, 140)       # Zone de description
        self.input_box = pygame.Rect(380, 450, 280, 60)
        self.bande_conseil_keiko_pos = (400, 520)  # Zone pour l'image de conseils
        
        # Variables qui seront définies dans load_assets() pour la gestion des objets
        self.liste_objet = []
        self.description_objet = []
        self.conseils_keiko = []
        self.nom_objet = ""
        self.image_objet = None
        self.prix_objet = 0
        self.current_description = ""
        self.current_conseil = ""
    
    ########## Démarrage du mini-jeu ##########
    def load(self):
        self.playing = True
        self.load_assets()
     
    def load_assets(self):
        # --- Chargement des sons ---
        try:
            self.correct_sound = self.sound.correct1
            self.wrong_sound = self.sound.incorrect1
            self.music.play(self.music.intro)
        except Exception as e:
            print("Erreur lors du chargement des sons:", e)
            self.correct_sound = None
            self.wrong_sound = None
        
        
        # Chargement du fond et des polices
        self.fond = pygame.image.load("../data/assets/bgs/Fond_Forêt_Bambou_3.png").convert()
        pygame.display.set_caption("Mini-jeu marchandage")
        self.police = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 60)
        self.police_conseil_bande_noir = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 30)
        self.police_conseils = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 20)
        self.police_description = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 24)
        self.police_description_gong = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 18)
        self.police_chiffre = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf", 20)
        
        # Images de l'interface
        self.input_inbox = pygame.image.load("../data/assets/minigm/Barre_Reponse.png").convert_alpha()
        self.fond_du_produit = pygame.image.load("../data/assets/minigm/Parchemin_Objet.png").convert_alpha()
        self.fond_detail_du_produit = pygame.image.load("../data/assets/minigm/Parchemin_Description_Objets_V1.png").convert_alpha()
        self.bande_conseil_keiko = pygame.image.load("../data/assets/minigm/Parchemin_Dialogues_Keiko.png").convert_alpha()
        
        # Mise à l'échelle
        self.input_inbox = pygame.transform.scale(self.input_inbox, (280, 60))
        self.fond_detail_du_produit = pygame.transform.scale(self.fond_detail_du_produit, (250, 330))
        self.bande_conseil_keiko = pygame.transform.scale(self.bande_conseil_keiko, (490, 130))
        
        # Chargement et mise à l'échelle des images des objets
        self.potion_de_soin = pygame.image.load("../data/assets/minigm/potion_de_soin.png").convert_alpha()
        self.cerise_sato_nishiki = pygame.image.load("../data/assets/minigm/cerise.png").convert_alpha()
        self.kg_de_riz_blanc_extra_premium = pygame.image.load("../data/assets/minigm/riz.png").convert_alpha()
        self.talisman_de_revanche = pygame.image.load("../data/assets/minigm/talisman.png").convert_alpha()
        self.gong_ceremonial_en_bronze = pygame.image.load("../data/assets/minigm/gong.png").convert_alpha()
        
        self.potion_de_soin = pygame.transform.scale(self.potion_de_soin, (250, 250))
        self.cerise_sato_nishiki = pygame.transform.scale(self.cerise_sato_nishiki, (250, 250))
        self.kg_de_riz_blanc_extra_premium = pygame.transform.scale(self.kg_de_riz_blanc_extra_premium, (250, 250))
        self.talisman_de_revanche = pygame.transform.scale(self.talisman_de_revanche, (250, 250))
        self.gong_ceremonial_en_bronze = pygame.transform.scale(self.gong_ceremonial_en_bronze, (250, 250))
        
        # Chargement et agrandissement des flèches
        self.fleche_haut_img = pygame.image.load("../data/assets/minigm/Fleche_Haute_Plus_Cher.png").convert_alpha()
        self.fleche_bas_img = pygame.image.load("../data/assets/minigm/Fleche_Bas_Plus_Cher.png").convert_alpha()
        self.fleche_haut_img = pygame.transform.scale(self.fleche_haut_img, (84, 126))
        self.fleche_bas_img = pygame.transform.scale(self.fleche_bas_img, (84, 126))
        
        # Définition de la liste des objets avec prix aléatoires
        self.liste_objet = [
            ["potion de soin", self.potion_de_soin, random.randint(20, 70)],
            ["cerise sato nishiki", self.cerise_sato_nishiki, random.randint(1000, 2000)],
            ["1kg de riz blanc extra premium", self.kg_de_riz_blanc_extra_premium, random.randint(300, 750)],
            ["talisman de revanche", self.talisman_de_revanche, random.randint(800, 1500)],
            ["gong ceremonial en bronze", self.gong_ceremonial_en_bronze, random.randint(1000, 2500)],
        ]
        
        if self.devmode:
            print("prix :",[self.liste_objet[i][2] for i in range(5)]) #Affichage des prix pour les développeurs, à supprimer
        
        # Descriptions des objets
        self.description_objet = [
            ["conseil potion", "Une potion \nmagique qui \nguérit les \nblessures et \nrestaure la santé, \nindispensable pour \ntout aventurier."],
            ["conseil cerise", "Des cerises \nrares et \ndélicieuses, \nprisées pour leur \nsaveur sucrée et \nleur chair juteuse."],
            ["1kg de riz premium", "Un riz de qualité \nsupérieure, idéal \npour préparer des \nplats raffinés \net savoureux."],
            ["talisman de revanche", "Un talisman imprégné \nd'une énergie sombre \nqui renvoie une partie \ndes dégâts subis à \nl'assaillant. \nIdéal pour ceux \nqui cherchent à punir \nleurs ennemis tout en \nencaissant les coups."],
            ["gong", "Un gong traditionnel \nen bronze, utilisé \ndans les temples et \nles cérémonies \nimportantes. Son \nrésonnant et profond, \nparfait pour \ncapter l'attention \net marquer des \nmoments significatifs."],
        ]
        
        # Conseils de Keiko
        self.conseils_keiko = [
            ["conseil potion", "Note de Keiko \nShikisha, si je me rappelle bien le sorcier \nle vendait à un prix faible, moins de \n100 pièces il me semble."],
            ["conseil cerise", "Note de Keiko \nShikisha, il me semble \nces cerises valent quelques milliers \nde pièces."],
            ["1kg de riz premium", "Note de Keiko \nShikisha, il me semble que \nle marchand le vendait entre \n300 et 750 pièces."],
            ["talisman de revanche", "Note de Keiko \nShikisha, Grand-mère avait \ndit que ce talisman valait entre \n800 et 1500 pièces."],
            ["gong", "Note de Keiko \nShikisha, le gardien du temple \nnous a averti du prix exorbitant \ndu gong."],
        ]
        
        # Chargement des personnages
        self.shikisha = pygame.image.load("../data/assets/cinematics/characters/Shikisha_16bit_Gauche_SansArme_V1.png")
        self.shikisha = pygame.transform.scale(self.shikisha, (238, 591))
        self.juzo = pygame.image.load("../data/assets/cinematics/characters/Juzo_16bit_Droite_SansArme_V1.png")
        self.juzo = pygame.transform.scale(self.juzo, (238, 591))
        self.shikisha_pos = (20, 250)
        self.juzo_pos = (1040, 250)
    
    ########## Intro/Fin ##########
    def intro(self, screen, saved):
        # Affichage de l'intro via la cinématique (attention à bien finir l'appel par running=self.running)
        if saved=='none':
            self.cin.cinematic_frame(screen, 'bamboo3', 2, "Votre arme m'a l'air fascinante. Avant cela, j'aimerai qu'on procède à", "des négociations.", kind_info=[["SM","no_weapon"],["JM","no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 2, "Des négociations ? Très bien. On les fera de ma manière.", kind_info=[["SM","no_weapon"],["JM","no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 2, "Tout d'abord, je vais prendre un total de 5 marchandises. Le but étant", "de deviner les prix de chacun.", kind_info=[["SM","no_weapon"],["JM","no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 2, "En fonction du nombre de bonnes réponses, je suis prêt à diminuer", "le coût de l'arme.", kind_info=[["SM","no_weapon"],["JM","no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 2, "Aucune objection ?", kind_info=[["SM","no_weapon"],["JM","no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 2, "Totalement ! Allons-y Marchand Juzo ! Débutons ces négociations.", kind_info=[["SM","no_weapon"],["JM","no_weapon"], 1], running=self.running)
        elif saved=='KM':
            self.cin.cinematic_frame(screen, 'bamboo3', 3, "Votre arme m'a l'air fascinante. Avant cela, j'aimerai qu'on procède à", "des négociations.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["JM","no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 3, "Des négociations ? Très bien. On les fera de ma manière.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["JM","no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 3, "Tout d'abord, je vais prendre un total de 5 marchandises. Le but étant", "de deviner les prix de chacun.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["JM","no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 3, "En fonction du nombre de bonnes réponses, je suis prêt à diminuer", "le coût de l'arme.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["JM","no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 3, "Aucune objection ?", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["JM","no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 3, "C'est une très belle occasion grand frère. On pourra payer moins", "cher pour une arme aussi puissante !", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["JM","no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 3, "Totalement ! Allons-y Marchand Juzo ! Débutons ces négociations.", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["JM","no_weapon"], 1], running=self.running)
        elif saved=='KT':
            self.cin.cinematic_frame(screen, 'bamboo3', 3, "Ce “Tengoku no Ikari”... Je pense que tu devrais la prendre.", "Elle pourra nous être très utile dans le futur.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["JM","no_weapon"], 2], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 3, "Votre arme m'a l'air fascinante. Avant cela, j'aimerai qu'on procède à", "des négociations.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["JM","no_weapon"], 1], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 3, "Des négociations ? Très bien. On les fera de ma manière.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["JM","no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 3, "Tout d'abord, je vais prendre un total de 5 marchandises. Le but étant", "de deviner les prix de chacun.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["JM","no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 3, "En fonction du nombre de bonnes réponses, je suis prêt à diminuer", "le coût de l'arme.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["JM","no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 3, "Aucune objection ?", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["JM","no_weapon"], 3], running=self.running)
            self.cin.cinematic_frame(screen, 'bamboo3', 3, "Totalement ! Allons-y Marchand Juzo ! Débutons ces négociations.", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["JM","no_weapon"], 1], running=self.running)
        self.in_minigm = True
        self.start_ticks = pygame.time.get_ticks()
        self.timer_active = True  # Active le timer
    
    def end(self, screen, saved):
        if self.compteur_de_point >= 3:
            self.victory = True
            if saved == 'none':
                self.cin.cinematic_frame(screen, 'bamboo3', 2, "Bravo. Vous vous êtes bien débrouillé. Désormais, que ferez-vous?", kind_info=[["SM","no_weapon"],["JM","no_weapon"], 2], running=self.running)
                self.switch_lowercase(True)
                self.cin.cinematic_frame(screen, 'bamboo3', 2, "Je dois maintenant décider d'acheter ou non l'arme...", kind_info=[["SM","no_weapon"],["JM","no_weapon"], 1], running=self.running)
                self.switch_lowercase(False)
            elif saved == 'KM':
                self.cin.cinematic_frame(screen, 'bamboo3', 3, "Bravo. Vous vous êtes bien débrouillé. Désormais, que ferez-vous?", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["JM","no_weapon"], 3], running=self.running)
                self.switch_lowercase(True)
                self.cin.cinematic_frame(screen, 'bamboo3', 3, "On devrait peut-être discuter avant de prendre une décision...", kind_info=[["SM","no_weapon"],["KM","no_weapon"],["JM","no_weapon"], 2], running=self.running)
                self.switch_lowercase(False)
            elif saved == 'KT':
                self.cin.cinematic_frame(screen, 'bamboo3', 3, "Bravo. Vous vous êtes bien débrouillé. Désormais, que ferez-vous?", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["JM","no_weapon"], 3], running=self.running)
                self.switch_lowercase(True)
                self.cin.cinematic_frame(screen, 'bamboo3', 3, "Cette arme pourrait être cruciale pour notre mission...", kind_info=[["SM","no_weapon"],["KT","no_weapon"],["JM","no_weapon"], 2], running=self.running)
                self.switch_lowercase(False)
        else:
            self.cin.cinematic_frame(screen, 'bamboo3', 2, "Hmm… Pas terrible. Vous auriez pu mieux faire. Mais bon, les affaires", "sont les affaires. Alors, que décidez-vous ?", kind_info=[["SM","no_weapon"], [saved,'no_weapon'],["JM","no_weapon"], 3], running=self.running)
            self.victory = False
        self.playing = False
        self.in_minigm = False
    
    ########## Partie 1 : évènements ##########
    def minigm_events(self):
        for event in pygame.event.get():
            # Vérification de la fermeture du jeu
            if event.type == pygame.QUIT:
                self.running = False
                pygame.event.post(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.reponse = self.reponse[:-1]
                elif event.unicode in self.liste_chiffre and len(self.reponse) < 19 :
                    self.reponse += event.unicode
                elif event.key == pygame.K_RETURN and self.reponse:
                    try:
                        reponse_joueur = int(self.reponse)
                    except ValueError:
                        reponse_joueur = 0
                    self.fleche = None  # Réinitialisation de la flèche
                    if reponse_joueur > self.prix_objet:
                        self.fleche = self.fleche_bas_img
                        self.flash_color = (255, 0, 0)
                        self.flash_start_time = pygame.time.get_ticks()
                        self.shake_start_time = pygame.time.get_ticks()
                        if self.wrong_sound:
                            self.wrong_sound.play()
                        for i in range(10):
                            p = Particle((self.product_bg_pos[0] + 125, self.product_bg_pos[1] + 125))
                            p.color = (255, 100, 100, 255)
                            self.particles.append(p)
                    elif reponse_joueur < self.prix_objet:
                        self.fleche = self.fleche_haut_img
                        self.flash_color = (255, 0, 0)
                        self.flash_start_time = pygame.time.get_ticks()
                        self.shake_start_time = pygame.time.get_ticks()
                        if self.wrong_sound:
                            self.wrong_sound.play()
                        for i in range(10):
                            p = Particle((self.product_bg_pos[0] + 125, self.product_bg_pos[1] + 125))
                            p.color = (255, 100, 100, 255)
                            self.particles.append(p)
                    else:
                        # Réponse correcte
                        self.compteur_de_point += 1
                        self.flash_color = (0, 255, 0)
                        self.flash_start_time = pygame.time.get_ticks()
                        # Générer les symboles yen pour l'animation
                        self.flash_yen = []
                        for i in range(30):
                            x = random.randint(0, 1280)
                            y = random.randint(0, 720)
                            base_alpha = random.randint(150, 255)
                            self.flash_yen.append({"x": x, "y": y, "base_alpha": base_alpha})
                        if self.correct_sound:
                            self.correct_sound.play()
                        self.object_scale = 1.2  # Effet de zoom
                        for i in range(20):
                            self.particles.append(Particle((self.product_bg_pos[0] + 125, self.product_bg_pos[1] + 125)))
                        self.reponse = ""
                        self.fin_phase_jeu = True
            # Vérification de la touche F11 pour le plein écran
            pressed_keys = pygame.key.get_pressed()
            if pressed_keys[pygame.K_F11]:
                pygame.display.toggle_fullscreen()
                pygame.time.Clock().tick(5)
    
    ########## Partie 2 : Mise à jour ##########
    def minigm_update(self):
        # Effet de zoom sur le produit
        if self.object_scale > 1.0:
            self.object_scale -= 0.005
            if self.object_scale < 1.0:
                self.object_scale = 1.0

        # Mise à jour des particules
        for p in self.particles[:]:
            p.update()
            if p.lifetime <= 0:
                self.particles.remove(p)

        # Gestion du timer
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_ticks
        self.time_left = max(0, 60 - elapsed_time // 1000)  # Temps en secondes

        # Si temps écoulé -> passage forcé à l'objet suivant
        if self.time_left <= 0 and not self.fin_phase_jeu:
            # Effets visuels/sonores
            self.flash_color = (255, 0, 0)
            self.flash_start_time = current_time
            self.shake_start_time = current_time
            if self.wrong_sound: self.wrong_sound.play()
            
            # Réinitialisation pour nouvelle manche
            self.manche += 1
            self.start_ticks = pygame.time.get_ticks()
            self.reponse = ""
            self.fleche = None
        
            # Générer des particules rouges
            for _ in range(10):
                p = Particle((self.product_bg_pos[0] + 125, self.product_bg_pos[1] + 125))
                p.color = (255, 100, 100, 255)
                self.particles.append(p)
        
        # Gestion des manches
        if self.manche < len(self.liste_objet):
            self.nom_objet = self.liste_objet[self.manche][0]
            self.image_objet = self.liste_objet[self.manche][1]
            self.prix_objet = self.liste_objet[self.manche][2]
            self.current_description = self.description_objet[self.manche][1]
            self.current_conseil = self.conseils_keiko[self.manche][1]
        else:
            self.playing = False

        # Passage à l'objet suivant après une réponse correcte
        if self.fin_phase_jeu:
            if self.manche < len(self.liste_objet):
                self.manche += 1
                self.start_ticks = pygame.time.get_ticks()
                self.fin_phase_jeu = False
            else:
                # Dernière manche terminée
                self.playing = False

        # Vérification de la fin du jeu après la 5ème manche
        elif self.manche >= 5 and not self.fin_phase_jeu:  #w Index 4 = 5ème élément
            self.playing = False
    
    ########## Partie 3 : Affichage ##########
    def minigm_draw(self, screen, saved):
        # Créer une surface de rendu temporaire
        render_surface = pygame.Surface((1280, 720))
        
        # Dessiner le fond
        render_surface.blit(self.fond, (0, 0))
        
        # --- TIMER VISUEL ---
        max_bar_width = 300
        ratio = max(0, self.time_left) / 60
        bar_width = int(max_bar_width * ratio)
        pygame.draw.rect(render_surface, (240, 120, 170), (490, 70, max_bar_width, 30), border_radius=5)
        pygame.draw.rect(render_surface, (220, 60, 140), (490, 70, bar_width, 30), border_radius=5)
        time_color = (255, 255, 255) if self.time_left > 10 else (255, 0, 0)
        timer_text = self.police_chiffre.render(f"{max(0, self.time_left)} s", True, time_color)
        render_surface.blit(timer_text, (490 + max_bar_width + 10, 75))
        
        # Affichage du fond du produit et du produit (avec zoom)
        render_surface.blit(self.fond_du_produit, self.product_bg_pos)
        scaled_size = int(250 * self.object_scale)
        # Calculer la position pour centrer l'image dans la zone (adapté à votre design)
        prod_x = self.product_bg_pos[0] + (400 - scaled_size) // 2
        prod_y = self.product_bg_pos[1] + (310 - scaled_size) // 2
        scaled_image = pygame.transform.smoothscale(self.image_objet, (scaled_size, scaled_size))
        render_surface.blit(scaled_image, (prod_x, prod_y))
        
        # Fond de description et affichage du texte
        render_surface.blit(self.fond_detail_du_produit, self.description_bg_pos)
        y_offset = 0
        for ligne in self.current_description.split("\n"):
            # Utilisation d'une police différente pour certaines manches (exemple pour les index 3 et 4)
            if self.manche in [3, 4]:
                txt = self.police_description_gong.render(ligne, True, (0, 0, 0))
                render_surface.blit(txt, (self.description_bg_pos[0] + 20, self.description_bg_pos[1] + 20 + y_offset))
                y_offset += 25
            else:
                txt = self.police_description.render(ligne, True, (0, 0, 0))
                render_surface.blit(txt, (self.description_bg_pos[0] + 20, self.description_bg_pos[1] + 20 + y_offset))
                y_offset += 30
        
        # Affichage des personnages
        render_surface.blit(self.shikisha, self.shikisha_pos)
        render_surface.blit(self.juzo, self.juzo_pos)
        
        # Zone de conseils (Keiko)
        if saved=='KM':
            render_surface.blit(self.bande_conseil_keiko, self.bande_conseil_keiko_pos)
            y_offset2 = 0
            for ligne in self.current_conseil.split("\n"):
                txt = self.police_conseils.render(ligne, True, (0, 0, 0))
                render_surface.blit(txt, (self.bande_conseil_keiko_pos[0] + 20, self.bande_conseil_keiko_pos[1] + 20 + y_offset2))
                y_offset2 += 25
        
        # Zone de saisie - affichage de la barre de réponse et du texte saisi
        render_surface.blit(self.input_inbox, (self.input_box.x, self.input_box.y))
        saisie_txt = self.police_chiffre.render(self.reponse, True, (0, 0, 0))
        render_surface.blit(saisie_txt, (self.input_box.x + 20, self.input_box.y + 20))
        
        # --- Effet des flèches en balancier ---
        t = pygame.time.get_ticks() / 1000.0
        offset = self.arrow_amplitude * math.sin(2 * math.pi * self.arrow_frequency * t)
        if self.fleche:
            if self.fleche == self.fleche_bas_img:
                pos = (self.arrow_bas_base_pos[0] - 50, self.arrow_bas_base_pos[1] + offset)
                render_surface.blit(self.fleche_bas_img, pos)
            elif self.fleche == self.fleche_haut_img:
                pos = (self.arrow_haut_base_pos[0] - 15, self.arrow_haut_base_pos[1] + offset)
                render_surface.blit(self.fleche_haut_img, pos)
        
        # --- Effet FLASH et animation des yen ---
        now = pygame.time.get_ticks()
        time_since_flash = now - self.flash_start_time
        if self.flash_color and time_since_flash < self.flash_duration:
            alpha = int(200 * (1 - time_since_flash / self.flash_duration))
            overlay = pygame.Surface((1280, 720), pygame.SRCALPHA)
            overlay.fill((self.flash_color[0], self.flash_color[1], self.flash_color[2], alpha))
            render_surface.blit(overlay, (0, 0))
            # Animation des symboles yen lors d'une réponse correcte
            if self.flash_color == (0, 255, 0):
                for yen in self.flash_yen:
                    progress = time_since_flash / self.flash_yen_duration
                    current_alpha = int(yen["base_alpha"] * (1 - progress))
                    if current_alpha < 0:
                        current_alpha = 0
                    new_y = yen["y"] + progress * 50  # Le yen descend progressivement
                    yen_surf = self.font_yen.render("¥", True, (0, 150, 0))
                    yen_surf.set_alpha(current_alpha)
                    render_surface.blit(yen_surf, (yen["x"], new_y))
        
        # Dessiner les particules (confettis)
        for p in self.particles:
            p.draw(render_surface)
        
        # --- Effet de shake sur l'écran ---
        current_time = pygame.time.get_ticks()
        if current_time - self.shake_start_time < self.shake_duration:
            global_shake_offset = (random.randint(-self.shake_magnitude, self.shake_magnitude),
                                   random.randint(-self.shake_magnitude, self.shake_magnitude))
        else:
            global_shake_offset = (0, 0)
        
        # Affichage final sur l'écran avec le shake
        screen.fill((0, 0, 0))
        screen.blit(render_surface, global_shake_offset)
        pygame.display.flip()
    
    ########## Boucle mini-jeu ##########
    def run(self, screen, saved,devmode=False):
        self.devmode=devmode
        self.load()
        self.intro(screen, saved)
        clock = pygame.time.Clock()
        
        while self.playing and self.running and self.in_minigm:
            self.minigm_events()
            self.minigm_update()
            
            # Vérification finale après la dernière mise à jour
            if self.manche >= 5:
                self.playing = False
                
            self.minigm_draw(screen, saved)
            clock.tick(60)
        
        if self.running:
            self.end(screen, saved)
        
        return self.running,self.victory

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
    pygame.display.set_caption("Kage no michi")
    
    mgm = minigm_trade()
    mgm.run(screen, 'KM')
    pygame.quit()
