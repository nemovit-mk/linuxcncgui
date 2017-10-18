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

class Main_Screen(gtk.VBox):
    __gtype_name__ = 'Main_Screen'
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
        path = self.ini.find('DISPLAY', 'MDI_HISTORY_FILE') or '~/.axis_mdi_history'
        self.filename = os.path.expanduser(path)

        self.action = gobject.GObject()
        gladefile = os.path.join( datadir, "../ui/main.glade" )
        self.bldr = gtk.Builder()
        self.bldr.add_from_file(gladefile)
        self.screen = self.bldr.get_object("main_container")
        self.widget = Widgets(self.bldr)

        self.mdi = self.bldr.get_object("mdi")
#        self.widget = Widgets(self.bldr)
        self.sensitive = True

        self.labelX = labels_X("main_screen")
        self.labelY = labels_Y("main_screen")
        self.prnt_screen = "main_screen"
        self.crnt_screen = "main_screen"
        self.lght_btn = ""

#        parent = None
#        md = gtk.MessageDialog(parent, 
#            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
#            gtk.BUTTONS_CLOSE, str(self.bldr))
#        md.run()
##        self.pack_start(self.screen)
#        self.sensitive = True
#        mdi_lbl = [ ["mdilabel0",],
#                    ["",], ]
#        crnt_lbl = "mdilabel1"
#        permissions = [True, True, True, True]
#        self.params = [mdi_lbl, crnt_lbl, permissions]
#        self.lbl_lst = LabelList(self.params, self.bldr)

        self.colors = Color()

#        self.gfile = Gfile(self.filename, self.bldr, "")
        self.screen.reparent(self)

        self.style()
#        self.prnt_screen = "main_screen"
#        self.crnt_screen = "main_screen"
#        self.lght_btn = ""

        self.show_all()

    def update(self):
        if self.action.x_in_ref: 
            self.widget.xhmd.set_label("X")
        else: 
            self.widget.xhmd.set_label("O")
        if self.action.z_in_ref: 
            self.widget.zhmd.set_label("X")
        else:
            self.widget.zhmd.set_label("O")

        self.widget.dro_x.set_label(str(self.action.dro_abs_x))
        self.widget.dro_z.set_label(str(self.action.dro_abs_z))
        self.widget.dro_c.set_label(str(self.action.dro_abs_c))
        
        self.widget.act_s.set_label(str(self.action.dro_abs_c))
        self.widget.set_s.set_label(str(self.action.dro_abs_c))
        self.widget.pos_s.set_label(str(self.action.dro_abs_c))
        self.widget.spindle_percent.set_label(str(self.action.dro_abs_c))


        self.widget.act_feed.set_label(str(self.action.dro_abs_c))
        self.widget.set_feed.set_label(str(self.action.dro_abs_c))
        self.widget.feed_per.set_label(str(self.action.dro_abs_c))
        self.widget.presel_tool.set_label(str(self.action.dro_abs_c))
        self.widget.tool_g_lbl.set_label(str(self.action.dro_abs_c))

    def on_key_pressed(self, data):
        if self.sensitive:
            self.mdi.on_key_pressed(data)
#        self.emit('change-screen')
#        if data == "1": self.change_label("screen_rvar")

    def on_soft_key_pressed(self, key):
        if key == "PARENT":
            if self.prnt_screen == "main_screen":
                self.crnt_screen = "main_screen"
                self.lght_btn = ""
                self.actions_on_enter()
        elif key == "MENU":
            self.lght_btn = ""
            self.prnt_screen == "main_screen"
            self.change_label("main_screen")
        elif key == "Machining":
            self.lght_btn = "lblY2"
            self.prnt_screen == "main_screen"
            self.change_label("screen_aux")
        elif key == "Parameters":
            self.crnt_screen = "screen_tool"
            self.change_screen()
        elif key == "Programs":
            self.crnt_screen = "screen_open_file"
#            self.actions_on_leave()
            self.change_screen()
        elif key == "AUTO":
            self.action.set_auto()
            print("WCS")
        elif key == "MDI":
            self.action.set_mdi()
            print("WCS")
        elif key == "JOG":
            self.action.set_jog()
            print("WCS")
        elif key == "REPOS":
            print("WCS")
        elif key == "REF":
            print("WCS")
        elif key == "G fct.+\ntransf.":
            self.lght_btn = "lblY1"
            self.change_label("screen_aux")
        elif key == "Auxiliary\nfunction":
            self.lght_btn = "lblY2"
            self.change_label("screen_aux")
        elif key == "Spindles":
            self.lght_btn = "lblY3"
            self.change_label("screen_aux")
        elif key == "Axis\nfeedrate":
            print("Axis")
        elif key == "Zoom\nact.val":
            print("Zoom")
        elif key == "WCS":
            print("WCS")


    def change_screen(self):
        self.emit('change-screen')

    def change_label(self, label_mark):
        self.labelX = labels_X(label_mark)
        self.labelY = labels_Y(label_mark)
        self.emit('change-labels')

    def actions_on_leave(self):        
        self.labelX = labels_X("main_screen")
        self.labelY = labels_Y("main_screen")
        self.prnt_screen = "main_screen"
        self.crnt_screen = "main_screen"
        self.lght_btn = ""

    def actions_on_enter(screen = "main_screen"):
#        self.labelX = labels_X(screen)
#        self.labelY = labels_Y(screen)
##        self.prnt_screen = "main_screen"
##        self.crnt_screen = "main_screen"
##        self.lght_btn = ""
#        self.change_label(screen)
        self.style()

    def style(self):
            boxs = self.widget.get_list(gtk.EventBox)
            for box in boxs: 
                box.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)

            ntbs = self.widget.get_list(gtk.Notebook)
            for ntb in ntbs: 
                ntb.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)

            lbls = self.widget.get_list(gtk.Label)
            for lbl in lbls: 
                lbl.modify_font(pango.FontDescription('dejavusans condensed 10'))


            self.widget["dro_head1"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
            self.widget["dro_head2"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
            self.widget["dro_head3"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
            self.widget["dro_head4"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
            self.widget["spindle_head1"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
            self.widget["spindle_head2"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
            self.widget["spindle_head3"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
            self.widget["feed_head"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
            self.widget["tool_head"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)

#            for i in self.screen.get_children():
#                if isinstance(i, gtk.Layout):
#                    i.modify_bg(gtk.STATE_NORMAL, self.colors.dgray)
#                if isinstance(i, gtk.Notebook):
#                    i.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
#                if isinstance(i, gtk.Table):
#                    i.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
#                if isinstance(i, gtk.HBox):
#                    i.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
#                if isinstance(i, gtk.Label):
#                    i.modify_font(pango.FontDescription('dejavusans condensed 10'))
#                    i.get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
#                if isinstance(i, gtk.EventBox):
#                    i.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
        #Set style for element1


