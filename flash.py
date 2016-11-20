#!/usr/bin/python3
from migen.build.generic_platform import *
import de0cv
plat = de0cv.Platform() 
plat.create_programmer().load_bitstream("build/top.sof")
