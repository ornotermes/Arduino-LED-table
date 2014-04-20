#!/usr/bin/env python
#
#+	Copyright (c) 2011,2014 Rikard Lindstrom <ornotermes@gmail.com>
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

def update():
	
	leds.send("C");
	for i in range(0,256):
		leds.send("S",( map(lambda x: int(x/float(arg["reduced"])), (random.randint(0,255), random.randint(0,255), random.randint(0,255)) )))
	leds.send("D");
	
	return True # keep running this event
	
def argParser():

	p = argparse.ArgumentParser()
	
	p.add_argument( "-p", "--port", dest="port", default="/dev/ttyACM0", metavar="/dev/ttyX", help="What device to use.")
	p.add_argument( "-i", "--identifier", dest="identifier", default="LED_TABLE", metavar="NAME", help="What name to look for in the identifier string.")
	
	p.add_argument( "-d", "--debug", dest="debug", action="store_const", default=False, const=True, help="Show debug messages.")
	
	p.add_argument( "-r", "--reduced", dest="reduced", default="1", metavar="4", help="Divide light by this.")
	p.add_argument( "-s", "--sleep", dest="sleep", type=float, default=0.03, metavar="float", help="Sleep time between updates.")
	
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
