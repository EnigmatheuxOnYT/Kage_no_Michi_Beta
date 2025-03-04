#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Wed Jan 15 22:47:29 2025

@author: clementroux--benabou
"""
import pygame

class Commands:
    def __init__ (self):
        self.left = False
        self.font_MFMG30 = pygame.font.Font("../data/assets/fonts/MadouFutoMaruGothic.ttf",30)
        self.warning_message = self.font_MFMG30.render("Terminal de commande ouvert. Pour le fermer, entrez '/leave' ou '/'",False,(255,0,0))
        self.locations_shortcut = ["mgm",
                                   "ine",
                                   "azw",
                                   "bos"
                                   #"tkh"
                                   ]
        self.locations = {"mgm":["spawn_Magome","Magome"],
                          "ine":["spawn_Ine","Ine"],
                          "azw":["spawn_Aizu","Aizuwakamatsu"],
                          "bos":["spawn_Boss","l'île du boss"]
                          #"tkh":"Planque de Takahiro"
                          }
        self.numbers = [str(i)+'' for i in range (10)]

    def terminal(self):
        self.cmd = input("/")
    
    def translate(self):
        if self.is_leave():
            self.left = True
            return 'left',[]
        elif self.is_tp():
            is_coords = self.is_tp_coords()
            if is_coords:
                 x,y = self.tp()
                 return 'tppos',[x,y]
            else:
                loc = self.tp_loc()
                return 'tploc',[loc]
        elif self.is_spawn():
            return 'spawn', []
        elif self.is_cinematic():
            cinematic_number = self.cinematic()
            return 'cinematic', [cinematic_number]
        elif self.is_mini_game():
            mini_game_number = self.mini_game()
            return  'minigm', [mini_game_number]
        elif self.is_choice():
            choice_no,choice = self.choice()
            return 'choice', [choice_no,choice]
        elif self.is_speed():
            speed=self.speed()
            return 'speed',[speed]
        elif self.is_map():
            map_no=self.map()
            return "mapno",[map_no]
        elif self.is_noclip():
            noclip_value = self.noclip()
            return 'noclip',[noclip_value]
        elif self.is_fps():
            fps = self.fps()
            return 'fps',[fps]
        elif self.is_arrow():
            subtype,arg = self.arrow()
            return "arrow", [subtype,arg]
        elif self.is_devmode():
            state=self.devmode()
            return 'devmode', [state]
        elif self.is_money():
            no=self.money()
            return "money",[no]
        else:
            print("commande inconnue ou sans argument")
            return "unknown",[]
    
    def is_leave(self):
        command_leave = ('leave')
        command_is_leave = self.cmd[:]
        if command_leave == command_is_leave or command_is_leave == '':
            return True
        else:
            return False
    
    
    def is_tp(self):
        command_tp = ('tp ')
        command_is_tp = self.cmd[:3]
        if command_tp == command_is_tp:
            return True
        else:
            return False
        
    def is_tp_coords (self):
        for char in self.cmd[3:]:
            if char in self.numbers+[","]:
                return True
        return False
    
    def tp_loc (self):
        loc = self.cmd[3:]
        if loc in self.locations_shortcut:
            point = self.locations[loc][0]
        else:
            point=loc
        print(f"Téléportation à {point}")
        return point
    
    
    def tp (self):
        comma_place = 0
        for char in range(len(self.cmd)):
            if self.cmd[char] == ',':
                comma_place = char
        if comma_place == 0:
            print("location incorrecte, tp en 0,0")
            return 0,0
        else:
            x_tp_pos = int(self.cmd[3:comma_place])
            y_tp_pos = int(self.cmd[comma_place+1:])
            print (f"Téléportation en {x_tp_pos,y_tp_pos}")
            return x_tp_pos, y_tp_pos
    
    def is_spawn(self):
        command_spawn = ('spawn')
        command_is_spawn = self.cmd[:5]
        if command_spawn == command_is_spawn:
            print("téléportation au spawn de la carte")
            return True
        else:
            return False
    
    def is_cinematic (self):
        command_cinematic = "cinematic "
        command_is_cinematic = self.cmd[:10]
        if command_cinematic == command_is_cinematic:
            return True
        else:
            return False

            
    
    def cinematic (self):
        if len(self.cmd) < 11:
            print("commande sans argument")
            return 0
        for char in self.cmd[10:]:
            if char not in self.numbers:
                print ("cinematique incorrecte")
                return 0
        n_cinematic = int(self.cmd[10:])
        print (f"lancement de la cinématique {n_cinematic}")
        return n_cinematic
    
    def is_mini_game (self):
        command_mini_game = "minigm "
        command_is_mini_game = self.cmd[:7]
        if command_is_mini_game == command_mini_game:
            return True
        else:
            return False
        
        
    def mini_game (self):
        for char in self.cmd[7:]:
            if char not in self.numbers:
                print ("mini jeu incorrect")
                return 0
        n_mini_game = int(self.cmd[7:])
        print(f"Lancement du mini jeu {n_mini_game}")
        return n_mini_game
    
    def is_choice (self):
        command_choice = "choice "
        command_is_choice = self.cmd[:7]
        if command_choice == command_is_choice:
            return True
        return False
    
    def choice_saved(self):
        saved = 'none'
        if self.cmd[9:] in ['KM','KT','none']:
            saved = self.cmd[9:]
        else:
            print('argument incorrect')
        return saved
    
    def choice_warriors (self):
        choose = 1
        if self.cmd[9:] in ['1','2','3']:
            choose = int(self.cmd[9])
        else:
            print("argument incorrect")
        return choose
    
    def choice_no (self):
        no = 0
        if self.cmd[7] in self.numbers and self.cmd[8]==' ':
            no = int(self.cmd[7])
        else:
            print(f"argument incorrect ({self.cmd[8]})")
        return no
    
    def choice (self):
        arg = 0
        choice_no = self.choice_no()
        if choice_no == 0 :
            print("pas d'argument")
            return []
        elif choice_no == 1:
            arg = self.choice_saved()
        elif choice_no == 2:
            arg = self.choice_warriors()
        print(f"choix numéro {choice_no} mis sur {arg}")
        return choice_no,arg
    
    def is_speed (self):
        command_should_speed='speed '
        command_is_speed = self.cmd[:6]
        if command_is_speed == command_should_speed:
            return True
        return False
    
    def speed(self):
        try:
            speed = int(self.cmd[6:])
            print("Vitesse du joueur mise sur",speed)
            return speed
        except:
            print(f"{self.cmd[6:]} n'est pas un nombre valide. Vitesse mise sur 3.")
            return 3
    
    def is_map (self):
        command_should_map = "map "
        command_is_map = self.cmd[:4]
        if command_is_map==command_should_map:
            return True
        return False
    
    def map(self):
        for i in self.cmd[4:]:
            if i not in self.numbers:
                print(f"{self.cmd[4:]} n'est pas un nombre")
                return 0
        print(f"Ouverture de la carte {self.cmd[4:]}")
        return int(self.cmd[4:])

    def run (self):
        while not self.left:
            self.terminal()
            self.translate()
    
    def is_noclip(self):
        command_should_noclip = "noclip "
        command_is_noclip = self.cmd[:7]
        if command_is_noclip == command_should_noclip:
            return True
        return False
    
    def noclip(self):
        if self.cmd[7:] == 'on':
            return True
        elif self.cmd[7:] == 'off':
            return False
        print(f"{self.cmd[7:]} n'est pas une valeur correcte (on ou off)")
        return False
    
    def is_fps(self):
        command_should_fps = "fps "
        command_is_fps = self.cmd[:4]
        return command_should_fps == command_is_fps
    
    def fps(self):
        if self.cmd[4:] == 'show':
            print('Fps visibles')
            return True
        elif not self.cmd[4:] == 'hide':
            print("Argument incorrect (show/hide)")
        print("Fps cachés")
        return False
    
    def is_arrow (self):
        command_should = "arrow "
        command_is = self.cmd[:6]
        return command_should == command_is
    
    def arrow (self):
        if self.cmd[6:] == "on":
            print("flèche visible")
            return "state",True
        elif self.cmd[6:] == "off":
            print("flèche cachée")
            return "state",False
        elif self.cmd[6:12] == "point ":
            return "point", self.cmd[12:]
        else:
            print("argument incorrect,désactivation")
            return "state",False
    
    def is_devmode (self):
        command_should = "devmode "
        command_is = self.cmd[:len(command_should)]
        return command_should == command_is
    
    def devmode (self):
        if self.cmd[8:]=="on":
            print("Mode développeur activé")
            return True
        elif self.cmd[8:]=="off":
            print("Mode développeur désactivé")
        else:
            print("argument incorrect, désactivation")
        return False
    
    def is_money (self):
        command_should = "money "
        command_is = self.cmd[:len(command_should)]
        return command_should == command_is
    
    def money (self):
        for i in self.cmd[6:]:
            if i  not in self.numbers:
                print(self.cmd[6:],"n'est pas un nombre")
                return -0.1
        print(f"argent mit à {self.cmd[6:]}")
        return int(self.cmd[6:])
            



if __name__ == '__main__':
    pygame.init()
    cmd = Commands()
    cmd.run()