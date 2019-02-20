## CharacterSelectScreen.py lets the player pick a character

import pygame
import Game, Player

# screen initializations
pygame.init()                                 
Clock = pygame.time.Clock()
MapDim = 576
HudYDim = 192
Screen = pygame.display.set_mode([MapDim, MapDim+HudYDim])
BLACK = (0, 0, 0)
pygame.display.set_caption('A-MAZE-ING')
GameFont = pygame.font.Font("Pixeled.ttf", 30)

class CharacterSelectScreen():
    def __init__(self):
        
        characterSelectScreen = pygame.image.load("graphics/player1selected.png")

        currentPlayerSelected = 1

        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and currentPlayerSelected == 1:
                        currentPlayerSelected = 2
                        characterSelectScreen = pygame.image.load("graphics/player2selected.png")
                    elif event.key == pygame.K_LEFT and currentPlayerSelected == 2:
                        currentPlayerSelected = 1
                        characterSelectScreen = pygame.image.load("graphics/player1selected.png")
                    if event.key == pygame.K_RETURN:
                        Dude = Player.Player("Dude", currentPlayerSelected, 1, 1, 15)
                        Game.Game(20, "Forest", Dude)
                        done = True
                        
            if not done:                                                                 
                characterSelectScreenRect = characterSelectScreen.get_rect()
                characterSelectScreenRect.x = 0
                characterSelectScreenRect.y = 0
                
                Screen.fill(BLACK)
                Screen.blit(characterSelectScreen, characterSelectScreenRect)

                Screen.blit(GameFont.render("CHOOSE YOUR PLAYER", 1, (232,245,224)), (35, 120))
                Screen.blit(GameFont.render("PRESS ENTER", 1, (232,245,224)), (130, 510))

                Clock.tick(60)
                
                pygame.display.flip()

        pygame.quit()
