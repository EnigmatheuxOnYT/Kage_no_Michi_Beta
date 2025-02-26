import pygame

class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self,name):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f"../data/assets/sprites/{name}.png")
        self.animation_index = 0
        self.clock = 0
        self.images = {
            "right": self.get_images(0),
            "down": self.get_images(44),
            "up": self.get_images(88),
            "left": self.get_images(132),
            "upright": self.get_images(176),
            "downleft": self.get_images(220),
            "downright": self.get_images(264),
            "upleft": self.get_images(308)
        }
        self.speed = 3


    def change_animation(self,name):
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey(0,0)
        self.clock += 20

        if self.clock >= 100:

            self.animation_index += 1
            if self.animation_index>=len(self.images[name]):
                self.animation_index = 0
            self.clock = 0

    def get_images(self,y):
        images=[]

        for i in range(3):
            x = i*34
            image = self.get_image(x,y)
            images.append(image)

        return images

    def get_image(self, x, y):
        image = pygame.Surface([34, 44])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 34, 44))
        return image

