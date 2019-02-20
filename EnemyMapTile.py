## EnemyMapTile.py represents an enemy on the TileGrid
## extends the MapTile class

import pygame
import random
from MapTile import MapTile

class EnemyMapTile(MapTile):
    def __init__(self, Column, Row, MapType, HP, Name = "Enemy"):

        MapTile.__init__(self, Name, Column, Row)

        # subtract 10 (10 added for display purposes)
        self.HP = HP - 10

        # depending on the current map, a random enemy sprite is picked
        if MapType == "Forest":
            enemyTypes = ["troll", "mouse", "wizard"]
            self.Type = random.choice(enemyTypes)
            spriteType = "graphics/ForestLevel/" + self.Type + ".png"
            
        elif MapType == "Cave":
            enemyTypes = ["goblin", "hand", "bones"]
            self.Type = random.choice(enemyTypes)
            spriteType = "graphics/CaveLevel/" + self.Type + ".png"
            
        elif MapType == "Creepy":
            enemyTypes = ["ghost", "moon", "shadow"]
            self.Type = random.choice(enemyTypes)
            spriteType = "graphics/CreepyLevel/" + self.Type + ".png"
            
        elif MapType == "House":
            enemyTypes = ["lilbro", "cat", "spidey"]
            self.Type = random.choice(enemyTypes)
            spriteType = "graphics/HouseLevel/" + self.Type + ".png"
            
        elif MapType == "Town":
            enemyTypes = ["knight", "mermaid", "pooch"]
            self.Type = random.choice(enemyTypes)
            spriteType = "graphics/TownLevel/" + self.Type + ".png"
            
        self.Sprite = pygame.image.load(spriteType)
