import pygame
import random
import time

pygame.init()

WIDTH_DEVICE, HEIGHT_DEVICE = (950,700)
screen = pygame.display.set_mode((WIDTH_DEVICE, HEIGHT_DEVICE))
pygame.display.set_caption("Flappy Bird")
running = True
clock = pygame.time.Clock()

#def colors
GREEN = (0,255,0)
RED = (255,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (242,242,242)

#variables
OFFSET_TUBE = 150
GRAVITY = 0.5
on_game = False
game_over = False
game_start = False
first_show = False

#Notification Game Start/ Reset
fnt_fredoka = pygame.font.SysFont('Fredoka One', 24)
game_start_noti = fnt_fredoka.render("Game Start", True, GREEN)
game_over_noti = fnt_fredoka.render('Game Over', True, RED)
noti_start = fnt_fredoka.render("Press 'Space' to Play", True, GREEN)
game_start_noti_displayed = False

#Background music game
sound = pygame.mixer.Sound('music/Fluffing-a-Duck.mp3')
sfx_tap = pygame.mixer.Sound('music/Cartoon Hit 02.wav')
sfx_gameover = pygame.mixer.Sound('music/Tap Wrong.wav')
game_over_music_played = False

class Score_table:
	def __init__(self):
		self.score = 0
		self.highest_score = 0
		self.fnt_fredoka = pygame.font.SysFont('Fredoka One', 14)
		
	def draw(self):
		if self.highest_score <= self.score:
			self.highest_score = self.score
		pygame.draw.rect(screen, GRAY, (20,20,145,50), width=0, border_radius=5)
		highest_score_content = self.fnt_fredoka.render('Highest_score:', True, BLACK)
		score_content = self.fnt_fredoka.render('Score:', True, BLACK)
		highest_score = self.fnt_fredoka.render(str(self.highest_score), True, BLACK)
		score_new = self.fnt_fredoka.render(str(self.score), True, BLACK)
		screen.blit(highest_score_content, (28, 28))
		screen.blit(score_content, (28, 43))
		screen.blit(highest_score, (135, 28))
		screen.blit(score_new, (73, 43))

	def save_highest_score(self):
		try:
			with open("highest_score.txt", "w") as file:
				file.write(str(self.highest_score))
		except:
			pass

	def load_highest_score(self):
		try:
			with open("highest_score.txt", "r") as file:
				self.highest_score = int(file.readline())
		except:
			pass

class Tube:
	def __init__(self, pos_X, pos_Y, height, HEIGHT_DEVICE, OFFSET_TUBE):
		self.pos_X = pos_X
		self.pos_Y = pos_Y
		self.height_tube = height
		self.WIDTH_TUBE = 50
		self.SPEED = 0
		self.HEIGHT_DEVICE = HEIGHT_DEVICE
		self.OFFSET_TUBE = OFFSET_TUBE
		self.pass_tube = False
		self.tube_img = pygame.image.load("asset/tube.png")
		self.tube_img_inverse = pygame.image.load("asset/tube_inverse.png")

	def draw(self):
		self.tube_img = pygame.transform.scale(self.tube_img, (self.WIDTH_TUBE, self.height_tube))
		self.pos_X -= self.SPEED
		return screen.blit(self.tube_img, (self.pos_X, self.pos_Y, self.WIDTH_TUBE, self.height_tube))
		# return pygame.draw.rect(screen, GREEN, (self.pos_X, self.pos_Y, self.WIDTH_TUBE, self.height_tube))

	def draw_inverse(self):
		pos_Y_tube_inverse = self.height_tube + self.OFFSET_TUBE
		self.tube_img_inverse = pygame.transform.scale(self.tube_img_inverse, (self.WIDTH_TUBE, self.HEIGHT_DEVICE - pos_Y_tube_inverse))
		return screen.blit(self.tube_img_inverse, (self.pos_X, pos_Y_tube_inverse, self.WIDTH_TUBE, self.HEIGHT_DEVICE - pos_Y_tube_inverse))
		# return pygame.draw.rect(screen, GREEN, (self.pos_X, pos_Y_tube_inverse, self.WIDTH_TUBE, self.HEIGHT_DEVICE - pos_Y_tube_inverse))

class Bird:
	def __init__(self):
		self.pos_X = 450
		self.pos_Y = 300
		self.drop_velocity = 0
		self.GRAVITY = 0

	def draw(self):
		return screen.blit(flappy_bird, (self.pos_X, self.pos_Y))
		# return pygame.draw.rect(screen, RED, (self.pos_X, self.pos_Y, 30, 30))


tube_1 = Tube(950, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)
tube_2 = Tube(1150, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)
tube_3 = Tube(1350, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)
tube_4 = Tube(1550, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)
tube_5 = Tube(1750, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)

bird = Bird()

cls_score_table = Score_table()

#Load graphic
background_img = pygame.image.load("asset/background.png")
background_img = pygame.transform.scale(background_img, (950,700))
landing = pygame.image.load("asset/Landing.png")
landing = pygame.transform.scale(landing, (950,100))
flappy_bird = pygame.image.load("asset/Flappy-Bird.png")
flappy_bird = pygame.transform.scale(flappy_bird, (45,32))

#def functions
class Count_down:
	def __init__(self, time):
		self.start_time = 0
		self.end_time = 0
		self.time = time
	def check_time(self):
		if int(self.end_time - self.start_time) >= self.time:
			return True

count_down = Count_down(1000)

while running:
	clock.tick(60)
	screen.fill(WHITE)

	screen.blit(background_img, (0,0))
	#Press Space to Start
	if not on_game:
		screen.blit(noti_start, (360, 180))

	#draw tube
	if on_game:
		pygame.mixer.Sound.play(sound, loops=-1) #Music background
		pygame.mixer.Sound.set_volume(sound, 0.3)
		cls_score_table.load_highest_score()
		
		tube_1_unit = tube_1.draw()
		tube_1_unit_inverse = tube_1.draw_inverse()
		tube_2_unit = tube_2.draw()
		tube_2_unit_inverse = tube_2.draw_inverse()
		tube_3_unit = tube_3.draw()
		tube_3_unit_inverse = tube_3.draw_inverse()
		tube_4_unit = tube_4.draw()
		tube_4_unit_inverse = tube_4.draw_inverse()
		tube_5_unit = tube_5.draw()
		tube_5_unit_inverse = tube_5.draw_inverse()

		count_down.end_time = pygame.time.get_ticks()
		if not game_start_noti_displayed:
			screen.blit(game_start_noti, (420, 180))
			if count_down.check_time():
				game_start_noti_displayed = True

	# land = pygame.draw.rect(screen, BLACK, (0,600,950,100))
	land = screen.blit(landing, (0,650))

	#draw bird
	bird_unit = bird.draw()

	#draw score table
	cls_score_table.draw()

	#Tube auto creat
	if tube_1.pos_X - tube_1.SPEED <= -tube_1.WIDTH_TUBE and on_game and not game_over:
		tube_1 = Tube(950, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)
	
	if tube_2.pos_X - tube_2.SPEED <= -tube_2.WIDTH_TUBE and on_game and not game_over:
		tube_2 = Tube(950, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)
	
	if tube_3.pos_X - tube_3.SPEED <= -tube_3.WIDTH_TUBE and on_game and not game_over:
		tube_3 = Tube(950, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)
	
	if tube_4.pos_X - tube_4.SPEED <= -tube_4.WIDTH_TUBE and on_game and not game_over:
		tube_4 = Tube(950, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)
	
	if tube_5.pos_X - tube_5.SPEED <= -tube_5.WIDTH_TUBE and on_game and not game_over:
		tube_5 = Tube(950, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)


	#Scores
	for tube in (tube_1, tube_2, tube_3, tube_4, tube_5):
		if tube.pos_X + tube.WIDTH_TUBE < bird.pos_X and not tube.pass_tube:
			cls_score_table.score += 1
			tube.pass_tube = True
				

	if not game_over:
		for tube in (tube_1, tube_2, tube_3, tube_4, tube_5):
			tube.SPEED = 3
		bird.drop_velocity += bird.GRAVITY
		bird.pos_Y += bird.drop_velocity
	else:
		screen.blit(game_over_noti, (420, 180))
		# pygame.mixer.pause()
		if not game_over_music_played:
			pygame.mixer.Channel(1).play(sfx_gameover) #Sound Effect Game Over
			game_over_music_played = True
		cls_score_table.save_highest_score()

	#check collision
	if on_game:
		for tube_unit in (tube_1_unit, tube_2_unit, tube_3_unit, tube_4_unit, tube_5_unit, tube_1_unit_inverse, tube_2_unit_inverse, tube_3_unit_inverse, tube_4_unit_inverse, tube_5_unit_inverse, land):
			if bird_unit.colliderect(tube_unit):
				for tube in (tube_1, tube_2, tube_3, tube_4, tube_5):
					game_over = True
					tube.SPEED = 0

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				if on_game == False:
					bird.GRAVITY = GRAVITY
					count_down.start_time = pygame.time.get_ticks()
					print(count_down.start_time)
					on_game = True
				else:
					pygame.mixer.Channel(0).play(sfx_tap)
					pygame.mixer.Sound.set_volume(sfx_tap, 0.6)

				if on_game and game_over:
					tube_1 = Tube(950, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)
					tube_2 = Tube(1150, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)
					tube_3 = Tube(1350, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)
					tube_4 = Tube(1550, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)
					tube_5 = Tube(1750, 0, int(random.uniform(200,350)), HEIGHT_DEVICE, OFFSET_TUBE)
					bird = Bird()
					bird.GRAVITY = GRAVITY
					game_over = False
					game_over_music_played = False
					game_start_noti_displayed = False
					count_down.start_time = pygame.time.get_ticks()
					cls_score_table.score = 0

				bird.drop_velocity = 0
				bird.drop_velocity -= 8

	pygame.display.flip()
pygame.quit()