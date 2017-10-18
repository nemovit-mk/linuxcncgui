#!/usr/bin/env python
# 
# Screen widget
#
# Tool screen for Sinumeric 840D project
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

from label_list import LabelList
from labels_data import *
from color import Color

from widget import Widgets


#from hal_widgets import _HalWidgetBase
import linuxcnc
#from hal_glib import GStat
#from hal_actions import _EMC_ActionBase, ensure_mode
#from testui import myGUI

class Screen_Tool(gtk.VBox):
    __gtype_name__ = 'Screen_Tool'
    __gsignals__ = {
        'change-screen': (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
        'change-labels':  (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
    }
    def __init__(self, *a, **kw):
        self.__gobject_init__()
        gtk.VBox.__init__(self, *a, **kw)
#        self.gstat = GStat()
        # if 'NO_FORCE_HOMING' is true, MDI  commands are allowed before homing.
#        inifile = os.environ.get('INI_FILE_NAME', '/dev/null')
#        self.ini = linuxcnc.ini(inifile)
#        no_home_required = int(self.ini.find("TRAJ", "NO_FORCE_HOMING") or 0)
#        path = self.ini.find('DISPLAY', 'MDI_HISTORY_FILE') or '~/.axis_mdi_history'
#        self.filename = os.path.expanduser(path)

        self.sensitive = True

        self.action = gobject.GObject()

        self.labelX = labels_X("screen_tool")
        self.labelY = labels_Y("screen_tool")
        self.prnt_screen = "main_screen"
        self.crnt_screen = "screen_tool"
        self.lght_btn = "lblX1"

        self.colors = Color()
#        self.labelX = labels_X("screen_tool")
#        self.labelY = labels_Y("screen_tool")
#        self.lght_btn = "lblX1"

#        rvar_lbl = [ ["lbl_rvar_0", "lbl_rvar_13"],
#                    ["lbl_rvar_1", "lbl_rvar_14"],
#                    ["lbl_rvar_2", "lbl_rvar_15"],
#                    ["lbl_rvar_3", "lbl_rvar_16"],
#                    ["lbl_rvar_4", "lbl_rvar_17"],
#                    ["lbl_rvar_5", "lbl_rvar_18"],
#                    ["lbl_rvar_6", "lbl_rvar_19"],
#                    ["lbl_rvar_7", "lbl_rvar_20"],
#                    ["lbl_rvar_8", "lbl_rvar_21"],
#                    ["lbl_rvar_9", "lbl_rvar_22"],
#                    ["lbl_rvar_10", "lbl_rvar_23"],
#                    ["lbl_rvar_11", "lbl_rvar_24"],
#                    ["lbl_rvar_12", "lbl_rvar_25"],]
#        crnt_lbl = "lbl_rvar_0"
#        permissions = [True, True, True, True]
#        self.params = [rvar_lbl, crnt_lbl, permissions]
#        self.lbl_lst = LabelList(self.params, self.bldr)

        self.model = gtk.ListStore(str)

        self.tv = gtk.TreeView()
        self.tv.set_model(self.model)
        self.cell = gtk.CellRendererText()

        self.col = gtk.TreeViewColumn("Command")
        self.col.pack_start(self.cell, True)
        self.col.add_attribute(self.cell, 'text', 0)

        self.tv.append_column(self.col)
        self.tv.set_search_column(0)
        self.tv.set_reorderable(False)
        self.tv.set_headers_visible(True)

        scroll = gtk.ScrolledWindow()
        scroll.add(self.tv)
        scroll.props.hscrollbar_policy = gtk.POLICY_AUTOMATIC
        scroll.props.vscrollbar_policy = gtk.POLICY_AUTOMATIC

        self.entry = gtk.Entry()
        self.entry.set_icon_from_stock(gtk.ENTRY_ICON_SECONDARY, 'gtk-ok')

#        self.entry.connect('activate', self.submit)
#        self.entry.connect('icon-press', self.submit)
#        self.tv.connect('cursor-changed', self.select)

     #   self.connect('my_syganal', on_my_signal)

        self.pack_start(scroll, True)
        self.pack_start(self.entry, False)
#        self.gstat.connect('state-off', lambda w: self.set_sensitive(False))
#        self.gstat.connect('state-estop', lambda w: self.set_sensitive(False))
#        self.gstat.connect('interp-idle', lambda w: self.set_sensitive(self.machine_on() and ( self.is_all_homed() or no_home_required ) ))
#        self.gstat.connect('interp-run', lambda w: self.set_sensitive(not self.is_auto_mode()))
#        self.gstat.connect('all-homed', lambda w: self.set_sensitive(self.machine_on()))
#        self.reload()
        self.show_all()


    def update(self):
        print("OK")

####################################################
#   Tooltable
####################################################

    # toggle the tool editor page forward
    # reload the page when doing this
    # If the user specified a tool editor spawn it. 
    def reload_tooltable(self):
        # show the tool table page or return to the main page
        if not self.widgets.notebook_main.get_current_page() == 3:
            self.widgets.notebook_main.set_current_page(3)
        else:
            self.widgets.notebook_main.set_current_page(0)
            return
        # set the tooltable path from the INI file and reload it
        path = os.path.join(CONFIGPATH,self.data.tooltable)
        print "tooltable:",path
        self.widgets.tooledit1.set_filename(path)
        # see if user requested an external editor and spawn it 
        editor = self.data.tooleditor
        if not editor == None:
            res = os.spawnvp(os.P_WAIT, editor, [editor, path])
            if res:
                self.notify(_("Error Message"),_("Tool editor error - is the %s editor available?"% editor,ALERT_ICON,3))
        # tell linuxcnc that the tooltable may have changed
        self.emc.reload_tooltable(1)


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
#        elif key == "MENU":
#            self.lght_btn = ""
#            self.prnt_screen == "main_screen"
#            self.change_label("main_screen")
        elif key == "Tool\noffset":
            self.lght_btn = "lblX1"
            self.prnt_screen == "main_screen"
            self.change_label("screen_tool")
        elif key == "R\nvariables":
            self.crnt_screen = "screen_rvar"
            self.change_screen()
        elif key == "Setting\ndata":
            self.lght_btn = "lblX3"
            self.change_label("screen_tool")
        elif key == "Work\noffset":
            self.lght_btn = "lblX4"
            self.change_label("screen_tool")
        elif key == "User\ndata":
            self.lght_btn = "lblX5"
            self.change_label("screen_tool")
        elif key == "Determine\ncompens.":
            self.lght_btn = "lblX8"
            self.change_label("screen_tool")
        elif key == "T no +":
            self.lght_btn = "lblY1"
            self.change_label("screen_tool")
        elif key == "T no -":
            self.lght_btn = "lblY2"
            self.change_label("screen_tool")
        elif key == "D no +":
            self.lght_btn = "lblY3"
            self.change_label("screen_tool")
        elif key == "D no -":
            self.lght_btn = "lblY4"
            self.change_label("screen_tool")
        elif key == "Delete":
            self.lght_btn = "lblY5"
            self.change_label("screen_tool")
        elif key == "Details":
            self.lght_btn = "lblY6"
            self.change_label("screen_tool")
        elif key == "Overview":
            self.lght_btn = "lblY7"
            self.change_label("screen_tool")
        elif key == "New\ntool":
            self.lght_btn = "lblY8"
            self.change_label("screen_tool")

    def change_screen(self):
        self.actions_on_leave()
        self.emit('change-screen')

    def change_label(self, label_mark):
        self.labelX = labels_X(label_mark)
        self.labelY = labels_Y(label_mark)
        self.emit('change-labels')

    def actions_on_leave(self):
        self.lght_btn = "lblX1"
        self.prnt_screen == "main_screen"
        self.labelX = labels_X("screen_tool")
        self.labelY = labels_Y("screen_tool")

    def actions_on_enter(screen = "screen_tool"):
        self.labelX = labels_X(screen)
        self.labelY = labels_Y(screen)
#        self.prnt_screen = "main_screen"
#        self.crnt_screen = "main_screen"
#        self.lght_btn = ""
        self.change_label(screen)
        self.style()


#    def style(self):
#            boxs = self.widget.get_list(gtk.EventBox)
#            for box in boxs: 
#                box.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)

#            ntbs = self.widget.get_list(gtk.Notebook)
#            for ntb in ntbs: 
#                ntb.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)

#            lbls = self.widget.get_list(gtk.Label)
#            for lbl in lbls: 
#                lbl.modify_font(pango.FontDescription('dejavusans condensed 10'))


#            self.widget["dro_head1"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
#            self.widget["dro_head2"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
#            self.widget["dro_head3"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
#            self.widget["dro_head4"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
#            self.widget["spindle_head1"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
#            self.widget["spindle_head2"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
#            self.widget["spindle_head3"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
#            self.widget["feed_head"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)
#            self.widget["tool_head"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)

