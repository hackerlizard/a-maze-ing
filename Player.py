## Player.py represents the player
## extends the MapTile class

import pygame
import MapTile

STATIC_ENERGY = 10

class Player:                    
    def __init__(self, Name, PlayerSelected, Column, Row, Energy):
        MapTile.MapTile.__init__(self, Name, Column, Row)
        self.TotalEnergy = Energy
        self.Energy = Energy

        # two different types of character sprites
        if PlayerSelected == 1:
            self.Sprite1 = pygame.image.load("graphics/player1_1.png")
            self.Sprite2 = pygame.image.load("graphics/player1_2.png")
        elif PlayerSelected == 2:
            self.Sprite1 = pygame.image.load("graphics/player2_1.png")
            self.Sprite2 = pygame.image.load("graphics/player2_2.png")

        # the tiles that will be drawn under the player as the player moves
        self.SavedTile = MapTile.MapTile("Blank", Column, Row)
        self.NextTile = MapTile.MapTile("Blank", Column, Row)

        # counters for stats and death screen
        self.NumEnemiesDefeated = 0
        self.TotalNumEnemiesDefeated = 0
        self.NumLevelsBeaten = 0

        # the player has 5 attempts to beat each level
        self.NumHearts = 5

    # STATIC_ENERGY amount of energy added when energy item picked up
    def AddEnergy(self):
        if self.Energy + STATIC_ENERGY > self.TotalEnergy:
            self.Energy = self.TotalEnergy
        else:
            self.Energy = self.Energy + STATIC_ENERGY

    # 1 energy removed with each step
    def RemoveEnergy(self):
        self.Energy = self.Energy - 1

    # removes the # of HP that the enemy had
    def RemoveEnergyEnemy(self, howMuch):
        self.Energy = self.Energy - howMuch
