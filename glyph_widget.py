# SPDX-FileCopyrightText: Copyright (c) 2022 Randall Bohn (dexter)
#
# SPDX-License-Identifier: MIT
"""
`glyph_widget` from dexter_widgets

You can get ForkAwesome-*.pcf
from https://emergent.unpythonic.net/01606790241
"""

import displayio
from adafruit_bitmap_font.bitmap_font import load_font
from adafruit_displayio_layout.widgets.widget import Widget
from adafruit_displayio_layout.widgets.control import Control
from adafruit_display_text.label import Label


__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/rsbohn/Dexter_CircuitPython_Widgets.git"

FONT = load_font("/fonts/forkawesome-42.pcf")


class GlyphWidget(Widget, Control):
    """Provides a ForkAwesome glyph as a Widget."""

    def __init__(self, glyph: str, **kwargs):
        super().__init__(**kwargs)
        self.touch_boundary = None
        self.label = Label(FONT, text=glyph)
        self.label.anchor_point = 0.5, 0.5
        self.label.anchored_position = 21, 21
        self.append(self.label)
        self._background_palette = None
        self.activated = False

    def _empty(self):
        """remove all items from this widget"""
        while len(self) > 0:
            self.pop()

    def resize(self, new_width: int, new_height: int) -> None:
        """Resize the widget to a new width and height.
        Since the font size is fixed, we update the
        label's anchored_position.

        :param int new_width: requested maximum width
        :param int new_height: request maximum height
        :return: None
        """
        self.touch_boundary = (0, 0, new_width, new_height)
        self.label.anchored_position = new_width // 2, new_height // 2
        if self._background_palette is not None:
            self._empty()
            background_bitmap = displayio.Bitmap(new_width, new_height, 1)
            self.append(
                displayio.TileGrid(
                    background_bitmap, pixel_shader=self._background_palette
                )
            )
            self.append(self.label)

    def contains(self, point):
        "True if the point is within this control."
        return super().contains((point[0] - self.x, point[1] - self.y))

    def selected(self, _):
        "Turn this control on."
        self.activated = True
        self.label.color = 0x992200

    def unselect(self):
        "Turn this control off."
        self.activated = False
        self.label.color = 0xFFFFFF

    @property
    def color(self):
        """returns foreground color"""
        return self.label.color

    @color.setter
    def color(self, new_color):
        self.label.color = new_color

    @property
    def background_color(self):
        """returns the background color"""
        if self._background_palette is not None:
            return self._background_palette[0]
        return None

    @background_color.setter
    def background_color(self, new_color):
        """please set an initial background color before you add the widget to a layout"""
        if self._background_palette is None:
            self._background_palette = displayio.Palette(1)
        self._background_palette[0] = new_color
