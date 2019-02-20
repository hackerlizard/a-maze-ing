## DeathScreen.py shows the player information about their playthrough after the player runs out of hearts

import pygame
import Player
#from TitleScreen import TitleScreen

# screen initializations
pygame.init()                                 
Clock = pygame.time.Clock()
MapDim = 576
HudYDim = 192
Screen = pygame.display.set_mode([MapDim, MapDim+HudYDim])
BLACK = (0, 0, 0)
pygame.display.set_caption('A-MAZE-ING')
GameFont = pygame.font.Font("Pixeled.ttf", 30)

class DeathScreen():
    def __init__(self, Dude):
        
        deathScreen = pygame.image.load("graphics/deathscreen.png")
        self.Dude = Dude

        done = False

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        #TitleScreen()
                        done = True
                        
            if not done:                                                                 
                deathScreenRect = deathScreen.get_rect()
                deathScreenRect.x = 0
                deathScreenRect.y = 0
                
                Screen.fill(BLACK)
                Screen.blit(deathScreen, deathScreenRect)

                Screen.blit(GameFont.render("YOU DIED", 1, (232,245,224)), (190, 140))
                if self.Dude.NumLevelsBeaten == 1:
                    Screen.blit(GameFont.render(str(self.Dude.NumLevelsBeaten) + " LEVEL", 1, (161,207,138)), (190, 250))
                else:
                    Screen.blit(GameFont.render(str(self.Dude.NumLevelsBeaten) + " LEVELS", 1, (161,207,138)), (190, 250))
                Screen.blit(GameFont.render(str(self.Dude.TotalNumEnemiesDefeated) + " ENEMIES", 1, (161,207,138)), (190, 380))
                Screen.blit(GameFont.render(str(self.Dude.TotalEnergy) + " MAX ENERGY", 1, (161,207,138)), (190, 510))
                Screen.blit(GameFont.render("PRESS ENTER", 1, (232,245,224)), (130, 650))

                Clock.tick(60)
                
                pygame.display.flip()

        pygame.quit()
