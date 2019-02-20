## PortalMapTile.py represents a portal tile on the TileGrid
## extends the MapTile class

import pygame
from MapTile import MapTile

class PortalMapTile(MapTile):
    def __init__(self, Column, Row, MapType, Name = "Portal"):

        MapTile.__init__(self, Name, Column, Row)

        # depending on the current map, a portal sprite is selected
        if MapType == "Forest":
            self.Sprite = pygame.image.load("graphics/ForestLevel/portal.png")
        elif MapType == "Cave":
            self.Sprite = pygame.image.load("graphics/CaveLevel/portal.png")
        elif MapType == "Creepy":
            self.Sprite = pygame.image.load("graphics/CreepyLevel/portal.png")
        elif MapType == "House":
            self.Sprite = pygame.image.load("graphics/HouseLevel/portal.png")
        elif MapType == "Town":
            self.Sprite = pygame.image.load("graphics/TownLevel/portal.png")

