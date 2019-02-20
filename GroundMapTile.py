## GroundMapTile.py represents a ground tile on the TileGrid
## extends the MapTile class

import pygame
import random
from MapTile import MapTile

class GroundMapTile(MapTile):
    def __init__(self, Column, Row, MapType, Name = "Ground"):

        MapTile.__init__(self, Name, Column, Row)

        # depending on the current map, a random ground sprite is picked
        if MapType == "Forest":
            sprites = ["graphics/ForestLevel/blank.png",
                       "graphics/ForestLevel/grass1.png",
                       "graphics/ForestLevel/grass2.png",
                       "graphics/ForestLevel/grass3.png"]
        elif MapType == "Cave":
            sprites = ["graphics/CaveLevel/blank.png",
                       "graphics/CaveLevel/dirt1.png",
                       "graphics/CaveLevel/dirt2.png",
                       "graphics/CaveLevel/dirt3.png"]
        elif MapType == "Creepy":
            sprites = ["graphics/CreepyLevel/blank.png",
                       "graphics/CreepyLevel/ground1.png",
                       "graphics/CreepyLevel/ground2.png",
                       "graphics/CreepyLevel/ground3.png"]
        elif MapType == "House":
            sprites = ["graphics/HouseLevel/carpet1.png",
                       "graphics/HouseLevel/carpet2.png",
                       "graphics/HouseLevel/carpet3.png"]
        elif MapType == "Town":
            sprites = ["graphics/TownLevel/blank.png",
                       "graphics/TownLevel/sand1.png",
                       "graphics/TownLevel/sand2.png",
                       "graphics/TownLevel/sand3.png"]

        self.Sprite = pygame.image.load(random.choice(sprites))
