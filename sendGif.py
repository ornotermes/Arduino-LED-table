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
	
	p.add_argument( "-f", "--file", dest="file", default="file.gif", metavar="file.gif", help="Select what file to draw.")
	p.add_argument( "-p", "--port", dest="port", default="/dev/ttyACM0", metavar="/dev/ttyX", help="What device to use.")
	p.add_argument( "-i", "--identifier", dest="identifier", default="LED_TABLE", metavar="NAME", help="What name to look for in the identifier string.")
	
	p.add_argument( "-d", "--debug", dest="debug", action="store_const", default=False, const=True, help="Show debug messages.")
	
	p.add_argument( "-o", "--overlay", dest="overlay", action="store_const", default=False, const=True, help="Overlay new layer on old.")
	
	p.add_argument( "-b", "--background", dest="back", default="FFFFFF", metavar="1F2E3D", help="Backround color.")
	
	return vars(p.parse_args())

def hex2rgb(s):
	red =  int(s[0], 16)<<8 | int(s[1], 16)
	green = int(s[2], 16)<<8 | int(s[3], 16)
	blue = int(s[4], 16)<<8 | int(s[5], 16)
	return (red, green, blue)

if __name__ == '__main__':

	arg = argParser()
	
	back = hex2rgb( arg["back"] )
	
	leds = serialLed();
	leds.connect(arg["port"], arg["identifier"])
	
	try:
		gif = Image.open(arg["file"]);
	except:
		print "Can't open file."
		sys.exit(1);
		
	print (gif.info)
	palette = gif.getpalette()
	output = Image.new("RGBA", (leds.width, leds.height), back)
	while 1:
		if(1 != arg["overlay"]):
			output = Image.new("RGBA", (leds.width, leds.height), back)
		gif.putpalette(palette)
		temp = gif.convert("RGBA")
		output.paste(temp, mask=temp.split()[3])

		pixdata = output.convert("RGB").load()		
		leds.send("C");
		for y in range(0, leds.height):
			for x in range(0, leds.width):
				leds.send("S",pixdata[x,y])
		leds.send("D");
	
		try:
			sleep(gif.info["duration"] / 1000.0);
		except KeyError:
			sleep(0.1);
		
		try:
			gif.seek(gif.tell()+1)
		except EOFError:
			gif.seek(0)
