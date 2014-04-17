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

import serial
import io
from time import sleep

class serialLed:
	width = 1
	height = 1
	
	def connect(self, port, identifier):
		self.serial = serial.Serial(port, 9600, timeout = 1)
		self.sio = io.TextIOWrapper(io.BufferedRWPair(self.serial, self.serial))
		self.serial.write("?")
		sleep(0.5)
		response = self.sio.readline().split(",");
		if ( response[0] != identifier ):
			raise Exception('Serial device did not give expected response!')
		for i in range(1, len(response)):
			operand = response[i][0]
			if(operand == "W"):
				self.width = int(response[i][1:])
			if(operand == "H"):
				self.height = int(response[i][1:])
		
	def send(self, cmd, data = 0):
		if cmd in ("C", "c", "D", "d"):
			self.serial.write(cmd)
			self.sio.flush()
			self.serial.read(1)
		if cmd in ("G", "g"):
			self.serial.write("%s%s%s" % (cmd, chr(data[0]), chr(data[1])))
		if cmd in ("S", "s"):
			self.serial.write("%s%s%s%s" % (cmd, chr(data[0]), chr(data[1]), chr(data[2])))
		#sleep(0.001)
		
