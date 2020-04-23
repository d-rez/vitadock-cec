#!/usr/bin/python3
# By d-rez a.k.a. /u/dark_skeleton
# See https://github.com/d-rez/vitadock-cec

import cec
import time

def cec_callback(event, *args):
  print(repr(event), repr(args))


cec.add_callback(cec_callback, cec.EVENT_ALL & ~cec.EVENT_LOG)
cec.init()

while True:
    time.sleep(5)
