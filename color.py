#!/usr/bin/python

import gtk

class Color:
	def __init__(self):
		self.dgray = gtk.gdk.Color('#3c3c3c')
		self.gray = gtk.gdk.Color('#dddddd')
		self.lgray = gtk.gdk.Color('#d2d1cf')
		self.lblue = gtk.gdk.Color('#cddddd')
		self.blue = gtk.gdk.Color('#067aa3')
		self.orange = gtk.gdk.Color('#ff7f00')
		self.white = gtk.gdk.Color('#FFFFFF')
    	def __getitem__(self, item):
        		return getattr(self, item)
    	def __setitem__(self, item, value):
        		return setattr(self, item, value)
