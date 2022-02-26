# Fritter and Waste

A virtual fretboard MIDI instrument

## What is it?

A six-string MIDI instrument that runs on the FeatherS2 and 3.5" TFT FeatherWing.
Should also work on the PyPortal Titano.

You can set a fret point on each string. As each string is 'plucked' the appropriate
MIDI note is sent over USB.

Tested on CircuitPython 7.2.0.

## Installation

1. Clone this repo, then copy to your device.
1. circup install adafruit_midi
1. circup install adafruit_featherwing
1. circup install adafruit_displayio_layout
1. Download font-awesome fonts (42, 20)
1. Copy fonts to the /fonts folder on your device
1. Restart the device (cold boot)
1. Connect 'CircuitPython Audio 0' to your MIDI software of choice
1. Make some noise

## Notes

`boot.py` disables usb_hid and enables usb_midi.
The ESP32-S2 doesn't have enough usb endpoints to run both.
This change requires that you cold boot the FeatherS2.

The tempo is fixed at about 90 bpm. You can change this in code.py.
You might want to add some other way to adjust the tempo.

The music stops when you use the touch screen. This is a known issue.
Perhaps a future version will work better. It would be fun to add
pitch bend and aftertouch controls, either using the touch screen
or stemma-qt connected controllers.

The randomize button will change all the fret points on the fretboard.

In this software most 'Strings' are guitar strings, not character strings.

The 3.5" TFT FeatherWing has a resistive touch screen.
For best results use a stylus.
In a pinch a fingernail will work.
You may need to adjust the touch screen scaling values in code.py.

Made with love in the beehive state by Dexter Starboard. Enjoy!
