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

def argParser():

	p = argparse.ArgumentParser()
	
	p.add_argument( "-p", "--port", dest="port", default="/dev/ttyACM0", metavar="/dev/ttyX", help="What device to use.")
	p.add_argument( "-i", "--identifier", dest="identifier", default="LED_TABLE", metavar="NAME", help="What name to look for in the identifier string.")
	
	p.add_argument( "-d", "--debug", dest="debug", action="store_const", default=False, const=True, help="Show debug messages.")
	
	return vars(p.parse_args())


if __name__ == '__main__':

	arg = argParser()
	
	
	leds = serialLed();
	leds.connect(arg["port"], arg["identifier"])
	
	v = 255;
	
	while 1:
		if(v):
			v = 0
		else:
			v = 255;
		leds.send("C");
		for y in range(0, leds.height):
			for x in range(0, leds.width):
				leds.send("S",(v, v, v))
		leds.send("D");
