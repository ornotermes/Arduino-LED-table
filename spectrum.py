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
import sys, gobject, os, time, math

bars = 16
class DioderImpulse () :

	def __init__ ( self, args, **keyword_args ):
	
		self.arg = args
		
		self.last = [0.0] * bars

		import impulse
		
		sys.modules[ __name__ ].impulse = impulse
		self.setAudioSource( self.arg["audio-source"] )

	def update (self):
	
		spectrum = [0.0] * bars
		audio_sample_array = impulse.getSnapshot( True )
		
		sections = int((len(audio_sample_array)/4) / bars)
		
		for i in range(0, bars):
			spectrum[i] = math.fsum(audio_sample_array[sections*i:sections*(i+1)]) / sections * self.arg["gain"] * bars
			
		if arg["debug"]: print "FFT Array: %i, Sections: %i" % (len(audio_sample_array), sections)
		if arg["debug"]: print "F", spectrum
		if arg["debug"]: print "L", self.last
		
		for i in range(0, bars):
			if self.last[i] >= bars:
				self.last[i] = bars
		
		for n in range(0, bars):
			self.last[n] -= arg["decay"]
			if self.last[n] < 0.0:
				self.last[n] = 0.0
			if (spectrum[n] < self.last[n]):
				spectrum[n] = self.last[n]
			else:
				self.last[n] = spectrum[n]
		
		fg = hex2rgb( arg["fore"] )
		bg = hex2rgb( arg["back"] )
		
		leds.send("C");
		for y in range(0, bars):
			for x in range(0, bars):
				if spectrum[x] > bars-y:
					leds.send("S",map(lambda x: int(x/float(arg["reduced"])), fg))
				else:
					leds.send("S",map(lambda x: int(x/float(arg["reduced"])), bg))
		leds.send("D");
				
		
		return True # keep running this event

	def setAudioSource( self, source, *args, **kwargs ):
		impulse.setSourceIndex( source )
		
def hex2rgb(s):
	red =  int(s[0], 16)<<4 | int(s[1], 16)
	green = int(s[2], 16)<<4 | int(s[3], 16)
	blue = int(s[4], 16)<<4 | int(s[5], 16)
	return (red, green, blue)
	
def mean(l):
	return math.fsum(l) / len(l)
		
def argParser():

	p = argparse.ArgumentParser()
	
	p.add_argument( "-as", "--audio-source", dest="audio-source", type=int, default=0, metavar="N", help="Audio source index.")
	p.add_argument( "-p", "--port", dest="port", default="/dev/ttyACM0", metavar="/dev/ttyX", help="What device to use.")
	p.add_argument( "-i", "--identifier", dest="identifier", default="LED_TABLE", metavar="NAME", help="What name to look for in the identifier string.")
	
	p.add_argument( "-d", "--debug", dest="debug", action="store_const", default=False, const=True, help="Show debug messages.")
	
	p.add_argument( "-o", "--overlay", dest="overlay", action="store_const", default=False, const=True, help="Overlay new layer on old.")
	
	p.add_argument( "-b", "--background", dest="back", default="000000", metavar="1F2E3D", help="Backround color.")
	p.add_argument( "-f", "--foreground", dest="fore", default="FFFFFF", metavar="1F2E3D", help="Foreround color.")
	
	p.add_argument( "-r", "--reduced", dest="reduced", default="1", metavar="4", help="Divide light by this.")
	p.add_argument( "-g", "--gain", dest="gain", type=float, default=1.0, metavar="float", help="Gain for all channels.")
	p.add_argument( "-e", "--decay", dest="decay", type=float, default=0.5, metavar="float", help="Decay of bar value.")
	p.add_argument( "-s", "--sleep", dest="sleep", type=float, default=0.03, metavar="float", help="Sleep time between updates.")
	
	return vars(p.parse_args())
			
# If the program is run directly or passed as an argument to the python
# interpreter then create a Screenlet instance and show it
if __name__ == "__main__":

	try:
		import ctypes
		libc = ctypes.CDLL('libc.so.6')
		libc.prctl(15, os.path.split( sys.argv[ 0 ] )[ 1 ], 0, 0, 0)
	except Exception:
		pass
		
	arg = argParser()
	
	if arg["debug"]: print arg
	
	leds = serialLed();
	leds.connect(arg["port"], arg["identifier"])
	
	imp = DioderImpulse(arg)
	
	while True:
		time.sleep(arg["sleep"])
		imp.update()
