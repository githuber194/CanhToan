import pygame, sys, random, asyncio
#TẠO HÀM CHO GAME
def draw_floor():
     screen.blit(floor,(floor_x_pos,570))
     screen.blit(floor,(floor_x_pos+432,570))
def create_pipe():
    random_pipe_pos=random.choice(pipe_height)
    bottom_pipe=pipe_surface.get_rect(midtop=(1080,random_pipe_pos))
    top_pipe=pipe_surface.get_rect(midtop=(1080,random_pipe_pos-670))
    return bottom_pipe, top_pipe
def move_pipe(pipes):
        for pipe in pipes:
            pipe.centerx -=1.9
        return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >=400:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe=pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False
    if bird_rect.top<=-75 or bird_rect.bottom>=570:
            hitfloor_sound.play()
            return False
    return True 
def rotate_bird(bird1):
    new_bird=pygame.transform.rotozoom(bird1,-bird_movement*3,1) 
    return new_bird 
def bird_animation():
    new_bird=bird_list[bird_index]
    new_bird_rect=new_bird.get_rect(center=(350,bird_rect.centery))
    return new_bird, new_bird_rect 
def score_display(game_state):
    if game_state=='main game':
        score_surface=game_font.render(str(int(score)), True, (255,255,0))
        score_rect=score_surface.get_rect(center=(550,70))
        screen.blit(score_surface, score_rect)
    if game_state=='game_over':
        score_surface=game_font.render(f'Score: {int(score)}', True, (255,255,0))
        score_rect=score_surface.get_rect(center=(550,70))
        screen.blit(score_surface, score_rect)

        high_score_surface=game_font.render(f'High Score: {int(high_score)}', True, (255,255,0))
        high_score_rect=high_score_surface.get_rect(center=(550,390))
        screen.blit(high_score_surface, high_score_rect)
def update_score(score,high_score):
    if score>high_score:
        high_score=score
    return high_score
pygame.init()
screen= pygame.display.set_mode((1120,630))
clock=pygame.time.Clock()
game_font=pygame.font.Font('LifeCraft_Font.ttf',40)
#TẠO CÁC BIẾN CHO GAME
gravity=0.1
bird_movement=0
game_active = True
score=0
high_score=0
#CHÈN BACKGROUND
bg=pygame.image.load('assets/background-new.png')
bg=pygame.transform.scale(bg,(1120,630))
#CHÈN SÀN
floor=pygame.image.load('assets/floor.png').convert()
floor=pygame.transform.scale(floor,(2240,140))
floor_x_pos=0
#TẠO CHIM
bird_up=pygame.image.load('assets/yellowbird-upflap.png').convert_alpha()
bird_down=pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_mid=pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_down=pygame.transform.scale(bird_down,(55,35))
bird_mid=pygame.transform.scale(bird_mid,(55,35))
bird_up=pygame.transform.scale(bird_up,(55,35))
bird_list=[bird_down,bird_mid,bird_up] #0 1 2
bird_index=1
bird=bird_list[bird_index]
bird=pygame.transform.scale(bird,(55,35))
bird_rect=bird.get_rect(center=(350,280))

#TẠO TIMER CHO BIRD
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap,200)
last_passed_pipe = None
#TẠO ỐNG
pipe_surface=pygame.image.load('assets/pipe-green.png').convert()
pipe_surface=pygame.transform.scale(pipe_surface,(82,506))
pipe_list=[]
pipe_passed = []
spawnpipe=pygame.USEREVENT
pygame.time.set_timer(spawnpipe, 1800)
pipe_height =[300,380,500]
game_over_surface=pygame.image.load('assets/message.png').convert_alpha()
game_over_rect=game_over_surface.get_rect(center=(552,220))
flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
hit_sound = pygame.mixer.Sound('sound/mixkit-cartoon-dazzle-hit-and-birds-746.wav')
hitfloor_sound = pygame.mixer.Sound('sound/mixkit-fast-blow-2144.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100
while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_SPACE and game_active:
                bird_movement=0 
                bird_movement=-3.8
                flap_sound.play()
            if event.key==pygame.K_SPACE and game_active==False:
                    game_active=True
                    pipe_list.clear() 
                    bird_rect.center=(350,280)
                    bird_movement=0
                    score=0  
        if event.type == spawnpipe:
            pipe_list.extend(create_pipe())
        if event.type==birdflap:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index=0
            bird, bird_rect = bird_animation()
    screen.blit(bg,(0,0))
    if game_active:
        #CHIM
        bird_movement+=gravity
        rotated_bird=rotate_bird(bird)
        bird_rect.centery+=bird_movement
        screen.blit(rotated_bird,bird_rect)
        game_active= check_collision(pipe_list)
        #ỐNG
        pipe_list=move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score_display('main game')
        for i, pipe in enumerate(pipe_list):
            if pipe.centerx < bird_rect.centerx and pipe not in pipe_passed:
                pipe_passed.append(pipe)
                score += 0.5
                score_sound.play()
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score=update_score(score,high_score)
        score_display('game_over')
    #SÀN
    floor_x_pos-=0.5
    draw_floor()
    if floor_x_pos <= -1120:
        floor_x_pos =0

    pygame.display.update()
    clock.tick(120)