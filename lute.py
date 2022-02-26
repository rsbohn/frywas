# SPDX-FileCopyrightText: Copyright (c) 2022 Randall Bohn (dexter)
#
# SPDX-License-Identifier: MIT
"""dexter_mics -- musical instrument construction set"""

import displayio
import vectorio
from adafruit_display_shapes.rect import Rect
from adafruit_displayio_layout.widgets.widget import Widget
from adafruit_displayio_layout.widgets.control import Control
from terminalio import FONT
from adafruit_display_text.label import Label

palette = displayio.Palette(3)
palette[0] = 0x99FF44
palette[1] = 0x443300
palette[2] = 0x444433

DEBUG = False


class String(Widget, Control):
    "a string with semitones"

    # pylint: disable=too-many-arguments
    def __init__(self, x, y, width, height, open_note, *kwargs):
        super().__init__(x=x, y=y, width=width, height=height, *kwargs)
        # for Control:
        self.open_note = open_note
        self.touch_boundary = [0, 0, width, height]
        self.background = self.fill_background(fill=palette[1])
        self.append(self.background)
        self.fret = vectorio.Rectangle(
            x=0, y=0, width=4, height=height, pixel_shader=palette
        )
        self.append(self.fret)
        if DEBUG:
            self.label = Label(FONT, text=str([x, y, width, height]))
            self.label.anchor_point = (0.5, 1.0)
            self.label.anchored_position = (320, self.height)
            self.append(self.label)

    def fill_background(self, fill):
        "Use a Rect to provide the background."
        rect = Rect(0, 0, self.width, self.height, fill=fill)
        return rect

    def resize(self, nwidth, nheight):
        "Adjust the size of the widget."
        # pylint: disable=attribute-defined-outside-init
        # Don't know why I can't set them in __init__.
        self.width = nwidth
        self.height = nheight
        self[0] = self.fill_background(fill=palette[1])
        self.fret.height = nheight

    def contains(self, point):
        "True if point is inside this control."
        inside = super().contains((point[0] - self.x, point[1] - self.y))
        if inside:
            self[0].fill = palette[2]
        else:
            self[0].fill = palette[1]
        return inside

    def selected(self, point):
        "Move the fret point."
        x = point[0] - self.x
        # future: use for pitch bend?
        # y = point[1] - self.y
        self.fret.x = x

    def note(self):
        "Return the MIDI note for this String."
        k = int(24 * self.fret.x / self.width)
        return self.open_note + k
