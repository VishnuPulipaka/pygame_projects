import pygame,sys,random

#function to keep the floor moving
def draw_floor():
	screen.blit(FLOOR,(FLOOR_X,610))
	screen.blit(FLOOR,(FLOOR_X+576,610))

def create_pipe():
	random_pipe_pos=random.choice(pipe_heights)
	bottom_pipe=pipes.get_rect(midtop=(1100,random_pipe_pos))
	top_pipe=pipes.get_rect(midbottom=(1100,random_pipe_pos-400))
	return bottom_pipe,top_pipe

def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx-=5
	return pipes

def draw_pipes(pipes_list):
	for pipe in pipes_list:
		if pipe.bottom>=700:
			screen.blit(pipes,pipe)
		else:
			flip_pipe=pygame.transform.flip(pipes,False,True)
			screen.blit(flip_pipe,pipe)


def check_collisions(pipes):
	for pipe in pipes: 
		if bird_rect.colliderect(pipe):
			death.play()
			return False
	if bird_rect.top<=-400 or bird_rect.bottom>=610:
		death.play()
		return False

	return True

def rotate_bird(bird):
	new_bird=pygame.transform.rotozoom(bird,-bird_movement*3,1)
	return new_bird

def bird_animation():
	new_bird=bird_frames[bird_index]
	new_bird_rect=new_bird.get_rect(center=(60,bird_rect.centery))
	return new_bird,new_bird_rect

def score_display(game_state):
	if game_state=="main_game":
		score_sruface=game_font.render(str(int(score)),True,(255,255,255))
		score_rect=score_sruface.get_rect(center=(288,80))
		screen.blit(score_sruface,score_rect)
	if game_state=="game_over":
		score_sruface=game_font.render(f'Score:{str(int(score))}',True,(255,255,255))
		score_rect=score_sruface.get_rect(center=(288,80))
		screen.blit(score_sruface,score_rect)
		Hscore_sruface=game_font.render(f'High Score:{str(int(high_score))}',True,(255,255,255))
		Hscore_rect=Hscore_sruface.get_rect(center=(288,550))
		screen.blit(Hscore_sruface,Hscore_rect)


#initializing the game window
pygame.mixer.pre_init(frequency=44100,channels=1,buffer=512,size=16)
pygame.init()

#setup screen
WIDTH,HEIGHT=576,700
screen=pygame.display.set_mode((WIDTH,HEIGHT))

#clock object 
clock=pygame.time.Clock()

#font object
game_font=pygame.font.Font('assets/flappy-bird-assets-master/sprites/flappy-bird.ttf',40)

#surfaces
BG=pygame.image.load('assets/flappy-bird-assets-master/sprites/background-day.png').convert()
BG=pygame.transform.scale(BG,(576,700))

#pipes
pipes=pygame.image.load('assets/flappy-bird-assets-master/sprites/pipe-green.png').convert()
pipes=pygame.transform.scale(pipes,(100,600))
pipe_list=[]

SPAWNPIPE=pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_heights=[500,350,200]

BIRDFLAP= pygame.USEREVENT+1
pygame.time.set_timer(BIRDFLAP,200)




FLOOR=pygame.image.load('assets/flappy-bird-assets-master/sprites/base.png').convert()
FLOOR=pygame.transform.scale(FLOOR,(576,90))
FLOOR_X=0

#the  bird
bird_up_s=pygame.transform.scale(pygame.image.load('assets/flappy-bird-assets-master/sprites/bluebird-upflap.png').convert_alpha(),(40,40))
bird_mid_s=pygame.transform.scale(pygame.image.load('assets/flappy-bird-assets-master/sprites/bluebird-midflap.png').convert_alpha(),(40,40))
bird_down_s=pygame.transform.scale(pygame.image.load('assets/flappy-bird-assets-master/sprites/bluebird-downflap.png ').convert_alpha(),(40,40))

bird_frames=[bird_down_s,bird_mid_s,bird_up_s]
bird_index=0
bird_s=bird_frames[bird_index]

bird_rect=bird_s.get_rect(center=(60,350))


GO=pygame.transform.scale(pygame.image.load('assets/flappy-bird-assets-master/sprites/message.png ').convert_alpha(),(300,300))
GOr=GO.get_rect(center=(288,350))
#game variables
gravity=0.25
bird_movement=0
game_active=True
score=0
high_score=0


#sounds
flap=pygame.mixer.Sound('assets/Everything/sfx_wing.wav')
death=pygame.mixer.Sound('assets/Everything/sfx_hit.wav')
score_sound=pygame.mixer.Sound('assets/Everything/sfx_point.wav')
score_count=100



#game loop

while True:

	#Event loop
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()

		#up movement by keyboard
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				bird_movement=0
				bird_movement-=12
				flap.play()

			if event.key==pygame.K_SPACE and game_active==False:
				game_active=True
				pipe_list.clear()
				bird_rect.center=(60,350)
				bird_movement=0
				score=0

		if event.type==SPAWNPIPE:
			pipe_list.extend(create_pipe())
			
		if event.type==BIRDFLAP:
			bird_index+=1
			bird_index%=3
			bird_s,bird_rect=bird_animation()

	screen.blit(BG,(0,0))

	if game_active:

		#bird_movement_logic
		bird_movement+=gravity
		rotated_bird=rotate_bird(bird_s)
		bird_rect.centery+=bird_movement
		screen.blit(rotated_bird,bird_rect)
		game_active=check_collisions(pipe_list)

		#pipes_logic
		pipe_list=move_pipes(pipe_list)
		draw_pipes(pipe_list)
		score+=0.01
		score_count-=1
		if score_count<=0:
			#score_sound.play()
			score_count=100
		score_display('main_game')

	else:
		if score>high_score:
			high_score=score
		score_display("game_over")
		screen.blit(GO,GOr)
		

	#floor lopgic
	FLOOR_X-=1
	draw_floor()
	if FLOOR_X<=-576:
		FLOOR_X=0
	pygame.display.update()
	clock.tick(120)

