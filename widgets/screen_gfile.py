#!/usr/bin/env python
# 
# GladeVcp MDI history widget
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

import os, time, string

import gobject, gtk

import pango

from g_file import Gfile
from labels_data import *
from color import Color

from widget import Widgets

#from hal_widgets import _HalWidgetBase
import linuxcnc
#from hal_glib import GStat
#from hal_actions import _EMC_ActionBase, ensure_mode
#from testui import myGUI
datadir = os.path.abspath( os.path.dirname( __file__ ) )

class Screen_Gfile(gtk.VBox):
    __gtype_name__ = 'Screen_Gfile'
    __gsignals__ = {
        'change-screen': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
        'change-labels':  (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
    }
    def __init__(self, *a, **kw):
        self.__gobject_init__()
        gtk.VBox.__init__(self, *a, **kw)


        # if 'NO_FORCE_HOMING' is true, MDI  commands are allowed before homing.
        inifile = os.environ.get('INI_FILE_NAME', '/dev/null')
        self.ini = linuxcnc.ini(inifile)
        no_home_required = int(self.ini.find("TRAJ", "NO_FORCE_HOMING") or 0)
        path = self.ini.find('DISPLAY', 'MDI_G_FILE') or "~/default.ngc"
        self.filename = os.path.expanduser(path)

        gladefile = os.path.join( datadir, "../ui/mdi.glade" )
        self.bldr = gtk.Builder()
        self.bldr.add_from_file(gladefile)
        self.screen = self.bldr.get_object("container")

        self.sensitive = True
        
        self.path_to_file = None

        self.labelX = labels_X("screen_gfile")
        self.labelY = labels_Y("screen_gfile")
        self.prnt_screen = "main_screen"
        self.crnt_screen = "screen_gfile"
        self.lght_btn = "lblX3"
        self.widget = Widgets(self.bldr)
        self.colors = Color()

#        self.labelX = labels_X("screen_gfile")
#        self.labelY = labels_Y("screen_gfile")

#        self.lght_btn = "lblX3"

##        self.pack_start(self.screen)
#        self.sensitive = True
#        mdi_lbl = [ ["mdilabel0",],
#                    ["",], ]
#        crnt_lbl = "mdilabel1"
#        permissions = [True, True, True, True]
#        self.params = [mdi_lbl, crnt_lbl, permissions]
#        self.lbl_lst = LabelList(self.params, self.bldr)

#        self.path_to_file
        if self.path_to_file:
            self.filename = self.path_to_file
        self.gfile = Gfile(self.filename, self.bldr, "")
        self.style()
        self.screen.reparent(self)

        self.show_all()

#    def scroll(self):
##        Get current csroll and set new value
#        adj = self.widget[scrolledmdi].get_vadjustment()
#        if self.crnt_lbl_nmbr < self.up_lbl:
#            scroll_to = (adj.upper-adj.lower)*(self.crnt_lbl_nmbr/lbls_nmbr)
#            if scroll_to>adj.upper: scroll_to = adj.upper
#        elif self.crnt_lbl_nmbr > self.dwn_lbl:
#            scroll_to = (adj.upper-adj.lower)*(self.crnt_lbl_nmbr/lbls_nmbr)-adj.page_size
#            if scroll_to<adj.lower: scroll_to = adj.lower
#        else: return
#        adj.set_value(scroll_to)

#    def reload(self):
##        self.model.clear()
##        Clear GTK

#        try:
#            fp = open(self.filename)
#        except:
#            return
#        lines = map(str.strip, fp.readlines())
#        fp.close()
#        lines = filter(bool, lines)

#        boxs = self.widgets.get_list(gtk.EventBox)
#        for box in boxs: 
#            self.widget[mdivbox].remove (box)
#        
#        for l in lines:
#            eventbox = gtk.EventBox()
#            eventbox.set_size_request(250, 15)
#            label = gtk.Label(l)
#            label.set_alignment(0.05, 0.5)
#            eventbox.add(label)
#            self.widget[mdivbox].pack_start(eventbox,True,False,0)
#            eventbox.show()

#        eventbox = gtk.EventBox()
#        eventbox.set_size_request(250, 15)
#        label = gtk.Label("==end of file=")
#        label.set_alignment(0.05, 0.5)
#        eventbox.add(label)
#        self.widget[mdivbox].pack_start(eventbox,True,False,0)
#        eventbox.show()

    def on_key_pressed(self, data):
        if self.sensitive:
            self.gfile.key_press(data)
#        self.emit('change-screen')
#        if data == "1": self.change_label("screen_rvar")

    def on_soft_key_pressed(self, key):
        if key == "PARENT":
            if self.prnt_screen == "main_screen":
                self.crnt_screen = "main_screen"
                self.lght_btn = ""
                self.actions_on_enter()
        elif key == "Workpiece":
            self.lght_btn = "lblY2"
            self.prnt_screen == "main_screen"
            self.change_label("screen_aux")
        elif key == "Part\nprograms":
            self.crnt_screen = "screen_tool"
            self.change_screen()
        elif key == "Sub\nprograms":
            self.crnt_screen = "screen_gfile"
            self.change_screen()
        elif key == "Strand\ncycles":
            print("WCS")
        elif key == "User\ncycles":
            print("WCS")
        elif key == "Manufact.\nCycles":
            print("WCS")
        elif key == "Memory\ninformation":
            print("WCS")
        elif key == "New":
            print("WCS")
        elif key == "Copy":
            self.lght_btn = "lblY1"
            self.change_label("screen_aux")
        elif key == "Insert":
            self.lght_btn = "lblY2"
            self.change_label("screen_aux")
        elif key == "Delete":
            self.lght_btn = "lblY3"
            self.change_label("screen_aux")
        elif key == "Rename":
            print("Axis")
        elif key == "Alter\nenable":
            print("Zoom")
        elif key == "Program\nselect":
            print("WCS")

    def change_screen(self):
        self.emit('change-screen')

    def change_label(self, label_mark):
        self.labelX = labels_X(label_mark)
        self.labelY = labels_Y(label_mark)
        self.emit('change-labels')

    def actions_on_leave():
        self.style()

    def actions_on_enter(screen = "screen_gfile"):
        self.labelX = labels_X(screen)
        self.labelY = labels_Y(screen)
#        self.prnt_screen = "main_screen"
#        self.crnt_screen = "main_screen"
#        self.lght_btn = ""
        self.change_label(screen)
        self.style()

    def style(self):
#            boxs = self.widget.get_list(gtk.EventBox)
#            for box in boxs: 
#                box.modify_bg(gtk.STATE_NORMAL, self.colors.white)
#            self.lbl_lst.highlite_lbl()
#            ntbs = self.widget.get_list(gtk.Table)
#            for ntb in ntbs: 
#                ntb.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)

            lbls = self.widget.get_list(gtk.Label)
            for lbl in lbls: 
                lbl.modify_font(pango.FontDescription('dejavusans condensed 10'))

#            self.widget["vpaned6"].modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
#            self.widget["viewport2"].modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
#            self.widget["rvar_header"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)

