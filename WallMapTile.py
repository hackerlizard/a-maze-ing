## WallMapTile.py represents a wall tile on the TileGrid
## extends the MapTile class

import pygame
import random
from MapTile import MapTile

class WallMapTile(MapTile):
    def __init__(self, Column, Row, MapType, Name = "Wall"):

        MapTile.__init__(self, Name, Column, Row)

        # depending on the current map, a random wall sprite is picked
        if MapType == "Forest":
            sprites = ["graphics/ForestLevel/tree1.png",
                       "graphics/ForestLevel/pinetree1.png",
                       "graphics/ForestLevel/rocks1.png"]
        elif MapType == "Cave":
            sprites = ["graphics/CaveLevel/rockwall1.png",
                       "graphics/CaveLevel/rockwall2.png",
                       "graphics/CaveLevel/rockwall3.png",
                       "graphics/CaveLevel/fire.png"]
        elif MapType == "Creepy":
            sprites = ["graphics/CreepyLevel/tree2.png",
                       "graphics/CreepyLevel/pinetree2.png",
                       "graphics/CreepyLevel/rocks2.png"]
        elif MapType == "House":
            sprites = ["graphics/HouseLevel/wall1.png",
                       "graphics/HouseLevel/wall2.png",
                       "graphics/HouseLevel/wall1.png",
                       "graphics/HouseLevel/wall2.png",
                       "graphics/HouseLevel/bookshelf.png"]
        elif MapType == "Town":
            sprites = ["graphics/TownLevel/castle.png",
                       "graphics/TownLevel/house.png",
                       "graphics/TownLevel/house.png",
                       "graphics/TownLevel/tree3.png",
                       "graphics/TownLevel/tree3.png",
                       "graphics/TownLevel/tree3.png"]

        self.Sprite = pygame.image.load(random.choice(sprites))
