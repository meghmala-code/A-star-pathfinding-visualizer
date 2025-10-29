import pygame
import math
from queue import PriorityQueue

WIDTH = 800#size of borad
WIN = pygame.display.set_mode((WIDTH, WIDTH))#dimension
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width#to trace actual coordinate position in the screeen
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color == GREEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == ORANGE

	def is_end(self):
		return self.color == TURQUOISE

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = ORANGE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = TURQUOISE

	def make_path(self):
		self.color = PURPLE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()


def algorithm(draw, grid, start, end):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col


def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)































'''import math
import pygame
from pygame.locals import *
pygame.init()
import sys

screen= pygame.display.set_mode((600,500))
pygame.display.set_caption("The Pie Game- press 1,2,3,4")
myfont= pygame.font.Font(None,60)

color= 200,80,60
width=4
x=300
y=250
radius=200
positions= x-radius, y-radius, radius*2, radius*2

piece1= False
piece2= False
piece3= False
piece4= False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type== KEYUP:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            elif event.key == pygame.K_1:
                piece1=True
            elif event.key == pygame.K_2:
                piece2= True
            elif event.key == pygame.K_3:
                piece3= True
            elif event.key == pygame.K_4:
                piece4= True
    #clear the screen
    screen.fill((0,0,255))

    #draw the four no
    textimg1= myfont.render("1",True, color)
    screen.blit(textimg1, (x+radius/2-20,y-radius/2))
    textimg2= myfont.render("2",True, color)
    screen.blit(textimg2, (x-radius/2,y-radius/2))
    textimg3= myfont.render("3",True, color)
    screen.blit(textimg3, (x-radius/2,y+radius/2))
    textimg4= myfont.render("4",True, color)
    screen.blit(textimg4, (x+radius/2-20,y+radius/2-20))

    #should the piece be drawn
    if piece1:
        start_angle= math.radians(0)
        end_angle= math.radians(90)
        pygame.draw.arc(screen, color, positions, start_angle, end_angle, width)
        pygame.draw.line(screen, color, (x,y), (x,y-radius), width)
        pygame.draw.line(screen , color , (x,y), (x+radius,y), width)
    if piece2:
        start_angle= math.radians(90)
        end_angle= math.radians(180)
        pygame.draw.arc(screen, color, positions, start_angle, end_angle, width)
        pygame.draw.line(screen, color, (x,y), (x,y-radius), width)
        pygame.draw.line(screen , color , (x,y), (x-radius,y), width)

    if piece3:
        start_angle= math.radians(180)
        end_angle= math.radians(270)
        pygame.draw.arc(screen, color, positions, start_angle, end_angle, width)
        pygame.draw.line(screen, color, (x,y), (x-radius,y), width)
        pygame.draw.line(screen , color , (x,y), (x,y+radius), width)

    if piece4:
        start_angle= math.radians(270)
        end_angle= math.radians(360)
        pygame.draw.arc(screen, color, positions, start_angle, end_angle, width)
        pygame.draw.line(screen, color, (x,y), (x,y+radius), width)
        pygame.draw.line(screen , color , (x,y), (x+radius,y), width)

    #is the pie finished?
    if piece1 and piece2 and piece3 and piece4:
        color= 0,255,0
    pygame.display.update()


'''












'''import math
import sys
import pygame
from pygame.locals import *
pygame.init()
screen= pygame.display.set_mode((600,500))
pygame.display.set_caption("drawing arcs")

while True:
    for event in pygame.event.get():
        if event.type==QUIT or event.type==KEYDOWN:
            pygame.quit()
            sys.exit()

    screen.fill((0,80,0)) #dark green
    #draw the line
    color= 255,0,255#cyan
    position= 200,150,200,200
    start_angle= math.radians(0)
    end_angle= math.radians(180)
    width= 8
    pygame.draw.arc(screen,color, position, start_angle, end_angle, width)
    pygame.display.update()

'''









'''import sys
import pygame
from pygame.locals import *
pygame.init()
screen= pygame.display.set_mode((600,500))
pygame.display.set_caption("drawing lines")

while True:
    for event in pygame.event.get():
        if event.type==QUIT or event.type==KEYDOWN:
            pygame.quit()
            sys.exit()

    screen.fill((0,80,0)) #dark green
    #draw the line
    color= 100,255,200  #cyan
    width= 8
    pygame.draw.line(screen,color, (100,100), (500,400), width)
    pygame.display.update()

'''














'''import sys
import pygame
from pygame.locals import *
screen= pygame.display.set_mode((600,500))
pygame.display.set_caption("drawing rectangle")

pos_x= 300
pos_y= 250
vel_x= 2
vel_y=1

while True:
    for event in pygame.event.get():
        if event.type== QUIT or event.type== KEYDOWN:
            pygame.quit()
            sys.exit()
    screen.fill((0,0,200))

    #move the rectangle
    pos_x += vel_x
    pos_y += vel_y

    #keep rectangle on the screen
    if pos_x > 500 or pos_x<0:
        vel_x= -vel_x
    if pos_y >400 or pos_y<0 :
        vel_y= -vel_y

    #draw the rectangle
    color= 255,255,0
    width= 0 #solid fill
    pos= pos_x, pos_y, 100,100
    pygame.draw.rect(screen,color,pos, width)
    pygame.display.update()
 '''   











'''import pygame
import sys
from pygame.locals import *
pygame.init()
screen= pygame.display.set_mode((600,500))
pygame.display.set_caption("drawing circles")
while True:
    for event in pygame.event.get():
        if event.type== pygame.QUIT or event.type== pygame.KEYDOWN:
            pygame.quit()
            sys.exit()
    screen.fill((0,0,200))
    #draw a circle
    color= 255,255,0  #yellow
    position= 300,300
    radius= 200
    width=10
    pygame.draw.circle(screen,color,position,radius,width)
    pygame.display.update()

'''


'''from pygame.locals import *
import pygame
import sys

white= 255,255,255
blue= 0,0,200

pygame.init()
screen= pygame.display.set_mode((600,500))
myfont= pygame.font.Font(None,60) #none shows default font is used


textimage= myfont.render("Hello pygame", True, white)


while True:
    for event in pygame.event.get():
        if event.type in (QUIT, KEYDOWN):
            sys.exit()
    screen.fill(blue)
    screen.blit(textimage, (100,100))
    pygame.display.update()
'''
