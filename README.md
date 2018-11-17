# RFID-Pi
repo for using a rfid tag to unlock a compuer using a raspberry pi

Post in question: https://redd.it/9g4owt

# Requirements

## Hardware

-	Raspberry Pi zero (w)
-	Micro USB cable with sync
-	RFID-522 + jumper cables
-	Micro USB to full USB and Ethernet to USB SSH for initial setup or Micro USB to full USB, USB keyboard and mini HDMI to HDMI cable and a display of course 

## Software

-	Raspian
-	P4wnP1 https://github.com/mame82/P4wnP1 (HID tools)
-	MFRC522-python https://github.com/mxgxw/MFRC522-python (RFID)
-	SPI-Py https://github.com/lthiery/SPI-Py
-	Python


# Setup

I won't go into Raspian too deep because it's not too complicated

## Raspian

Install raspbian on an SD card and get ssh by dropping a file called "ssh" with no extension and no content into the boot partition of the SD card.

the default user is "pi" and the default password is: raspberry

Then type "sudo raspi-config"
Go into the second option and enable wifi and change the hostname to something recognizable (I think P4wnP1 will overwrite the hostname)
Then go to interfacing options and enable SPI for the RFID reader and ssh if you haven't already

expand the filesystem, change the user password etc if you want to

and reboot!

## P4wnP1

once rebooted find the IP of your pi by checking the HDMI output or with an IP scanner/router webpage

I'd use putty for this

Follow install.md or capy paste this:

sudo apt-get -y install git
cd /home/pi
git clone --recursive https://github.com/mame82/P4wnP1
cd P4wnP1
./install.sh

this will take a WHILE

DON'T reboot

When that's done we can change things.

I'd recommend using WinSCP or something for this.

Open setup.cfg and disable wifi AP mode and enable Client mode with your ssid etc.

change lang from "us" to your keyboard lang, choose between these: be, br, ca, ch, cs, de, dk, es, fi, fr, gb, hr, it, no, pt, ru, si, sv, tr, us

Go to the bottom and comment out "PAYLOAD=network_only.txt" and uncomment "PAYLOAD=hid_keyboard.txt"

Now go to the payloads folder and edit hid_keyboard.txt.

"hid_keyboard.txt" usually opens notepad and types out "Hello world!" but we only want to launch the HID tools.

So all you need to do is to delete everything from "GUI r" to "DELAY 1000" and "echo "Keyboard is running" | outhid"

also change lang from "us" to your keyboard lang, choose between these: be, br, ca, ch, cs, de, dk, es, fi, fr, gb, hr, it, no, pt, ru, si, sv, tr, us

once that's done you can navigate to the boot folder in the P4wnP1 folder. 

we need to change boot_P4wnP1 so that it doesn't launch unnecessary things that lag the pi up

just copy paste this Pastebin https://pastebin.com/ZRq0RGmb it disables LED_blink and autossh, If you want to want to change the hostname then do so in line 132.
I have it set to “NFC-Pi”

NOW reboot

## MFRC522-python/RFID

type "sudo apt-get install python-rpi.gpio"

follow the instructions on GitHub

then clone the repo with "git clone https://github.com/mxgxw/MFRC522-python.git"

and SPI-Py 

"git clone https://github.com/lthiery/SPI-Py.git"

"cd SPI-Py"

"sudo python setup.py install"

Confirm that the reader is working by running “python /path/to/MFRC522-python/Read.py” and placing RFID tag nearby

Also, write down the card’s UID without commas

# My bit

Once you’ve rebooted and plugged your pi into your pc with the data port you’re ready to continue

Download this git: https://github.com/tokfrans03/RFID-Pi.git

It contains the RFID python script, lock and unlock duck scripts.

Place them inside the MFRC522-python folder and make sure that the directory locations in "key_card_lock.py" are correct for the unlock/lock scripts
Don't forget to add your card UID at line 87 without commas

This is how a .duck script works:

DELAY x

delays x amount of milliseconds so 1000 = 1 second


STRING blah

Types “blah”


ENTER

Presses enter


GUI r

Holds GUI (windows key) and presses r

REM comment

for leaving comments


Now we need to edit the unlock.duck to match your password. Because I have a pin I don’t need to press enter, you may have to.

 You can try the unlock script it easily by putting a delay in the beginning, running “cat /path/to/script.duck | duckhid” and quickly press windows + l to lock

You can skip typing the last letters of your password for some extra security

## Autostart

To make this auto start on boot you need to make a .sh file with this in it:

sleep 10 #optional
python path/to/script.py
​
and make it runnable: chmod +x startup.sh
when that's done type "sudo crontab -e" it will probably ask you what editor you want to use so choose one ( id recommend nano) then paste this at the bottom:

@reboot /full/path/to/script.sh


##For any further questions/support just ask!

and my wallper: https://steamcommunity.com/sharedfiles/filedetails/?id=1322008613

Edit: I’ve made it work with dual profiles/rfid tags so just ask ;)