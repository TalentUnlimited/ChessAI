import pygame
pygame.init()

running = True

WIDTH = 500
HEIGHT = 500

win = pygame.display.set_mode((WIDTH,HEIGHT))

while running:
	win.fill((255,255,255))

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	for y in range(9):
		for x in range(9):
			if (x+y) % 2 == 0:
				pygame.draw.rect(win,(234, 233, 210),pygame.Rect(x*(WIDTH/8),y*(HEIGHT/8),WIDTH/8,HEIGHT/8))
			else:
				pygame.draw.rect(win,(75, 115, 153),pygame.Rect(x*(WIDTH/8),y*(HEIGHT/8),WIDTH/8,HEIGHT/8))

	# i = pygame.transform.scale(pygame.image.load(f"D:/Python/ProjImages/Chess Pieces/{fen_l[y][x]}.png"),(int(WIDTH/8), int(HEIGHT/8)))
	# win.blit(i, (x*(WIDTH/8),y*(HEIGHT/8)))

	pygame.display.update()