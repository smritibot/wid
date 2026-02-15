import random
from time import sleep

Z = (0, 0)
N = (0, -1)
E = (1, 0)
S = (0, 1)
W = (-1, 0)

directions = [N, E, S, W]

#Initialize globals, sorry not really constants
DOOR_THRES = .6
ROUGH_THRES = .1
FAILED_ATTEMPTS = 100 
BIAS_STRAIGHT = False
MIN_ROOM_DIM = 3
ROOM_VAR = 5

WRITE_MAP_SETTINGS = True
ANIMATE = False and __name__=="__main__"


def set_constants():
	DOOR_THRES = random.random()*.9 + .1
	ROUGH_THRES = random.random() * .3
	FAILED_ATTEMPTS = random.randint(0, 40)
	BIAS_STRAIGHT = random.randint(0, 1)
	MIN_ROOM_DIM = random.randint(3, 5)
	ROOM_VAR = random.randint(3, 6)
	
	#DOOR_THRES = 0.32234678069988054
	#ROUGH_THRES = 0.14971437014511607
	#FAILED_ATTEMPTS = 32
	#BIAS_STRAIGHT = 1
	#MIN_ROOM_DIM = 1
	#ROOM_VAR = 0
	
	if WRITE_MAP_SETTINGS:
		with open("lastmapsettings.txt", "w+") as f:
			f.write("\n".join([
			
				"Door threshold: " + str(DOOR_THRES),
				"Roughness threshold: " + str(ROUGH_THRES),
				"Allowed failed room attempts: " + str(FAILED_ATTEMPTS),
				"Staight line bias? " + str(BIAS_STRAIGHT),
				"Min room dim: " + str(MIN_ROOM_DIM),
				"Room variation: " + str(ROOM_VAR),			
			]))
			
	if __name__ == "__main__":
		print("\n".join([
			
				"Door threshold: " + str(DOOR_THRES),
				"Roughness threshold: " + str(ROUGH_THRES),
				"Allowed failed room attempts: " + str(FAILED_ATTEMPTS),
				"Staight line bias? " + str(BIAS_STRAIGHT),
				"Min room dim: " + str(MIN_ROOM_DIM),
				"Room variation: " + str(ROOM_VAR),
			]))
			
	return DOOR_THRES,ROUGH_THRES,FAILED_ATTEMPTS,BIAS_STRAIGHT,MIN_ROOM_DIM,ROOM_VAR



def delay_func(tm = .1):
	sleep(tm)
	print()
	#input()
	
def gap_func():
	input()
	
def av(a, b):
	return (a[0] + b[0], a[1] + b[1])
	
class Room(object):
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.merged = False
		self.neighbours = set([av(pt, dir) for pt in self.points for dir in directions if av(pt, dir) not in self.points])
	@property
	def nw(self):
		return (self.x, self.y)
		
	@property
	def se(self):
		return (self.x + self.width, self.y + self.height)
		
	@property
	def points(self):
		return [(x,y) for x in range(self.x, self.x + self.width) for y in range(self.y, self.y + self.height)]
		
		
		
class Maze(object):
	def __init__(self, points):
		self.points = points
		self.merged = False
		self.neighbours = set([av(pt, dir) for pt in points for dir in directions if av(pt, dir) not in points])

class Map(object):
	def __init__(self, width, height):
		self.height = height
		self.width = width
		self.ym = 2 * self.height + 1
		self.xm = 2 * self.width + 1
	
		self.grid = []
		for i in range(self.ym):
			self.grid.append(["#" for _ in range(self.xm)])
		
	def __str__(self):
		return "\n".join("".join(i) for i in self.grid)
		
	def __contains__(self, point):
		x,y = point
		return (y >= 0 and y < self.ym and x >= 0 and x < self.xm)
		
	def spot_empty(self, point):
		x,y = point
		return self.grid[y][x] == " "
		
	def get(self, point):
		x,y = point
		return self.grid[y][x]
		
	def clear(self, point):
		x,y = point
		self.grid[y][x] = " "
		
	def fill(self, point):
		x,y = point
		self.grid[y][x] = "X"
		
	def add_room(self, room):
		
		
		if room.nw not in self or room.se not in self:
			return False
			
		if any(
			[self.spot_empty((x,y)) for x in range(room.x, room.x + room.width) for y in range(room.y, room.y + room.height)]
		):
			return False
		
		for x in range(room.x, room.x + room.width):
			for y in range(room.y, room.y + room.height):
				self.clear((x,y))
		if ANIMATE:
				print(self)
				delay_func()
		return True
		
	def pt_has_avail_path(self, point):
		for direction in directions:
			one = av(point, direction)
			two = av(one, direction)
			if one in self and two in self and not (self.spot_empty(one) or self.spot_empty(two)):
				return True
		else:
			return False
		
		
	def get_align_points(self):
		return [(2 * x + 1, 2 * y + 1) for x in range(self.width) for y in range(self.height)]
	def get_off_points(self):
		return [(2 * x, 2 * y) for x in range(self.width) for y in range(self.height)]

def makeMaze(mp):
	options = [p for p in mp.get_align_points() if (not mp.spot_empty(p)) and mp.pt_has_avail_path(p) ]
	
	if not options:
		return False
	
	start = random.choice(options)
	
	active = set([start])
	clear_points = set([start])
	mazepoints = set()
	
	lastDirection = None
	
	while len(active):
		curr = active.pop()
		valid = []
		valid = []
		for direction in directions:
			one = av(curr, direction)
			two = av(one, direction)
			if one in mp and two in mp and not(mp.spot_empty(one) or mp.spot_empty(two)):
				valid.append(direction)
			
		if len(valid):
			
			if lastDirection and lastDirection in valid and BIAS_STRAIGHT:# and random.random() < .9:
				chosen = lastDirection
			else:
				chosen = random.choice(valid)
			lastDirection = chosen
			one = av(curr, chosen)
			two = av(one, chosen)
			clear_points.update([one, two])
			active.add(two)
			
		for point in clear_points:
			mp.clear(point)
			mazepoints.add(point)
			if ANIMATE:
				print(mp)
				delay_func(.15)
		clear_points.clear()
	return Maze(mazepoints)
	#for pt in options:
	#	x,y = pt
	#	mp.grid[y][x] = "h"


		
def getMap(wdth, ht):
	DOOR_THRES,ROUGH_THRES,FAILED_ATTEMPTS,BIAS_STRAIGHT,MIN_ROOM_DIM,ROOM_VAR = set_constants()



	m = Map(wdth, ht)
	if ANIMATE:
		print(m)
		print("\nClearing...")
	failed_attempts = FAILED_ATTEMPTS
	rooms = []
	mazes = []
	while failed_attempts > 0:
		rx = 2 * random.randint(1, m.width) - 1
		ry = 2 * random.randint(1, m.height) - 1
		width = 2 * random.randint(MIN_ROOM_DIM, MIN_ROOM_DIM + ROOM_VAR) - 1
		height = 2 * random.randint(MIN_ROOM_DIM, MIN_ROOM_DIM + ROOM_VAR) - 1
		rm = Room(rx, ry, width, height)
		if m.add_room(rm):
			rooms.append(rm)
		else:
			failed_attempts -= 1
	more = True
	while more:
		#print("Making maze...")
		more = makeMaze(m)
		mt = str(more)
		#print("More was " + mt)
		#if more:
			#print(len(more.points))
			#print(more.points)
		if more:
			mazes.append(more)
	zones = rooms + mazes
	
	if ANIMATE:
		print("\nCleared.\n")
		print(m)
		print("\n")
	#for point in mazes[0].points:
	#	x,y = point
	#	m.grid[y][x] = "o"
	#for point in mazes[0].neighbours:
	#	x,y = point
	#	m.grid[y][x] = "."
	#for point in rooms[0].points:
	#	x,y = point
	#	m.grid[y][x] = "o"
	potential_doors = dict()
	for point in m.get_off_points():
		x,y = point
		nzs = set([zn for zn in zones for dr in directions if point in zn.neighbours])
		if not m.spot_empty(point) and len(nzs) == 2:
			potential_doors[point] = nzs
			#m.grid[y][x] = "&" #str(len(nzs))[-1]
	start = zones[0]
	working = set([start])
	while len(working):
		curr = working.pop()
		curr.merged = True
		if ANIMATE:
			for pt in curr.points:
				px,py = pt
				m.grid[py][px] = "."
		for pt in curr.neighbours:
			if pt in potential_doors:
				oz = [z for z in potential_doors[pt] if z != curr][0]
				if not oz.merged and not(oz in working and random.random() < DOOR_THRES):
					working.add(oz)
					px,py = pt
					m.grid[py][px] = "_"
					if ANIMATE:
						print(m)
						delay_func()
					
	if ANIMATE:
		gap_func()
	open_points = set()
	for y,row in enumerate(m.grid):
		for x in range(len(row)):
			if row[x] != "#":
				open_points.add((x,y))
				row[x] = " "
	if ANIMATE:
		print()
		print(m)
		gap_func()
	dead_ends = set()
	
	for point in open_points:
		ns = [av(point, dir) for dir in directions if not m.spot_empty(av(point,dir))]
		if len(ns) == 3:
			x,y=point
			m.grid[y][x] = "#"
			dead_ends.add((x,y))
			
	
	while len(dead_ends):
		for de in dead_ends:
			open_points.discard(de)
		dead_ends = set()
		for point in open_points:
			ns = [av(point, dir) for dir in directions if not m.spot_empty(av(point,dir))]
			if len(ns) >= 3:
				x,y=point
				m.grid[y][x] = "#"
				dead_ends.add((x,y))
				if ANIMATE:
					print(m)
					delay_func()
	if ANIMATE:
		gap_func()
	for point in open_points:
		for dir in directions:
			if not m.spot_empty(av(point, dir)):
				if random.random() < ROUGH_THRES:
					m.clear(av(point,dir))
					if ANIMATE:
						print(m)
						delay_func()
			
	if ANIMATE:
		print()
		print(m)
	return m
	
if __name__=="__main__":
	m = getMap(40, 20)
	print(m)