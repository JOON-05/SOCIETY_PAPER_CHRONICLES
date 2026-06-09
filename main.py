import pygame
import sys
# bridgerton regency theme
COLOR_CREAM = (247, 244, 234)       #parchment background
COLOR_GOLD = (212, 175, 55)         #accents, borders, and wax seals
COLOR_CHARCOAL = (44, 44, 44)       #high-readability serif text color
COLOR_DUCK_EGG = (202, 218, 224)    #secondary button/ highlight color
COLOR_WAX_RED = (141, 30,31)       #crimson-brick red for the wax seals
COLOR_WHITE = (255,255,255)        #for the dialogue card background

# INITIALIZATION & DISPLAY SETUP
pygame.init()
pygame.font.init() #initialising the typography engine

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Society Paper Chronicles📜")

clock = pygame.time.Clock()
FPS = 60

#TYPOGRAPHY
font_title= pygame.font.SysFont("georgia", 25, bold=True)
font_body= pygame.font.SysFont("georgia", 18, italic=True)

#NARRATIVE STATE MACHINE DATA
#structured matrix holding the sequential flow of story script
story_script= [
    {"speaker": "Lady Whistledown", "text": "\"Dearest gentle reader, the town is abuzz with the latest scandal...\""},
    {"speaker": "Lady Whistledown", "text": "\"It appears a certain Duke was spotted walking alone in the gardens.\""},
    {"speaker": "Lord Anthony", "text": "\"A proper gentleman never whispers secrets in the ballroom.\""},
    {"speaker": "Lady Whistledown", "text": "\"But of course, this author always finds a way to hear them.\""}
    ]
current_story_index=0

#tracking variable for the interactive button area
dialogue_rect = pygame.Rect(0, 0, 0, 0)

#reusable UI components
def draw_dialogue_box(speaker, text):
    """Draws a refined, high- society parchment text box with proper layout nesting."""
    global dialogue_rect

    box_width= 760
    box_height= 140
    box_x= (SCREEN_WIDTH -  box_width)//2   #mathematically centre horizontally
    box_y= SCREEN_HEIGHT - box_height - 50  #position at lower quadrant

    dialogue_rect= pygame.Rect(box_x, box_y, box_width, box_height)

# 1.subtle soft shadow
    shadow_rect= pygame.Rect(box_x + 2, box_y + 2, box_width, box_height)
    pygame.draw.rect(screen, (220, 215, 200), shadow_rect)  #soft warm greyish shadow

# 2.main dialogue card
    pygame.draw.rect(screen, COLOR_WHITE, dialogue_rect)

# 3.double thin accent border
#        outer crimson border
    pygame.draw.rect(screen, COLOR_WAX_RED, dialogue_rect, 2)
#        inner decorative thin gold border
    inner_rect= pygame.Rect(box_x + 4, box_y + 4, box_width - 8, box_height - 8)
    pygame.draw.rect(screen, COLOR_GOLD, inner_rect, 1)

# 4.typography Layout (With distinct, intentional padding offsets)
    speaker_surface = font_title.render(speaker, True, COLOR_WAX_RED)
    text_surface = font_body.render(text, True, COLOR_CHARCOAL)

#stamping typography
    screen.blit(speaker_surface, (box_x + 35, box_y + 20))
    screen.blit(text_surface, (box_x + 35, box_y + 65))
    #render layout elements ( DROP_SHADOW+ MAIN CARD+ CRIMSON ACCENT BORDER)
    #pygame.draw.rect(screen, COLOR_CHARCOAL, (box_x + 4, box_y + 4, box_width, box_height))
    #pygame.draw.rect(screen, COLOR_WHITE, dialogue_rect)
    #pygame.draw.rect(screen, COLOR_WAX_RED, dialogue_rect, 2)

    #render typography strings
    #speaker_surface= font_title.render(speaker, True, COLOR_WAX_RED)
    #text_surface= font_body.render(text,True, COLOR_CHARCOAL)

    # BLOCK IMAGE TRANSFER (BLIT) SURFACES ONTO SCREEN COORDINATES
    #screen.blit(speaker_surface, (box_x + 35, box_y + 25))
    #screen.blit(text_surface, (box_x + 35, box_y + 75))
    

# MAIN GAME LOOP (STATE MACHINE ELEMENT)

running = True
while running:
    # 1.user interaction 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        #detect left mouse clicks to interact with narrative script state
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 1= left click
                mouse_pos= event.pos

                # check if the player click occured inside our defined container area
                if dialogue_rect.collidepoint(mouse_pos):
                    if current_story_index< len(story_script) - 1:
                        current_story_index += 1
                    else:
                        print("End of the current society chronicle preview!")

    # 2.UI Layout Layer
    screen.fill(COLOR_CREAM) #clean movement
    
    #drawing a thin, elegant gold border around the entire window edge
    border_margin = 15
    pygame.draw.rect(
        screen, 
        COLOR_GOLD, 
        (border_margin, border_margin, SCREEN_WIDTH - (border_margin * 2), SCREEN_HEIGHT - (border_margin * 2)), 
        2
    )
    # dynamic UI component insertion: fetch current dialogue state values
    current_scene = story_script[current_story_index]
    draw_dialogue_box(current_scene["speaker"], current_scene["text"])

    #Double-Buffering Refresh
    pygame.display.flip() #flips the images on the monitor
    clock.tick(FPS) #limits the frames per sec

#exit from system memory
pygame.quit()
sys.exit()