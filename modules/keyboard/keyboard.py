#!/usr/bin/env python

#   Keyboard for 840D on all alphanumeric entries

#   Copyright (c) 2017 Maksym Kotelnikov
#        <nemovit.mk@gmail.com>
#
#   This file is part of 840D simulation program.
#
#   It is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   It is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License,
#   see <http://www.gnu.org/licenses/>.

import pygtk
pygtk.require("2.0")
import gtk
import os
import sys
import gobject

from widget import Widgets
from color import Color

py_file_dir = os.path.abspath(os.path.dirname(__file__))
IMAGEDIR = os.path.join(py_file_dir , "ui")

class Keyboard(gobject.GObject):

	def __init__(self):
	
		self.__gobject_init__()

		# Glade setup
		gladefile = os.path.join(IMAGEDIR, 'keyboard.glade')

		self.builder = gtk.Builder()
		self.builder.add_from_file(gladefile)

		self.widgets = Widgets(self.builder)

		self.SHIFTED = False

		self.colors = Color()
		self.set_style()
		self.connect_signals()
		self.show()


# ==========================================================
# Set style
# ==========================================================
	def set_style(self):	
		try:	
			self.widgets.window2.set_title("Alfa-Numeric Keyboard")
			layouts = self.widgets.get_list(gtk.Layout)
			for lyt in layouts: 
				lyt.modify_bg(gtk.STATE_NORMAL, self.colors.dgray)
		except:
			print ("Problem with style settings of Keyboard")


# ==========================================================
# Connect signals
# ==========================================================

	def connect_signals(self):
		try:		
			self.widgets.kb11.connect('clicked', self.on_kb11_clicked)
			self.widgets.kb12.connect('clicked', self.on_kb12_clicked)
			self.widgets.kb13.connect('clicked', self.on_kb13_clicked)
			self.widgets.kb14.connect('clicked', self.on_kb14_clicked)
			self.widgets.kb15.connect('clicked', self.on_kb15_clicked)
			self.widgets.kb21.connect('clicked', self.on_kb21_clicked)
			self.widgets.kb22.connect('clicked', self.on_kb22_clicked)
			self.widgets.kb23.connect('clicked', self.on_kb23_clicked)
			self.widgets.kb24.connect('clicked', self.on_kb24_clicked)
			self.widgets.kb25.connect('clicked', self.on_kb25_clicked)
			self.widgets.kb31.connect('clicked', self.on_kb31_clicked)
			self.widgets.kb32.connect('clicked', self.on_kb32_clicked)
			self.widgets.kb33.connect('clicked', self.on_kb33_clicked)
			self.widgets.kb34.connect('clicked', self.on_kb34_clicked)
			self.widgets.kb35.connect('clicked', self.on_kb35_clicked)
			self.widgets.kb41.connect('clicked', self.on_kb41_clicked)
			self.widgets.kb42.connect('clicked', self.on_kb42_clicked)
			self.widgets.kb43.connect('clicked', self.on_kb43_clicked)
			self.widgets.kb44.connect('clicked', self.on_kb44_clicked)
			self.widgets.kb45.connect('clicked', self.on_kb45_clicked)
			self.widgets.kb51.connect('clicked', self.on_kb51_clicked)
			self.widgets.kb52.connect('clicked', self.on_kb52_clicked)
			self.widgets.kb53.connect('clicked', self.on_kb53_clicked)
			self.widgets.kb54.connect('clicked', self.on_kb54_clicked)
			self.widgets.kb55.connect('clicked', self.on_kb55_clicked)
			self.widgets.kb61.connect('clicked', self.on_kb61_clicked)
			self.widgets.kb62.connect('clicked', self.on_kb62_clicked)
			self.widgets.kb63.connect('clicked', self.on_kb63_clicked)
			self.widgets.kb64.connect('clicked', self.on_kb64_clicked)
			self.widgets.kb65.connect('clicked', self.on_kb65_clicked)
			self.widgets.kb71.connect('clicked', self.on_kb71_clicked)
			self.widgets.kb72.connect('clicked', self.on_kb72_clicked)
			self.widgets.kb73.connect('clicked', self.on_kb73_clicked)
			self.widgets.kb74.connect('clicked', self.on_kb74_clicked)
			self.widgets.kb75.connect('clicked', self.on_kb75_clicked)
			self.widgets.kb81.connect('clicked', self.on_kb81_clicked)
			self.widgets.kb82.connect('clicked', self.on_kb82_clicked)
			self.widgets.kb83.connect('clicked', self.on_kb83_clicked)
			self.widgets.kb84.connect('clicked', self.on_kb84_clicked)
			self.widgets.kb85.connect('clicked', self.on_kb85_clicked)

		except:
			print ("Signal connection of Keyboard: could not connect ")

# ==========================================================
# On key pressed
# ==========================================================
	#FIRST ROW
	def on_kb11_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("A")
		else: self.place_sign("7")
	def on_kb12_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("B")
		else: self.place_sign("8")
	def on_kb13_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("C")
		else: self.place_sign("9")
	def on_kb14_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("D")
		else: self.place_sign("/")
	def on_kb15_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("E")
		else: self.place_sign("(")
	#SECOND ROW
	def on_kb21_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("F")
		else: self.place_sign("4")
	def on_kb22_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("G")
		else: self.place_sign("5")
	def on_kb23_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("H")
		else: self.place_sign("6")
	def on_kb24_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("I")
		else: self.place_sign("*")
	def on_kb25_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("J")
		else: self.place_sign(")")
	#THIRD ROW
	def on_kb31_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("K")
		else: self.place_sign("1")
	def on_kb32_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("L")
		else: self.place_sign("2")
	def on_kb33_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("M")
		else: self.place_sign("3")
	def on_kb34_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("N")
		else: self.place_sign("-")
	def on_kb35_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("O")
		else: self.place_sign("[")
	#FOURTH ROW
	def on_kb41_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("P")
		else: self.place_sign("=")
	def on_kb42_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("Q")
		else: self.place_sign("0")
	def on_kb43_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("R")
		else: self.place_sign(".")
	def on_kb44_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("S")
		else: self.place_sign("+")
	def on_kb45_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("T")
		else: self.place_sign("]")
	#FIFTH ROW
	def on_kb51_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("U")
		else: self.place_sign("\\")
	def on_kb52_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("V")
		else: self.place_sign(",")
	def on_kb53_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("W")
		else: self.channel_key("CHANNEL") 
	def on_kb54_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("X")
		else: self.alarm_cancel_key("ALARM_CANCEL")
	def on_kb55_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("Y")
		else: self.help_key("HELP")
	#Sixth row
	def on_kb61_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("Z")
		else: self.place_sign(";")
	def on_kb62_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("?")
		else: self.next_win_key("NEXT_WIN")
	def on_kb63_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("!")
		else: self.action_key("UP")
	def on_kb64_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("\'")
		else: self.page_key("DOWN")
	def on_kb65_clicked(self, widget, data=None):
		self.backspace_key("BACKSPACE")
	#Seventh row
	def on_kb71_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("_")
		else: self.place_sign(" ")
	def on_kb72_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("<")
		else: self.action_key("LEFT")
	def on_kb73_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign(">")
		else: self.select_key("SELECT")
	def on_kb74_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("\"")
		else: self.action_key("RIGHT")
	def on_kb75_clicked(self, widget, data=None):
		self.insert_key("INSERT")

	def on_kb81_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.SHIFTED = False
		else: self.SHIFTED = True
	def on_kb82_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign(":")
		else: self.end_key("END")
	def on_kb83_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("$")
		else: self.action_key("DOWN")
	def on_kb84_clicked(self, widget, data=None):
		if self.SHIFTED:
			self.place_sign("%")
		else: self.page_key("DOWN")
	def on_kb85_clicked(self, widget, data=None):
		self.input_key("INPUT")

# ==========================================================
# Emmit signals
# ==========================================================
	def _emit_signal(self, data):
		if data:
			self.data = data
		else: self.data = ""
		self.emit('key_press_keyboard')

	def place_sign(self, data):
		self._emit_signal(data)

	def action_key(self, action):
		self._emit_signal(action)

#	def action_key(self, direction):
#		lbl = self.CURRENTLABEL
#		if lbl:
#			st1, tbl, st3 = lbl.split('_')
#			lblLst = getattr(self.scrnlbl, tbl)
#			maxY = len(lblLst) - 1
#			y = 0
#			for lst in lblLst:
#				print("list %r"% lst)
#				try: 	
#					print("lbl %r"% lbl)
#					x = lst.index(lbl)
#					print("x is  %r"% x)
#				except:
#					x = None
#				if x != None:
#					maxX = len(lst) - 1
#					break
#				y = y + 1
#			if direction == "LEFT":
#				while True:
#					newX = x - 1
#					if newX < 0: 
#						newX = maxX
#						newY = y - 1
#						if newY < 0:
#							newY = maxY
#					else: newY = y
#					if lblLst[newY][newX]: break
#			elif direction == "RIGHT":
#				while True:
#					newX = x + 1
#					if newX > maxX: 
#						newX = 0
#						newY = y + 1
#						if newY > maxY:
#							newY = 0
#					else: newY = y
#					if lblLst[newY][newX]: break
#			elif direction == "UP":
#				while True:
#					newY = y - 1
#					if newY < 0: 
#						newY = maxY
#						newX = x - 1
#						if newX < 0:
#							newX = maxX
#					else: newX = x
#					if lblLst[newY][newX]: break		
#			elif direction == "DOWN":
#				while True:
#					newY = y + 1
#					if newY > maxY: 
#						newY = 0
#						newX = x + 1
#						if newX > maxX:
#							newX = 0
#					else: newX = x
#					if lblLst[newY][newX]: break	
#			newLbl = lblLst[newY][newX]
#			if self.CURRENTLABEL != newLbl:
#				self.highliteLBL(newLbl, self.CURRENTLABEL)
#				self.CURRENTLABEL = newLbl
#				self.editPosition = ""
#		print("OK")

	def page_key(self, action):
		self._emit_signal(action)


	def channel_key(self, action):
		self._emit_signal(action)
	def alarm_cancel_key(self, action):
		self._emit_signal(action)
	def help_key(self, action):
		self._emit_signal(action)

	def next_win_key(self, action):
		self._emit_signal(action)
	def backspace_key(self, action):
		self._emit_signal(action)

	def select_key(self, action):
		self._emit_signal(action)
	def insert_key(self, action):
		self._emit_signal(action)
	def end_key(self, action):
		self._emit_signal(action)
	def input_key(self, action):
		self._emit_signal(action)

# ==========================================================
# Show the keyboard
# ==========================================================

#	def show(self, entry, persistent=False ):
#		self.entry = entry
#		self.persistent = persistent
#		self.entry.connect('focus-out-event', self.on_entry_loses_focus)
#		self.entry.connect('key-press-event', self.on_entry_key_press)
#		if self.parent:
#			pos = self.parent.get_position()
#			self.window.move(pos[0]+105, pos[1]+440)
	def show(self):
		self.widgets.window2.show()

#	def set_parent(self, parent):
#		self.parent = parent


# ==========================================================
# Creating signal
# ==========================================================
#gobject.type_register(Keyboard)
gobject.signal_new("key_press_keyboard", Keyboard, gobject.SIGNAL_RUN_FIRST,
	gobject.TYPE_NONE, ())

