# SPDX-FileCopyrightText: None
# SPDX-License-Identifier: Unlicense
"""For FeatherS2:
Not enough usb endpoints. Disable usb_hid, enable usb_midi."""
import usb_hid
import usb_midi

usb_hid.disable()
usb_midi.enable()
