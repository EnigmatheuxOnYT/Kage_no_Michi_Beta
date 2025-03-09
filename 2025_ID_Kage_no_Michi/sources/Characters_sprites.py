#Projet : Kage no Michi
#Auteurs : Alptan Korkmaz, Clément Roux--Bénabou, Maxime Rousseaux, Ahmed-Adam Rezkallah, Cyril Zhao


# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 00:46:24 2025

@author: clementroux--benabou
"""
import pygame

class Characters_sprites:
    
    def __init__ (self):
                               #Shikisha Musashi
        self.for_cinematics = {'SM': {'right': {'no_weapon': {'main': self.ldc("Shikisha_16bit_Droite_SansArme_V1.png"),
                                                              'secondary': self.ldc("Shikisha_16bit_Droite_SansArme_Ombre_V1.png")
                                                              },
                                                'wood_katana': {'main': self.ldc(),
                                                                'secondary':self.ldc()
                                                                },
                                                'jizo_katana': {'main': self.ldc(),
                                                                'secondary': self.ldc()
                                                                }
                                                },
                                      'left':  {'no_weapon': {'main': self.ldc("Shikisha_16bit_Gauche_SansArme_V1.png"),
                                                              'secondary': self.ldc("Shikisha_16bit_Gauche_SansArme_Ombre_V1.png")
                                                              },
                                                'wood_katana': {'main': self.ldc(),
                                                                'secondary': self.ldc()
                                                                },
                                                'jizo_katana': {'main': self.ldc(),
                                                                'secondary': self.ldc()
                                                                }
                                                }
                                      },
                               #Sensei Hoshida
                               'SH': {'right': {'no_weapon': {'main': self.ldc("Hoshida_16bit_Droite_SansArme_V1.png"),
                                                              'secondary': self.ldc("Hoshida_16bit_Droite_SansArme_Ombre_V1.png")
                                                              },
                                                'wood_katana': {'main': self.ldc(),
                                                                'secondary':self.ldc()
                                                                }
                                                },
                                      'left': {'no_weapon': {'main': self.ldc("Hoshida_16bit_Gauche_SansArme_V1.png"),
                                                             'secondary': self.ldc("Hoshida_16bit_Gauche_SansArme_Ombre_V1.png")
                                                             },
                                               'wood_katana': {'main': self.ldc(),
                                                               'secondary':self.ldc()
                                                               }
                                               }
                                      },
                               #Senshi Akuma
                               'SA': {'right': {'no_weapon': {'main': self.ldc("Senshi_16bit_Droite_SansArme_V1.png"),
                                                              'secondary': self.ldc("Senshi_16bit_Droite_SansArme_Ombre_V1.png")
                                                              }
                                                },
                                      'left': {'no_weapon': {'main': self.ldc("Senshi_16bit_Gauche_SansArme_V1.png"),
                                                             'secondary': self.ldc("Senshi_16bit_Gauche_SansArme_Ombre_V1.png")
                                                             }
                                               }
                                      },
                                #Takahiro Korijo
                               'TK': {'right': {'no_weapon': {'main': self.ldc("Takahiro_16bit_Droite_SansArme_V2.png"),
                                                              'secondary': self.ldc("Takahiro_16bit_Droite_SansArme_Ombre_V2.png")
                                                              }
                                                },
                                      'left': {'no_weapon': {'main': self.ldc("Takahiro_16bit_Gauche_SansArme_V2.png"),
                                                             'secondary': self.ldc("Takahiro_16bit_Gauche_SansArme_Ombre_V2.png")
                                                             }
                                               }
                                      },
                               #Keiko Musashi
                               'KM': self.load_character("Keiko"),
                               #Kurosawa Takeshi
                               'KT': {'right': {'no_weapon': {'main': self.ldc("Takeshi_16bit_Droite_SansArme_V1.png"),
                                                              'secondary': self.ldc("Takeshi_16bit_Droite_SansArme_Ombre_V1.png")
                                                              },
                                                'wood_katana': {'main': self.ldc(),
                                                                'secondary': self.ldc()
                                                                },
                                                'main_katana': {'main': self.ldc(),
                                                                'secondary': self.ldc()
                                                                }
                                                },
                                      'left':{'no_weapon': {'main': self.ldc("Takeshi_16bit_Gauche_SansArme_V1.png"),
                                                            'secondary': self.ldc("Takeshi_16bit_Gauche_SansArme_Ombre_V1.png")
                                                            },
                                              'wood_katana': {'main': self.ldc(),
                                                              'secondary': self.ldc()
                                                              },
                                              'main_katana': {'main': self.ldc(),
                                                              'secondary': self.ldc()
                                                              }
                                              }
                                      },
                               #Juzo Ma
                               'JM': {'right': {'no_weapon': {'main': self.ldc("Juzo_16bit_Droite_SansArme_V1.png"),
                                                              'secondary': self.ldc("Juzo_16bit_Droite_SansArme_Ombre_V1.png")
                                                               },
                                                },
                                      'left':{'no_weapon': {'main': self.ldc("Juzo_16bit_Gauche_SansArme_V1.png"),
                                                            'secondary': self.ldc("Juzo_16bit_Gauche_SansArme_Ombre_V1.png")
                                                            }
                                              }
                                      },
                               #Yoshiro
                               'Y?' : self.load_character("Yoshiro"),
                               # Guerrier takahiro
                               'TW' : {'right': {'no_weapon': {'main': self.ldc("Soldat_16bit_Droite_SansCapuche_SansArme_V1.png"),
                                                               'secondary': self.ldc("Soldat_16bit_Droite_SansCapuche_SansArme_Ombre_V1.png")
                                                               }
                                                 },
                                       'left':{'no_weapon': {'main': self.ldc("Soldat_16bit_Gauche_SansCapuche_SansArme_V1.png"),
                                                             'secondary': self.ldc("Soldat_16bit_Gauche_SansCapuche_SansArme_Ombre_V1.png")
                                                             }
                                               }
                                       },
                               'TW_H' : {'right': {'no_weapon': {'main': self.ldc("Soldat_16bit_Droite_AvecCapuche_SansArme_V1.png"),
                                                                 'secondary': self.ldc("Soldat_16bit_Droite_AvecCapuche_SansArme_Ombre_V1.png")
                                                                 },
                                                   "cin07" : {'secondary': self.ldc("Soldat_16bit_Gauche_AvecCapuche_SansArme_Ombre_V1.png"),
                                                              'main': self.ldc("Soldat_16bit_Gauche_AvecCapuche_SansArme_V1.png")
                                                              }
                                                   },
                                       'left':{'no_weapon': {'main': self.ldc("Soldat_16bit_Gauche_AvecCapuche_SansArme_V1.png"),
                                                             'secondary': self.ldc("Soldat_16bit_Gauche_AvecCapuche_SansArme_Ombre_V1.png")
                                                             }
                                               }
                                       },
                               'TWs' : {'left':{'no_weapon': {'main': self.ldc("Soldats_16bit_Gauche_SansArme_V1.png"),
                                                             'secondary': self.ldc("Soldats_16bit_Gauche_SansArme_Ombre_V1.png")
                                                             }
                                               }
                                       },
                               'none' : {'right': {'no_weapon': {'main': self.ldc('none.png'),
                                                                 'secondary': self.ldc('none.png')
                                                                 }
                                                   },
                                         'left': {'no_weapon': {'main': self.ldc('none.png'),
                                                                'secondary': self.ldc('none.png')
                                                                }
                                                  }
                                         },

                                'P' : {'left': {'no_weapon': {'main': self.ldc('Pancarte_Dialogues_V4.png')}}},
                                'VL1': self.load_villager(1),
                                'VL2': self.load_villager(2),
                                'VL3': self.load_villager(3)
                               }
        
        
        self.for_mgm = {"villager1": self.ldc("Villager12_Droite_SansArme_V1.png"), # Artisan, homme
                        "villager2": self.ldc("Villager8_Droite_SansArme_V1.png"), # Experte des eaux, femme
                        "villager3": self.ldc("Villager10_Droite_SansArme_V1.png"), # Combattante, femme
                        "villager4": self.ldc("Villager14_Droite_SansArme_V1.png"), # Mushoku (sans profession), homme
                        "villager5": self.ldc("Villager6_Droite_SansArme_V1.png"), # Boulangère, femme
                        "villager6": self.ldc("Villager7_Droite_SansArme_V1.png"), # Etudiant, homme
                        "villager7": self.ldc("Villager13_Droite_SansArme_V1.png"), # Potière, femme
                        "villager8": self.ldc("Villager4_Droite_SansArme_V1.png"), # Pécheur, homme
                        "villager9": self.ldc("Villager5_Droite_SansArme_V1.png"), # Charbonnier, homme
                        "villager10": self.ldc("Villager9_Droite_SansArme_V1.png"),# Poète, homme
                        "villager11": self.ldc("Villager11_Droite_SansArme_V1.png"),# Saltimbanque, homme
                        "villager12": self.ldc("Villager15_Droite_SansArme_V1.png") # Mineur, homme
                        }
        
        
        
        
    def ldc (self,file="Placeholder.png"):
        return pygame.image.load("../data/assets/cinematics/characters/"+file)
    
    def ldm (self,file):
        return pygame.image.load("../data/assets/minigm/"+file)
    
    def load_character (self,name):
        char = {'right': {'no_weapon': {'main': self.ldc(f"{name}_16bit_Droite_SansArme_V1.png"),
                                        'secondary': self.ldc(f"{name}_16bit_Droite_SansArme_Ombre_V1.png")
                                         },
                        },
                'left':{'no_weapon': {'main': self.ldc(f"{name}_16bit_Gauche_SansArme_V1.png"),
                                      'secondary': self.ldc(f"{name}_16bit_Gauche_SansArme_Ombre_V1.png")
                                      }
                        }
                }
        return char

    def load_villager (self,no):
        name=str(no)
        char = {'right': {'no_weapon': {'main': self.ldc(f"Villager{name}_16bit_Droite_SansArme_V1.png"),
                                        'secondary': self.ldc(f"Villager{name}_16bit_Droite_SansArme_Ombre_V1.png")
                                         },
                        },
                'left':{'no_weapon': {'main': self.ldc(f"Villager{name}_16bit_Gauche_SansArme_V1.png"),
                                      'secondary': self.ldc(f"Villager{name}_16bit_Gauche_SansArme_Ombre_V1.png")
                                      }
                        }
                }
        return char
