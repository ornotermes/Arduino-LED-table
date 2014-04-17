#!/usr/bin/env python
#
#+	Copyright (c) 2014 Rikard Lindstrom <ornotermes@gmail.com>
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

from PIL import Image
from time import sleep
import argparse
import sys

def argParser():

	p = argparse.ArgumentParser()
	
	p.add_argument( "-p", "--port", dest="port", default="/dev/ttyACM0", metavar="/dev/ttyX", help="What device to use.")
	p.add_argument( "-i", "--identifier", dest="identifier", default="LED_TABLE", metavar="NAME", help="What name to look for in the identifier string.")
	
	p.add_argument( "-d", "--debug", dest="debug", action="store_const", default=False, const=True, help="Show debug messages.")
	
	p.add_argument( "-c", "--color", dest="color", default="000000", metavar="1F2E3D", help="Fill color.")
	
	return vars(p.parse_args())

def hex2rgb(s):
	red =  int(s[0], 16)<<4 | int(s[1], 16)
	green = int(s[2], 16)<<4 | int(s[3], 16)
	blue = int(s[4], 16)<<4 | int(s[5], 16)
	if(arg["debug"]):
		print (red, green, blue)
	return (red, green, blue)

if __name__ == '__main__':

	arg = argParser()
	
	color = hex2rgb( arg["color"] )
	
	leds = serialLed();
	leds.connect(arg["port"], arg["identifier"])
	
	for y in range(0, leds.height):
		for x in range(0, leds.width):
			leds.send("S", color)
	leds.send("D");

