#!/usr/bin/env python
#
# G-files widget
#
# Copyright (c) 2017  Maksym Kotelnikov
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
from os import listdir
from os.path import isfile, join

import gobject, gtk

from widget import Widgets
from color import Color
#from hal_widgets import _HalWidgetBase
import linuxcnc
#from hal_glib import GStat
#from hal_actions import _EMC_ActionBase, ensure_mode
#from testui import myGUI
datadir = os.path.abspath( os.path.dirname( __file__ ) )

class Open_File():
    def __init__(self, path, box_widget, key):

        print ("Create file choser %r"% path, box_widget)
        self.key = key
        self.path = path
        self.widget = Widgets(box_widget)
        self.crnt_file = ""

        self.colors = Color()

        
        boxs = self.widget.get_list(gtk.EventBox)
        for box in boxs: 
                box.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)

        self.widget["sub_menu_header"].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.blue)

        for i in self.widget["scrolled"].get_children():
                if isinstance(i, gtk.Layout):
                    i.modify_bg(gtk.STATE_NORMAL, self.colors.dgray)
                if isinstance(i, gtk.Notebook):
                    i.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
                if isinstance(i, gtk.Table):
                    i.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
                if isinstance(i, gtk.HBox):
                    i.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
                if isinstance(i, gtk.Label):
                    i.modify_font(pango.FontDescription('dejavusans condensed 10'))
                    i.get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
                if isinstance(i, gtk.EventBox):
                    i.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)


        self.read_dir()
#        self.crnt_plc = len(self.crnt_lbl.get_text())

#        self.highlite_lbl()

        # Additional help lists
        self.dirrection = ["LEFT", "RIGHT", "UP", "DOWN"]
        self.actions = ["PAGE_DOWN", "PAGE_UP", "BACKSPACE", "INPUT", "INSERT", "END", "SELECT", "CHANNEL", "ALARM_CANCEL", "NEXT_WIN", "HELP"]
#        self.show_all()

#        gladefile = os.path.join( datadir, "ui/mdi.glade" )
#        self.bldr = gtk.Builder()
#        self.bldr.add_from_file(gladefile)
#        self.screen = self.bldr.get_object("container")
##        self.pack_start(self.screen)
#        self.sensitive = True
#        mdi_lbl = [ ["mdilabel0",],
#                    ["",], ]
#        crnt_lbl = "mdilabel1"
#        permissions = [True, True, True, True]
#        self.params = [mdi_lbl, crnt_lbl, permissions]
#        self.lbl_lst = LabelList(self.params, self.bldr)


    def scroll(self):
#        Get current csroll and set new value
        adj = self.widget["scrolled"].get_vadjustment()
        if self.crnt_lbl_nmbr < self.list.index(self.up_lbl):
            scroll_to = (adj.upper-adj.lower)*((self.crnt_lbl_nmbr+1)/self.lbls_nmbr)
            if scroll_to > adj.upper: scroll_to = adj.upper
            self.up_lbl = self.crnt_lbl
            self.dwn_lbl = self.list[self.list.index(self.up_lbl) + self.lbls_pp]
        elif self.crnt_lbl_nmbr > self.list.index(self.dwn_lbl):
            scroll_to = (adj.upper-adj.lower)*((self.crnt_lbl_nmbr+1)/self.lbls_nmbr)-adj.page_size
            if scroll_to < adj.lower: scroll_to = adj.lower
            self.dwn_lbl = self.crnt_lbl
            self.up_lbl = self.list[self.list.index(self.dwn_lbl) - self.lbls_pp]
        else: return
        print("scrool to %r"% scrool_to)
        adj.set_value(scroll_to)

    def read_dir(self):
        adj = self.widget["scrolled"].get_vadjustment()
#        self.widget["sub_menu_header"].set_text()
#        onlyfiles = []
#        del onlyfiles[:]
        print ("path %r"% self.path)
        try:
            onlyfiles = [f for f in listdir(self.path) if isfile(join(self.path, f))]
#            fp = open(self.filename)
        except:
            print ("cant read %r"% self.path)
            return
#        lines = map(str.strip, fp.readlines())
#        fp.close()
#        lines = filter(bool, lines)

        if isinstance(self.widget["textvbox"], gtk.Container):
            for i in self.widget["textvbox"].get_children():
                self.widget["textvbox"].remove(i)
#foreach (Gtk.Widget element in self.widget["textvbox"].get_children ())
#        self.widget["textvbox"].remove (element);

#        boxs = self.widget.get_list(gtk.EventBox, self.widget["textvbox"])
#        n =0
#        if boxs != None:
#            for box in list(boxs): 
#                print("-", box)
#                n = n+1
#                try:
#                    self.widget["textvbox"].remove(box)
#                except:
#                    pass

#        if self.key == "mdi":
#            all_heigth = 140
#        else:
#            all_heigth = 292
        all_heigth = 225
        row_heigth = 15

        self.list = []
#        del self.list[:]
        self.file_list = []
#        del self.file_list[:]
        print("- %r"% len(self.list))

        for f in onlyfiles:
            file_path = os.path.join(self.path, f)
            eventbox = gtk.EventBox()
            eventbox.set_size_request(-1, row_heigth)
            text_line = "{0:<{col1}}{1:<{col2}}{2:<{col3}}{3:<{col4}}{4:<{col5}}".format(str(f),os.path.splitext(f)[-1].upper(), str(os.path.getsize(file_path)), time.strftime('%m/%d/%Y', time.gmtime(os.path.getmtime(file_path ))), "X",col1=40,col2=6,col3=10,col4=14,col5=4)
            print("file info %r"% text_line)
            label = gtk.Label(text_line)
            label.set_alignment(0.05, 0.5)
            eventbox.add(label)
            self.widget["textvbox"].pack_start(eventbox,True,False,0)
            self.list.append(label)
            self.file_list.append(file_path)
            eventbox.show()
#        for l in lines:
#            print("%r"% l)
#            eventbox = gtk.EventBox()
#            eventbox.set_size_request(-1, row_heigth)
#            label = gtk.Label(l)
#            label.set_alignment(0.05, 0.5)
#            eventbox.add(label)
#            self.widget["textvbox"].pack_start(eventbox,True,False,0)
#            self.list.append(label)
#            eventbox.show()
        
        if len(self.list) < 1:
            eventbox = gtk.EventBox()
            eventbox.set_size_request(-1, row_heigth)
            label = gtk.Label("")
            label.set_alignment(0.05, 0.5)
            eventbox.add(label)
            self.widget["textvbox"].pack_start(eventbox,True,False,0)
            self.list.append(label)
            eventbox.show()


        self.lbls_nmbr = len(self.list)
        self.crnt_lbl = self.list[0]
        self.crnt_lbl_nmbr = 0
        self.up_lbl = self.crnt_lbl
        self.lbls_pp = int(19)
#        self.lbls_pp = int(adj.page_size/row_heigth)
        if (len(self.list)<self.list.index(self.up_lbl) + self.lbls_pp - 1):
            self.dwn_lbl = self.list[len(self.list) - 1]
        else:
            self.dwn_lbl = self.list[self.list.index(self.up_lbl) + self.lbls_pp - 1]
        self.crnt_file = self.file_list[self.crnt_lbl_nmbr]
#int(adj.page_size/row_heigth)
#        self.dwn_lbl = self.list[self.list.index(self.up_lbl) + self.lbls_pp - 1]

#        print("list", len(self.list))
#        print("in crnt ", self.crnt_lbl.get_text())
#        print("in up ", self.up_lbl.get_text())
#        print("in dwn ", self.dwn_lbl.get_text())

#        eventbox = gtk.EventBox()
#        eventbox.set_size_request(-1, row_heigth)
#        label = gtk.Label("==end of file=")
#        label.set_alignment(0.15, 0.5)
#        eventbox.add(label)
#        eventbox.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
#        self.widget["textvbox"].pack_start(eventbox,True,True,0)
#        eventbox.show()

        last_box_height = all_heigth - (self.lbls_nmbr) * row_heigth
        if last_box_height < 0: last_box_height = -1
#        print("heigth %r"% last_box_height)
        eventbox = gtk.EventBox()
        eventbox.set_size_request(-1, last_box_height)
        label = gtk.Label(str(last_box_height))
        label.set_alignment(0.15, 0.5)
        eventbox.add(label)
        eventbox.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
        self.widget["textvbox"].pack_end(eventbox,True,True,0)
        eventbox.show()

        self.widget["textvbox"].show_all()
        self.highlite_lbl()

    def write (self, *a):
#        cmd = self.entry.get_text()
#        if not cmd:
#            return
#        ensure_mode(self.stat, self.linuxcnc, linuxcnc.MODE_MDI)

        try:
            fp = open(self.filename, 'a')
            fp.write(cmd + "\n")
            fp.close()
        except:
            pass

#        self.linuxcnc.mdi(cmd)
#        last = self.model.append((cmd,))
#        path = self.model.get_path(last)
#        self.tv.scroll_to_cell(path)
#        self.tv.set_cursor(path)
#        self.entry.set_text('')
#        self.entry.grab_focus()

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

#        boxs = self.widgets.get_list(gtk.EventBox,self.widget[textvbox])
#        for box in boxs: 
#            self.widget[textvbox].remove (box)
#        
#        for l in lines:
#            eventbox = gtk.EventBox()
#            eventbox.set_size_request(250, 15)
#            label = gtk.Label(l)
#            label.set_alignment(0.05, 0.5)
#            eventbox.add(label)
#            self.widget[textvbox].pack_start(eventbox,True,False,0)
#            eventbox.show()

#        self.list = self.widgets.get_list(gtk.Label,self.widget[textvbox])
#        self.lbls_nmbr = len(self.list)

#        eventbox = gtk.EventBox()
#        eventbox.set_size_request(250, 15)
#        label = gtk.Label("==end of file=")
#        label.set_alignment(0.05, 0.5)
#        eventbox.add(label)
#        self.widget[textvbox].pack_start(eventbox,True,False,0)
#        eventbox.show()



#    def on_key_pressed(self, data):
#        if self.sensitive:
#            self.lbl_lst.key_press(data)



#        # Create instanse of class. Set internal values
#        self.widget = Widgets(box_widget)
##        labels = self.widget.get_list(gtk.Label)
##        for lbl in labels: 
##            print("lbl - %r"% lbl)
#        self.colors = Color()
#        self.list = label_list
#        self.crnt_lbl = current_label
#        self.crnt_plc = len(self.widget[self.crnt_lbl].get_text())
#        self.set_permissions (permissions)
#        self.get_index()
#        self.highlite_lbl()


    def highlite_lbl(self, new_lbl = None):
#        print("inside highlite", self.crnt_lbl.get_text())
        if new_lbl:
            self.crnt_lbl.get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
            new_lbl.get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.orange)
        else:
#            self.list[0].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.orange)
            for lbl in self.list:
                if lbl: lbl.get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
            self.crnt_lbl.get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.orange)

    def set_permissions (self, permissions):
        allow_alfa_in, allow_num_in, allow_dirrection, allow_action = permissions #Unpack

    def key_press (self, sign):
        if sign == None: return
#        sign = str (sign)
        print("sign is %r"% sign)
        if len(sign) == 1:
#            if sign.isalpha() and allow_alfa_in: self.put_sign(sign)
#            elif sign.isnumeric() and allow_num_in: self.put_sign(sign)
#            else: self.put_sign(sign)
            return
#            self.put_sign(sign)
        elif sign in self.dirrection: self.change_label(sign)
        elif sign in self.actions: self.make_action(sign)

    def put_sign (self, sign):
        text = self.crnt_lbl.get_text()
        text = text[:self.crnt_plc] + sign + text[self.crnt_plc:]
        try:
            self.crnt_lbl.set_text(text)
            self.crnt_plc = self.crnt_plc + 1
        except:
            pass

#    def get_index(self):
#        self.maxY = len(self.list) - 1
#        self.y = 0
#        for lst in self.list:
#            try:
#                self.x = lst.index(self.crnt_lbl)
#            except:
#                self.x = None
#            if self.x != None:
#                self.maxX = len(lst) - 1
#                break
#            self.y = self.y + 1

    def change_label(self, dirrection):
        if dirrection == "LEFT":
            print("OK")
#            self.crnt_plc = self.crnt_plc - 1
#            if self.crnt_plc < 0:  self.crnt_plc = 0
        elif dirrection == "RIGHT":
            print("OK")
#            self.crnt_plc = self.crnt_plc + 1
#            if self.crnt_plc > len(self.crnt_lbl.get_text()):  self.crnt_plc = len(self.crnt_lbl.get_text())
        elif dirrection == "UP":
            self.crnt_lbl_nmbr = self.crnt_lbl_nmbr - 1
            if self.crnt_lbl_nmbr < 0: self.crnt_lbl_nmbr = 0
            self.highlite_lbl(self.list[self.crnt_lbl_nmbr])
            self.crnt_lbl = self.list[self.crnt_lbl_nmbr]
            self.crnt_file = self.file_list[self.crnt_lbl_nmbr]
#            self.crnt_plc = len(self.crnt_lbl.get_text())
            self.scroll()
        elif dirrection == "DOWN":
            self.crnt_lbl_nmbr = self.crnt_lbl_nmbr + 1
            if self.crnt_lbl_nmbr > (self.lbls_nmbr-1): self.crnt_lbl_nmbr = (self.lbls_nmbr-1)
            self.highlite_lbl(self.list[self.crnt_lbl_nmbr])
            self.crnt_lbl = self.list[self.crnt_lbl_nmbr]
            self.crnt_file = self.file_list[self.crnt_lbl_nmbr]
#            self.crnt_plc = len(self.crnt_lbl.get_text())
            self.scroll()

    def make_action(self, action):
        if action == "HELP": print("Help!")
#        elif action == "BACKSPACE":
#            text = self.crnt_lbl.get_text()
#            if self.crnt_plc > 0:
#                text = text[:self.crnt_plc-1] + text[self.crnt_plc:]
#                try:
#                    self.crnt_lbl.set_text(text)
##                    self.crnt_plc = self.crnt_plc -1
#                except:
#                    pass



#    def __init__(self, *a, **kw):
#        self.__gobject_init__()
#        gtk.VBox.__init__(self, *a, **kw)

#        self.gstat = GStat()
#        # if 'NO_FORCE_HOMING' is true, MDI  commands are allowed before homing.
#        inifile = os.environ.get('INI_FILE_NAME', '/dev/null')
#        self.ini = linuxcnc.ini(inifile)
#        no_home_required = int(self.ini.find("TRAJ", "NO_FORCE_HOMING") or 0)
#        path = self.ini.find('DISPLAY', 'MDI_HISTORY_FILE') or '~/.axis_mdi_history'
#        self.filename = os.path.expanduser(path)

#        self.model = gtk.ListStore(str)

#        self.tv = gtk.TreeView()
#        self.tv.set_model(self.model)
#        self.cell = gtk.CellRendererText()

#        self.col = gtk.TreeViewColumn("Command")
#        self.col.pack_start(self.cell, True)
#        self.col.add_attribute(self.cell, 'text', 0)

#        self.tv.append_column(self.col)
#        self.tv.set_search_column(0)
#        self.tv.set_reorderable(False)
#        self.tv.set_headers_visible(True)

#        scroll = gtk.ScrolledWindow()
#        scroll.add(self.tv)
#        scroll.props.hscrollbar_policy = gtk.POLICY_AUTOMATIC
#        scroll.props.vscrollbar_policy = gtk.POLICY_AUTOMATIC

#        self.entry = gtk.Entry()
#        self.entry.set_icon_from_stock(gtk.ENTRY_ICON_SECONDARY, 'gtk-ok')

#        self.entry.connect('activate', self.submit)
#        self.entry.connect('icon-press', self.submit)
#        self.tv.connect('cursor-changed', self.select)

#     #   self.connect('my_syganal', on_my_signal)

#        self.pack_start(scroll, True)
#        self.pack_start(self.entry, False)
#        self.gstat.connect('state-off', lambda w: self.set_sensitive(False))
#        self.gstat.connect('state-estop', lambda w: self.set_sensitive(False))
#        self.gstat.connect('interp-idle', lambda w: self.set_sensitive(self.machine_on() and ( self.is_all_homed() or no_home_required ) ))
#        self.gstat.connect('interp-run', lambda w: self.set_sensitive(not self.is_auto_mode()))
#        self.gstat.connect('all-homed', lambda w: self.set_sensitive(self.machine_on()))
#        self.reload()
#        self.show_all()

#    def style(self):
#        print("OK")
#        #Set style for element1

#    def on_my_signal(self, data):
#        self.entry.set_text(data) 

#    def reload(self):
#        self.model.clear()

#        try:
#            fp = open(self.filename)
#        except:
#            return
#        lines = map(str.strip, fp.readlines())
#        fp.close()

#        lines = filter(bool, lines)
#        for l in lines:
#            self.model.append((l,))
#        path = (len(lines)-1,)
#        self.tv.scroll_to_cell(path)
#        self.tv.set_cursor(path)
#        self.entry.set_text('')

#    def submit(self, *a):
#        cmd = self.entry.get_text()
#        if not cmd:
#            return
#        ensure_mode(self.stat, self.linuxcnc, linuxcnc.MODE_MDI)

#        try:
#            fp = open(self.filename, 'a')
#            fp.write(cmd + "\n")
#            fp.close()
#        except:
#            pass

#        self.linuxcnc.mdi(cmd)
#        last = self.model.append((cmd,))
#        path = self.model.get_path(last)
#        self.tv.scroll_to_cell(path)
#        self.tv.set_cursor(path)
#        self.entry.set_text('')
#        self.entry.grab_focus()

#    def select(self, w):
#        idx = w.get_cursor()[0]
#        if idx is None:
#            return
#        self.entry.set_text(self.model[idx][0])
