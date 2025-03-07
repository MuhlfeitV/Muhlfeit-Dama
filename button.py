import pygame

class Button:
    
    def __init__(self, asset, asset_h, x, y):
        self.img = asset
        self.img_h = asset_h
        self.rect = self.img.get_rect()
        self.rect_H = self.img_h.get_rect()
        self.rect.topleft = (x, y)
        self.rect_H.topleft = (x, y)
        self.clicked = False

    def draw(self, screen):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                return True
            if not pygame.mouse.get_pressed()[0]:
                self.clicked = False
            screen.blit(self.img_h, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.img, (self.rect.x, self.rect.y))