import pygame
import sys
# bridgerton regency theme
COLOR_CREAM = (247, 244, 234)       #parchment background
COLOR_GOLD = (212, 175, 55)         #accents, borders
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
font_ui= pygame.font.SysFont("georgia", 14, bold=True)

#ENGINE STATES
STATE_PROLOGUE= "PROLOGUE"
STATE_CHAR_SELECT= "CHAR_SELECT"
STATE_MAIN_STORY= "MAIN_STORY"
current_state= STATE_PROLOGUE

#PLAYER SELECTION
player_archetype= None
character_buttons={}
character_images={}

def load_character_assets():
    """Loads and scales the painted sibling potraits to fit selection cards."""
    global character_images
    siblings=["Anthony", "Benedict", "Colin", "Daphne", "Eloise"]
    card_width, card_height= 140, 220
    for name in siblings:
        try:
            raw_img=pygame.image.load(f"assets/{name}.jpg")
            scaled_img= pygame.transform.smoothscale(raw_img, (card_width, card_height))
            character_images[name]=scaled_img
        except pygame.error:
            fallback= pygame.Surface(( card_width, card_height))
            fallback.fill((230, 222, 208))
            character_images[name] = fallback
#load image arrays right before execution loop
load_character_assets()


#NARRATIVE STATE MACHINE DATA
#structured matrix holding the sequential flow of story script
prolouge_script= [
    {"speaker": "Lady Whistledown", "text": ["\"Dearest gentle reader, the town is abuzz with the"," most scandalous news of the season...\""]},
    {"speaker": "Lady Whistledown", "text": ["\"It appears, the historic, priceless Featherington"," Emaralds have vanished from under her ladyship's very nose.\""]},
    {"speaker": "Lady Whistledown", "text": ["\"With the Queen threatening to cancel the Social season,"," a hero must step forward. However it is to see who"," will take up the mantle?\""]},
    
    ]
act_1_script= [
    {
        "speaker": "The Bridgerton Drawing Room",
        "text": {
            "Anthony":[ 
               "Pacing the floor, voice cutting like ice,", 
               "'This theft threatens our family honor. We must fix this.'"],
            "Benedict":[ 
               "Leaning against the mantle, pouring a drink,", "'Well... at least the Featherington balls won't be boring now.'"],
            "Colin":[ 
               "Gazing out the window thoughtfully,", 
               "'To lose something so vital...the desperation must have been immense.'"],
            "Daphne":[ 
               "Maintaining a flawless, composed posture, masking her worry,", 
               "'We must assist Lady Featherington calmly.'"],
            "Eloise":[ 
               "Slamming her book shut with a triumphant grin,", 
               "'A real mystery! Finally, something worth investigating!'"]
        }
    }
]
current_story_index=0

#tracking variable for the interactive button area
dialogue_rect = pygame.Rect(0, 0, 0, 0)

#reusable UI components
def draw_dialogue_box(speaker, text_lines):
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
    screen.blit(speaker_surface, (box_x + 35, box_y + 20))

    if isinstance(text_lines, str):
        text_lines = [text_lines]
        
    line_y_offset = 65
    for line in text_lines:
        text_surface = font_body.render(line, True, COLOR_CHARCOAL)
        screen.blit(text_surface, (box_x + 35, box_y + line_y_offset))
        line_y_offset += 25      #moving the next line down slightly

#stamping typography
    #screen.blit(speaker_surface, (box_x + 35, box_y + 20))   #otherwise causes overlapping
    #screen.blit(text_surface, (box_x + 35, box_y + 65))
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
def draw_character_selection():
    """Renders 5 interactive picture frames carrying the painted sibling potraits."""
    global character_buttons
    title_surface= font_title.render("Choose Your Perspective for the Season", True, COLOR_WAX_RED)
    screen.blit(title_surface, (SCREEN_WIDTH // 2 - title_surface.get_width() // 2, 50))

    siblings= ["Anthony", "Benedict", "Colin", "Daphne", "Eloise"]
    card_width, card_height = 140, 220
    start_x = (SCREEN_WIDTH - (5 * card_width + 4 * 20)) // 2
    card_y = 150
    for i, name in enumerate(siblings):
        cx = start_x + i * (card_width + 20)
        card_rect = pygame.Rect(cx, card_y, card_width, card_height)
        character_buttons[name] = card_rect
        
        # 1.soft card shadow block
        pygame.draw.rect(screen, (220, 215, 200), (cx + 3, card_y + 3, card_width, card_height))
        
        # 2.render painted portrait image blit
        screen.blit(character_images[name], (cx, card_y))
        
        # 3.outer regal gold picture framing accent over image
        pygame.draw.rect(screen, COLOR_GOLD, card_rect, 3)
        pygame.draw.rect(screen, COLOR_WAX_RED, (cx + 3, card_y + 3, card_width - 6, card_height - 6), 1)
        
        # 4.bottom identity tag text
        name_surf = font_ui.render(name, True, COLOR_CHARCOAL)
        screen.blit(name_surf, (cx + card_width // 2 - name_surf.get_width() // 2, card_y + card_height + 10))

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

                #INTERACTION STATE: COMMON PROLOGUE
                if current_state == STATE_PROLOGUE:
                        if current_story_index < len(prolouge_script)- 1:
                            current_story_index +=1
                        else:
                            #common prologue ends here. next to character select grid
                            current_state = STATE_CHAR_SELECT
                            current_story_index = 0


                # INTERACTION STATE: CHARACTER SELECTION CARD GRID
                elif current_state == STATE_CHAR_SELECT:
                    for sibling_key, rect_zone in character_buttons.items():
                        if rect_zone.collidepoint(mouse_pos):
                            player_archetype = sibling_key
                            current_state = STATE_MAIN_STORY
                            current_story_index = 0
                            print(f"[SYSTEM] Perspective locked to: {player_archetype}")


                ## INTERACTION STATE : BRANCHED MAIN STORY
                elif current_state == STATE_MAIN_STORY:
                    if dialogue_rect.collidepoint(mouse_pos):
                        if current_story_index < len(act_1_script) - 1:
                            current_story_index += 1
                        else:
                            print("End of the current society chronicle preview!")
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # reset shortcut to step back through game flow
                    current_state = STATE_PROLOGUE
                    current_story_index = 0
                    player_archetype = None   


                # check if the player click occured inside our defined container area
                #if dialogue_rect.collidepoint(mouse_pos):
                    #if current_story_index< len(story_script) - 1:
                        #current_story_index += 1
                    #else:
                        #print("End of the current society chronicle preview!")

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
## RENDERING ROUTER 
    if current_state == STATE_PROLOGUE:
        current_scene = prolouge_script[current_story_index]
        draw_dialogue_box(current_scene["speaker"], current_scene["text"])
        
    elif current_state == STATE_CHAR_SELECT:
        draw_character_selection()
        
    elif current_state == STATE_MAIN_STORY:
        current_scene = act_1_script[current_story_index]
        # Dynamically pulls unique line matching your selected character key variable
        dynamic_text = current_scene["text"][player_archetype]
        draw_dialogue_box(current_scene["speaker"], dynamic_text)
    # dynamic UI component insertion: fetch current dialogue state values
    #current_scene = story_script[current_story_index]
    #draw_dialogue_box(current_scene["speaker"], current_scene["text"])

    #Double-Buffering Refresh
    pygame.display.flip() #flips the images on the monitor
    clock.tick(FPS) #limits the frames per sec

#exit from system memory
pygame.quit()
sys.exit()