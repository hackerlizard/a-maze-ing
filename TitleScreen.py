## TitleScreen.py launches the game

import pygame
import CharacterSelectScreen

# screen initializations
pygame.init()                                 
Clock = pygame.time.Clock()
MapDim = 576
HudYDim = 192
Screen = pygame.display.set_mode([MapDim, MapDim+HudYDim])
BLACK = (0, 0, 0)
pygame.display.set_caption('A-MAZE-ING')
GameFont = pygame.font.Font("Pixeled.ttf", 30)

class TitleScreen():
    def __init__(self):
        titleScreen = pygame.image.load("graphics/titlescreen.png")
        titleScreenRect = titleScreen.get_rect()
        titleScreenRect.x = 0
        titleScreenRect.y = 0

        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        CharacterSelectScreen.CharacterSelectScreen()
                        done = True

            if not done:
                Screen.fill(BLACK)
                Screen.blit(titleScreen, titleScreenRect)
                Screen.blit(GameFont.render("PRESS ENTER", 1, (232,245,224)), (130, 510))

                Clock.tick(60)
                pygame.display.flip()

        pygame.quit()

go = TitleScreen()
