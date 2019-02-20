# Game.py contains the main game loop
# a new instance of this class is created for every new level

import pygame
import Player, Map, Hud

# screen initializations
pygame.init()                                 
Clock = pygame.time.Clock()
MapDim = 576
HudYDim = 192
Screen = pygame.display.set_mode([MapDim, MapDim+HudYDim])                                                                 
BLACK = (0, 0, 0)
pygame.display.set_caption('A-MAZE-ING')

VisibleArea = 6    # gives the player a 6x6 view of the current grid
TileSize = MapDim/VisibleArea

class Game():
    def __init__(self, MapSize, MapType, Dude):
        TileGrid = []   # contains MapTile objects representing the level

        GameHud = Hud.Hud()
        GameMap = Map.Map(TileGrid, MapSize, MapType, GameHud, Dude)

        frameCount = 0   # for use in idle sprite animation

        Done = False 

        # main game loop
        while not Done:

            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    Done = True       

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        GameMap.MovePlayer("LEFT")
                    if event.key == pygame.K_RIGHT:
                        GameMap.MovePlayer("RIGHT")
                    if event.key == pygame.K_UP:
                        GameMap.MovePlayer("UP")
                    if event.key == pygame.K_DOWN:
                        GameMap.MovePlayer("DOWN")

            Screen.fill(BLACK)

            # zoomed in scrolling camera effect
            startRowBoundary = GameMap.Dude.Row - 2
            startColumnBoundary = GameMap.Dude.Column - 2

            if startRowBoundary < 0:
                startRowBoundary = 0
            if startColumnBoundary < 0:
                startColumnBoundary = 0

            endRowBoundary = startRowBoundary + (VisibleArea - 1)
            endColumnBoundary = startColumnBoundary + (VisibleArea - 1)

            if endRowBoundary > MapSize:
                endRowBoundary = MapSize
            if endColumnBoundary > MapSize:
                endColumnBoundary = MapSize

            startRowBoundary = endRowBoundary - (VisibleArea - 1)
            startColumnBoundary = endColumnBoundary - (VisibleArea - 1)

            rowCount = 0
            colCount = 0

            # draws the sprite for each tile on the screen
            for Row in range(startRowBoundary, endRowBoundary+1):
                colCount = 0
                for Column in range(startColumnBoundary, endColumnBoundary+1):
                    sprite = pygame.image.load("graphics/ForestLevel/blank.png")
                    spriterect = sprite.get_rect()
                    
                    if GameMap.TileGrid[Column][Row].Name == "Wall":
                        sprite = GameMap.TileGrid[Column][Row].Sprite
                        
                    if GameMap.TileGrid[Column][Row].Name == "Dude":
                        if frameCount < 15:
                            sprite = GameMap.TileGrid[Column][Row].Sprite1
                        else:
                            sprite = GameMap.TileGrid[Column][Row].Sprite2
                        
                    if GameMap.TileGrid[Column][Row].Name == "Energy":
                        sprite = pygame.image.load("graphics/energy.png")
                        
                    if GameMap.TileGrid[Column][Row].Name == "Ground":
                        sprite = GameMap.TileGrid[Column][Row].Sprite

                    if GameMap.TileGrid[Column][Row].Name == "Enemy":
                        sprite = GameMap.TileGrid[Column][Row].Sprite

                    if GameMap.TileGrid[Column][Row].Name == "Portal":
                        sprite = GameMap.TileGrid[Column][Row].Sprite

                    spriterect = sprite.get_rect()
                    spriterect.x = TileSize * colCount
                    spriterect.y = TileSize * rowCount
                    Screen.blit(sprite, spriterect)
                    
                    colCount = colCount + 1
                rowCount = rowCount + 1
                    
            GameHud.draw(Screen, GameMap.Dude)
            
            frameCount = frameCount + 1
            if frameCount == 30:
                frameCount = 0

            Clock.tick(30)

            pygame.display.flip()
            GameMap.update()

        pygame.quit()
        
