#!/usr/bin/env python
#
# Screen widget
#
# R var screen for Sinumeric 840D project
#
# Copyright (c) 2017  Maksym Kotelnikov <nemovit.mk@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.


#import pygtk
#pygtk.require("2.0")
import gtk
import os, time, string
#import sys
import gobject
#import time, string

import pango

from label_list import LabelList
from labels_data import *
from color import Color

from widget import Widgets


#from hal_widgets import _HalWidgetBase
#import linuxcnc
#from hal_glib import GStat
#from hal_actions import _EMC_ActionBase, ensure_mode
datadir = os.path.abspath( os.path.dirname( __file__ ) )

class Screen_Rvar(gtk.VBox):
    __gtype_name__= 'Screen_Rvar'
    __gsignals__ = {
        'change-screen': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
        'change-labels':  (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
    }
    def __init__(self, *a, **kw):
        self.__gobject_init__()
        gtk.VBox.__init__(self, *a, **kw)

        gladefile = os.path.join( datadir, "../ui/rvar.glade" )
        self.bldr = gtk.Builder()
        self.bldr.add_from_file(gladefile)
        self.screen = self.bldr.get_object("container")
#        self.pack_start(self.screen)
        self.sensitive = True

        self.labelX = labels_X("screen_rvar")
        self.labelY = labels_Y("screen_rvar")
        self.prnt_screen = "main_screen"
        self.crnt_screen = "screen_rvar"
        self.lght_btn = "lblX2"

        self.colors = Color()
#        self.labelX = labels_X("screen_rvar")
#        self.labelY = labels_Y("screen_rvar")
#        self.lght_btn = "lblX2"

        rvar_lbl = [ ["lbl_rvar_0", "lbl_rvar_13"],
                    ["lbl_rvar_1", "lbl_rvar_14"],
                    ["lbl_rvar_2", "lbl_rvar_15"],
                    ["lbl_rvar_3", "lbl_rvar_16"],
                    ["lbl_rvar_4", "lbl_rvar_17"],
                    ["lbl_rvar_5", "lbl_rvar_18"],
                    ["lbl_rvar_6", "lbl_rvar_19"],
                    ["lbl_rvar_7", "lbl_rvar_20"],
                    ["lbl_rvar_8", "lbl_rvar_21"],
                    ["lbl_rvar_9", "lbl_rvar_22"],
                    ["lbl_rvar_10", "lbl_rvar_23"],
                    ["lbl_rvar_11", "lbl_rvar_24"],
                    ["lbl_rvar_12", "lbl_rvar_25"],]
        crnt_lbl = "lbl_rvar_0"
        permissions = [True, True, True, True]
        self.params = [rvar_lbl, crnt_lbl, permissions]
        self.lbl_lst = LabelList(self.params, self.bldr)

        self.widget = Widgets(self.bldr)

        self.style()
        self.screen.reparent(self)
        self.show_all()

    def on_key_pressed(self, data):
#        out = labels_X("screen_rvar")
#        print("%r"% out)
        if self.sensitive:
            self.lbl_lst.key_press(data)

    def on_soft_key_pressed(self, key):
        if key == "PARENT":
            if self.prnt_screen == "main_screen":
                self.crnt_screen = "main_screen"
                self.lght_btn = ""
                self.actions_on_enter()
#        elif key == "MENU":
#            self.lght_btn = ""
#            self.prnt_screen == "main_screen"
#            self.change_label("main_screen")
        elif key == "Tool\noffset":
            self.crnt_screen = "screen_tool"
            self.change_screen()
        elif key == "R\nvariables":
            self.lght_btn = "lblX2"
            self.prnt_screen == "main_screen"
            self.change_label("screen_rvar")
        elif key == "Setting\ndata":
            self.lght_btn = "lblX3"
            self.change_label("screen_rvar")
        elif key == "Work\noffset":
            self.lght_btn = "lblX4"
            self.change_label("screen_rvar")
        elif key == "User\ndata":
            self.lght_btn = "lblX5"
            self.change_label("screen_rvar")
        elif key == "Determine\ncompens.":
            self.lght_btn = "lblX8"
            self.change_label("screen_rvar")
        elif key == "Delete\nselect":
            self.lght_btn = "lblY4"
            self.change_label("screen_rvar")
        elif key == "Delete\nAll":
            self.lght_btn = "lblY5"
            self.change_label("screen_rvar")
        elif key == "Search":
            self.lght_btn = "lblY6"
            self.change_label("screen_rvar")

    def change_screen(self):
        self.actions_on_leave()
        self.emit('change-screen')

    def change_label(self, label_mark):
        self.labelX = labels_X(label_mark)
        self.labelY = labels_Y(label_mark)
        self.emit('change-labels')

    def actions_on_leave(self):
        self.lght_btn = "lblX2"
        self.prnt_screen == "main_screen"
        self.labelX = labels_X("screen_rvar")
        self.labelY = labels_Y("screen_rvar")
#        self.style()

    def actions_on_enter(screen = "screen_rvar"):
        self.labelX = labels_X(screen)
        self.labelY = labels_Y(screen)
#        self.prnt_screen = "main_screen"
#        self.crnt_screen = "main_screen"
#        self.lght_btn = ""
        self.change_label(screen)
        self.style()

#    def on_soft_key(self, line, btn):
#        if line == "X":
#            new_screen = self.labelX[btn][1]
#        elif line == "Y":
#            new_screen = self.labelY[btn][1]
#        else: return
#        if new_screen != None:

#    def actions_on_leave():
#        self.style()

#    def actions_on_came():
#        self.style()

    def style(self):
            boxs = self.widget.get_list(gtk.EventBox)
            for box in boxs: 
                box.modify_bg(gtk.STATE_NORMAL, self.colors.white)
            self.lbl_lst.highlite_lbl()
#            ntbs = self.widget.get_list(gtk.Table)
#            for ntb in ntbs: 
#                ntb.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)

            lbls = self.widget.get_list(gtk.Label)
            for lbl in lbls: 
                lbl.modify_font(pango.FontDescription('dejavusans condensed 10'))

            self.widget["vpaned6"].modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
            self.widget["viewport2"].modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
            self.widget["rvar_header"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)

