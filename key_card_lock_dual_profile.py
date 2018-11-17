#!/usr/bin/env python
# -*- coding: utf8 -*-
#
#    Copyright 2014,2018 Mario Gomez <mario.gomez@teubi.co>
#
#    This file is part of MFRC522-Python
#    MFRC522-Python is a simple Python implementation for
#    the MFRC522 NFC Card Reader for the Raspberry Pi.
#
#    MFRC522-Python is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MFRC522-Python is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with MFRC522-Python.  If not, see <http://www.gnu.org/licenses/>.
#

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import os
import sys

continue_reading = True


lock = 0
card_id = ("No cards Yet")
counter = 0
state = 0

# 0 = my
# 1 = other

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
	global continue_reading
	print "Ctrl+C captured, ending read."
	continue_reading = False
	GPIO.cleanup()

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

# Welcome message
print "Welcome to Tokilokit's lock / unlock script! (Thanks to Mario Gomez for the original script)"
print "Press Ctrl-C to stop."

print(card_id)

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:



	# Scan for cards
	(status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

	# Get the UID of the card
	(status,uid) = MIFAREReader.MFRC522_Anticoll()

	if status != MIFAREReader.MI_OK:
		counter = counter + 1
		print counter
		if counter >= 3:
			counter = 3
		if (counter == 2):
			os.system('python /home/pi/MFRC522-python/lock.py')
			lock = 2

	# If we have the UID, continue
	if status == MIFAREReader.MI_OK:
		counter = 0


		# Print UID
		card_id = "%x:%x:%x:%x" % (uid[0], uid[1], uid[2], uid[3])
		print "Card detected, UID:", card_id


		if (card_id == "ex:am:pl:e0") & (lock == 2) & (state == 1):
			print("my card detected, unlocking if I need to")
			os.system('python /home/pi/MFRC522-python/unlock_change_to_my.py')
			print("unlocked")
			lock = 0

		if (card_id == "ex:am:pl:e0") & (lock == 2) & (state == 0):
            print("card detected, unlocking if I need to")
            os.system('python /home/pi/MFRC522-python/unlock_my.py')
            print("unlocked")
            lock = 0




		if (card_id == "ex:am:pl:e0") & (lock == 2) & (state == 0):
            print("vr card detected, unlocking if I need to")
            os.system('python /home/pi/MFRC522-python/unlock_change_to_other.py')
            print("unlocked")
            lock = 0


        if (card_id == "ex:am:pl:e0") & (lock == 2) & (state == 1):
            print("other card detected, unlocking if I need to")
            os.system('python /home/pi/MFRC522-python/unlock_other.py')
            print("unlocked")
            lock = 0

        if ((card_id != "ex:am:pl:e0") & (card_id != "ex:am:pl:e0")):
			print("No authenticated card detected, locking")
			lock = 1

		time.sleep(.5)
