from math import hypot

import pygame

from Utils.GUI.Pathing.Path import dataProcessing
from Utils.GUI.Utils import loadImage, getScreenDimensions


class Target(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.screen = screen
        self.coordinates = dataProcessing()
        self.radius = 40
        self.image = loadImage('/Users/Tinku/Desktop/Eye-Tracking-Disease-Detection/TestingGUI/Assets/target.png',
                               self.radius)
        self.rect = self.image.get_rect()
        self.velocity = 100
        self.index = 0
        self.isMovementFinished = False
        self.finalDestReached = False
        self.getEyeCoords = False
        self.rect.center = [getScreenDimensions()[0] / 2, getScreenDimensions()[1] / 2]
        self.cloneRect = self.rect

    def followPath(self, ticks):
        try:
            if self.isMovementFinished:
                self.index += 1
            self.move(self.coordinates[self.index], ticks)
        except IndexError:
            self.finalDestReached = True
            pass

    def move(self, point, ticks):
        self.isMovementFinished = False
        self.getEyeCoords = False
        rectList = list(self.rect.center)
        distX = point[0] - rectList[0]
        distY = point[1] - rectList[1]
        if distX > 0:
            rectList[0] += ((self.velocity * ticks) / 1000)
        if distX < 0:
            rectList[0] -= ((self.velocity * ticks) / 1000)
        if distY > 0:
            if distX <= self.radius:
                rectList[1] += ((self.velocity * ticks) / 1000)
            else:
                rectList[1] += ((self.velocity * ticks) / 1000)
        if distY < 0:
            if distX <= self.radius:
                rectList[1] -= ((self.velocity * ticks) / 1000)
            else:
                rectList[1] -= ((self.velocity * ticks) / 1000)
        self.rect.center = rectList
        constrainedRect = self.rect.clamp(self.screen.get_rect())
        self.rect = constrainedRect
        self.screen.blit(self.image, self.rect)
        if point == [0, getScreenDimensions()[1]] or point == [0, 0] or point == [getScreenDimensions()[0],
                                                                                  0] or point == getScreenDimensions():
            if self.rect.topleft == tuple([0, 0]) or self.rect.topright == tuple(
                    [getScreenDimensions()[0], 0]) or self.rect.bottomright == \
                    tuple(getScreenDimensions()) or self.rect.bottomleft == tuple([0, getScreenDimensions()[1]]):
                self.getEyeCoords = True
                self.isMovementFinished = True
        elif hypot(point[0] - rectList[0], point[1] - rectList[1]) <= 5:
            self.isMovementFinished = True
        return None
