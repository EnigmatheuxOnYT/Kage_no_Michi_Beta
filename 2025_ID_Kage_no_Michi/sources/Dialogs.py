#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 18:55:37 2025

@author: clementroux--benabou
"""


import pygame
from Cinematics import Cinematics

class Dialogs(Cinematics):
    def __init__ (self):
        Cinematics.__init__(self)
    
    def dialog_example (self,screen,saved):
        # Tu peux utiliser les foncions de la même façon que dans cinematics (exemple :)
        self.cinematic_frame(screen,"azw1",0,"Exemple")
        output1,output2 = self.choice_frame(screen,"azw1",[0,2],["choix 1","choix 2"])
        if output1=="choice":
            print("Tu as choisi le choix", output2)


    def dialog_minigm1(self, screen, saved):
        if saved == 'none':
            self.cinematic_frame(screen, "azw1", 2, "Monsieur ! Monsieur ! Oui, vous, celui qui porte l’apparence d’un", "samouraï, venez m’aider ! ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],1])
            self.cinematic_frame(screen, "azw1", 2, "(Est-ce que j’accepte de l’aider..?) ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],2])
            output1, output2 = self.choice_frame(screen, "azw1", [0, 2], ["OUI", "NON"])
            if output2 == 1:
                self.cinematic_frame(screen, "azw1", 2, "Très bien monsieur, je vais vous sortir de ces débris. Je m’en occupe !",kind_info=[['VL1', 'no_weapon'], ['SM', 'no_weapon'], 2])
                self.cinematic_frame(screen, "azw1", 2, "Je vous remercie fortement. ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],1])
                self.ecran_noir(screen)
                self.cinematic_frame(screen, "azw1", 2, "Merci beaucoup monsieur de m’avoir sorti de ce pétrin ! Tenez, voici de", "l’argent en guise de compensation. ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],1])
                self.cinematic_frame(screen, "azw1", 0, "(Le joueur obtient 15 pièces argent)")
                self.cinematic_frame(screen, "azw1", 2, " L’argent n’était pas nécessaire mais je vous remercie de votre générosité.", "Faîtes très attention lors de votre retour !",kind_info=[['VL1', 'no_weapon'], ['SM', 'no_weapon'], 2])
                self.cinematic_frame(screen, "azw1", 2, "A vous aussi monsieur ! Bonne chance à vous !", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],1])
            elif output2==2:
                self.cinematic_frame(screen, "azw1", 2, "Je suis navré monsieur, mais j’ai actuellement, des tâches de la plus", "haute importance, je reviendrai vers vous dans quelques instants.", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],2])
                self.cinematic_frame(screen, "azw1", 2, " Pas de problème monsieur, mais essayez de vous dépêcher ! Je n’ai pas", "envie de rester coincé dans ces débris..",kind_info=[['VL1', 'no_weapon'], ['SM', 'no_weapon'], 1])
        elif saved =='KM':
            self.cinematic_frame(screen, "azw1", 3, "Monsieur ! Monsieur ! Oui, vous, celui qui porte l’apparence d’un", "samouraï, venez m’aider ! ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],['KM','no_weapon'], 1])
            self.cinematic_frame(screen, "azw1", 3, "(Est-ce que j’accepte de l’aider..?) ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],['KM','no_weapon'],2])
            output1, output2 = self.choice_frame(screen, "azw1", [0, 2], ["OUI", "NON"])
            if output1 == "OUI":
                self.cinematic_frame(screen, "azw1", 3, "Très bien monsieur, je vais vous sortir de ces débris. Je m’en occupe !",kind_info=[['VL1', 'no_weapon'], ['SM', 'no_weapon'],['KM','no_weapon'], 2])
                self.cinematic_frame(screen, "azw1", 3, "Je vous remercie fortement. ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],['KM','no_weapon'],1])
                self.ecran_noir(screen)
                self.cinematic_frame(screen, "azw1", 3, "Merci beaucoup monsieur de m’avoir sorti de ce pétrin ! Tenez, voici de", "l’argent en guise de compensation. ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],['KM','no_weapon'],1])
                self.cinematic_frame(screen, "azw1", 0, "(Le joueur obtient 15 pièces argent)")
                self.cinematic_frame(screen, "azw1", 3, " L’argent n’était pas nécessaire mais je vous remercie de votre générosité.", "Faîtes très attention lors de votre retour !",kind_info=[['VL1', 'no_weapon'], ['SM', 'no_weapon'],['KM','no_weapon'], 2])
                self.cinematic_frame(screen, "azw1", 3, "A vous aussi monsieur ! Bonne chance à vous !", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],['KM','no_weapon'],1])
            elif output1 =="NON":
                self.cinematic_frame(screen, "azw1", 3, "Je suis navré monsieur, mais j’ai actuellement, des tâches de la plus", "haute importance, je reviendrai vers vous dans quelques instants.", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],['KM','no_weapon'],2])
                self.cinematic_frame(screen, "azw1", 3, " Pas de problème monsieur, mais essayez de vous dépêcher ! Je n’ai pas", "envie de rester coincé dans ces débris..",kind_info=[['VL1', 'no_weapon'], ['SM', 'no_weapon'],['KM','no_weapon'], 1])
        elif saved =='KT':
            self.cinematic_frame(screen, "azw1", 3, "Monsieur ! Monsieur ! Oui, vous, celui qui porte l’apparence d’un", "samouraï, venez m’aider ! ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],['KT','no_weapon'], 1])
            self.cinematic_frame(screen, "azw1", 3, "(Est-ce que j’accepte de l’aider..?) ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],['KT','no_weapon'],2])
            output1, output2 = self.choice_frame(screen, "azw1", [0, 2], ["OUI", "NON"])
            if output1 == "OUI":
                self.cinematic_frame(screen, "azw1", 3, "Très bien monsieur, je vais vous sortir de ces débris. Je m’en occupe !",kind_info=[['VL1', 'no_weapon'], ['SM', 'no_weapon'],['KT','no_weapon'], 2])
                self.cinematic_frame(screen, "azw1", 3, "Je vous remercie fortement. ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],['KT','no_weapon'],1])
                self.ecran_noir(screen)
                self.cinematic_frame(screen, "azw1", 3, "Merci beaucoup monsieur de m’avoir sorti de ce pétrin ! Tenez, voici de", "l’argent en guise de compensation. ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],['KT','no_weapon'],1])
                self.cinematic_frame(screen, "azw1", 0, "(Le joueur obtient 15 pièces argent)")
                self.cinematic_frame(screen, "azw1", 3, " L’argent n’était pas nécessaire mais je vous remercie de votre générosité.", "Faîtes très attention lors de votre retour !",kind_info=[['VL1', 'no_weapon'], ['SM', 'no_weapon'],['KT','no_weapon'], 2])
                self.cinematic_frame(screen, "azw1", 3, "A vous aussi monsieur ! Bonne chance à vous !", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],['KT','no_weapon'],1])
            elif output1 =="NON":
                self.cinematic_frame(screen, "azw1", 3, "Je suis navré monsieur, mais j’ai actuellement, des tâches de la plus", "haute importance, je reviendrai vers vous dans quelques instants.", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],['KT','no_weapon'],2])
                self.cinematic_frame(screen, "azw1", 3, " Pas de problème monsieur, mais essayez de vous dépêcher ! Je n’ai pas", "envie de rester coincé dans ces débris..",kind_info=[['VL1', 'no_weapon'], ['SM', 'no_weapon'],['KT','no_weapon'], 1])


    def dialog_minigm2(self, screen,saved):
        if saved == 'none':
            self.cinematic_frame(screen, "azw1", 2, "Tiens monsieur ? Vous ne serez pas par hasard un samouraï ?", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],1])
            self.cinematic_frame(screen, "azw1", 2, "Si, effectivement, je le suis.", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],2])
            self.cinematic_frame(screen, "azw1", 2, "Eh bien parfait, puisque j’ai une requête à vous demander. Auriez-vous du", "temps libre pour pouvoir accorder cette aide ?", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],1])
            self.cinematic_frame(screen, "azw1", 2, "(Voyons voir..Ai-je quelque chose de très urgent ?)", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],2])
            output1, output2 = self.choice_frame(screen, "azw1", [0, 2], ["OUI", "NON"])
            if output1 == "OUI":
                self.cinematic_frame(screen, "azw1", 2, "En effet monsieur, j’ai du temps libre à ma disposition. Que","voudriez vous que je fasse ?",kind_info=[['VL2', 'no_weapon'], ['SM', 'no_weapon'], 2])
                self.cinematic_frame(screen, "azw1", 2, "Très bien. Alors ma requête consiste tout simplement à récolter des", "ingrédients pour produire des vivres à la population.", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],1])
                self.cinematic_frame(screen, "azw1", 2, "Je vois, auriez-vous une liste pour que je puisse obtenir les produits", "que vous recherchez ?", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],2])
                self.cinematic_frame(screen, "azw1", 2, "Effectivement, j’en ai une. Voici de l’argent pour que vous puissiez", "les acheter. Je compte sur vous ! ",kind_info=[['VL2', 'no_weapon'], ['SM', 'no_weapon'], 1])
                self.ecran_noir(screen)
            elif output1 =="NON":
                self.cinematic_frame(screen, "azw1", 2, "Je suis désolé monsieur. Il se trouve que je n’ai pas beaucoup de temps", "libre à ma disposition.", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],2])
                self.cinematic_frame(screen, "azw1", 2, "Je reviendrai vers vous une fois que je me serai occupé de mon affaire.", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],2])
                self.cinematic_frame(screen, "azw1", 2, "Pas de souci monsieur. Je resterai ici, vous pourrez me retrouver facilement.",kind_info=[['VL2', 'no_weapon'], ['SM', 'no_weapon'], 1])
        elif saved == 'KM':
            self.cinematic_frame(screen, "azw1", 3, "Tiens monsieur ? Vous ne serez pas par hasard un samouraï ?", kind_info=[['VL2','no_weapon'],['SM','no_weapon'], ['KM','no_weapon'],1])
            self.cinematic_frame(screen, "azw1", 3, "Si, effectivement, je le suis.", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KM','no_weapon'],2])
            self.cinematic_frame(screen, "azw1", 3, "Eh bien parfait, puisque j’ai une requête à vous demander. Auriez-vous du", "temps libre pour pouvoir accorder cette aide ?", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KM','no_weapon'],1])
            self.cinematic_frame(screen, "azw1", 3, "(Voyons voir..Ai-je quelque chose de très urgent ?)", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KM','no_weapon'],2])
            output1, output2 = self.choice_frame(screen, "azw1", [0, 2], ["OUI", "NON"])
            if output1 == "OUI":
                self.cinematic_frame(screen, "azw1", 3, "En effet monsieur, j’ai du temps libre à ma disposition. Que","voudriez vous que je fasse ?",kind_info=[['VL2', 'no_weapon'], ['SM', 'no_weapon'],['KM','no_weapon'], 2])
                self.cinematic_frame(screen, "azw1", 3, "Très bien. Alors ma requête consiste tout simplement à récolter des", "ingrédients pour produire des vivres à la population.", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KM','no_weapon'],1])
                self.cinematic_frame(screen, "azw1", 3, "Je vois, auriez-vous une liste pour que je puisse obtenir les produits", "que vous recherchez ?", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KM','no_weapon'],2])
                self.cinematic_frame(screen, "azw1", 3, "Effectivement, j’en ai une. Voici de l’argent pour que vous puissiez", "les acheter. Je compte sur vous ! ",kind_info=[['VL2', 'no_weapon'], ['SM', 'no_weapon'],['KM','no_weapon'], 1])
                self.ecran_noir(screen)
            elif output1 =="NON":
                self.cinematic_frame(screen, "azw1", 3, "Je suis désolé monsieur. Il se trouve que je n’ai pas beaucoup de temps", "libre à ma disposition.", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KM','no_weapon'],2])
                self.cinematic_frame(screen, "azw1", 3, "Je reviendrai vers vous une fois que je me serai occupé de mon affaire.", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KM','no_weapon'],2])
                self.cinematic_frame(screen, "azw1", 3, "Pas de souci monsieur. Je resterai ici, vous pourrez me retrouver facilement.",kind_info=[['VL2', 'no_weapon'], ['SM', 'no_weapon'], ['KM','no_weapon'],1])

        elif saved == 'KT':
            self.cinematic_frame(screen, "azw1", 3, "Tiens monsieur ? Vous ne serez pas par hasard un samouraï ?", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "azw1", 3, "Si, effectivement, je le suis.", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, "azw1", 3, "Eh bien parfait, puisque j’ai une requête à vous demander. Auriez-vous du", "temps libre pour pouvoir accorder cette aide ?", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "azw1", 3, "(Voyons voir..Ai-je quelque chose de très urgent ?)", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KT','no_weapon'],2])
            output1, output2 = self.choice_frame(screen, "azw1", [0, 2], ["OUI", "NON"])
            if output1 == "OUI":
                self.cinematic_frame(screen, "azw1", 3, "En effet monsieur, j’ai du temps libre à ma disposition. Que","voudriez vous que je fasse ?",kind_info=[['VL2', 'no_weapon'], ['SM', 'no_weapon'],['KT','no_weapon'], 2])
                self.cinematic_frame(screen, "azw1", 3, "Très bien. Alors ma requête consiste tout simplement à récolter des", "ingrédients pour produire des vivres à la population.", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KT','no_weapon'],1])
                self.cinematic_frame(screen, "azw1", 3, "Je vois, auriez-vous une liste pour que je puisse obtenir les produits", "que vous recherchez ?", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KT','no_weapon'],2])
                self.cinematic_frame(screen, "azw1", 3, "Effectivement, j’en ai une. Voici de l’argent pour que vous puissiez", "les acheter. Je compte sur vous ! ",kind_info=[['VL2', 'no_weapon'], ['SM', 'no_weapon'],['KT','no_weapon'], 1])
                self.ecran_noir(screen)
            elif output1 =="NON":
                self.cinematic_frame(screen, "azw1", 3, "Je suis désolé monsieur. Il se trouve que je n’ai pas beaucoup de temps", "libre à ma disposition.", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KT','no_weapon'],2])
                self.cinematic_frame(screen, "azw1", 3, "Je reviendrai vers vous une fois que je me serai occupé de mon affaire.", kind_info=[['VL2','no_weapon'],['SM','no_weapon'],['KT','no_weapon'],2])
                self.cinematic_frame(screen, "azw1", 3, "Pas de souci monsieur. Je resterai ici, vous pourrez me retrouver facilement.",kind_info=[['VL2', 'no_weapon'], ['SM', 'no_weapon'],['KT','no_weapon'], 1])




if __name__ =="__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Kage no Michi - Dialogues")
    Dialogs().dialog_minigm1(screen,"none")
    pygame.quit()
