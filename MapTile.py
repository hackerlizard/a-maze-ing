## MapTile.py is the parent class for all classes that extend MapTile

import pygame

class MapTile:
    def __init__(self, Name, Column, Row):
        self.Name = Name
        self.Column = Column
        self.Row = Row
