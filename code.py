# SPDX-FileCopyrightText: Copyright (c) 2022 Randall Bohn (dexter)
#
# SPDX-License-Identifier: MIT

# Each section may import needed modules.
# pylint: disable=imports
"""Fritter & Waste: A virtual MIDI instrument."""
import random
import time
import board
import displayio
from adafruit_featherwing.tft_featherwing_35 import TFTFeatherWing35
import glyph_widget

if "feathers2" in board.board_id:
    wing = TFTFeatherWing35(cs=board.D5, dc=board.D6, ts_cs=board.D21, sd_cs=board.D20)
    display = wing.display
    ts = wing.touchscreen
else:
    raise NotImplementedError("Where am I?")

splash = displayio.Group()
display.show(splash)

#%% title and randomize button
from adafruit_bitmap_font.bitmap_font import load_font
from adafruit_display_text.label import Label

font = load_font("/fonts/Lora-32.pcf")
title = Label(font, text="Fritter & Waste", x=20, y=20)
splash.append(title)

# use the smaller -20 font
glyph_widget.FONT = load_font("/fonts/forkawesome-20.pcf")
rando = glyph_widget.GlyphWidget("\uF074")
rando.x = 400
rando.y = 0
rando.resize(80, 80)
splash.append(rando)

#%% Building the fretboard. Strings here are not character strings.
from lute import palette, String

h = int((display.height - 80) / 6)
fingerboard = [
    String(0, 80 + h * 0, 400, h - 1, 64),
    String(0, 80 + h * 1, 400, h - 1, 59),
    String(0, 80 + h * 2, 400, h - 1, 55),
    String(0, 80 + h * 3, 400, h - 1, 50),
    String(0, 80 + h * 4, 400, h - 1, 45),
    String(0, 80 + h * 5, 400, h, 40),
]

for s in fingerboard:
    splash.append(s)


def randomize(strings):
    "move all the frettings"
    for item in strings:
        item.fret.x = int(item.width * random.random())


#%% The pick
import vectorio

pick = vectorio.Circle(radius=h // 4, x=400, y=80 + h * 5 - 40, pixel_shader=palette)
splash.append(pick)

#%% touchscreen dispatch -- This will interrupt the MIDI stream :sad:
def dispatch(touchscreen):
    "Send touch input to the control widgets."
    if touchscreen.buffer_empty:
        return
    points = touchscreen.touches
    last_point = points[-1]
    # swap x and y
    # you may need to tune the scaling values here for your device
    pyy = (last_point["x"] - 200) * display.height // 3700
    pyy = display.height - pyy
    pxx = (last_point["y"] - 120) * display.width // 3680
    if rando.contains((pxx, pyy)):
        rando.selected((pxx, pyy))
    for item in fingerboard:
        if item.contains((pxx, pyy)):
            item.selected((pxx, pyy))


#%% MIDI section
import usb_midi
import adafruit_midi
from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)


def main():
    "Do all the things."
    velocity = 120
    bpm = 90
    note_time = 60 / bpm / 4
    last_note = None
    alarm = 0
    string = 5

    #%% The big loop
    while True:
        now = time.monotonic()
        if now >= alarm:
            alarm = now + note_time
            if last_note is not None:
                midi.send(NoteOff(last_note, 0))
            last_note = fingerboard[string].note()
            midi.send(NoteOn(last_note, velocity))
            pick.y = 80 + string * h + h // 2
            string = string - 1
            if rando.activated:
                randomize(fingerboard)
                rando.unselect()
            if string < 0:
                string = 5

        dispatch(ts)


if __name__ == "__main__":
    main()
