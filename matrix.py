# Falling Matrix effect in Unix/Linux terminal
# Note: pycurses and a colored terminal is required.

# Import libraries and init
import curses
import random
import time
import sys

SCREEN = curses.initscr()

HEIGHT, WIDTH = SCREEN.getmaxyx()

# Define colors
curses.start_color()
curses.init_pair(1, 219, curses.COLOR_BLACK)
curses.init_pair(2, 125, curses.COLOR_BLACK) 
curses.init_pair(3, 229, curses.COLOR_BLACK)
curses.init_pair(4, 136, curses.COLOR_BLACK) 
curses.init_pair(5, 255, curses.COLOR_BLACK)
curses.init_pair(6, 240, curses.COLOR_BLACK) 

COLOR_THEMES = {
	"red":[
		curses.color_pair(1), # Light
		curses.color_pair(2) # Dark
	],
	"gold":[
		curses.color_pair(3), # Light
		curses.color_pair(4) # Dark
	],
	"white":[
		curses.color_pair(5), # Light
		curses.color_pair(6) # Dark
	]
}

class Column:
	def __init__(self,text,color):
		self.length = random.randint(4,15)
		self.y = -self.length-1
		self.x = random.randint(0,WIDTH-1)
		self.speed = random.randint(2,10)
		self.counter = self.speed
		self.colors = color
		self.chars = []
		for char in text[:HEIGHT]:
			self.chars.append(char)
		# Add extra content if text is shorter than window height
		for i in range(HEIGHT-len(text)):
			self.chars.append(str(random.randint(0,1)))

	def update(self):
		self.counter -= 0.1
		if self.counter <= 0:
			self.y += 1
			self.counter = self.speed 

	def render(self):
		# Calculate out what characters in the charset to show
		start = self.y
		end = self.y + self.length
		if start < 0: start = 0
		if end < 0: end = 0
		displayer_text = self.chars[start : end]
		# Render each character
		for i in range(len(displayer_text)):
			if  0 < self.y + i < HEIGHT-1:
				char = displayer_text[i]
				color = self.colors[1]
				# The first character is white
				if i == len(displayer_text)-1:
					color = self.colors[0]
				SCREEN.addstr(self.y+i,self.x,char,color)

class Matrix:
	def __init__(self):
		self.columns = [] # Current displayed characters

	def update(self):
		# Add columns
		if len(self.columns) < int(WIDTH * 4/5):
			for i in range(int(WIDTH * 4/5) - len(self.columns)):
				self.columns.append(Column("".join(str(random.randint(0,1)) for i in range(HEIGHT)),COLOR_THEMES["white"]))
		# Update Columns
		for i in reversed(range(len(self.columns))):
			col = self.columns[i]
			col.update()
			if col.y > HEIGHT:
				self.columns.pop(i)

	def render(self):
		for col in self.columns:
			col.render()

matrix = Matrix()

# Loop
while True:
	try:
	    SCREEN.refresh()
	    SCREEN.erase()
	    matrix.update()
	    matrix.render()
	except KeyboardInterrupt:
		break

#End Program and Quit
curses.endwin()
sys.exit(0)

