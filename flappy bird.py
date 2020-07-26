import pygame
import random

pygame.mixer.pre_init(frequency=44100,size=16,channels=1,buffer=520)
pygame.init()
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()
game_font=pygame.font.Font("freesansbold.ttf",30)

#game variables
gravity=0.25
bird_movement=0
game_active=True
score=0
high_score=0

# bird
birdIMG = pygame.image.load("bird.png").convert_alpha()
bird_rect=birdIMG.get_rect(center=(80,200))

# caption and icon
pygame.display.set_caption("udta panchi")

icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# statement
enter = pygame.font.Font("freesansbold.ttf", 20)
textX = 75
textY = 270

#game over
game_over_surface=pygame.image.load("gameover.png")
gameover_rect=game_over_surface.get_rect(center=(200,300))

#green_pipe
green_pipe = pygame.image.load('pipe_green.png').convert()
green_pipet = pygame.transform.flip(green_pipe,False,True)
pipe_list = []
SPAWNPIPE=pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
# bg image
cx = 0
cy = 0
background = pygame.image.load("cloud_bg.jpg").convert()

# ground
floor = pygame.image.load("Floor.png")
gx = 0
gy = 470

#sounds
flap_sound=pygame.mixer.Sound("wing.wav")
death_sound=pygame.mixer.Sound("hit.wav")
score_sound=pygame.mixer.Sound("point.wav")
die_sound=pygame.mixer.Sound("die.wav")
score_sound_countdown=100
def create_rect():
    pipe_height = random.randint(220,420)
    pipe_heightchange = random.randint(520,600)
    pipe_rect_bottom = green_pipe.get_rect(midtop=(500, pipe_height))
    pipe_rect_top = green_pipe.get_rect(midtop=(500, pipe_height-pipe_heightchange))
    return pipe_rect_bottom, pipe_rect_top
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx-=3
    return pipes

def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom>=600:
            screen.blit(green_pipe,pipe)
        else:
            screen.blit(green_pipet,pipe)
def enter_text(x, y):
    Input = enter.render("PRESS SPACE TO START", True, (0, 0, 0))
    screen.blit(Input, (x, y))

def score_display(game_state):
    if game_state=="main_game":
        score_surface=game_font.render("score:"+str(int(score)),True,(0,0,0))
        score_rect=score_surface.get_rect(center=(188,50))
        screen.blit(score_surface,score_rect)

    if game_state=="game_over":
        score_surface=game_font.render("score:"+str(int(score)),True,(0,0,0))
        score_rect=score_surface.get_rect(center=(188,50))
        screen.blit(score_surface,score_rect)

        high_score_surface=game_font.render("high score:"+str(int(score)),True,(0,0,0))
        high_score_rect=score_surface.get_rect(center=(150,100))
        screen.blit(high_score_surface,high_score_rect)

def update_score(score,high_score):
    if score>high_score:
        high_score=score
    return high_score

def rotate_bird(bird):
    new_bird=pygame.transform.rotozoom(bird,-bird_movement*4,1)
    return new_bird


def ground(x,y):
    screen.blit(floor,(x,y))

def cloud(x,y):
    screen.blit(background, (x, y))

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            die_sound.play()
            return False
     
    if bird_rect.top<=-100 or bird_rect.bottom>=510:
        return False
    return True         
 
running = True
starting = True
while starting:
    cloud(cx,cy)
    enter_text(textX, textY)
    ground(gx, gy)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            starting = False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE:
                starting = False
                while running:
                    # bg image
                    cloud(cx,cy)
                    cloud(cx + 400,cy)
                    cx -= 1
                    if cx<=-400:
                        cx = 0
                    for event in pygame.event.get():
                        if event.type==pygame.QUIT:
                            running = False

                        if event.type==pygame.KEYDOWN:
                            if event.key==pygame.K_SPACE and game_active:
                                bird_movement=0
                                bird_movement-=6
                                flap_sound.play()

                            if event.key==pygame.K_SPACE and game_active==False:
                                game_active=True
                                pipe_list.clear()
                                bird_rect.center=(70,200)
                                bird_movement=0
                                score=0

                           
                        
                        if event.type == SPAWNPIPE:
                            pipe_list.extend(create_rect())

                    clock.tick(120)

                    
                    if game_active:
                        #bird
                        bird_movement+=gravity
                        rotated_bird=rotate_bird(birdIMG)
                        bird_rect.centery+=bird_movement
                        screen.blit(rotated_bird,bird_rect)
                        game_active=check_collision(pipe_list)  

                        #pipe
                        pipe_list = move_pipe(pipe_list)
                        draw_pipe(pipe_list)
                        score+=0.01
                        score_display("main_game")
                        score_sound_countdown-=1
                        if score_sound_countdown<=0:
                            score_sound.play()
                            score_sound_countdown=100 
                    else:
                        high_score=update_score(score,high_score)
                        score_display("game_over")  
                        screen.blit(game_over_surface,gameover_rect)  
                        enter_text(textX, textY+100)
                    #scrolling ground
                    ground(gx,gy)
                    ground(gx + 395,gy)
                    gx-=3
                    if gx <= -395:
                        gx=0
                    
                    
                    
                   
                    pygame.display.update()
