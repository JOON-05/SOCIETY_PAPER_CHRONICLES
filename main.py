import pygame
import sys
# bridgerton regency theme
COLOR_CREAM = (247, 244, 234)       #parchment background
COLOR_GOLD = (212, 175, 55)         #accents, borders, and wax seals
COLOR_CHARCOAL = (44, 44, 44)       #high-readability serif text color
COLOR_DUCK_EGG = (202, 218, 224)    #secondary button / highlight color

# INITIALIZATION & DISPLAY SETUP
pygame.init()

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Society Paper Chronicles📜")

clock = pygame.time.Clock()
FPS = 60

# MAIN GAME LOOP (STATE MACHINE ELEMENT)

running = True
while running:
    #user interaction 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #UI Layout Layer
    screen.fill(COLOR_CREAM) #clean movement
    
    #drawing a thin, elegant gold border around the entire window edge
    border_margin = 15
    pygame.draw.rect(
        screen, 
        COLOR_GOLD, 
        (border_margin, border_margin, SCREEN_WIDTH - (border_margin * 2), SCREEN_HEIGHT - (border_margin * 2)), 
        2
    )

    #Double-Buffering Refresh
    pygame.display.flip() #flips the images on the monitor
    clock.tick(FPS) #limits the frames per sec

#exit from system memory
pygame.quit()
sys.exit()