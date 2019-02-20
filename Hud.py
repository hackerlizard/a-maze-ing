import pygame, sys
import Player

pygame.init()

GameFont = pygame.font.Font("Pixeled.ttf", 30)
MaxStatusChars = 13

class Hud(pygame.sprite.Sprite):
    
    def __init__(self):
        
        self.playerStatus = GameFont.render("WALKING.....", 1, (232,245,224))
        self.Emote = pygame.image.load("graphics/HUD/emote_walking.png")
        

    def draw(self, screen, Player):
        self.playerEnergy = GameFont.render(str(Player.Energy), 1, (232,245,224))
        self.totalPlayerEnergy = GameFont.render("/" + str(Player.TotalEnergy), 1, (232,245,224))
       
        for hudRow in range(0, 2):
                for hudCol in range(0, 6):
                    sprite = pygame.image.load("graphics/HUD/border" +  str(hudRow) + str(hudCol) + ".png")
                    spriterect = sprite.get_rect()

                    spriterect.x = 96 * hudCol
                    spriterect.y = 576 + (96 * hudRow)
                    
                    screen.blit(sprite, spriterect)
                    
        screen.blit(self.playerEnergy, (50, 590))
        screen.blit(self.totalPlayerEnergy, (110, 600))
        screen.blit(self.playerStatus, (250, 670))

        emoteSpriteRect = self.Emote.get_rect()
        emoteSpriteRect.x = 450
        emoteSpriteRect.y = 600
        screen.blit(self.Emote, emoteSpriteRect)

        fraction = (Player.Energy/Player.TotalEnergy) * 99.9

        numBar = 0

        counter = 0
        for bracket in range(1, 16):
            rangeNum = 6.66 * bracket
            if fraction >= rangeNum - 6.66 and fraction <= rangeNum:
                numBar = bracket

        #print(numBar)
        barSprite = pygame.image.load("graphics/HUD/bar/" +  str(numBar) + ".png")

##        if Player.Energy > 15:
##            barSprite = pygame.image.load("graphics/HUD/bar/15.png")
##        elif Player.Energy < 0:
##            barSprite = pygame.image.load("graphics/HUD/bar/0.png")
##        else:
##            barSprite = pygame.image.load("graphics/HUD/bar/" +  str(Player.Energy) + ".png")
            
        barSpriteRect = barSprite.get_rect()
        barSpriteRect.x = 20
        barSpriteRect.y = 675
        screen.blit(barSprite, barSpriteRect)

##        heartSprite = pygame.image.load("graphics/HUD/powerups/heart" +  str(Player.NumHearts) + ".png")
##        heartSpriteRect = heartSprite.get_rect()
##        heartSpriteRect.x = 240
##        heartSpriteRect.y = 600
##        screen.blit(heartSprite, heartSpriteRect)
##        starSprite = pygame.image.load("graphics/HUD/powerups/star" +  str(Player.NumStars) + ".png")
##        starSpriteRect = heartSprite.get_rect()
##        starSpriteRect.x = 290
##        starSpriteRect.y = 600
##        screen.blit(starSprite, starSpriteRect)
##        arrowSprite = pygame.image.load("graphics/HUD/powerups/arrow" +  str(Player.NumArrows) + ".png")
##        arrowSpriteRect = arrowSprite.get_rect()
##        arrowSpriteRect.x = 340
##        arrowSpriteRect.y = 600
##        screen.blit(arrowSprite, arrowSpriteRect)

        heartSprite = pygame.image.load("graphics/HUD/hearts/" +  str(Player.NumHearts) + ".png")
        heartSpriteRect = heartSprite.get_rect()
        heartSpriteRect.x = 240
        heartSpriteRect.y = 620
        screen.blit(heartSprite, heartSpriteRect)

    def updateHearts(self, event):
        heartSprite = pygame.image.load("graphics/HUD/hearts/" +  str(Player.NumHearts) + ".png")
        heartSpriteRect = heartSprite.get_rect()
        heartSpriteRect.x = 240
        heartSpriteRect.y = 600
        screen.blit(heartSprite, heartSpriteRect)

    def updateEmote(self, event):
        if event == "energy":
            self.Emote = pygame.image.load("graphics/HUD/emote_energy.png")
        elif event == "walking":
            self.Emote = pygame.image.load("graphics/HUD/emote_walking.png")
        elif event == "enemy":
            self.Emote = pygame.image.load("graphics/HUD/emote_enemy.png")
        elif event == "portal":
            self.Emote = pygame.image.load("graphics/HUD/emote_portal.png")
        elif event == "death":
            self.Emote = pygame.image.load("graphics/HUD/emote_death.png")

    def updateStatus(self, event):
        if event == "energy":
            self.playerStatus = GameFont.render("+ENERGY!", 1, (232,245,224))
        elif event == "walking":
            self.playerStatus = GameFont.render("WALKING......", 1, (232,245,224))
        elif event == "portal":
            self.playerStatus = GameFont.render("PORTAL!!!", 1, (232,245,224))
        elif event == "death":
            self.playerStatus = GameFont.render("YOU DIED", 1, (232,245,224))

    def updateStatusEnemy(self, EnemyType, EnemyHP):
        self.playerStatus = GameFont.render(EnemyType.upper() + " " + str(EnemyHP) + "HP", 1, (232,245,224))
