import random
import os
import time
import math

def initialise():
	global dimension
	number_of_cells = dimension**3
	number_of_traps = int((5/100)*number_of_cells) # % of traps
	trap_location = []
	for trap in range(0, number_of_traps):
		check_trap = random.choice(range(0,number_of_cells))
		while check_trap in trap_location:
			check_trap = random.choice(range(0,number_of_cells))
		trap_location.append(check_trap)
	trap_location = sorted(trap_location)
	exit_point = random.choice(range(0,number_of_cells))
	entry_point = random.choice(range(0,number_of_cells))
	while entry_point == exit_point or entry_point in trap_location:
		entry_point = random.choice(range(0,number_of_cells))
	return entry_point, exit_point, trap_location

def display_location(coordinate, trap_nearby):
	padding_character = " "
	padding  = padding_character * (24-len(str(coordinate)))
	os.system('clear')
	print()
	print("          ╔══════════════════════════════════════╗")
	print("          ║       The Infinite Monkey Cage       ║")
	print("          ║                                      ║")
	print("          ║            Current Cell is           ║")
	print(f"          ║              {coordinate}{padding}║")
	print("          ║                                      ║")
	if trap_nearby:
		print("          ║        There is a trap nearby!       ║")
	else:
		print("          ║                                      ║")
	print("          ║                                      ║")
	print("          ╚══════════════════════════════════════╝")
	print()
	return
	
def move_location(location, move_to):
	global dimension
	if move_to in ('up', 'u'):
		location -= dimension**2
	elif move_to in ('down', 'd'):
		location += dimension**2
	elif move_to in ('north', 'n'):
		location -= dimension
	elif move_to in ('south', 's'):
		location += dimension
	elif move_to in ('west', 'w'):
		location -= 1
	elif move_to in ('east', 'e'):
		location += 1
	return location
	
def directions(coordinate):
	global dimension
	valid_directions = []
	up = down = north = south = east = west = False
	if coordinate[0] != 0:
		valid_directions.append("up")
		valid_directions.append("u")
	if coordinate[0] != dimension-1:
		valid_directions.append("down")
		valid_directions.append("d")
	if coordinate[1] != 0:
		valid_directions.append("north")
		valid_directions.append("n")
	if coordinate[1] != dimension-1:
		valid_directions.append("south")
		valid_directions.append("s")
	if coordinate[2] != 0:
		valid_directions.append("west")
		valid_directions.append("w")
	if coordinate[2] != dimension-1:
		valid_directions.append("east")
		valid_directions.append("e")
	return valid_directions
	
def coordinates(location):
	global dimension
	level = int(location/(dimension**2))
	row = int((location-(level*dimension**2))/dimension)
	column = location - (level*dimension**2)-(row*dimension)
	coordinate = [level, row, column]
	return coordinate

def trap_proximity(location, trap_location):
	global dimension
	trap_nearby=False
	locations_nearby = [location+1, location-1, location+dimension, location-dimension, location+(dimension**2), location-(dimension**2)]
	for trap in locations_nearby:
		if trap in trap_location:
			trap_nearby = True
			break  # Exit the loop if a match is found
	return trap_nearby

def areyousure(prompt):
	yes_or_no = ""
	while yes_or_no not in ('y', 'n', 'yes', 'no'):	
		yes_or_no = input(f"{prompt} ")
	if yes_or_no in('y', 'yes'):
		return True
	else:
		return False
	
def win_game():
	os.system('clear')
	print()
	print("          ╔══════════════════════════════════════╗")
	print("          ║       The Infinite Monkey Cage       ║")
	print("          ║                                      ║")
	print("          ║                                      ║")
	print("          ║              Well done!              ║")
	print("          ║                                      ║")
	print("          ║          You found the exit.         ║")
	print("          ║                                      ║")
	print("          ╚══════════════════════════════════════╝")
	print()
	time.sleep(3)
	restart = areyousure("                          Again? ")
	if restart:
		return restart
	else:
		bye()

def loose_game():
	os.system('clear')
	print()
	print("          ╔══════════════════════════════════════╗")
	print("          ║       The Infinite Monkey Cage       ║")
	print("          ║                                      ║")
	print("          ║                                      ║")
	print("          ║                 Oops!                ║")
	print("          ║                                      ║")
	print("          ║         You fell into a trap!        ║")
	print("          ║                                      ║")
	print("          ╚══════════════════════════════════════╝")
	print()
	time.sleep(3)
	restart = areyousure("                          Again? ")
	if restart:
		return restart
	else:
		bye()
		
def introduction():
	os.system('clear')
	print()
	print("          ╔══════════════════════════════════════╗")
	print("          ║       The Infinite Monkey Cage       ║")
	print("          ║                                      ║")
	print("          ║ You find yourself in a brightly lit  ║")
	print("          ║ square room with portals going off   ║")
	print("          ║ in all directions. Your coordinates  ║")
	print("          ║ are displayed as well as a warning.  ║")
	print("          ║                                      ║")
	print("          ╚══════════════════════════════════════╝")
	print()
	time.sleep(10)
	return

def help_screen():
	os.system('clear')
	print()
	print("          ╔══════════════════════════════════════╗")
	print("          ║       The Infinite Monkey Cage       ║")
	print("          ║                                      ║")
	print("          ║ You can go in all 6 directions.      ║")
	print("          ║                                      ║")
	print("          ║ North, South, East and West as well  ║")
	print("          ║ as Up and Down (n, s, e, w, u, d)    ║")
	print("          ║                                      ║")
	print("          ╚══════════════════════════════════════╝")
	print()
	time.sleep(10)
	return

def shortest_way_to_exit(location, exit_point):
	here = coordinates(location)
	there = coordinates(exit_point)
	level = here[0]-there[0]
	row = here[1]-there[1]
	column = here[2]-there[2]
	shortest_distance = positive_integer(level)+positive_integer(row)+positive_integer(column)
	return shortest_distance


def status(coordinate, location, move_to, trap_nearby, valid_directions, trap_location):
	print(f"\n Variable status\n\nCoordinate = {coordinate}\nLocation = {location}\nTrap nearby = {trap_nearby}\nValid directions = {valid_directions}\nTrap locations = {trap_location}\n")
	pause=input("")
	return

def positive_integer(pi):
	pi = int(math.sqrt((pi)**2))
	return pi

def bye():
	print("              \n              Bye...")
	time.sleep(3)
	raise SystemExit

def restart_game():
	global dimension
	location, exit_point, trap_location = initialise()
	return location, exit_point, trap_location

introduction()
dimension = 16
location, exit_point, trap_location = restart_game()
while True:
	if location == exit_point:
		win_game()
		location, exit_point, trap_location = restart_game()
	if location in trap_location:
		loose_game()
		location, exit_point, trap_location, = restart_game()
	coordinate = coordinates(location)
	valid_directions = directions(coordinate)
	trap_nearby = trap_proximity(location, trap_location)
	display_location(coordinate, trap_nearby)
	shortest_distance = shortest_way_to_exit(location, exit_point)
	move_to = input(f"              You are {shortest_distance} {'steps' if shortest_distance > 1 else 'step'} from the exit. ({positive_integer(exit_point-location)})\n              Where to  now? ")
	if move_to in valid_directions:
		location = move_location(location, move_to)
	elif move_to in ('q', 'quit', 'exit'):
		bye()
	elif move_to in ('h', 'help'):
		help_screen()
	elif move_to in ('status', 'stat'):
		status(coordinate, location, move_to, trap_nearby, valid_directions, trap_location)
	else:
		print("              That particular portal is locked.")
		time.sleep(2)
