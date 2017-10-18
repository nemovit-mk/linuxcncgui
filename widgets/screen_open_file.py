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

from open_file import Open_File
from labels_data import *

#from hal_widgets import _HalWidgetBase
import linuxcnc
#from hal_glib import GStat
#from hal_actions import _EMC_ActionBase, ensure_mode
#from testui import myGUI
datadir = os.path.abspath( os.path.dirname( __file__ ) )

class Screen_Open_File(gtk.VBox):
    __gtype_name__ = 'Screen_Open_File'
    __gsignals__ = {
        'change-screen': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
        'change-labels':  (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
    }
    def __init__(self, *a, **kw):
        self.__gobject_init__()
        gtk.VBox.__init__(self, *a, **kw)

#        global path_to_file

        # if 'NO_FORCE_HOMING' is true, MDI  commands are allowed before homing.
        inifile = os.environ.get('INI_FILE_NAME', '/dev/null')
        self.ini = linuxcnc.ini(inifile)
        no_home_required = int(self.ini.find("TRAJ", "NO_FORCE_HOMING") or 0)
        self.work_dir = self.ini.find('DISPLAY', 'WORKPIECE_DIR') or "~"
        self.part_prog_dir = self.ini.find('DISPLAY', 'PART_PROG_DIR') or "~"
        self.sub_prog_dir = self.ini.find('DISPLAY', 'SUB_PROG_DIR') or "~"
        self.strand_cycl_dir = self.ini.find('DISPLAY', 'STRAND_CYCLES') or "~"
        self.user_cycl_dir = self.ini.find('DISPLAY', 'USER_CYCLES') or "~"
        self.manufact_cycl_dir = self.ini.find('DISPLAY', 'MANUFACT_CYCLES') or "~"

        self.path = self.sub_prog_dir
        self.path = os.path.expanduser(self.path)

        gladefile = os.path.join( datadir, "../ui/open.glade" )
        self.bldr = gtk.Builder()
        self.bldr.add_from_file(gladefile)
        self.screen = self.bldr.get_object("container")

        self.sensitive = True
        self.labelX = labels_X("screen_open_file")
        self.labelY = labels_Y("screen_open_file")
        self.prnt_screen = "main_screen"
        self.crnt_screen = "screen_open_file"
        self.lght_btn = "lblX3"

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

        self.open_file = Open_File(self.path, self.bldr, "")
        
        self.open_file.widget["sub_menu_header"].set_label("Sub programs")

#        self.actions_on_enter()
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
            if data == "INPUT":
#                global path_to_file
                self.path_to_file = self.open_file.crnt_file
                self.crnt_screen = "screen_gfile"
                self.change_screen()
            else: 
                self.open_file.key_press(data)

    def on_soft_key_pressed(self, key):
        if key == "PARENT":
            if self.prnt_screen == "main_screen":
                self.crnt_screen = "main_screen"
                self.lght_btn = ""
                self.actions_on_enter()
        elif key == "Workpiece":
            self.lght_btn = "lblX1"
            self.open_file.path = os.path.expanduser(self.work_dir)
#            self.prnt_screen == "main_screen"
            self.crnt_screen = "screen_open_file"
            self.change_label("screen_open_file")
            self.open_file.read_dir()
            self.open_file.widget["sub_menu_header"].set_label("Workpiece")
        elif key == "Part\nprograms":
            self.lght_btn = "lblX2"
            self.open_file.path = os.path.expanduser(self.part_prog_dir)
#            self.prnt_screen == "main_screen"
            self.crnt_screen = "screen_open_file"
            self.change_label("screen_open_file")
            self.open_file.read_dir()
            self.open_file.widget["sub_menu_header"].set_label("Part programs")
        elif key == "Sub\nprograms":
            self.lght_btn = "lblX3"
            self.open_file.path = os.path.expanduser(self.sub_prog_dir)
#            self.prnt_screen == "main_screen"
            self.crnt_screen = "screen_open_file"
            self.change_label("screen_open_file")
            self.open_file.read_dir()
            self.open_file.widget["sub_menu_header"].set_label("Sub programs")
        elif key == "Strand\ncycles":
            self.lght_btn = "lblX4"
            self.open_file.path = os.path.expanduser(self.strand_cycl_dir)
#            self.prnt_screen == "main_screen"
            self.crnt_screen = "screen_open_file"
            self.change_label("screen_open_file")
            self.open_file.read_dir()
            self.open_file.widget["sub_menu_header"].set_label("Strand cycles")
        elif key == "User\ncycles":
            self.lght_btn = "lblX5"
            self.open_file.path = os.path.expanduser(self.user_cycl_dir)
#            self.prnt_screen == "main_screen"
            self.crnt_screen = "screen_open_file"
            self.change_label("screen_open_file")
            self.open_file.read_dir()
            self.open_file.widget["sub_menu_header"].set_label("User cycles")
        elif key == "Manufact.\nCycles":
            self.lght_btn = "lblX6"
            self.open_file.path = os.path.expanduser(self.manufact_cycl_dir)
#            self.prnt_screen == "main_screen"
            self.crnt_screen = "screen_open_file"
            self.change_label("screen_open_file")
            self.open_file.read_dir()
            self.open_file.widget["sub_menu_header"].set_label("Manufact. Cycles")
        elif key == "Memory\ninformation":
            self.lght_btn = "lblX7"
            print("OK")
        elif key == "New":
            print("New")
        elif key == "Copy":
            print("Copy")
        elif key == "Insert":
            print("Insert")
        elif key == "Delete":
            print("Delete")
        elif key == "Rename":
            print("Rename")
        elif key == "Alter\nenable":
            print("Enable")
        elif key == "Program\nselect":
            print("Select")

    def change_screen(self):
        self.emit('change-screen')

    def change_label(self, label_mark):
        self.labelX = labels_X(label_mark)
        self.labelY = labels_Y(label_mark)
        self.emit('change-labels')

    def actions_on_leave(self):
        self.labelX = labels_X("screen_open_file")
        self.labelY = labels_Y("screen_open_file")
        self.prnt_screen = "main_screen"
        self.crnt_screen = "screen_open_file"
        self.lght_btn = "lblX3"

        self.open_file.path = os.path.expanduser(self.strand_cycl_dir)
        self.open_file.read_dir()
        self.open_file.widget["sub_menu_header"].set_text("Strand cycles")
        self.style()

    def actions_on_enter(screen = "screen_open_file"):
#        self.labelX = labels_X(screen)
#        self.labelY = labels_Y(screen)

#        self.crnt_screen = "screen_open_file"
#        self.prnt_screen = "main_screen"
##        self.crnt_screen = "main_screen"
##        self.lght_btn = ""
#        self.lght_btn = "lblX3"
#        self.change_label(screen)
#        self.open_file.path = os.path.expanduser(self.sub_prog_dir)
#        self.open_file.read_dir()
#        self.open_file.widget["sub_menu_header"].set_text("Sub programs")
        self.style()

    def style(self):
        print("OK")
        #Set style for element1



