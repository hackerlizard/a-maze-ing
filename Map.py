## Map.py creates and manages the map for one level
## a new instance of this class is created for every new level

import pygame, copy, time
from random import shuffle, randrange, randint, choice
import Game, Player, MapTile, WallMapTile, GroundMapTile, EnemyMapTile, PortalMapTile, Hud, DeathScreen

# integer mapping to game elements
BLANK = 0
WALL = 1
ENERGY = 2
SOLVED_PATH = 3
PORTAL = 5
SECONDARY_PATH = 6
PRIMARY_PATH = 9

class Map():
    def __init__(self, TileGrid, MapSize, MapType, GameHud, Dude):

        self.GameHud = GameHud

        self.MapSize = MapSize
        self.MapType = MapType
        self.TileGrid = TileGrid
        self.PrimaryPath = []
        self.SecondaryPath = []

        # initialize the tile grid
        for Row in range(self.MapSize+1):
            self.TileGrid.append([])
            for Column in range(self.MapSize+1):
                self.TileGrid[Row].append(MapTile.MapTile("Blank", Column, Row))

        # initialize the player
        self.Dude = Dude

        # generate the level
        self.MazeArray = self.GenerateMaze()

        print(self.MazeArray)

        # generate the end point of the level
        self.GenerateEndPoint()

        # solve from player's initial position (always (1,1)) to the end point
        self.Solve(1,1)

        # highlight the primary path
        self.MarkPrimaryPath()

        # use primary path to make secondary path
        self.GenerateSecondaryPath()

        # distribute enemies and energy items
        self.DistributeItems()

        print(self.MazeArray)

        # use MazeArray to populate the tile grid
        self.PopulateTileGrid()

        # copy the original level for use when the player dies and resets
        self.OriginalMaze = [[0 for x in range(self.MapSize+1)] for y in range(self.MapSize+1)]
        for Row in range(self.MapSize+1):
            for Column in range(self.MapSize+1):
                self.OriginalMaze[Column][Row] = self.MazeArray[Column][Row]

    # updates the player
    def update(self):              
        for Column in range(self.MapSize):      
            for Row in range(self.MapSize):
                if self.TileGrid[Column][Row].Name == "Dude":
                    self.TileGrid[Column][Row] = self.Dude.SavedTile
                    self.Dude.SavedTile = self.Dude.NextTile
        self.TileGrid[int(self.Dude.Column)][int(self.Dude.Row)] = self.Dude

                    
    # moves the player
    def MovePlayer(self, Direction):

        if Direction == "UP":
            if self.Dude.Row > 0:                
                if self.CollisionCheck("UP") == False:
                    self.Dude.Row -= 1            

        elif Direction == "LEFT":
            if self.Dude.Column > 0:
                if self.CollisionCheck("LEFT") == False:
                    self.Dude.Column -= 1

        elif Direction == "RIGHT":
            if self.Dude.Column < self.MapSize-1:
                if self.CollisionCheck("RIGHT") == False:
                    self.Dude.Column += 1

        elif Direction == "DOWN":
            if self.Dude.Row < self.MapSize-1:
                if self.CollisionCheck("DOWN") == False:
                    self.Dude.Row += 1
        
        self.update()


    # initiates collision detection for a direction
    def CollisionCheck(self, Direction):
        if Direction == "UP":
            return self.CollisionAction(self.TileGrid[self.Dude.Column][self.Dude.Row-1])
        elif Direction == "LEFT":
            return self.CollisionAction(self.TileGrid[self.Dude.Column-1][self.Dude.Row])
        elif Direction == "RIGHT":
            return self.CollisionAction(self.TileGrid[self.Dude.Column+1][self.Dude.Row])
        elif Direction == "DOWN":
            return self.CollisionAction(self.TileGrid[self.Dude.Column][self.Dude.Row+1])
        return False


    # determines what to do upon collision
    def CollisionAction(self, Element):
        if Element.Name == "Wall":
            return True
        elif Element.Name == "Energy":
            self.GameHud.updateEmote("energy")
            self.GameHud.updateStatus("energy")
            self.Dude.AddEnergy()
            return False
        elif Element.Name == "Enemy":
            self.GameHud.updateEmote("enemy")
            self.GameHud.updateStatusEnemy(Element.Type, Element.HP)
            self.Dude.RemoveEnergyEnemy(Element.HP)
            if self.Dude.Energy <= 0:
                self.ResetPlayer()
                return True
            self.Dude.NumEnemiesDefeated = self.Dude.NumEnemiesDefeated + 1
            return False
        elif Element.Name == "Portal":
            self.GameHud.updateEmote("portal")
            self.GameHud.updateStatus("portal")
            self.Dude.NumLevelsBeaten = self.Dude.NumLevelsBeaten + 1
            self.Dude.TotalEnergy = self.Dude.TotalEnergy + 5
            self.Dude.Energy = self.Dude.TotalEnergy
            self.Dude.TotalNumEnemiesDefeated = self.Dude.TotalNumEnemiesDefeated + self.Dude.NumEnemiesDefeated
            self.Dude.NumEnemiesDefeated = 0
            self.Dude.Column = 1
            self.Dude.Row = 1
            self.Dude.NumHearts = 5
            levelTypes = ["Forest", "Cave", "Creepy", "House", "Town"]
            Game.Game(self.MapSize + 2, choice(levelTypes), self.Dude)
            return False
        elif Element.Name == "Blank" or Element.Name == "Ground":
            self.GameHud.updateEmote("walking")
            self.GameHud.updateStatus("walking")
            self.Dude.RemoveEnergy()
            self.Dude.NextTile = Element
            if self.Dude.Energy <= 0:
                self.ResetPlayer()
                return True
            return False


    # resets player when player runs out of energy
    def ResetPlayer(self):
        self.Dude.NumHearts = self.Dude.NumHearts - 1
        if (self.Dude.NumHearts < 0):
            DeathScreen.DeathScreen(self.Dude)
            return
        for Row in range(self.MapSize+1):
            for Column in range(self.MapSize+1):
                self.MazeArray[Column][Row] = self.OriginalMaze[Column][Row]
        self.PopulateTileGrid()
        
        self.MazeArray[self.Dude.Column][self.Dude.Row] = MapTile.MapTile("Blank", self.Dude.Column, self.Dude.Row)
        self.Dude.Column = 1
        self.Dude.Row = 1
        self.Dude.Energy = self.Dude.TotalEnergy

    # generates the end point for the level
    def GenerateEndPoint(self):

        notValid = True

        while notValid:
            randomCol = randint(self.MapSize / 2, self.MapSize)
            randomRow = randint(self.MapSize / 2, self.MapSize)
            if self.MazeArray[randomCol][randomRow] == 0:
                self.MazeArray[randomCol][randomRow] = 5
                notValid = False

                
    # generates the maze
    def GenerateMaze(self):
        maze = self.MakeMaze().strip().split('\n')

        ones = ['+', '|', '-']
        zeros = [' ']
        mazeArray = [] 

        for line in maze: 

                mazeLine = [] 
                for c in line: 
                        if (c in ones): mazeLine.append(1)
                        elif (c in zeros): mazeLine.append(0)
                
                mazeArray.append(mazeLine) 
                      
        return mazeArray


    # implemented from:
    # https://rosettacode.org/wiki/Maze_generation
    def MakeMaze(self):

        size = (int)(self.MapSize/2)

        vis = [[0] * size + [1] for _ in range(size)] + [[1] * (size + 1)]
        ver = [["| "] * size + ['|'] for _ in range(size)] + [[]]
        hor = [["+-"] * size + ['+'] for _ in range(size + 1)]

        def walk(x, y):
            vis[y][x] = 1

            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
               if vis[yy][xx]: continue
               if xx == x: hor[max(y, yy)][x] = "+ "
               if yy == y: ver[y][max(x, xx)] = "  "
               walk(xx, yy)

        walk(randrange(size), randrange(size))

        s = ""
        for (a, b) in zip(hor, ver):
            s += ''.join(a + ['\n'] + b + ['\n'])
        return s


    # implemented from:
    # https://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/
    def Solve(self, x, y):

        if self.MazeArray[x][y] == PORTAL:
            return True
        elif self.MazeArray[x][y] == WALL:
            return False
        elif self.MazeArray[x][y] == SOLVED_PATH:
            return False
     
        self.PrimaryPath.append((x, y))
 
        # mark as visited
        self.MazeArray[x][y] = SOLVED_PATH
 
        # explore neighbors clockwise starting by the one on the right
        if ((x < len(self.MazeArray)-1 and self.Solve(x+1, y))
            or (y > 0 and self.Solve(x, y-1))
            or (x > 0 and self.Solve(x-1, y))
            or (y < len(self.MazeArray)-1 and self.Solve(x, y+1))):
            return True

        self.PrimaryPath.pop()
        
        return False


    # generates the secondary path
    def GenerateSecondaryPath(self):
        for coordinates in self.PrimaryPath:
            self.SecondaryPath.append(coordinates)
            numStepsToTake = 5
            numStepsTaken = self.GenerateBranch(0, coordinates, numStepsToTake)
            if numStepsTaken != 0:
                for listIndex in range (len(self.SecondaryPath) - 2, (len(self.SecondaryPath) - numStepsTaken) - 2, -1):
                    self.SecondaryPath.append(self.SecondaryPath[listIndex])

            
    # generates a branch for the secondary path
    def GenerateBranch(self, numStepsTaken, coordinates, numStepsToTake):
        if numStepsTaken == numStepsToTake:
            return numStepsTaken
        # N
        if self.MazeArray[coordinates[0] + 1][coordinates[1]] == BLANK or self.MazeArray[coordinates[0] + 1][coordinates[1]] == SOLVED_PATH:
            self.SecondaryPath.append((coordinates[0] + 1, coordinates[1]))
            self.MazeArray[coordinates[0] + 1][coordinates[1]] = SECONDARY_PATH
            numStepsTaken = self.GenerateBranch(numStepsTaken + 1, (coordinates[0] + 1, coordinates[1]), numStepsToTake)
        # E                                                             
        elif self.MazeArray[coordinates[0]][coordinates[1] + 1] == BLANK or self.MazeArray[coordinates[0]][coordinates[1] + 1] == SOLVED_PATH:
            self.SecondaryPath.append((coordinates[0], coordinates[1] + 1))
            self.MazeArray[coordinates[0]][coordinates[1] + 1] = SECONDARY_PATH
            numStepsTaken = self.GenerateBranch(numStepsTaken + 1, (coordinates[0], coordinates[1] + 1), numStepsToTake)
        # S                                     
        elif self.MazeArray[coordinates[0] - 1][coordinates[1]] == BLANK or self.MazeArray[coordinates[0] - 1][coordinates[1]] == SOLVED_PATH:
            self.SecondaryPath.append((coordinates[0] - 1, coordinates[1]))
            self.MazeArray[coordinates[0] - 1][coordinates[1]] = SECONDARY_PATH
            numStepsTaken = self.GenerateBranch(numStepsTaken + 1, (coordinates[0] - 1, coordinates[1]), numStepsToTake)
        # W                                     
        elif self.MazeArray[coordinates[0]][coordinates[1] - 1] == BLANK or self.MazeArray[coordinates[0]][coordinates[1] - 1] == SOLVED_PATH:
            self.SecondaryPath.append((coordinates[0], coordinates[1] - 1))
            self.MazeArray[coordinates[0]][coordinates[1] - 1] = SECONDARY_PATH
            numStepsTaken = self.GenerateBranch(numStepsTaken + 1, (coordinates[0], coordinates[1] - 1), numStepsToTake)
            
        return numStepsTaken


    # distribute enemies and energy items                                       
    def DistributeItems(self):

        numEnergyUsed = 0
        for coordinates in self.SecondaryPath:
            enemyNum = randint(0, 5)
            # if roll a 5, try to place enemy
            if enemyNum == 5:
                enemyHP = randint(1, 3)
                if enemyHP < (self.Dude.TotalEnergy - numEnergyUsed):
                    self.MazeArray[coordinates[0]][coordinates[1]] = enemyHP + 10
                    numEnergyUsed = numEnergyUsed + enemyHP
                elif numEnergyUsed == self.Dude.TotalEnergy:
                    self.MazeArray[coordinates[0]][coordinates[1]] = ENERGY
                    numEnergyUsed = numEnergyUsed - 10
                else:
                    numEnergyUsed = numEnergyUsed + 1
            elif numEnergyUsed == self.Dude.TotalEnergy:
                self.MazeArray[coordinates[0]][coordinates[1]] = ENERGY
                numEnergyUsed = numEnergyUsed - 10
            else:
                numEnergyUsed = numEnergyUsed + 1

                
    # highlight the primary path
    def MarkPrimaryPath(self):
        for coordinates in self.PrimaryPath:
            self.MazeArray[coordinates[0]][coordinates[1]] = PRIMARY_PATH


    # translate array to TileGrid array
    def PopulateTileGrid(self):
        for Row in range(len(self.MazeArray)):
                for Column in range(len(self.MazeArray)):
                    if self.MazeArray[Row][Column] == WALL:
                        TempTile = WallMapTile.WallMapTile(Column, Row, self.MapType)
                    elif self.MazeArray[Row][Column] == ENERGY:
                        TempTile = MapTile.MapTile("Energy", Column, Row)
                    elif self.MazeArray[Row][Column] == SOLVED_PATH or self.MazeArray[Row][Column] == PRIMARY_PATH or self.MazeArray[Row][Column] == BLANK or self.MazeArray[Row][Column] == SECONDARY_PATH:
                        TempTile = GroundMapTile.GroundMapTile(Column, Row, self.MapType)
                    elif self.MazeArray[Row][Column] == PORTAL:
                        TempTile = PortalMapTile.PortalMapTile(Column, Row, self.MapType)
                    elif self.MazeArray[Row][Column] > 10:
                        TempTile = EnemyMapTile.EnemyMapTile(Column, Row, self.MapType, self.MazeArray[Row][Column])
                    self.TileGrid[Column][Row] = TempTile
        

