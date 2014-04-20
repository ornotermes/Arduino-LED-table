#!/usr/bin/env python
#
#+	Copyright (c) 2014 Rikard Lindstrom <ornotermes@gmail.com>
#
#	This software is a modified version of Impulse by Ian Halpern ( http://impulse.ian-halpern.com/ ).
#
#	This program is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.
#
#	This program is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.
#
#	You should have received a copy of the GNU General Public License
#	along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from serialLedLib import *
import argparse
import sys, gobject, os, time, math, random

width = 16
height = 16

game = -1

hist = []
histc = 0
rep = 0

def update():
	global game
	global hist, histc
	
	for l in hist:
		if l == game:
			game = -1
			histc = 0
			hist = []
	
	if game != -1:		
		if histc == 61:
			histc = 0
			hist.append(game)
		histc += 1
	
	new_game = []
	if game == -1:
		new_game = []
		for y in range(0,height):
			new_game.append([])
			for x in range(0,width):
				new_game[y].append(random.randint(0,1))
	else:
		for y in range(0,height):
			new_game.append([])
			for x in range(0,width):
				new_game[y].append(getAlive(y, x))
	game = new_game
	
	if arg["debug"]:
		for y in range(0, height):
			print game[y]
		
	display();
	return True # keep running this event
	
def display():
	global game
	fg = hex2rgb( arg["fore"] )
	bg = hex2rgb( arg["back"] )
	
	
	leds.send("C");
	for y in range(0,height):
		for x in range(0,width):
			if game[y][x]:
				leds.send("S",map(lambda x: int(x/float(arg["reduced"])), fg))
			else:
				leds.send("S",map(lambda x: int(x/float(arg["reduced"])), bg))
	leds.send("D");
	

def getCell(y,x):
	global game
	while y < 0:
		y += height
	while y >= height:
		y -= height
	while x < 0:
		x += width
	while x >= width:
		x -= width
	return game[y][x]
	
def getNeighbours(y,x):
	c = 0
	for dy in range(-1,2):
		for dx in range(-1,2):
			c += getCell(y+dy, x+dx)
	c -= getCell(y, x)
	return c
	
def getAlive(y,x):
	c = getNeighbours(y,x)
	a = 0
	if c == 3:
		a = 1
	if c == 2:
		if getCell(y,x):
			a = 1
	return a
		
def hex2rgb(s):
	red =  int(s[0], 16)<<4 | int(s[1], 16)
	green = int(s[2], 16)<<4 | int(s[3], 16)
	blue = int(s[4], 16)<<4 | int(s[5], 16)
	return (red, green, blue)
	
def argParser():

	p = argparse.ArgumentParser()
	
	p.add_argument( "-as", "--audio-source", dest="audio-source", type=int, default=0, metavar="N", help="Audio source index.")
	p.add_argument( "-p", "--port", dest="port", default="/dev/ttyACM0", metavar="/dev/ttyX", help="What device to use.")
	p.add_argument( "-i", "--identifier", dest="identifier", default="LED_TABLE", metavar="NAME", help="What name to look for in the identifier string.")
	
	p.add_argument( "-d", "--debug", dest="debug", action="store_const", default=False, const=True, help="Show debug messages.")
	
	p.add_argument( "-b", "--background", dest="back", default="000000", metavar="1F2E3D", help="Backround color.")
	p.add_argument( "-f", "--foreground", dest="fore", default="FFFFFF", metavar="1F2E3D", help="Foreround color.")
	
	p.add_argument( "-r", "--reduced", dest="reduced", default="1", metavar="4", help="Divide light by this.")
	p.add_argument( "-s", "--sleep", dest="sleep", type=float, default=0.05, metavar="float", help="Sleep time between updates.")
	
	return vars(p.parse_args())
			
# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":
		
	arg = argParser()
	
	if arg["debug"]: print arg
	
	leds = serialLed();
	leds.connect(arg["port"], arg["identifier"])
	
	while True:
		update()
		time.sleep(arg["sleep"])
