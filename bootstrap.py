#!/usr/bin/env python
import os

# This is the python file that is executed on boot. It is left here as an easy way to add or remove other scripts

os.system("/home/pi/sande/boot.py &")



f = open("testoutput.txt", "w")
f.write("hello\n")
f.close()

