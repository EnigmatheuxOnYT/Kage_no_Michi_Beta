#Projet : Kage no Michi
#Auteurs : Alptan KorKTaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


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
        self.cinematic_frame(screen,"azw2",0,"Exemple")
        output1,output2 = self.choice_frame(screen,"azw2",[0,2],["choix 1","choix 2"],timer=5000)
        if output1=="choice":
            print("Tu as choisi le choix", output2)
        elif output1=="timer_end":
            print("tu n'as plus de temps")
        elif output1=='QUIT':
            print("Tu as fermé la fenètre")


    def dialog_minigm1(self, screen, saved):
        if saved == 'none':
            self.cinematic_frame(screen, "azw2", 2, "Monsieur ! Monsieur ! Oui, vous, celui qui porte l'apparence d'un", "samouraï, venez m'aider ! ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],1])
            self.cinematic_frame(screen, "azw2", 2, "(Est-ce que j'accepte de l'aider..?) ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],2])
            output1, output2 = self.choice_frame(screen, "azw2", [0, 2], ["OUI", "NON"])
            if output1 == "choice":
                self.cinematic_frame(screen, "azw2", 2, "Très bien monsieur, je vais vous sortir de ces débris. Je m'en occupe !",kind_info=[['VL1', 'no_weapon'], ['SM', 'no_weapon'], 2])
                self.cinematic_frame(screen, "azw2", 2, "Je vous remercie fortement. ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],1])
                self.ecran_noir(screen)
                self.cinematic_frame(screen, "azw2", 2, "Merci beaucoup monsieur de m'avoir sorti de ce pétrin ! Tenez, voici de", "l'argent en guise de compensation. ", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 0, "(Le joueur obtient 15 pièces argent)")
                self.cinematic_frame(screen, "azw2", 2, " L'argent n'était pas nécessaire mais je vous remercie de votre générosité.", "Faîtes très attention lors de votre retour !",kind_info=[['VL1', 'no_weapon'], ['SM', 'no_weapon'], 2])
                self.cinematic_frame(screen, "azw2", 2, "A vous aussi monsieur ! Bonne chance à vous !", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],1])
            elif output2 =="choice":
                self.cinematic_frame(screen, "azw2", 2, "Je suis navré monsieur, mais j'ai actuellement, des tâches de la plus", "haute importance, je reviendrai vers vous dans quelques instants.", kind_info=[['VL1','no_weapon'],['SM','no_weapon'],2])
                self.cinematic_frame(screen, "azw2", 2, " Pas de problème monsieur, mais essayez de vous dépêcher ! Je n'ai pas", "envie de rester coincé dans ces débris..",kind_info=[['VL1', 'no_weapon'], ['SM', 'no_weapon'], 1])
        elif saved =='KM':
            self.cinematic_frame(screen, "azw2", 3, "Monsieur ! Monsieur ! Oui, vous, celui qui porte l'apparence d'un", "samouraï, venez m'aider ! ", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL1','no_weapon'],3])
            self.cinematic_frame(screen, "azw2", 3, "(Est-ce que j'accepte de l'aider..?) ", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL1','no_weapon'],1])
            output1, output2 = self.choice_frame(screen, "azw2", [0, 2], ["OUI", "NON"])
            if output1 == "choice":
                self.cinematic_frame(screen, "azw2", 3, "Très bien monsieur, je vais vous sortir de ces débris. Je m'en occupe !",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'],['VL1','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 3, "Je vous remercie fortement. ", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL1','no_weapon'],3])
                self.ecran_noir(screen)
                self.cinematic_frame(screen, "azw2", 3, "Merci beaucoup monsieur de m'avoir sorti de ce pétrin ! Tenez, voici de", "l'argent en guise de compensation. ", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL1','no_weapon'],3])
                self.cinematic_frame(screen, "azw2", 0, "(Le joueur obtient 15 pièces argent)")
                self.cinematic_frame(screen, "azw2", 3, "L'argent n'était pas nécessaire mais je vous remercie de votre générosité.", "Faîtes très attention lors de votre retour !",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['VL1','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 3, "A vous aussi monsieur ! Bonne chance à vous !", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL1','no_weapon'],3])
            elif output2 =="choice":
                self.cinematic_frame(screen, "azw2", 3, "Je suis navré monsieur, mais j'ai actuellement, des tâches de la plus", "haute importance, je reviendrai vers vous dans quelques instants.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL1','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 3, "Pas de problème monsieur, mais essayez de vous dépêcher ! Je n'ai pas", "envie de rester coincé dans ces débris..",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['VL1','no_weapon'],3])
        elif saved =='KT':
            self.cinematic_frame(screen, "azw2", 3, "Monsieur ! Monsieur ! Oui, vous, celui qui porte l'apparence d'un", "samouraï, venez m'aider ! ", kind_info=[['SM','no_weapon'],['KT','no_weapon'], ['VL1','no_weapon'],3])
            self.cinematic_frame(screen, "azw2", 3, "(Est-ce que j'accepte de l'aider..?) ", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL1','no_weapon'],1])
            output1, output2 = self.choice_frame(screen, "azw2", [0, 2], ["OUI", "NON"])
            if output1 == "OUI":
                self.cinematic_frame(screen, "azw2", 3, "Très bien monsieur, je vais vous sortir de ces débris. Je m'en occupe !",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'],['VL1','no_weapon'], 1])
                self.cinematic_frame(screen, "azw2", 3, "Je vous remercie fortement. ", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL1','no_weapon'],3])
                self.ecran_noir(screen)
                self.cinematic_frame(screen, "azw2", 3, "Merci beaucoup monsieur de m'avoir sorti de ce pétrin ! Tenez, voici de", "l'argent en guise de compensation. ", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL1','no_weapon'],3])
                self.cinematic_frame(screen, "azw2", 0, "(Le joueur obtient 15 pièces argent)")
                self.cinematic_frame(screen, "azw2", 3, " L'argent n'était pas nécessaire mais je vous remercie de votre générosité.", "Faîtes très attention lors de votre retour !",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'],['VL1','no_weapon'], 1])
                self.cinematic_frame(screen, "azw2", 3, "A vous aussi monsieur ! Bonne chance à vous !", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL1','no_weapon'],3])
            elif output1 =="NON":
                self.cinematic_frame(screen, "azw2", 3, "Je suis navré monsieur, mais j'ai actuellement, des tâches de la plus", "haute importance, je reviendrai vers vous dans quelques instants.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL1','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 3, " Pas de problème monsieur, mais essayez de vous dépêcher ! Je n'ai pas", "envie de rester coincé dans ces débris..",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'],['VL1','no_weapon'], 3])


    def dialog_minigm2(self, screen,saved):
        if saved == 'none':
            self.cinematic_frame(screen, "azw2", 2, "Tiens monsieur ? Vous ne serez pas par hasard un samouraï ?", kind_info=[['SM','no_weapon'],['VL2','no_weapon'],2])
            self.cinematic_frame(screen, "azw2", 2, "Si, effectivement, je le suis.", kind_info=[['SM','no_weapon'],['VL2','no_weapon'],1])
            self.cinematic_frame(screen, "azw2", 2, "Eh bien parfait, puisque j'ai une requête à vous demander. Auriez-vous du", "temps libre pour pouvoir accorder cette aide ?", kind_info=[['SM','no_weapon'],['VL2','no_weapon'],2])
            self.cinematic_frame(screen, "azw2", 2, "(Voyons voir..Ai-je quelque chose de très urgent ?)", kind_info=[['SM','no_weapon'],['VL2','no_weapon'],1])
            output1, output2 = self.choice_frame(screen, "azw2", [0, 2], ["OUI", "NON"])
            if output1 == "choice":
                self.cinematic_frame(screen, "azw2", 2, "En effet monsieur, j'ai du temps libre à ma disposition. Que","voudriez vous que je fasse ?",kind_info=[['SM', 'no_weapon'],['VL2', 'no_weapon'], 1])
                self.cinematic_frame(screen, "azw2", 2, "Très bien. Alors ma requête consiste tout simplement à récolter des", "ingrédients pour produire des vivres à la population.", kind_info=[['SM','no_weapon'],['VL2','no_weapon'],2])
                self.cinematic_frame(screen, "azw2", 2, "Je vois, auriez-vous une liste pour que je puisse obtenir les produits", "que vous recherchez ?", kind_info=[['SM','no_weapon'],['VL2','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 2, "Effectivement, j'en ai une. Voici de l'argent pour que vous puissiez", "les acheter. Je compte sur vous ! ",kind_info=[['SM', 'no_weapon'], ['VL2', 'no_weapon'], 2])
                self.ecran_noir(screen)
            elif output2 =="choice":
                self.cinematic_frame(screen, "azw2", 2, "Je suis désolé monsieur. Il se trouve que je n'ai pas beaucoup de temps", "libre à ma disposition.", kind_info=[['SM','no_weapon'],['VL2','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 2, "Je reviendrai vers vous une fois que je me serai occupé de mon affaire.", kind_info=[['SM','no_weapon'],['VL2','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 2, "Pas de souci monsieur. Je resterai ici, vous pourrez me retrouver facilement.",kind_info=[['SM', 'no_weapon'], ['VL2', 'no_weapon'], 2])
        elif saved == 'KM':
            self.cinematic_frame(screen, "azw2", 3, "Tiens monsieur ? Vous ne serez pas par hasard un samouraï ?", kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['VL2','no_weapon'],3])
            self.cinematic_frame(screen, "azw2", 3, "Si, effectivement, je le suis.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL2','no_weapon'],1])
            self.cinematic_frame(screen, "azw2", 3, "Eh bien parfait, puisque j'ai une requête à vous demander. Auriez-vous du", "temps libre pour pouvoir accorder cette aide ?", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL2','no_weapon'],3])
            self.cinematic_frame(screen, "azw2", 3, "(Voyons voir..Ai-je quelque chose de très urgent ?)", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL2','no_weapon'],1])
            output1, output2 = self.choice_frame(screen, "azw2", [0, 2], ["OUI", "NON"])
            if output1 == "choice":
                self.cinematic_frame(screen, "azw2", 3, "En effet monsieur, j'ai du temps libre à ma disposition. Que","voudriez vous que je fasse ?",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'],['VL2', 'no_weapon'], 1])
                self.cinematic_frame(screen, "azw2", 3, "Très bien. Alors ma requête consiste tout simplement à récolter des", "ingrédients pour produire des vivres à la population.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL2','no_weapon'],3])
                self.cinematic_frame(screen, "azw2", 3, "Je vois, auriez-vous une liste pour que je puisse obtenir les produits", "que vous recherchez ?", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL2','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 3, "Effectivement, j'en ai une. Voici de l'argent pour que vous puissiez", "les acheter. Je compte sur vous ! ",kind_info=[ ['SM', 'no_weapon'],['KM','no_weapon'],['VL2', 'no_weapon'], 3])
                self.ecran_noir(screen)
            elif output2 =="choice":
                self.cinematic_frame(screen, "azw2", 3, "Je suis désolé monsieur. Il se trouve que je n'ai pas beaucoup de temps", "libre à ma disposition.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL2','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 3, "Je reviendrai vers vous une fois que je me serai occupé de mon affaire.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL2','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 3, "Pas de souci monsieur. Je resterai ici, vous pourrez me retrouver facilement.",kind_info=[ ['SM', 'no_weapon'], ['KM','no_weapon'],['VL2', 'no_weapon'],3])

        elif saved == 'KT':
            self.cinematic_frame(screen, "azw2", 3, "Tiens monsieur ? Vous ne serez pas par hasard un samouraï ?", kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['VL2','no_weapon'],3])
            self.cinematic_frame(screen, "azw2", 3, "Si, effectivement, je le suis.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL2','no_weapon'],1])
            self.cinematic_frame(screen, "azw2", 3, "Eh bien parfait, puisque j'ai une requête à vous demander. Auriez-vous du", "temps libre pour pouvoir accorder cette aide ?", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL2','no_weapon'],3])
            self.cinematic_frame(screen, "azw2", 3, "(Voyons voir..Ai-je quelque chose de très urgent ?)", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL2','no_weapon'],1])
            output1, output2 = self.choice_frame(screen, "azw2", [0, 2], ["OUI", "NON"])
            if output1 == "choice":
                self.cinematic_frame(screen, "azw2", 3, "En effet monsieur, j'ai du temps libre à ma disposition. Que","voudriez vous que je fasse ?",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'],['VL2', 'no_weapon'], 1])
                self.cinematic_frame(screen, "azw2", 3, "Très bien. Alors ma requête consiste tout simplement à récolter des", "ingrédients pour produire des vivres à la population.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL2','no_weapon'],3])
                self.cinematic_frame(screen, "azw2", 3, "Je vois, auriez-vous une liste pour que je puisse obtenir les produits", "que vous recherchez ?", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL2','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 3, "Effectivement, j'en ai une. Voici de l'argent pour que vous puissiez", "les acheter. Je compte sur vous ! ",kind_info=[ ['SM', 'no_weapon'],['KT','no_weapon'],['VL2', 'no_weapon'], 3])
                self.ecran_noir(screen)
            elif output2 =="choice":
                self.cinematic_frame(screen, "azw2", 3, "Je suis désolé monsieur. Il se trouve que je n'ai pas beaucoup de temps", "libre à ma disposition.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL2','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 3, "Je reviendrai vers vous une fois que je me serai occupé de mon affaire.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL2','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 3, "Pas de souci monsieur. Je resterai ici, vous pourrez me retrouver facilement.",kind_info=[ ['SM', 'no_weapon'], ['KT','no_weapon'],['VL2', 'no_weapon'],3])


    def dialog_minigm3(self, screen,saved):
        if saved == 'none':
            self.cinematic_frame(screen, "azw2", 2, "Oh ? Un samouraï ? Je vous souhaite la bienvenue à Aizuwakamatsu.", kind_info=[['VL3','no_weapon'],['SM','no_weapon'],1])
            self.cinematic_frame(screen, "azw2", 2, "Je vous remercie de votre accueil. Que s'est-il passé exactement ? ", kind_info=[['VL3','no_weapon'],['SM','no_weapon'],2])
            self.cinematic_frame(screen, "azw2", 2, "Eh bien, pour la faire courte, une grande escouade du clan Takahiro a envahi", "nos terres pour détruire la ville.", kind_info=[['VL3','no_weapon'],['SM','no_weapon'],1])
            self.cinematic_frame(screen, "azw2", 2, "(C'est donc à nouveau à cause de ce clan que la ville est détruite..Si on ne", "les arrête pas, cela risque d'être très problématique..)", kind_info=[['VL3','no_weapon'],['SM','no_weapon'],2])
            self.cinematic_frame(screen, "azw2", 2, "Cela explique donc la reconstruction d'un de vos bâtiments. ", kind_info=[['VL3','no_weapon'],['SM','no_weapon'],2])
            self.cinematic_frame(screen, "azw2", 2, "C'est très juste. Tant que vous y êtes, voudriez-vous bien nous passer un","coup de main ?", kind_info=[['VL3','no_weapon'],['SM','no_weapon'],1])
            self.cinematic_frame(screen, "azw2", 2, " (Hmm, que faire ? Ai-je quelque chose de plus urgent ?)", kind_info=[['VL3','no_weapon'],['SM','no_weapon'],2])
            output1, output2 = self.choice_frame(screen, "azw2", [0, 2], ["OUI", "NON"])
            if output1 == "choice":
                self.cinematic_frame(screen, "azw2", 2, "Pourquoi pas. C'est le mieux que je puisse faire pour pouvoir aider", "Aizuwakamatsu.",kind_info=[['VL3', 'no_weapon'], ['SM', 'no_weapon'], 2])
                self.cinematic_frame(screen, "azw2", 2, "Merci de vos efforts, monsieur le samouraï. Ce que vous devez faire, c'est", "suivre le plan de ce parchemin. Elle contient toutes les étapes nécessaires", "à la reconstruction de ce mur. A vous de jouer !", kind_info=[['VL3','no_weapon'],['SM','no_weapon'],1])
                self.ecran_noir(screen)
                self.cinematic_frame(screen, "azw2", 2, "Splendide ! Vous avez un très bon travail. Je vous félicite.",kind_info=[['VL3', 'no_weapon'], ['SM', 'no_weapon'], 1])
                self.cinematic_frame(screen, "azw2", 2, "L'honneur est pour moi monsieur. Je me suis contenté du nécessaire, c'est tout", "simplement du bon sens.", kind_info=[['VL3','no_weapon'],['SM','no_weapon'],2])
                self.cinematic_frame(screen, "azw2", 2, "C'est formidable. N'hésitez-pas à aller voir les autres habitants dans le coin", "qui auront peut-être besoin de votre aide.",kind_info=[['VL3', 'no_weapon'], ['SM', 'no_weapon'], 1])
            elif output2 =="choice":
                self.cinematic_frame(screen, "azw2", 2, "Veuillez me pardonner, mais j'ai une tâche très urgente à réaliser. Je", "reviendrai vers vous une fois l'affaire réglée.", kind_info=[['VL3','no_weapon'],['SM','no_weapon'],2])
                self.cinematic_frame(screen, "azw2", 2, "Prenez votre temps monsieur ! Faîtes ce que vous devez faire.", kind_info=[['VL3','no_weapon'],['SM','no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 2, "Par ailleurs, si vous croisez d'autres habitants en détresse, essayez de les", "aider une fois que vous aurez du temps libre.",kind_info=[['VL3', 'no_weapon'], ['SM', 'no_weapon'], 1])
        elif saved == 'KM':
            self.cinematic_frame(screen, "azw2", 3, "Oh ? Un samouraï ? Je vous souhaite la bienvenue à Aizuwakamatsu.", kind_info=[['SM','no_weapon'], ['KM','no_weapon'],['VL3','no_weapon'],3])
            self.cinematic_frame(screen, "azw2", 3, "Je vous remercie de votre accueil. Que s'est-il passé exactement ? ", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL3','no_weapon'],1])
            self.cinematic_frame(screen, "azw2", 3, "Eh bien, pour la faire courte, une grande escouade du clan Takahiro a envahi", "nos terres pour détruire la ville.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL3','no_weapon'],3])
            self.cinematic_frame(screen, "azw2", 3, "(C'est donc à nouveau à cause de ce clan que la ville est détruite..Si on ne", "les arrête pas, cela risque d'être très problématique..)", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL3','no_weapon'],1])
            output1, output2 = self.choice_frame(screen, "azw2", [0, 2], ["OUI", "NON"])
            if output1 == "choice":
                self.cinematic_frame(screen, "azw2", 3, "Pourquoi pas. C'est le mieux que je puisse faire pour pouvoir aider", "Aizuwakamatsu.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'],['VL3', 'no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 3, "Merci de vos efforts, monsieur le samouraï. Ce que vous devez faire, c'est", "suivre le plan de ce parchemin. Elle contient toutes les étapes nécessaires", "à la reconstruction de ce mur. A vous de jouer !", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL3', 'no_weapon'], 3])
                self.ecran_noir(screen)
                self.cinematic_frame(screen, "azw2", 3, "Splendide ! Vous avez un très bon travail. Je vous félicite.", "que vous recherchez ?", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL3','no_weapon'],3])
                self.cinematic_frame(screen, "azw2", 3, "L'honneur est pour moi monsieur. Je me suis contenté du nécessaire, c'est tout", "simplement du bon sens.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'],['VL3', 'no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 3, "C'est formidable. N'hésitez-pas à aller voir les autres habitants dans le coin", "qui auront peut-être besoin de votre aide.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL3','no_weapon'],3])
            elif output2 =="choice":
                self.cinematic_frame(screen, "azw2", 3, "Veuillez me pardonner, mais j'ai une tâche très urgente à réaliser. Je", "reviendrai vers vous une fois l'affaire réglée.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL3', 'no_weapon'], 1])
                self.cinematic_frame(screen, "azw2", 3, "Prenez votre temps monsieur ! Faîtes ce que vous devez faire.", kind_info=[['SM','no_weapon'],['KM','no_weapon'],['VL3', 'no_weapon'], 3])
                self.cinematic_frame(screen, "azw2", 3, "Par ailleurs, si vous croisez d'autres habitants en détresse, essayez de les", "aider une fois que vous aurez du temps libre.",kind_info=[['SM', 'no_weapon'], ['KM','no_weapon'],['VL3', 'no_weapon'], 3])

        elif saved == 'KT':
            self.cinematic_frame(screen, "azw2", 3, "Oh ? Un samouraï ? Je vous souhaite la bienvenue à Aizuwakamatsu.", kind_info=[['SM','no_weapon'], ['KT','no_weapon'],['VL3','no_weapon'],3])
            self.cinematic_frame(screen, "azw2", 3, "Je vous remercie de votre accueil. Que s'est-il passé exactement ? ", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL3','no_weapon'],1])
            self.cinematic_frame(screen, "azw2", 3, "Eh bien, pour la faire courte, une grande escouade du clan Takahiro a envahi", "nos terres pour détruire la ville.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL3','no_weapon'],3])
            self.cinematic_frame(screen, "azw2", 3, "(C'est donc à nouveau à cause de ce clan que la ville est détruite..Si on ne", "les arrête pas, cela risque d'être très problématique..)", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL3','no_weapon'],1])
            output1, output2 = self.choice_frame(screen, "azw2", [0, 2], ["OUI", "NON"])
            if output1 == "choice":
                self.cinematic_frame(screen, "azw2", 3, "Pourquoi pas. C'est le mieux que je puisse faire pour pouvoir aider", "Aizuwakamatsu.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'],['VL3', 'no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 3, "Merci de vos efforts, monsieur le samouraï. Ce que vous devez faire, c'est", "suivre le plan de ce parchemin. Elle contient toutes les étapes nécessaires", "à la reconstruction de ce mur. A vous de jouer !", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL3', 'no_weapon'], 3])
                self.ecran_noir(screen)
                self.cinematic_frame(screen, "azw2", 3, "Splendide ! Vous avez un très bon travail. Je vous félicite.", "que vous recherchez ?", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL3','no_weapon'],3])
                self.cinematic_frame(screen, "azw2", 3, "L'honneur est pour moi monsieur. Je me suis contenté du nécessaire, c'est tout", "simplement du bon sens.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'],['VL3', 'no_weapon'],1])
                self.cinematic_frame(screen, "azw2", 3, "C'est formidable. N'hésitez-pas à aller voir les autres habitants dans le coin", "qui auront peut-être besoin de votre aide.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL3','no_weapon'],3])
            elif output2 =="choice":
                self.cinematic_frame(screen, "azw2", 3, "Veuillez me pardonner, mais j'ai une tâche très urgente à réaliser. Je", "reviendrai vers vous une fois l'affaire réglée.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL3', 'no_weapon'], 1])
                self.cinematic_frame(screen, "azw2", 3, "Prenez votre temps monsieur ! Faîtes ce que vous devez faire.", kind_info=[['SM','no_weapon'],['KT','no_weapon'],['VL3', 'no_weapon'], 3])
                self.cinematic_frame(screen, "azw2", 3, "Par ailleurs, si vous croisez d'autres habitants en détresse, essayez de les", "aider une fois que vous aurez du temps libre.",kind_info=[['SM', 'no_weapon'], ['KT','no_weapon'],['VL3', 'no_weapon'], 3])


    def dialog_infiltration(self,screen,saved,filature_reussie,passcode):
        if saved=='none':
            self.cinematic_frame(screen, "tkh1", 1,"Toc Toc", kind_info=["SM","SM", "no_weapon","right"])
            self.cinematic_frame(screen,"tkh1",2,"Vous faites partie du clan ? Quel est le code ?",kind_info=[['SM','no_weapon'],['TW','no_weapon'],2])
            self.cinematic_frame(screen,"tkh1",2,"(Un code ? Qu'est-ce que ça peut bien être ?)",kind_info=[['SM','no_weapon'],['TW','no_weapon'],1])
            if filature_reussie==True:
                self.cinematic_frame(screen, "tkh1", 2, "(Mais oui !)",kind_info=[['SM', 'no_weapon'], ['TW', 'no_weapon'], 1])
                self.cinematic_frame(screen, "tkh1", 2, passcode,kind_info=[['SM','no_weapon'],['TW','no_weapon'],1])
                self.cinematic_frame(screen, "tkh1", 2, "Ok, entrez discrètement",kind_info=[['SM','no_weapon'],['TW','no_weapon'],2])
                self.cinematic_frame(screen, "tkh1", 2, "Je le savais ! C'est bien le code que j'ai entendu !", kind_info=["SM","SM", "no_weapon","right"])
                self.cinematic_frame(screen, "tkh1", 2, "Cela signifie que cela doit être la sous-planque secrète du clan Takahiro !", kind_info=["SM","SM", "no_weapon","right"])
                self.cinematic_frame(screen, "tkh1", 2, "Bon, que faire ? Est-ce que j'inflitre la base ou j'effectue des préparations ?", kind_info=["SM","SM", "no_weapon","right"])
            elif filature_reussie==False:
                self.cinematic_frame(screen, "tkh1", 2, "Hem… jaimelacouscoustajine ?",kind_info=[['SM', 'no_weapon'], ['?', 'no_weapon'], 1])
                self.cinematic_frame(screen,"tkh1",2,"Vas-t-en et laisse-nous tranquilles. Ne reviens pas si tu ne veux pas avoir", "des problèmes.",kind_info=[['SM','no_weapon'],['?','no_weapon'],2])
                self.cinematic_frame(screen, "tkh1", 2, "Mais pour qui il se prend, lui ?",kind_info=["SM","SM", "no_weapon","right"])
        elif saved=='KM':
            self.cinematic_frame(screen, "tkh1", 1,"Toc Toc", kind_info=[["SM",'no_weapon'],['KM','no_weapon'],1])
            self.cinematic_frame(screen,"tkh1",2,"Vous faites partie du clan ? Quel est le code ?",kind_info=[['SM','no_weapon'],['KM','no_weapon'],['?','no_weapon'],2])
            self.cinematic_frame(screen,"tkh1",2,"(Un code ? Qu'est-ce que ça peut bien être ?)",kind_info=[['SM','no_weapon'],['KM','no_weapon'],['?','no_weapon'],1])
            if filature_reussie==True:
                self.cinematic_frame(screen, "tkh1", 2, " (Mais oui !)",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['?', 'no_weapon'], 1])
                self.cinematic_frame(screen,"tkh1",2,"*dit le code* ",kind_info=[['SM','no_weapon'],['KM','no_weapon'], ['?','no_weapon'],1])
                self.cinematic_frame(screen,"tkh1",2,"Ok, entrez discrètement",kind_info=[['SM','no_weapon'],['KM','no_weapon'],3])
                self.cinematic_frame(screen,"tkh1",2,"Je le savais ! C'est bien le code que j'ai entendu quand j'ai suivi les gardes !",kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
                self.cinematic_frame(screen,"tkh1",2,"Quand nous étions au dojo ?",kind_info=[['SM','no_weapon'],['KM','no_weapon'],2])
                self.cinematic_frame(screen,"tkh1",2,"Exactement ! Cela signifie que cela doit être la sous-planque secrète du clan", "Takahiro ! ",kind_info=[['SM','no_weapon'],['KM','no_weapon'],1])
            elif filature_reussie==False:
                self.cinematic_frame(screen, "tkh1", 2, "Hem… jaimelacouscoustajine ?",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['?', 'no_weapon'], 1])
                self.cinematic_frame(screen, "tkh1", 2, "Allez-vous-en et laissez-nous tranquilles. Ne revenez pas si vous ne voulez", "pas avoir des problèmes.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], ['?', 'no_weapon'], 3])
                self.cinematic_frame(screen, "tkh1", 2, "Hé bien ! Ils ont l'air de bien rigoler ici.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'], 2])
                self.cinematic_frame(screen, "tkh1", 2, "C'est sûrement une sous-planque de Takahiro, faisons-nous discrets.",kind_info=[['SM', 'no_weapon'],['KM','no_weapon'],1])
        elif saved=='KT':
            self.cinematic_frame(screen, "tkh1", 1,"Toc Toc", kind_info=[["SM",'no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen,"tkh1",2,"Vous faites partie du clan ? Quel est le code ?",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['?','no_weapon'],2])
            self.cinematic_frame(screen,"tkh1",2,"(Un code ? Qu'est-ce que ça peut bien être ?)",kind_info=[['SM','no_weapon'],['KT','no_weapon'],['?','no_weapon'],1])
            if filature_reussie==True:
                self.cinematic_frame(screen, "tkh1", 2, " (Mais oui !)",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['?', 'no_weapon'], 1])
                self.cinematic_frame(screen,"tkh1",2,"*dit le code* ",kind_info=[['SM','no_weapon'],['KT','no_weapon'], ['?','no_weapon'],1])
                self.cinematic_frame(screen,"tkh1",2,"Ok, entrez discrètement",kind_info=[['SM','no_weapon'],['KT','no_weapon'],3])
                self.cinematic_frame(screen,"tkh1",2,"Je le savais ! C'est bien le code que j'ai entendu quand j'ai suivi les gardes !",kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
                self.cinematic_frame(screen,"tkh1",2,"Cela signifie que cela doit être la sous-planque secrète du clan Takahiro ?",kind_info=[['SM','no_weapon'],['KT','no_weapon'],2])
                self.cinematic_frame(screen,"tkh1",2,"Tout-à-fait,Takeshi. Bon, entrons…",kind_info=[['SM','no_weapon'],['KT','no_weapon'],1])
            elif filature_reussie==False:
                self.cinematic_frame(screen, "tkh1", 2, "Hem… jaimelacouscoustajine ?",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['?', 'no_weapon'], 1])
                self.cinematic_frame(screen, "tkh1", 2, "Allez-vous-en et laissez-nous tranquilles. Ne revenez pas si vous ne voulez", "pas avoir des problèmes.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], ['?', 'no_weapon'], 3])
                self.cinematic_frame(screen, "tkh1", 2, "Hé bien ! Ils ont l'air de bien rigoler ici.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'], 2])
                self.cinematic_frame(screen, "tkh1", 2, "C'est sûrement une sous-planque de Takahiro, faisons-nous discrets.",kind_info=[['SM', 'no_weapon'],['KT','no_weapon'],1])

    def dialog_infiltration_base(self,screen,saved):
        if saved=='none' or saved=='KM':
            self.cinematic_frame(screen,"tkh1",1,"Bon, que faire maintenant ?",kind_info=["SM","SM", "no_weapon","right"])
            self.cinematic_frame(screen,"tkh1",1,"Je pourrais leur faire perdre du temps, en cachant leurs armes. Mais je", "pourrais aussi directement venger mon village en les tuant dans leur", "sommeil...",kind_info=["SM","SM", "no_weapon","right"])
            output1, output2 = self.choice_frame(screen, "tkh1", [0, 2], ["PRENDRE LES ARMES", "TOUS LES TUER"])
            if output1 == "choice":
                self.cinematic_frame(screen, "tkh1", 1, "J'ai enfin pris ma décision.",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen,"tkh1",1,"Si je décide de tous les massacrer, je deviendrai celui que je déteste le","plus. Un tueur à gages, qui ne fait que détruire tout devant son chemin.",kind_info=["SM","SM", "no_weapon","right"])
                self.cinematic_frame(screen,"tkh1",1,"Au lieu d'essayer de les exécuter, je pense que je vais confisquer leurs", "armes.",kind_info=["SM","SM", "no_weapon","right"])
                self.cinematic_frame(screen,"tkh1",1,"Que feront-ils s'ils n'ont aucun moyen pour se défendre..voire pour", "attaquer ?",kind_info=["SM","SM", "no_weapon","right"])
                self.cinematic_frame(screen,"tkh1",1,"Mon choix est fait. Je prends toutes les armes et les équipements qui sont", "dans cette planque avec discrétion. ",kind_info=["SM","SM", "no_weapon","right"])
            elif output2 == "choice":
                self.cinematic_frame(screen, "tkh1", 1, "Attends une minute..Ai-je vraiment l'audace de penser à les laisser en vie..",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1, "Après tout ce qu'ils ont fait ? J'ose les pardonner avec toutes les horreurs", "qu'ils ont commises ? ",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1, "Franchement je suis un peu trop gentil. Non, j'en ai tout simplement marre.",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1, "J'ai envie de tous les détruire, tous les massacrer, tous les exécuter, tous", "les trucider, tous les couper.",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1, "Mon choix est fait. Ils vont subir un châtiment très désagréable. Leur sang..","Leurs tortures.. Leurs cris constitueront ma joie..",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1, "Oui.. ça y est.. Enfin…le moment pour tous les tuer.. Ha.. Ha HA..",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1, "HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA !", "HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! ",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1, "...J'ai hâte de vous égorger..bande de minables ! ! ",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1, "...",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1, "Préparez-vous à rencontrer votre fin.",kind_info=["SM", "SM", "no_weapon", "right"])
        
        elif saved=='KT':
            self.cinematic_frame(screen, "tkh1", 2, "Bon, que faire maintenant ?",kind_info=[["SM",'no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "tkh1", 2,"On pourrait cacher leurs armes ça les rendrait inoffensifs.",kind_info=[["SM",'no_weapon'],['KT','no_weapon'],2])
            self.cinematic_frame(screen, "tkh1", 2, "Mais on pourrait aussi directement venger notre village en les tuant dans", "leur sommeil…",kind_info=[["SM",'no_weapon'],['KT','no_weapon'],1])
            self.cinematic_frame(screen, "tkh1", 2,"Quoi ? Tu veux vraiment faire ça ?",kind_info=[["SM",'no_weapon'],['KT','no_weapon'],2])
            output1, output2 = self.choice_frame(screen, "tkh1", [0, 2], ["PRENDRE LES ARMES", "TOUS LES TUER"])
            if output1 == "choice":
                self.cinematic_frame(screen, "tkh1", 2, "Alors Musashi. Que feras-tu?",kind_info=[["SM",'no_weapon'],['KT','no_weapon'],2])
                self.cinematic_frame(screen, "tkh1", 2,"J'ai enfin pris ma décision.",kind_info=[["SM",'no_weapon'],['KT','no_weapon'],1])
                self.cinematic_frame(screen, "tkh1", 2,"Si je décide de tous les massacrer, je deviendrai celui que je déteste le","plus. Un tueur à gages, qui ne fait que détruire tout devant son chemin.", kind_info=[["SM",'no_weapon'],['KT','no_weapon'],1])
                self.cinematic_frame(screen, "tkh1", 2,"Au lieu d'essayer de les exécuter, je pense que je vais confisquer leurs","armes.", kind_info=[["SM",'no_weapon'],['KT','no_weapon'],1])
                self.cinematic_frame(screen, "tkh1", 2,"Que feront-ils s'ils n'ont aucun moyen pour se défendre..voire pour", "attaquer ?", kind_info=[["SM",'no_weapon'],['KT','no_weapon'],1])
                self.cinematic_frame(screen, "tkh1", 2,"Mon choix est fait. Prenons toutes les armes et les équipements qui sont","dans cette planque avec discrétion. ",kind_info=[["SM",'no_weapon'],['KT','no_weapon'],1])
            elif output2 == "choice":
                self.cinematic_frame(screen, "tkh1", 2,"Alors Musashi. Que feras-tu?",kind_info=[["SM",'no_weapon'],['KT','no_weapon'],2])
                self.cinematic_frame(screen, "tkh1", 2,"Takeshi, retrouve-moi dehors.",kind_info=[["SM",'no_weapon'],['KT','no_weapon'],1])
                self.cinematic_frame(screen, "tkh1", 2,"T'es sûr..Je doute de ce que tu comptes faire.",kind_info=[["SM",'no_weapon'],['KT','no_weapon'],2])
                self.cinematic_frame(screen, "tkh1", 2,"Fais ce que je dis. Fais moi confiance.",kind_info=[["SM",'no_weapon'],['KT','no_weapon'],1])
                self.cinematic_frame(screen,'tkh1',0,"(Takeshi part de la planque)")
                self.cinematic_frame(screen, "tkh1", 1,"...Bon, je les laisse en vie ? ",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1,"Mouais c'est pour le bien de tous.",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1,"Attends une minute..Ai-je vraiment l'audace de penser à les laisser en vie..",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1,"Après tout ce qu'ils ont fait ? J'ose les pardonner avec toutes les horreurs","qu'ils ont commises ? ", kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1,"Franchement je suis un peu trop gentil. Non, j'en ai tout simplement marre.",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1,"J'ai envie de tous les détruire, tous les massacrer, tous les exécuter, tous","les trucider, tous les couper.", kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1,"Mon choix est fait. Ils vont subir un châtiment très désagréable. Leur sang..","Leurs tortures.. Leurs cris constitueront ma joie..",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1,"Oui.. ça y est.. Enfin…le moment pour tous les tuer.. Ha.. Ha HA..",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1,"HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA !","HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! HA ! ",kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1, "...J'ai hâte de vous égorger..bande de minables ! ! ", kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1, "...", kind_info=["SM", "SM", "no_weapon", "right"])
                self.cinematic_frame(screen, "tkh1", 1, "Préparez-vous à rencontrer votre fin.",kind_info=["SM", "SM", "no_weapon", "right"])


if __name__ =="__main__":
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    pygame.display.set_caption("Kage no Michi - Dialogues")
    Dialogs().dialog_infiltration(screen,'none',True,"AAAAAAAA")
    pygame.quit()
