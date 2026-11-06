import pygame
from spacing import *

pygame.init()

REALWIDTH = 20
REALHEIGHT = 15

MULTIPLIER = 40

SCREENWIDTH = REALWIDTH*MULTIPLIER
SCREENHEIGHT = REALHEIGHT*MULTIPLIER

rect = RectPhysical(1,1,2,4)

otherthing = Physical(0,0)

screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))

font = pygame.font.SysFont('Arial', 36)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    mousex,mousey = pygame.mouse.get_pos()
    otherthing.x = (mousex-SCREENWIDTH/2)/MULTIPLIER
    otherthing.y = (mousey-SCREENHEIGHT/2)/MULTIPLIER
    screen.fill(255)
    apx = rect.x + REALWIDTH / 2
    apy = rect.y + REALHEIGHT / 2
    pygame.draw.rect(screen, "black",
                     (apx * MULTIPLIER, apy * MULTIPLIER, rect.w * MULTIPLIER, rect.h * MULTIPLIER),
                     2)
    pygame.draw.circle(screen, "black",(otherthing.x,otherthing.y), 2)

    text_surface = font.render(str(rect.dist(otherthing)), True, (255, 255, 255))
    screen.blit(text_surface, (100, 200))

    pygame.display.flip()
