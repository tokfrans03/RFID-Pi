#!/usr/bin/env python3
import os

#change language to your keybord layout, choose between : be, br, ca, ch, cs, de, dk, es, fi, fr, gb, hr, it, no, pt, ru, si, sv, tr, us

os.system('cat /home/pi/MFRC522-python/lock.duck | cat | python /home/pi/P4wnP1/duckencoder/duckencoder.py -l LANGUAGE -p | python /home/pi/P4wnP1/hidtools/transhid.py')
