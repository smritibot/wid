import random
import os
import time 
import msvcrt
import curses
import math

import dungeon_map as map

#PREFERENCES
#Uses Dvorak keyboard, set with USE_DVORAK = True  or USE_DVORAK = False
USE_DVORAK = True
WRITE_MAP = True

#Shows all dividers and slots in status bar, " | stuff |  | morestuff" for True, "stuff | morestuff" for False
SHOW_ALL_STATUS_GAPS = False

SCALING = 1

#CHEATS:
#HANDICAP = 7 #RADIANT
HANDICAP = 1
START_FL    = False
START_TORCH = False
START_BEAM  = False
START_CAST  = False
START_TRAP  = False
START_BOMB  = False
START_SNAKE = False
START_PING  = False
VIEW_ALL    = False

DISCOVER_BEAM = False
DISCOVER_FIRST_LEVEL = False
DISCOVER_CAULDRON = False

#this is good, not a cheat.
DISCOVER_ONE = True

FPS = 12
BEAMPS = 12
BEAMCREATEPS = 4
ENEMYPS = .8
TRGTPS = 1
BOMBPS = 6
CASTPS = 1

HELD_ITEMS_BLOCK = False

ENEMY_MV_THRES = .2
ENEMY_LIGHT_MV_THRES = .8
ENEMY_HARSH_LIGHT_MV_THRES = .99
PRED_HIDE = False

INSANITY = False
INSANITY_CHARS = "X#&@a|^v<>!=....................................."
INSANITY_THRES = .01
INSANITY_RET_THRES = .99
if INSANITY:
	INSANITY_DICT = dict()
	
RIGHT_BORDER = True
RIGHT_BORDER_CHR = "R"

NEW_ROCK_ALG = True
	
USE_DUNGEON_MAP = True
ROCK_MIN = 10
ROCK_MAX = 6

#TRAP SETTINGS
TRAP_MAX  = 5
TRAP_RECOVERY_MODIFIER = 2

#CAULDRON RECOVERY MODIFIER
CAULDRON_RECOVERY_MODIFIER = 5
CAULDRON_REMOVES_LIGHT = False
ALLOW_CAULDRON_ACTION = False
CAULDRON_PROVIDES_LIGHT = True
CAULDRON_RANGE = 3

#SNAKE
SNAKE_MAX = 9
SNAKE_USE_PER_LEVEL_AGE = True
SNAKE_MAX_AGE_PER_LEVEL = 50
SNAKE_MAX_AGE = 300
SNAKE_COST = 0
SNAKE_USAGE_COST = 20
SNAKE_ENERGY_COST = 6

#BOMB
BOMB_MAX = 2
BOMB_END_AGE = 4
BOMB_MAX_AGE = 12
BOMBS_BREAK_WALL = True
BOMBS_HURT_SELF = True

BOMB_DEBRIS = ",;:\"'-_/\\{}[]"

#TORCH_SETTINGS
TORCH_MAX = 5
TORCH_RANGE = 6
TORCH_COST = 1

pred_in_light_char = "X"
if PRED_HIDE:
	pred_in_light_char = "#"

#FL SETTINGS
#FL_COST = 4
#FL_RANGE = 9
#FL_SLOPE = .8

#FL POWER
#settings
#    name ,cost,range, slope, isHarsh
flsettingsinit = [
	("Low"   , 0 , 4 , .4, False),
	("Medium", 2 , 6 , .6, False),
	("High"  , 6 , 9 , .8, True ),
	("Absurd", 10, 20, 4, True )
]
#FL_SETTINGS = [None]



#PRED SETTINGS, 
PRED_THRESH = 15
PRED_SPAWN_SQDIST = 4 ** 2
PRED_PER_LEVEL = 2
PRED_INITIAL_COUNT = 2 + (HANDICAP * PRED_PER_LEVEL)

#CAST SETTINGS
#CAST_RANGE = 7
CAST_MAX = 4
MAX_CAST_AGE = 30
CAST_COST = 2
CAST_DISCOVER = True

#BEAM SETTINGS
BEAM_COST = 3
USE_DUAL_BEAMS = False
BEAM_PASSTHROUGH = 12

#PING SETTINGS
PING_USAGE_COST = 5
PING_ENERGY_COST = 2
PING_LIMIT = 10
#SUPER SIGHT PING
#PING_PASSTHROUGH = 10
#PING_DESTROYS = False
#PING_SEE_AHEAD = False
#PING_WIDE_DESTROY = False
#Normal ping: ping destroys true, wide destroy false, see ahead true
PING_PASSTHROUGH = 1
PING_DESTROYS_PRED = True
PING_DESTROYS_ROCKS = True
PING_SEE_AHEAD = False
PING_WIDE_DESTROY = False
PING_LINGER = True
PING_LINGER_LENGTH = 4
PING_LINGER_BIG = True
#



#
LANTERN_COST = 40
LANTERN_RANGE = 50
LIGHT_MIN_MAX = 10
LIGHT_SMALL_MAX = 20
LIGHT_MEDIUM_MAX = 30
LIGHT_BIG_MAX = 60
LIGHT_HUGE_MAX = 100
LIGHT_HUGER_MAX = 150
LIGHT_HUGEST_MAX = 200
LIGHT_RADIATING_MAX = 300

#LEVEL DEPENDENT
LPLEVELS = [LIGHT_RADIATING_MAX, LIGHT_HUGEST_MAX, LIGHT_HUGER_MAX, LIGHT_HUGE_MAX, LIGHT_BIG_MAX, LIGHT_MEDIUM_MAX, LIGHT_SMALL_MAX, LIGHT_MIN_MAX]
LPRECOVERIES = [12, 5, 3, 2, 2, 1, 1, 0]
CASTMAXES = [16, 10, 8, 4, 3, 2, 1, 1]
CASTRANGES = [6.5, 4.5, 4, 3.25, 3, 2.8, 2.75, 2]
BEAM_RANGES = [6, 5, 4, 3, 2, 2, 1, 1]
LEVELNAMES = ["Radiant", "Master", "Teacher", "Adept", "Student", "Pupil", "Trainee", "Novice"]

NE = (1, -1)
E = (1, 0)
SE = (1, 1)
S = (0, 1)
SW = (-1, 1)
W = (-1, 0)
NW = (-1, -1)
N = (0, -1)
NOP = (0, 0)
L = (2, 3)
TN = (-5, -5)
TS = (-5, -4)
TE = (-5, -3)
TW = (-5, -2)
TF = ("TRAP", "FULL")
TNE = (-6, 6)
TSE = (-6, 1)
TSW = (-6, 2)
TNW = (-6, 3)
YN = (-2, -5)
YS = (-2, -4)
YE = (-2, -3)
YW = (-2, -2)
CT = (5,5) #clear traps
CY = (5,7)
OFF = ("off", "Flashlight")
ON = ("ON", "Flashlight")
O = ("TOGGLE", "FLASHLIGHT")
FLC = ""
FLD = "FLD"
CASTN = ("CASTN", "THING")
CASTW = ("CASTW", "THING")
CASTS = ("CASTS", "THING")
CASTE = ("CASTE", "THING")
CASTFULL = ("CASTF", "THING")
B = ("BEAM", "BEAM")
BOM = "BOMB"
BOMC = "BOMBC"
SNK = "SNAKE"
SNKC = "SNKC"
PKUP = "PKUP"
PING = "PING"

trgtdrs = [NE, E, SE, S, SW, W, NW, N, NOP]
carddrs = [N, E, S, W]
alldrs = [NE, E, SE, S, SW, W, NW, N]

trapdict = {
	TE : E,
	TS : S,
	TW : W,
	TN : N,
	TSE : SE,
	TSW : SW,
	TNE : NE,
	TNW : NW
}
torchdict = {
	YE : E,
	YS : S,
	YW : W,
	YN : N
}
castdict = {
	CASTN: N,
	CASTW: W,
	CASTE: E,
	CASTS: S
}

preddrs = [N, E, S, W]#, NE, SW, NW, SE]

#bmbdrs = [N, E, S, W, NE, SW, NW, SE, (0, 0)]
bmbdrs = [N, E, S, W, NE, SW, NW, SE, (0, 0), (2,0), (0, 2), (-2, 0), (0, -2)]

#motion
ARROWOP = {b'H' : N,#"N",
	b'P' : S,#"S",
	b'M' : E,#"E",
	b'K' : W,#"W",
	b'Q' : S,#"S",
	b'I' : N,#"N",
	}
	
#appended to suffixes
ARROWCODE = {b'H' : "N",
	b'P' : "S",
	b'M' : "E",
	b'K' : "W",
	b'Q' : "S",
	b'I' : "N",
	}	
	
DVORAK_NAMES = {
	#"OFF" : OFF,
	#"OF" : OFF,
	#"ON" : ON,
	"O" : O,
	#"L" : L,
	#"TE" : TE,
	#"TN" : TN,
	#"TS" : TS,
	#"TW" : TW,
	"AE" : TE,
	"AN" : TN,
	"AS" : TS,
	"AW" : TW,
	#"TF" : TF,
	"AF" : TF,
	"AA" : TF,
	#"TNE" : TNE,
	#"TSE" : TSE,
	#"TSW" : TSW,
	#"TNW" : TNW,
	"YE" : YE,
	"YN" : YN,
	"YS" : YS,
	"YW" : YW,
	"CT" : CT,
	"A." : CT,
	"CY" : CY,
	"Y." : CY,
	#"NE" : NE,
	#"E" : E,
	#"SE" : SE,
	#"S" : S,
	#"SW" : SW,
	#"W" : W,
	#"NW" : NW,
	#"N" : N,
	#"CASTN" : CASTN,
	#"CASTS" : CASTS,
	#"CASTE" : CASTE,
	#"CASTW" : CASTW,
	#"CASTFULL" : CASTFULL,
	#"CN" : CASTN,
	#"CS" : CASTS,
	#"CE" : CASTE,
	#"CW" : CASTW,
	#"CF" : CASTFULL,
	"UN" : CASTN,
	"US" : CASTS,
	"UE" : CASTE,
	"UW" : CASTW,
	"UF" : CASTFULL,
	"UU" : CASTFULL,
	"F" : CASTFULL,
	"B" : B,
	";" : B,
	"," : FLC,
	"'" : FLD,
	"I" : BOM,
	"D" : BOMC,
	"K" : SNK,
	"J" : SNKC,
	" " : PKUP,
	"E" : PING,
}

QWERTY_NAMES = {
	"S" : O,
	"KE" : TE,
	"KN" : TN,
	"KS" : TS,
	"KW" : TW,
	"AE" : TE,
	"AN" : TN,
	"AS" : TS,
	"AW" : TW,
	"KF" : TF,
	"AF" : TF,
	"AA" : TF,
	#"TNE" : TNE,
	#"TSE" : TSE,
	#"TSW" : TSW,
	#"TNW" : TNW,
	"TE" : YE,
	"TN" : YN,
	"TS" : YS,
	"TW" : YW,
	"IK" : CT,
	"AE" : CT,
	"IT" : CY,
	"TE" : CY,
	#"NE" : NE,
	"E" : E,
	#"SE" : SE,
	"S" : S,
	#"SW" : SW,
	"W" : W,
	#"NW" : NW,
	"N" : N,
	#"CASTN" : CASTN,
	#"CASTS" : CASTS,
	#"CASTE" : CASTE,
	#"CASTW" : CASTW,
	#"CASTFULL" : CASTFULL,
	"IN" : CASTN,
	"IS" : CASTS,
	"IE" : CASTE,
	"IW" : CASTW,
	"IF" : CASTFULL,
	"FN" : CASTN,
	"FS" : CASTS,
	"FE" : CASTE,
	"FW" : CASTW,
	"FF" : CASTFULL,
	"FU" : CASTFULL,
	"Y" : CASTFULL,
	"B" : B,
	"N" : B,
	"Z" : B,
	"W" : FLC,
	"Q" : FLD,
	"G" : BOM,
	"H" : BOMC,
	"V" : SNK,
	"C" : SNKC,
	" " : PKUP,
}

if USE_DVORAK:
	prfxs = "CTYAU"
	plyrdrnames = DVORAK_NAMES
else:
	prfxs = "IKTAF"
	plyrdrnames = QWERTY_NAMES

class Cast(object):
	def __init__(self, pos, dir):
		self.pos = pos
		self.dir = dir
		self.age = 0
		self.over = False
	
class Beam(object):
	def __init__(self, pos, dir):
		self.pos = pos
		self.dir = dir
		self.passthrough = BEAM_PASSTHROUGH
		self.over = False
		self.energy = 0
		
	def update(self, allowed, inGrid):
		p = mve(self.pos, self.dir)
		if allowed(p):
			self.pos = p
		elif self.passthrough > 0 and inGrid(p):
			self.pos = p
			self.passthrough -= 1
		else:
			self.over = True
		
class Ping(object):
	def __init__(self, pos, dir):
		self.pos = pos
		self.dir = dir
		self.passthrough = PING_PASSTHROUGH
		
		self.linger_length = PING_LINGER_LENGTH
		self.lingering = False
		
		self.over = False
		self.energy = 0
		
	def update(self, allowed, inGrid):
		if self.over:
			return
		self.energy += 1
		if self.energy >= PING_ENERGY_COST:
			self.energy -= PING_ENERGY_COST
			if not self.lingering:
				p = mve(self.pos, self.dir)
				
				alwd = allowed(p)
				
				if PING_WIDE_DESTROY:
					idx = carddrs.index(self.dir)
					otherdirs = [mve(p, nxt) for nxt in [carddrs[(idx + 1) % 4], carddrs[(idx + 3) % 4]]]
					alwd = alwd and all([allowed(ps) for ps in otherdirs])
				
				if alwd:
					self.pos = p
				elif self.passthrough > 0 and inGrid(p):
					self.pos = p
					self.passthrough -= 1
				else:
					if PING_LINGER:
						self.lingering = True
					else:
						self.over = True
			elif self.lingering:
				if self.linger_length > 0:
					self.linger_length -= 1
				else:
					self.over = True
		
class FLSetting(object):
	def __init__(self, name, cost, range, slope, is_harsh):
		self.name = name
		self.cost = cost
		self.range = range
		self.slope = slope
		self.is_harsh = is_harsh
		
class Cauldron(object):
	def __init__(self, position):
		self.position = position
		self.being_carried = False
		self.discovered = False
		
class Bomb(object):
	def __init__(self, position):
		self.position = position
		self.age = BOMB_MAX_AGE
		self.exploding = False
		self.blewselfup = False
		
class Snake(object):
	def __init__(self, position, direction):
		self.position = position
		self.direction = direction
		self.rh = random.randint(0,1)
		self.drs = [[S, E, N, W], [N, E, S, W]][self.rh]
		
		self.drIndex = self.drs.index(self.direction)
		self.dead = False
		self.age = 0
		self.foundWall = False
		
		self.energy = 0
		self.speed = random.randint(1, SNAKE_ENERGY_COST)
		
	def update(self, allowed, max_age):
		self.energy += self.speed
		if self.energy < SNAKE_ENERGY_COST:
			return
		else:
			self.energy -= SNAKE_ENERGY_COST
			self.age += 1
			self.dead = (self.age > max_age)
			if not self.foundWall:
				if allowed(mve(self.position, self.direction)):
					self.position = mve(self.position, self.direction)
					return
				else:
					self.foundWall = True
					self.drIndex = (self.drIndex + 3) % len(self.drs)
			if self.foundWall:
				testIndex = (self.drIndex + 1) % len(self.drs)
				if allowed(mve(self.position, self.drs[testIndex])):
					self.direction = self.drs[testIndex]
					self.drIndex = testIndex
					self.position = mve(self.position, self.direction)
					return
				else:
					testIndex = (self.drIndex)
					if allowed(mve(self.position, self.drs[testIndex])):
						self.direction = self.drs[testIndex]
						self.drIndex = testIndex
						self.position = mve(self.position, self.direction)
						return
					else:
						testIndex = (self.drIndex + 3) % len(self.drs)
						if allowed(mve(self.position, self.drs[testIndex])):
							self.direction = self.drs[testIndex]
							self.drIndex = testIndex
							self.position = mve(self.position, self.direction)
							return
						else:
							testIndex = (self.drIndex + 2) % len(self.drs)
							if allowed(mve(self.position, self.drs[testIndex])):
								self.direction = self.drs[testIndex]
								self.drIndex = testIndex
								self.position = mve(self.position, self.direction)
								return
							else:
								self.dead = True

FL_SETTINGS = [FLSetting(*obj) for obj in flsettingsinit]

def mve(pt1, pt2):
	return (pt1[0] + pt2[0], pt1[1] + pt2[1])

def scale(value, dim):
	return max(1,int(value * (SCALING ** dim)))
	
class Grid(object):
	def __init__(self, xm, ym): 
		# = sight
		self.lastop = N
		self.lastmovop = N
		self.lastchr = "^"
		self.xm = xm
		self.ym = ym
		self.lighton = False
		self.spotted = False
		self.turns = 0
		self.walls_destroyed = 0
		
		self.flSettingInd = 0
		
		self.hasFL = START_FL
		self.hasTorch = START_TORCH
		self.hasCast = START_CAST
		self.hasTrap = START_TRAP
		self.hasBeam = START_BEAM
		self.hasBomb = START_BOMB
		self.hasSnake = START_SNAKE
		self.hasPing = START_PING
		self.heldItem = None
		
		self.beamOn = False
		
		self.boundarySet = set()
		for i in range(self.xm):
			self.boundarySet.add((i, 0))
			self.boundarySet.add((i, self.ym - 1))
			
		for i in range(self.ym):
			self.boundarySet.add((0, i))
			self.boundarySet.add((self.xm - 1, i))
		
		#print(self.boundarySet)
		#exit(0)
		self.preds = []
		self.casts = []
		self.beams  = []
		self.pings = []
		
		self.plyr = (-1, -1)
		self.trgt = (-1, -1)
		self.traps = []
		self.bombs = []
		self.torches = []
		self.snakes = []
		
		self.cauldrons = []
		
		self.map = None

		if USE_DUNGEON_MAP:
			self.rocks = []
			mp = map.getMap(xm // 2, ym // 2)
			for y in range(len(mp.grid)):
				for x in range(len(mp.grid[y])):
					if mp.grid[y][x] == "#":
						self.rocks.append((x,y))
			self.map = mp.grid
		else:
			rockfactor = random.randint(xm * ym // ROCK_MIN, xm * ym // ROCK_MAX)
			#print("Rock factor is " + str(rockfactor))
			self.rocks = [(random.randint(1, xm -2), random.randint(1, ym - 2)) for i in range(rockfactor)]
			self.map = []
			for y in range(ym):
				row = []
				self.map.append(row)
				for x in range(xm):
					if (x,y) in self.rocks:
						row.append("#")
					else:
						row.append(" ")
		if WRITE_MAP:
			with open("lastmap.txt", "w+") as f:
				f.write("\n".join("".join(j) for j in self.map))
		self.discovered = []
		
		self.trgt = (random.randint(0, xm-2), random.randint(0, ym -2))
		while not self.allowed(self.trgt):
			self.trgt = (random.randint(0, xm-2), random.randint(0, ym -2))

		self.plyr = (random.randint(0, xm-1), random.randint(0, ym -1))
		while not (self.allowed(self.plyr) and (self.plyr != self.trgt)) :
			self.plyr = (random.randint(0, xm-1), random.randint(0, ym -1))
			
		for i in range(scale(PRED_INITIAL_COUNT, 2)):
			pred = (random.randint(0, xm-1), random.randint(0, ym -1))
			while not (self.allowed(pred) and (pred != self.trgt) and (pred != self.plyr)) :
				pred = (random.randint(0, xm-1), random.randint(0, ym -1))
			self.preds.append(pred)
			
		self.lpexps = []
		for i in range(len(LPLEVELS) - 1 - HANDICAP):
			lpexp = (random.randint(0, xm-1), random.randint(0, ym -1))
			while not (self.allowed(lpexp) and (lpexp != self.trgt) and (lpexp != self.plyr)) :
				lpexp = (random.randint(0, xm-1), random.randint(0, ym -1))
			self.lpexps.append(lpexp)
		self.lightpower = self.getLPMax()
		
		#item positions
		self.flGetter, self.castGetter, self.trapGetter, self.torchGetter, self.beamGetter, self.bombGetter, self.snakeGetter,self.pingGetter,cpt = random.sample([(x,y) for x in range(xm) for y in range(ym) if self.allowed((x,y))], 9)
		cdrn = Cauldron(cpt)
		self.cauldrons.append(cdrn)
		if DISCOVER_CAULDRON:
			cdrn.discovered = True
		
		if START_FL:
			self.flGetter = None
		if START_TORCH:
			self.torchGetter = None
		if START_BEAM:
			self.beamGetter = None
		if START_CAST:
			self.castGetter = None
		if START_TRAP:
			self.trapGetter = None
		if START_BOMB:
			self.bombGetter = None
		if START_SNAKE:
			self.snakeGetter = None
		if START_PING:
			self.pingGetter = None
	
		if DISCOVER_BEAM:
			self.discovered.append(self.beamGetter)
		if DISCOVER_ONE and not DISCOVER_BEAM:
			#self.discovered.append(random.choice(tuple(self.getItemPositionList())))
			self.discovered.append(min(self.getLightGetterPositionList(), key = lambda p: self.getSqEulDist(p, self.plyr)))
		if DISCOVER_FIRST_LEVEL and len(self.lpexps):
			self.discovered.append(self.lpexps[0])
			
	def bumpFLSetting(self):
		self.flSettingInd = (self.flSettingInd + 1) % len(FL_SETTINGS)
		
	def spawnPreds(self):
		#lazy about what happens if not enough free spots. Shouldn't happen often.
		newPreds = random.sample([(x,y) for x in range(self.xm) for y in range(self.ym) if self.allowed((x,y)) and (self.getSqEulDist(self.plyr, (x,y)) > scale(PRED_SPAWN_SQDIST, 2))], scale(PRED_PER_LEVEL, 2))
		self.preds.extend(newPreds)
		
	def dropFLSetting(self):
		self.flSettingInd = max((self.flSettingInd - 1), 0)
		
	def getCurrentFLSetting(self):
		return FL_SETTINGS[self.flSettingInd]
	
	def getDscChr(self, x, y):
		if (x, y) in self.rocks:
			return "*"
		elif (x,y) in self.getItemPositionList():
			return "!"
		else:
			return "~"
			
	def getGetterPositionList(self):
		items = set()
		for i2 in [self.flGetter, self.torchGetter,  self.castGetter, self.beamGetter, self.trapGetter, self.bombGetter, self.snakeGetter, self.pingGetter]:
			if i2 is not None:
				items.add(i2)
		return items
		
	def getLightGetterPositionList(self):
		items = set()
		for i2 in [self.flGetter, self.torchGetter,  self.castGetter, self.beamGetter, self.pingGetter]:
			if i2 is not None:
				items.add(i2)
		return items
		
	def getItemPositionList(self):
		items = set()
		for item in self.lpexps:
			if item is not None:
				items.add(item)
		for i2 in [self.flGetter, self.torchGetter,  self.castGetter, self.beamGetter, self.trapGetter, self.bombGetter, self.snakeGetter, self.pingGetter]:
			if i2 is not None:
				items.add(i2)
		return items
		
		
	def getIgnChr(self, x, y):
		if (x,y) == self.plyr:
			c = self.getPlyrChr()
			self.lastchr = c
			return c
		if (x,y) in [mve(b.position, dr) for dr in bmbdrs for b in self.bombs if b.exploding]:
			return random.choice(BOMB_DEBRIS)
		if (x,y) in [b.position for b in self.bombs if b.age > BOMB_END_AGE]:
			return "b"
		if (x,y) in [b.position for b in self.bombs if b.age <= BOMB_END_AGE]:
			return "B"
		if (x,y) in self.traps:
			return "%"
		if (x,y) in self.torches:
			return "Y"
		if (x,y) in [cast.pos for cast in self.casts]:
			return "O"
		if (x,y) in [c.position for c in self.cauldrons if not c.being_carried]:
			for c in self.cauldrons:
				if (x,y) == c.position:
					c.discovered = True
			return "U"
		if (x,y) in [c.position for c in self.cauldrons if c.being_carried and c.position not in self.rocks]:
			return "u"
		if (x,y) in [c.position for c in self.cauldrons if c.being_carried and c.position in self.rocks]:
			return "w"
		if (x,y) in self.rocks:
			if (x,y) not in self.discovered:
				self.discovered.append((x,y))
			return "#"
		if (x,y) == self.trgt:
			if self.inHarshLight(self.trgt):
				return " "
			elif self.inLight(self.trgt):
				return "a"
			else:
				return "@"
		elif (x,y) in self.preds:
			if self.inHarshLight((x,y)):
				return "G"
			elif self.inLight((x,y)):
				return pred_in_light_char
			else:
				return "X"
			
		if (x,y) == self.flGetter:
			return "|"
			
		if (x,y) == self.castGetter:
			return "o"
			
		if (x,y) == self.trapGetter:
			return "A"
		
		if (x,y) == self.torchGetter:
			return "y"

		if (x,y) == self.beamGetter:
			return "+"
			
		if (x,y) == self.bombGetter:
			return "b"

		if (x,y) == self.snakeGetter:
			return "S"
			
		if (x,y) == self.pingGetter:
			return "\""
			
		if (x,y) in self.lpexps:
			return "="
			
			
			
			
		if (x,y) in [beam.pos for beam in self.beams]:
			return "+"
			
		if (x,y) in [ping.pos for ping in self.pings if ping.dir in (N,S) and not ping.lingering]:
			return "\""
		
		if (x,y) in [ping.pos for ping in self.pings if ping.dir in (E, W) and not ping.lingering]:
			return ":"
		
		if (x,y) in [snk.position for snk in self.snakes if not snk.foundWall]:
			return "-"
			
		if (x,y) in [snk.position for snk in self.snakes if snk.foundWall and snk.rh]:
			return "s"
		
		if (x,y) in [snk.position for snk in self.snakes if snk.foundWall and not snk.rh]:
			return "z"
			
			
		else:
			if INSANITY:
				if (x,y) in INSANITY_DICT:
					if random.random() < INSANITY_RET_THRES:
						return INSANITY_DICT[(x,y)]
					else:
						if random.random() < INSANITY_THRES:
							ret = random.choice(INSANITY_CHARS)
							INSANITY_DICT[(x,y)] = ret
							return ret
						else:
							del INSANITY_DICT[(x,y)]
							return "."
				else:
					if random.random() < INSANITY_THRES:
						ret = random.choice(INSANITY_CHARS)
						INSANITY_DICT[(x,y)] = ret
						return ret
					else:
						return "."
			
			else:
				return "."

	def getChr(self, x, y):
		if (x,y) == self.plyr:
			c = self.getPlyrChr()
			self.lastchr = c
			return c
		if (x,y) in self.bombs:
			return "\""
		if (x,y) in self.traps:
			return "%"
		if (x,y) in self.torches:
			return "Y"
		if (x,y) in [cast.pos for cast in self.casts]:
			return "O"
			
		if not self.inView((x,y)) and ((x,y) not in self.discovered) and not ((len(self.lpexps) == 0) and (x,y) in [self.flGetter, self.castGetter, self.trapGetter, self.torchGetter, self.beamGetter]):
			return " "
		elif not self.inView((x,y)) and ((x,y) in self.discovered):
			return "*"
		if (x,y) in self.rocks:
			if (x,y) not in self.discovered:
				self.discovered.append((x,y))
			return "#"
		if (x,y) == self.trgt:
			if (self.inFlashlight(self.trgt) or self.inLantern(self.trgt) or self.inCast(self.trgt) or self.inBeam(self.trgt) or self.inPing(self.trgt)):
				return "a"
			else:
				return "@"
		elif (x,y) in self.preds:
			if self.inTorch((x,y)):
				return "G"
			if self.inLight((x,y)):
				return "&"
			else:
				return "X"
			
		if (x,y) == self.flGetter:
			return "|"
			
		if (x,y) == self.castGetter:
			return "o"
			
		if (x,y) == self.trapGetter:
			return ":"
		
		if (x,y) == self.torchGetter:
			return "y"

		if (x,y) == self.beamGetter:
			return "+"
			
		if (x,y) == self.bombGetter:
			return "'"
			
		if (x,y) in self.lpexps:
			return "="
			
			
			
		#if (x,y) in [beam.pos for beam in self.beams]:
		#	return "+"
			
		else:
			return "."
			
	def getAttemptedPathTo(self, p1, p2, limit = None, passthrough = 0):
		past = passthrough
		x1,y1 = p1
		x2,y2 = p2
		dx = x2 - x1
		dy = y2 - y1
		retlist = [p1]
		steps = max(abs(dx), abs(dy))
		if steps == 0:
			retlist.append(p2)
			return retlist
		if abs(dx) > abs(dy):
			slope = dy / dx
			if dx > 0:
				step = 1
			else:
				step = -1

			if dy > 0:
				rnd = math.ceil
			else:
				rnd = math.floor

			for i in range(0, dx, step):
				px = x1 + i
				py = int(rnd(slope* (i) + y1))
				testpoint = (px, py)
				if limit is not None and (self.getSqEulDist(testpoint, p1) > (limit ** 2)):
					return retlist
				retlist.append(testpoint)
				if ((not self.allowed(testpoint) and past == 0) or (testpoint == self.trgt)):
					return retlist
				if not self.allowed(testpoint) and past > 0:
					past -= 1
		else:
			slope = dx / dy
			if dy > 0:
				step = 1
			else:
				step = -1

			if dx > 0:
				rnd = math.ceil
			else:
				rnd = math.floor
			for i in range(0, dy, step):
				py = y1 + i
				px = int(rnd(slope* (i) + x1))
				testpoint = (px, py)
				if limit is not None and (self.getSqEulDist(testpoint, p1) > (limit ** 2)):
					return retlist
				retlist.append(testpoint)
				if ((not self.allowed(testpoint) and past == 0) or (testpoint == self.trgt)):
					return retlist
				if not self.allowed(testpoint) and past > 0:
					past -= 1
		return retlist
					
	def getPointsInView(self, p1, limit = None):
		retset = set()
		
		boundary = self.boundarySet
		if limit is not None:
			boundary = set()
			x,y = p1
			for i in range(int(limit+2)):
				lim = int(limit) + 1
				boundary.add((x + i, y + lim))
				boundary.add((x - i, y + lim))
				boundary.add((x + i, y - lim))
				boundary.add((x - i, y - lim))
				boundary.add((x + lim, y + i))
				boundary.add((x + lim, y - i))
				boundary.add((x - lim, y + i))
				boundary.add((x - lim, y - i))
			
		for point in boundary:
			#print(point)
			#print(p1)
			#print(limit)
			#print("retset")
			#print(retset)
			#print("nextset")
			#print(self.getAttemptedPathTo(p1, point, limit = limit))
			retset.update(self.getAttemptedPathTo(p1, point, limit = limit))
		return retset

	def hasAvailableStraightLine(self, p1, p2):
		x1,y1 = p1
		x2,y2 = p2
		dx = x2 - x1
		dy = y2 - y1
		steps = max(abs(dx), abs(dy))
		#print(steps)
		if steps == 0:
			return True
		if abs(dx) > abs(dy):
			slope = dy / dx
			if dx > 0:
				step = 1
			else:
				step = -1
			for i in range(0, dx, step):
				px = x1 + i 
				py = int(slope*(i) + y1)
				testpoint = (px,py)
				#print(testpoint)
				if (not self.allowed(testpoint)) or (testpoint in self.preds) or (testpoint == self.trgt):
					return False
				
			return True
		else:
			slope = dx / dy
			if dy > 0:
				step = 1
			else:
				step = -1
			for i in range(0, dy, step):
				py = y1 + i 
				px = int(slope*(i) + x1)
				testpoint = (px,py)
				#print(testpoint)
				if (not self.allowed(testpoint)) or (testpoint in self.preds) or (testpoint == self.trgt):
					return False
				
			return True

	def hasVerbAvailableStraightLine(self, p1, p2):
		x1,y1 = p1
		x2,y2 = p2
		dx = x2 - x1
		dy = y2 - y1
		steps = max(abs(dx), abs(dy))
		print(steps)
		if steps == 0:
			return True
		if abs(dx) > abs(dy):
			slope = dy / dx
			if dx > 0:
				step = 1
			else:
				step = -1
			for i in range(0, dx, step):
				px = x1 + i 
				py = int(slope*(i) + y1)
				testpoint = (px,py)
				print(testpoint)
				if (not self.allowed(testpoint)) or (testpoint in self.preds) or (testpoint == self.trgt):
					return False
				
			return True
		else:
			slope = dx / dy
			if dy > 0:
				step = 1
			else:
				step = -1
			for i in range(0, dy, step):
				py = y1 + i 
				px = int(slope*(i) + x1)
				testpoint = (px,py)
				print(testpoint)
				if (not self.allowed(testpoint)) or (testpoint in self.preds) or (testpoint == self.trgt):
					return False
				
			return True
			
	def getPlyrChr(self):
		if self.lastop in (OFF, ON, L):
			return self.lastchr
		if self.lastmovop == N:
			return "^"
		elif self.lastmovop == W:
			return "<"
		elif self.lastmovop == S:
			return "v"
		elif self.lastmovop == E:
			return ">"
		else:
			return "O"
			
	def inTorch(self, pt):
		return any((self.getSqEulDist(pt, trch) <= (TORCH_RANGE ** 2) and self.hasAvailableStraightLine(trch, pt)) for trch in self.torches)
		
		
		
		
	def inCast(self, pt):
		return any(pt in self.getPointsInView(cast.pos, limit=self.getCastRange()) for cast in self.casts)
	
	def inSnake(self, pt):
		return any(pt in self.getPointsInSnake(snk) for snk in self.snakes)
	
	
	def inPing(self,pt):
		return any(pt in self.getPointsInPing(ping) for ping in self.pings)
	def inBeam(self, pt):
	
		return (any(pt in self.getPointsInBeam(beam) for beam in self.beams))
		#for beam in self.beams:
		#	bx,by = beam.pos
		#	x,y = pt
		#	if beam.dir in (N, S):
		#		if x == bx and (abs(by - y) <= self.getBeamRange()) and self.hasAvailableStraightLine(beam.pos, pt):
		#			
		#			return True
		#	elif beam.dir in (E, W):
		#		if y == by and (abs(bx - x) <= self.getBeamRange()) and self.hasAvailableStraightLine(beam.pos, pt):
		#			return True
		#return False
	
	def getPointsInBeam(self, beam):
		result = set()
		bx,by = beam.pos
		if beam.dir in (N, S):
			result.update(self.getAttemptedPathTo(beam.pos, (bx, by + self.getBeamRange()), passthrough = beam.passthrough))
			result.update(self.getAttemptedPathTo(beam.pos, (bx, by - self.getBeamRange()), passthrough = beam.passthrough))
		else:
			result.update(self.getAttemptedPathTo(beam.pos, (bx + self.getBeamRange(), by), passthrough = beam.passthrough))
			result.update(self.getAttemptedPathTo(beam.pos, (bx - self.getBeamRange(), by), passthrough = beam.passthrough))
		return result           
		
	def getPointsInPing(self, ping):
		result = set()
		bx,by = ping.pos
		
		
		result.update([mve(ping.pos, dr) for dr in carddrs if dr != ping.dir or PING_SEE_AHEAD])
		
		if PING_LINGER_BIG and ping.lingering:
			i = alldrs.index(ping.dir)
			result.update([mve(ping.pos, alldrs[(i + j) % 8]) for j in (-1, 0, 1)])
		
		result.update([ping.pos])
		
		#return [(bx + i), (by + j) for i in (-1, 0, ]
		
		#if ping.dir in (N, S):
			#result.update(self.getAttemptedPathTo(ping.pos, (bx, by + self.getBeamRange()), passthrough = ping.passthrough))
			#result.update(self.getAttemptedPathTo(ping.pos, (bx, by - self.getBeamRange()), passthrough = ping.passthrough))
		#	result.update([(bx - 1, by), (bx + 1, by), ping.pos])
		#else:
			#result.update(self.getAttemptedPathTo(ping.pos, (bx + self.getBeamRange(), by), passthrough = ping.passthrough))
			#result.update(self.getAttemptedPathTo(ping.pos, (bx - self.getBeamRange(), by), passthrough = ping.passthrough))
		#	result.update([(bx, by-1), (bx,by+1), ping.pos])
		return result           
		
	def getPointsInSnake(self, snake):
		if not snake.foundWall:
			return [snake.position]
		return [mve(snake.position, dr) for dr in [N,S,E,W,(0,0), NW, NE, SW, SE]]
	
	def inFlashlight(self,pt):
		return self.lighton and pt in self.getPointsInFlashlight()
		#flashlight = False
		#if self.inLantern(pt):
		#	return True
		#x = pt[0]
		#y = pt[1]
		#plx = self.plyr[0]
		#ply = self.plyr[1]
		#
		#delx = abs(x - plx)
		#dely = abs(y - ply)
		#if self.lastmovop == W:
		#	flashlight = (x < plx) and (delx < self.sight) and (dely < delx)
		#elif self.lastmovop == E:
		#	flashlight = (x > plx) and (delx < self.sight) and (dely < delx)
		#elif self.lastmovop == S:
		#	flashlight = (y > ply) and (dely < self.sight) and (dely > delx)
		#elif self.lastmovop == N:
		#	flashlight = (y < ply) and (dely < self.sight) and (dely > delx)
		#return flashlight and (self.lighton) and self.hasAvailableStraightLine(self.plyr, pt)
		
	def getPointsInFlashlight(self):
		boundary = []
		plx,ply = self.plyr
		
		setting = self.getCurrentFLSetting()
		flrange = setting.range
		slope = setting.slope
		
		if self.lastmovop in (N, S):
			plx += .5
			minx = int(plx - (flrange * slope))
			maxx = int(plx + (flrange * slope))
			if self.lastmovop == N:
				boundy = ply - flrange
			else:
				boundy = ply + flrange
			boundary = [(x, boundy) for x in range(minx, maxx + 1)]
		elif self.lastmovop in (E, W):
			ply += .5 
			miny = int(ply - (flrange * slope))
			maxy = int(ply + (flrange * slope ))
			if self.lastmovop == W:
				boundx = plx - flrange
			else:
				boundx = plx + flrange
			boundary = [(boundx, y) for y in range(miny, maxy + 1)]
		result = set()
		for pt in boundary:
			result.update(self.getAttemptedPathTo(self.plyr, pt))
		return result
		
	def inLantern(self, pt):
		return self.lastop == L and (self.getSqEulDist(pt, self.plyr) <= LANTERN_RANGE) and self.hasAvailableStraightLine(self.plyr, pt)
			
	def inLight(self, pt):
		return self.inLantern(pt) or self.inFlashlight(pt) or self.inCast(pt) or self.inTorch(pt) or self.inBeam(pt)
		
	def inHarshLight(self, pt):
		return self.inCast(pt) or self.inBeam(pt) or self.inPing(pt) or self.inSnake(pt) or (self.inFlashlight(pt) and self.getCurrentFLSetting().is_harsh)
			
	#def inView(self, pt):
	#	#return True
	#	#return self.hasAvailableStraightLine(self.plyr, pt)
	#	#radiating = (len(self.lpexps) == 0) and  self.hasAvailableStraightLine(self.plyr, pt)
	#	x = pt[0]
	#	y = pt[1]
	#	plx = self.plyr[0]
	#	ply = self.plyr[1]
	#	
	#	delx = abs(x - plx)
	#	dely = abs(y - ply)
	#	facing = False
	#	
	#	if self.lastmovop == W:
	#		facing = (x <= plx) and (dely <= delx + 1)
	#	elif self.lastmovop == E:
	#		facing = (x >= plx) and (dely <= delx + 1)
	#	elif self.lastmovop == S:
	#		facing = (y >= ply) and (dely + 1 >= delx)
	#	elif self.lastmovop == N:
	#		facing = (y <= ply) and (dely + 1 >= delx)
	#	
	#	reflection = self.lighton and (self.getCDist(pt, self.plyr) < 2)
	#	
	#	closeby = (self.getCDist(pt, self.plyr) < 2) and ((facing or reflection) and self.hasAvailableStraightLine(self.plyr,pt))
	#	#flashlight = self.inFlashlight(pt)
	#	flashlight = False
	#	#torch = self.inTorch(pt)
	#	#cast = self.inCast(pt)
	#	cast = False
	#	#beam = self.inBeam(pt)
	#	return closeby
		
	def getPointsCloseBy(self):
		compass = [N, NE, E, SE, S, SW, W, NW]
		
		flreflection = self.lighton and (self.flSettingInd > 0)
		
		if not flreflection:
			shift = {E:0, S: 2, W:4, N: 6}[self.lastmovop]
			cshift = compass[shift:] + compass[:shift]
			drs = cshift[:5]
		else:
			drs = compass
		return [mve(self.plyr, dr) for dr in drs]


	def getDist(self, cord1, cord2):
		return abs(cord1[0] - cord2[0]) + abs(cord1[1] - cord2[1])
		
	def getCDist(self, cord1, cord2):
		return max(abs(cord1[0] - cord2[0]), abs(cord1[1] - cord2[1]))
		
	def getSqEulDist(self, cord1, cord2):
		return ((cord1[0] - cord2[0]) ** 2) + ((cord1[1] - cord2[1]) ** 2)

	def getCharGrid(self):
		return [[self.getChr(i,j) for i in range(self.xm)] for j in range(self.ym)]

	def gridToString(self):
		grd = self.getCharGrid()
		
		return "\n".join("".join(line) for line in grd)
		
	def getLPMax(self):
		return LPLEVELS[len(self.lpexps)]

	#def gridToString(self):
	#	grd = self.getCharGrid()
	#	end = "+" + "-"*self.xm + "+"
	#	
	#	lines = [end]l
	#	lines.extend("|" + "".join(line) + "|" for line in grd)
	#	lines.append(end)
	#	
	#	return "\n".join(lines)

		
	def inGrid(self, pt):
		x = pt[0]
		y = pt[1]
		return not any([x >= self.xm, x < 0, y >= self.ym, y < 0])
		
	def isRock(self, pt):
		if NEW_ROCK_ALG:
			x,y = pt
			return not self.map[y][x] == " "
		else:
			return pt in self.rocks
			
		
	def allowed(self, pt):
		return self.inGrid(pt) and (not self.isRock(pt)) and (pt not in self.traps) and (pt not in self.preds) and (pt not in [c.position for c in self.cauldrons if not c.being_carried]) and (pt not in [b.position for b in self.bombs])

	def moveTrgt(self):
		
		alloweddirs = [dr for dr in trgtdrs if self.allowed(mve(self.trgt, dr)) and (mve(self.trgt, dr) != self.plyr)]
		if (not (self.inFlashlight(self.trgt) or self.inLantern(self.trgt) or self.inCast(self.trgt) or self.inPing(self.trgt) or self.inBeam(self.trgt))) or self.getDist(self.plyr, self.trgt) > 15:
			self.trgt = mve(self.trgt, random.choice(alloweddirs))
			return
		else:
			dsts = {dr : self.getDist(self.plyr, mve(self.trgt, dr)) for dr in alloweddirs}

			self.trgt = mve(self.trgt, max(dsts, key = dsts.get))
			
	def movePred(self, pred):
		#self.spotted = False
		if pred not in self.preds:
			print("Curiously")
			return
		movt = ENEMY_MV_THRES
		if self.inLight(pred):
			movt = ENEMY_LIGHT_MV_THRES
		if self.inHarshLight(pred):
			movt = ENEMY_HARSH_LIGHT_MV_THRES
		val = random.random()
		if val < movt:
			#print("Can't move because of " + str(val))
			return
			
		alloweddirs = [dr for dr in preddrs if self.allowed(mve(pred, dr))]
		

		
		if len(alloweddirs) and ((self.getDist(self.plyr, pred) > scale(PRED_THRESH, 2)) or (not self.hasAvailableStraightLine(self.plyr, pred))):
			newpred = mve(pred, random.choice(alloweddirs))
			self.preds.remove(pred)
			self.preds.append(newpred)
			
		else:
			self.spotted = True
			dsts = {dr : self.getDist(self.plyr, mve(pred, dr)) for dr in alloweddirs}
			if len(dsts) == 0:
				return
			#print(dsts)
			newpred = mve(pred, min(dsts, key = dsts.get))
					
			
			self.preds.remove(pred)
			self.preds.append(newpred)
			
		
		for b in self.bombs:
			if b.exploding:
				for bm in [mve(b.position, dr) for dr in bmbdrs]:
					if newpred == bm:
						self.preds.remove(newpred)
						self.bombs.remove(b)
						
						randpred = (random.randint(0, self.xm-1), random.randint(0, self.ym -1))
						while not (self.allowed(randpred) and (randpred not in self.preds) and (randpred != self.trgt) and (randpred != self.plyr)) :
							randpred = (random.randint(0, self.xm-1), random.randint(0, self.ym -1))
						self.preds.append(randpred)
						return
		
		if PING_DESTROYS_PRED:
			for p in self.pings[:]:
				if newpred == p.pos:
					self.preds.remove(newpred)
					self.pings.remove(p)
					randpred = (random.randint(0, self.xm-1), random.randint(0, self.ym -1))
					while not (self.allowed(randpred) and (randpred not in self.preds) and (randpred != self.trgt) and (randpred != self.plyr)) :
						randpred = (random.randint(0, self.xm-1), random.randint(0, self.ym -1))
					self.preds.append(randpred)
					return
					
					
				if PING_WIDE_DESTROY:
					idx = carddrs.index(p.dir)
					otherpts = [mve(p.pos, nxt) for nxt in [carddrs[(idx + 1) % 4], carddrs[(idx + 3) % 4]]]
					for pt in otherpts:
						if pt in self.preds:
							ping.over = True
							self.preds.remove(pt)
							randpred = (random.randint(0, self.xm-1), random.randint(0, self.ym -1))
							while not (self.allowed(randpred) and (randpred not in self.preds) and (randpred != self.trgt) and (randpred != self.plyr)) :
								randpred = (random.randint(0, self.xm-1), random.randint(0, self.ym -1))
							self.preds.append(randpred)
				
	def nearCauldron(self):
		return any(mve(self.plyr, dr) in [c.position for c in self.cauldrons if not c.being_carried ] for dr in alldrs)
				
	def getRecoveryModifier(self):
		modifier = 1
		if any(mve(self.plyr, dr) in self.traps for dr in carddrs):
			modifier *= TRAP_RECOVERY_MODIFIER
		if self.nearCauldron():
			modifier *= CAULDRON_RECOVERY_MODIFIER
		return modifier
				
	def getRecoveryRate(self):
		return int(LPRECOVERIES[len(self.lpexps)] * self.getRecoveryModifier())
	
	def getBeamRange(self):
		return BEAM_RANGES[len(self.lpexps)]
	
	def getCastMax(self):
		return CASTMAXES[len(self.lpexps)]
		
	def getCastRange(self):
		return CASTRANGES[len(self.lpexps)]
		
	def getLevelName(self):
		return LEVELNAMES[len(self.lpexps)]
		
	def getSnakeMaxAge(self):
		if SNAKE_USE_PER_LEVEL_AGE:
			return  (len(LEVELNAMES) - len(self.lpexps) - 1) * SNAKE_MAX_AGE_PER_LEVEL
		else:
			return SNAKE_MAX_AGE

	def getStatus(self):
		flstate = "FL "
		if self.lighton:
			flstate += "ON" + " " + self.getCurrentFLSetting().name
		if not self.lighton and self.hasFL:
			flstate += "OFF"
		if not self.hasFL:
			flstate = ""
			
		if self.getRecoveryModifier() > 1:
			mod = "!"
		else:
			mod = ""
			
		sptd = ""
		if self.spotted:
			sptd = "SPOTTED "
		
		if self.hasTrap:
			trp = str(TRAP_MAX - len(self.traps)) + " TRP"
		else:
			trp = ""
			
		if self.hasBomb:
			bmb = str(BOMB_MAX - len(self.bombs)) + " BMB"
		else:
			bmb = ""
			
		if self.hasBeam:
			bm = "BEAM (" + str(self.getBeamRange()) + ") "
			if self.beamOn:
				bm += "ON"
			else:
				bm += "OFF"
		else:
			bm = ""
			
		if self.hasTorch:
			trch = str(TORCH_MAX - len(self.torches)) + " TRCH"
		else:
			trch = ""
			
		if self.hasCast:
			cst = str(self.getCastMax() - len(self.casts)) + " CST (" + str(self.getCastRange()) +")"
		else:
			cst = ""

		snk = ""
		if self.hasSnake:
			snk = str(SNAKE_MAX - len(self.snakes)) + " SNK (" + str(self.getSnakeMaxAge()) + ")"
			
		if self.hasPing:
			png = "PING"
		else:
			png = ""
		
		if self.lighton:
			lc = self.getCurrentFLSetting().cost
		else:
			lc = 0
			
		if self.beamOn:
			lc += BEAM_COST
			
		if len(self.snakes):
			lc += (SNAKE_COST * len(self.snakes))
			
		ct = (CAST_COST * len(self.casts)) + (TORCH_COST * len(self.torches)) + lc - (self.getRecoveryRate())
		if ct >= 0:
			cs = "-" + str(ct)
		else:
			if self.lightpower == self.getLPMax():
				cs = "+0"
			else:
				cs = "+" + str(abs(ct))
		
		lp = "LP: " + str(self.lightpower) + " (" + cs + ")"
		
		if not any([self.hasTorch, self.hasFL, self.hasCast, self.hasBeam, self.hasSnake, self.hasPing]):
			lp = ""
			
		levname = self.getLevelName()
		levname += " (" + str(len(LEVELNAMES) - len(self.lpexps)) + ")"
			
		if self.hasCast and self.hasFL and self.hasTorch and self.hasTrap and self.hasBeam and self.hasBomb and self.hasSnake and self.hasPing:
			levname += "+"
			
		#print ("")
		if SHOW_ALL_STATUS_GAPS:
			whatToPrint = [i for i in [levname, mod, flstate, trp, bmb, bm,png, trch, cst, snk, lp, sptd]]
		else:
			whatToPrint = [i for i in [levname, mod, flstate, trp, bmb, bm,png, trch, cst, snk, lp, sptd] if len(i) > 0]
		printString = " | ".join(whatToPrint)
		if len(printString) > 70:
		
			leng = len(whatToPrint)
			split1, split2= whatToPrint[:leng // 2 + 1], whatToPrint[leng // 2 + 1:]
			if len(split1) > 50 or len(split2) > 50:
				incr = leng // 3
				sp1, sp2, sp3 = whatToPrint[:incr], whatToPrint[incr:2*incr], whatToPrint[2*incr:]
				return "\n".join(" | ".join(s) for s in (sp1, sp2, sp3))
			return(" | ".join(split1) + "\n" + " | ".join(split2))
		else:
			return(printString)
		
		#print(str(d1) + " | " + str(d2) + " | " + state + " | "  + trp + " | " + trch + " | " + sptd + " ")
		#print(" | ".join(i for i in [state, trp, trch, cst, lp, sptd] if len(i) > 0))
		
	def get_bonus(self, amount = 5):
		self.lightpower = min(self.lightpower + amount, self.getLPMax())

	def pm(self, scr):
		#inp = input("> ").upper()
		curses.curs_set(0)
		scr.nodelay(1)
		self.spotted = False
		selfblewup = False
		currtime = time.time()
		lastFrame = time.time()
		
		
		while True:
			enmv = ((self.turns % (FPS // ENEMYPS)) == 0)
			castmv = ((self.turns % (FPS // CASTPS)) == 0)
			beamcreatemv = ((self.turns % (FPS // BEAMCREATEPS)) == 0)
			trgtmv = ((self.turns % (FPS // TRGTPS)) == 0)
			bmbmv = ((self.turns % (FPS // BOMBPS)) == 0)
			x = msvcrt.kbhit()
			if x:
				try:
					inpraw = msvcrt.getch()
					if inpraw == b'\xe0':
						arrow = msvcrt.getch()
						op = ARROWOP[arrow]
						
					else:
						i = inpraw.decode("ascii")
						if len(i) > 0 and i in "QX":
							break
						inp = i.upper()
						if inp in prfxs or inp == "P":
							try:
								if inp == "P":
									scr.addstr(self.ym + 1, 0, "---PAUSED---")
									scr.refresh()
								scraw = msvcrt.getch()
								if scraw == b'\xe0':
									sc = ARROWCODE.get(msvcrt.getch(), "X")
								else:
									sc = scraw.decode("ascii").upper()
								inp += sc
							except UnicodeDecodeError:
								pass
						
						op = plyrdrnames.get(inp, NOP)
				except UnicodeDecodeError:
					op = NOP
				#print ("INPUT IS " + inp)
			else:
				inp = ""
				op = NOP
			#op = plyrdrnames.get(inp, NOP)
			

			
			lastFrame = currtime
			currtime = time.time()
			
			if bmbmv:
				for bmb in self.bombs[:]:
					bmb.age -= 1
					if bmb.age == 0:
						bmb.exploding = True
					elif bmb.age < 0:
						self.bombs.remove(bmb)
						if bmb.blewselfup:
							return -2, self.walls_destroyed
							
			
			for snk in self.snakes[:]:
				snk.update(self.allowed, self.getSnakeMaxAge())
				if snk.dead:
					self.snakes.remove(snk)
			
			for bmb in self.bombs:
				if bmb.exploding:
					if self.plyr in [mve(bmb.position, dr) for dr in bmbdrs] and BOMBS_HURT_SELF:
						bmb.blewselfup = True
				
					if BOMBS_BREAK_WALL:
						for bm in [mve(bmb.position, dr) for dr in bmbdrs if mve(bmb.position, dr) in self.rocks[:]]:
							
							self.rocks.remove(bm)
							self.walls_destroyed += 1
							
							if bm in self.discovered:
								self.discovered.remove(bm)
							x,y = bm
							self.map[y][x] = " "
				
					for ps in [mve(bmb.position, dr) for dr in bmbdrs if mve(bmb.position, dr) in self.preds]:
						
						self.preds.remove(ps)
						
						randpred = (random.randint(0, self.xm-1), random.randint(0, self.ym -1))
						while not (self.allowed(randpred) and (randpred not in self.preds) and (randpred != self.trgt) and (randpred != self.plyr)) :
							randpred = (random.randint(0, self.xm-1), random.randint(0, self.ym -1))
						self.preds.append(randpred)
						
			if PING_DESTROYS_ROCKS:
				for ping in self.pings:
					if ping.pos in self.rocks[:]:
						self.rocks.remove(ping.pos)
						if ping.pos in self.discovered:
							self.discovered.remove(ping.pos)
						x,y = ping.pos
						self.map[y][x] = " "
					if PING_WIDE_DESTROY:
						for p in [mve(ping.pos, dr) for dr in carddrs if (dr != ping.dir) and mve(ping.pos, dr) in self.rocks[:]]:
							self.rocks.remove(p)
							if p in self.discovered:
								self.discovered.remove(p)
							x,y	= p
							self.map[y][x] = " "
			
			if PING_DESTROYS_PRED:
				for ping in self.pings:
					if PING_WIDE_DESTROY:
						idx = carddrs.index(ping.dir)
						otherpts = [mve(ping.pos, nxt) for nxt in [carddrs[(idx + 1) % 4], carddrs[(idx + 3) % 4]]]
						for pt in otherpts:
							if pt in self.preds:
								ping.over = True
								self.preds.remove(pt)
								randpred = (random.randint(0, self.xm-1), random.randint(0, self.ym -1))
								while not (self.allowed(randpred) and (randpred not in self.preds) and (randpred != self.trgt) and (randpred != self.plyr)) :
									randpred = (random.randint(0, self.xm-1), random.randint(0, self.ym -1))
								self.preds.append(randpred)
					
					if ping.pos in self.preds:
						ping.over = True
						self.preds.remove(ping.pos)
						randpred = (random.randint(0, self.xm-1), random.randint(0, self.ym -1))
						while not (self.allowed(randpred) and (randpred not in self.preds) and (randpred != self.trgt) and (randpred != self.plyr)) :
							randpred = (random.randint(0, self.xm-1), random.randint(0, self.ym -1))
						self.preds.append(randpred)
					
					
			
			if enmv:
				self.spotted = False
			self.turns += 1
			#print(inp)
			#if inp == "" and len(self.casts) == 0:
			#	op = self.lastmovop
			if op == L:
				if self.lightpower >= LANTERN_COST and self.hasFL:
					self.lightpower -= LANTERN_COST
				else:
					op = NOP
					
			if op == B:
				if self.lightpower >= BEAM_COST and self.hasBeam:
					self.lightpower -= BEAM_COST
				else:
					op = NOP
					
			self.lastop = op
			
			self.movePlyr(op, beamcreatemv)
			
			if self.plyr == self.trapGetter:
				if self.trapGetter in self.discovered:
					self.discovered.remove(self.trapGetter)
				self.trapGetter = None
				self.hasTrap = True
				self.get_bonus(10)
				
			if self.plyr == self.castGetter:
				if self.castGetter in self.discovered:
					self.discovered.remove(self.castGetter)
				self.castGetter = None
				self.hasCast = True
				self.get_bonus()

			if self.plyr == self.flGetter:
				if self.flGetter in self.discovered:
					self.discovered.remove(self.flGetter)
				self.flGetter = None
				self.hasFL = True
				self.get_bonus()
				
			if self.plyr == self.torchGetter:
				if self.torchGetter in self.discovered:
					self.discovered.remove(self.torchGetter)
				self.torchGetter = None
				self.hasTorch = True
				self.get_bonus()
				
			if self.plyr == self.beamGetter:
				if self.beamGetter in self.discovered:
					self.discovered.remove(self.beamGetter)
				self.beamGetter = None
				self.hasBeam = True
				self.get_bonus()
				
			if self.plyr == self.bombGetter:
				if self.bombGetter in self.discovered:
					self.discovered.remove(self.bombGetter)
				self.bombGetter = None
				self.hasBomb = True
				self.get_bonus()
				
			if self.plyr == self.snakeGetter:
				if self.snakeGetter in self.discovered:
					self.discovered.remove(self.snakeGetter)
				self.snakeGetter = None
				self.hasSnake = True
				self.get_bonus()

			if self.plyr == self.pingGetter:
				if self.pingGetter in self.discovered:
					self.discovered.remove(self.pingGetter)
				self.pingGetter = None
				self.hasPing = True
				self.get_bonus()
				
				
			if self.plyr in self.lpexps:
				if self.plyr in self.discovered:
					self.discovered.remove(self.plyr)
				self.lpexps.remove(self.plyr)
				self.spawnPreds()
			
			losinglight = (self.lighton) or (len(self.torches) >= 1)  or (len(self.casts) >= 1)or (op == L) or self.beamOn or len(self.snakes)

			if self.lightpower < self.getLPMax() and enmv:
				#self.lightpower += RECOVERY_RATE
				self.lightpower += (self.getRecoveryRate())
				if self.lightpower > self.getLPMax():
					self.lightpower = self.getLPMax()
			
			if self.nearCauldron() and CAULDRON_REMOVES_LIGHT:
				self.torches = []
				self.casts = []
				self.snakes = []
				self.beamOn = False
				#self.beams = []
				self.lighton = False
				self.flSettingInd = 0
				
			if losinglight:
				if op != L and self.lighton:
					cost = self.getCurrentFLSetting().cost
				else:
					cost = 0
				if self.beamOn:
					cost += BEAM_COST
				cost += (TORCH_COST * len(self.torches))
				cost += (CAST_COST * len(self.casts))
				cost += (SNAKE_COST * len(self.snakes))
				#print("Cost is " + str(cost))
				
				if (self.lightpower + self.getRecoveryRate()) < cost:
					#(self.lightpower < 0 and losinglight):
					self.lightpower = 0
					self.torches = []
					self.casts = []
					self.snakes = []
					self.beamOn = False
					#self.beams = []
					self.lighton = False
					self.flSettingInd = 0
				if enmv:
					self.lightpower = max(0, self.lightpower - cost)
					
				
			
			if self.plyr in self.torches:
				self.torches.remove(self.plyr)
			if self.plyr == self.trgt:
				print("You won in " + str(self.turns) + " turns!")
				return 1, self.walls_destroyed
			for pred in self.preds:
					if self.plyr == pred:
						print("You lost in " + str(self.turns) + " turns!")
						return -1, self.walls_destroyed
				
			if trgtmv:
				self.moveTrgt()
			if self.trgt in self.torches:
				self.torches.remove(self.trgt)
			if self.plyr == self.trgt:
				print("You won in " + str(self.turns) + " turns!")
				return 1, self.walls_destroyed
			#self.moveTrgt()
			if castmv:
				for cast in self.casts[:]:
					cast.age += 1
					p = mve(cast.pos, cast.dir)
					if self.allowed(p):
						cast.pos = p
					else:
						cast.over = True
					if cast.pos == self.trgt:
						if any(pred == cast.pos for pred in self.preds):
							cast.over = True
					if cast.over or cast.age > MAX_CAST_AGE:
						self.casts.remove(cast)
					
			
			for beam in self.beams[:]:
				beam.update(self.allowed, self.inGrid)

				if beam.over:
					self.beams.remove(beam)
			for ping in self.pings[:]:
				ping.update(self.allowed, self.inGrid)

				if ping.over:
					self.pings.remove(ping)
			
			if enmv:
				for pred in self.preds[:]:
					#print (self.plyr, pred)
					if self.plyr == pred:
						print("You lost in " + str(self.turns) + " turns!")
						return -1, self.walls_destroyed
					self.movePred(pred)
					if pred in self.torches:
						self.torches.remove(pred)
				for pred in self.preds:
					#print (self.plyr, pred)
					if self.plyr == pred:
						print("You lost in " + str(self.turns) + " turns!")
						return -1, self.walls_destroyed
			#clear()
			#self.print()
			scr.erase()
			scr.addstr(self.ym + 1, 0, self.getStatus())
			if RIGHT_BORDER:
				for i in range(self.ym):
					scr.addch(i, self.xm, RIGHT_BORDER_CHR)

			if VIEW_ALL:
				for i in range(self.ym):
					for j in range(self.xm):
						scr.addch(i, j, self.getIgnChr(j, i))
					
			#radiating
			else:
			
				visiblePoints = set()
				visiblePoints.add(self.plyr)
				visiblePoints.update(self.traps)
				visiblePoints.update(c.position for c in self.cauldrons if c.discovered)
				if CAULDRON_PROVIDES_LIGHT:
					for c in self.cauldrons:
						if c.discovered and c.being_carried:
							visiblePoints.update(self.getPointsInView(c.position, limit = CAULDRON_RANGE))
				visiblePoints.update([b.position for b in self.bombs])
				visiblePoints.update([mve(mve(bm.position, dr), d2) for bm in self.bombs for dr in bmbdrs for d2 in carddrs if bm.exploding])
				if (len(self.lpexps) == 0):
					visiblePoints.update(self.getPointsInView(self.plyr))
					visiblePoints.update([t for t in self.getGetterPositionList() if t is not None])
	
				visiblePoints.update(self.getPointsCloseBy())
				
				if self.lighton:
					visiblePoints.update(self.getPointsInFlashlight())
				
				for cast in self.casts:
					castPoints = self.getPointsInView(cast.pos, limit=self.getCastRange())
					if CAST_DISCOVER:
						items = self.getItemPositionList()
						for pt in castPoints:
							if pt in items and pt not in self.discovered:
								self.discovered.append(pt)
					visiblePoints.update(castPoints)
					
				for torch in self.torches:
					visiblePoints.update(self.getPointsInView(torch, limit = TORCH_RANGE))
					
				for beam in self.beams:
					beamPoints = self.getPointsInBeam(beam)
					items = self.getItemPositionList()
					for pt in beamPoints:
						if pt in items and pt not in self.discovered:
							self.discovered.append(pt)
					visiblePoints.update(beamPoints)
					
				for ping in self.pings:
					pingPoints = self.getPointsInPing(ping)
					items = self.getItemPositionList()
					for pt in pingPoints:
						if pt in items and pt not in self.discovered:
							self.discovered.append(pt)
					visiblePoints.update(pingPoints)
					
				for snake in self.snakes:
					snakePoints = self.getPointsInSnake(snake)
					items = self.getItemPositionList()
					for pt in snakePoints:
						if pt in items and pt not in self.discovered:
							self.discovered.append(pt)
					visiblePoints.update(snakePoints)
				
				for point in visiblePoints:
					if self.inGrid(point):
					
						plx,  ply = point
						scr.addch(ply, plx, self.getIgnChr(plx, ply))
						
				for disc in self.discovered:
					if disc not in visiblePoints:
						scr.addch(disc[1], disc[0], self.getDscChr(disc[0], disc[1]))
			scr.refresh()
			#print(self.plyr)
			#print((0,0))
			#self.hasVerbAvailableStraightLine(self.plyr,(0, 0))
			sleepTime = 1./FPS - (time.time() - lastFrame)
			if sleepTime > 0:
				time.sleep(sleepTime)
			
		return 0, self.walls_destroyed

	def movePlyr(self, dr, makeBeam):
		#print(dr)
		if (self.heldItem is None and not self.nearCauldron()) or (ALLOW_CAULDRON_ACTION):
			if dr == L:
				return
			if dr in trapdict.keys() and self.hasTrap:
				lx,ly = trapdict[dr]
				x,y = self.plyr
				trapspot = (x+lx, y+ly)
				if trapspot in self.traps:
					self.traps.remove(trapspot)
					return
				else:
					if self.allowed(trapspot) and len(self.traps) < TRAP_MAX:
						if trapspot in self.torches:
							self.torches.remove(trapspot)
						self.traps.append(trapspot)
					return
					
					
			if dr == BOM and self.hasBomb:
				lx,ly = self.lastmovop
				x,y = self.plyr
				bombspot = (x+lx, y+ly)
				if (self.allowed(bombspot) or bombspot in self.preds) and len(self.bombs) < BOMB_MAX:
					self.bombs.append(Bomb(bombspot))
					return
			if dr == BOMC:
				self.bombs = []
				
			if dr == SNK and self.hasSnake:
				if self.lightpower < SNAKE_USAGE_COST:
					return
				self.lightpower -= SNAKE_USAGE_COST
				lx,ly = self.lastmovop
				x,y = self.plyr
				snkspot = (x,y)
				if len(self.snakes) < SNAKE_MAX:
					self.snakes.append(Snake(snkspot, (lx, ly)))
					return
			if dr == SNKC:
				self.snakes = []
				
			if dr == TF and self.hasTrap:
				for lx,ly in (N, S, E, W):
					#lx,ly = trapdict[dr]
					x,y = self.plyr
					trapspot = (x+lx, y+ly)
					if trapspot in self.traps:
						continue
					else:
						if self.allowed(trapspot) and len(self.traps) < TRAP_MAX:
							if trapspot in self.torches:
								self.torches.remove(trapspot)
							self.traps.append(trapspot)
						#return
				
			if dr in (YE, YW, YS, YN) and self.hasTorch:
				lx,ly = torchdict[dr]
				x,y = self.plyr
				torchspot = (x+lx, y+ly)
				if torchspot in self.torches:
					self.torches.remove(torchspot)
					return
				else:
					if self.allowed(torchspot) and len(self.torches) < TORCH_MAX:
						self.torches.append(torchspot)
					return
			if dr == CT:
				self.traps = []
			if dr == CY:
				self.torches = []
			if dr in (CASTN, CASTW, CASTS, CASTE) and self.hasCast:
				castdir = castdict[dr]
				castpos = mve(self.plyr, castdir)
				if self.allowed(castpos) and len(self.casts) < self.getCastMax():
					newcast = Cast(self.plyr, castdir)
					self.casts.append(newcast)
			if dr == CASTFULL and self.hasCast:
				castcount = 0
				succdir = []
				for castdir in (N, S, E, W):
					if self.allowed(mve(self.plyr, castdir)):
						succdir.append(castdir)
				if len(succdir) <= (self.getCastMax() - len(self.casts)):
					for cdir in succdir:
						newcast = Cast(self.plyr, cdir)
						self.casts.append(newcast)
				else:
					for cdir in random.sample(succdir, self.getCastMax() - len(self.casts)):
						newcast = Cast(self.plyr, cdir)
						self.casts.append(newcast)
			if dr == B:
				self.beamOn = not self.beamOn
				
			if dr == O and self.hasFL:
				if self.lighton:
					#turning off
					self.flSettingInd = 0
				self.lighton = not self.lighton
			if dr == PING and self.hasPing and len(self.pings) < PING_LIMIT:
				if self.lightpower < PING_USAGE_COST:
					return
				self.lightpower -= PING_USAGE_COST
				b = Ping(self.plyr, self.lastmovop)
				self.pings.append(b)
				
			if self.beamOn and self.hasBeam and makeBeam:
				succdir = []
				for bdir in (N, S, E, W):
					if True or self.allowed(mve(self.plyr, bdir)):
						succdir.append(bdir)
				if len(succdir) > 0:
					if USE_DUAL_BEAMS:
						vert = (N, S)
						horz = (E, W)
						ors = []
						if N in succdir or S in succdir:
							ors.append(vert)
						if E in succdir or W in succdir:
							ors.append(horz)
						orientation = random.choice(ors)
						for d in orientation:
							newbeam = Beam(self.plyr,d)
							self.beams.append(newbeam)
					else:
						bd = random.choice(succdir)
						newbeam = Beam(self.plyr,bd)
						self.beams.append(newbeam)
					
			if dr == OFF:
				self.lighton = False
				self.flSettingInd = 0
				return
				
			elif dr == FLC and self.hasFL and not self.lighton:
				self.lighton = True
				return
				
			elif dr == FLC and self.hasFL and self.lighton:
				self.bumpFLSetting()
				return
				
			elif dr == FLD and self.hasFL and self.lighton:
				self.dropFLSetting()
				return
				
			elif dr == ON and self.hasFL:
				self.lighton = True
				return
		
		if dr == PKUP and (self.heldItem is None):
			ahead = mve(self.plyr, self.lastmovop)
			for c in self.cauldrons:
				if c.position == ahead and not c.being_carried:
					c.being_carried = True
					self.heldItem = c
					
		elif dr == PKUP and self.heldItem:
			ahead = mve(self.plyr, self.lastmovop)
			if self.allowed(ahead):
				self.heldItem.being_carried = False
				self.heldItem = None
			else:
				return
			
		if dr in [N, S, E, W, NE, NW, SE, SW]:
			orig = self.lastmovop
			self.lastmovop = dr
			res = mve(self.plyr, dr)
			if self.heldItem is not None:
				if self.allowed(res):
					res2 = mve(res, dr)
					if not HELD_ITEMS_BLOCK or self.allowed(res2):
						self.heldItem.position = res2
						self.plyr = res
					else:
						self.heldItem.position = res
				else:
					if HELD_ITEMS_BLOCK:
						self.lastmovop = orig
					else:
						self.heldItem.position = res
			elif self.allowed(res):
				self.plyr = res
	
def play(xm, ym):
	c = Grid(xm, ym)
	#c.print()
	return curses.wrapper(c.pm)



def startGame():
	again = "Y"
	#xm = int(input("Width? "), 10)
	#ym = int(input("Height? "), 10)
	xm = scale(70,1)
	ym = scale(40,1)
	
	wins = 0
	losses = 0 
	quits = 0
	while again == "" or again[0] == "Y":
		out = play(xm, ym)
		if not isinstance(out, int):
			res, wd = out
		else:
			res = out
			wd = 0
		rs = ""
		if res == 1:
			rs = "You won!"
			wins += 1
		if res == 0:
			rs = "You drew."
			quits += 1
		if res == -1:
			rs = "You lost :-("
			losses += 1
		if res == -2:
			rs = "You blew yourself up :-/"
			losses += 1
		print(rs)
		if wd:
			print("You destroyed " + str(wd) + " rocks!")
		print("W/L/D: " + "/".join(str(i) for i in [wins ,losses, quits]))
		again = input("Play again?(Y/N) ").upper().strip()

if __name__=="__main__":
	startGame()
