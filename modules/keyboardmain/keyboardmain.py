#!/usr/bin/env python

#   Main Keyboard emulator for 840D

#   Copyright (c) 2017 Maksym Kotelnikov
#        <nemovit.mk@gmail.com>
#
#   This file is part of 840D project.
#
#   This is free software: you can redistribute it and/or modify
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

import gladevcp.makepins
#from gladevcp.gladebuilder import GladeBuilder
from linuxcnc_actions import *
from widget import Widgets
from color import Color

py_file_dir  = os.path.abspath(os.path.dirname(__file__))
IMAGEDIR = os.path.join(py_file_dir , "ui")

class Keyboardmain(gobject.GObject):

    def __init__(self):
    
        self.__gobject_init__()

        # Glade setup
        gladefile = os.path.join(IMAGEDIR, 'keyboardmain.glade')

        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)
        self.widgets = Widgets(self.builder)

        self.widgets.window3.connect('destroy', self.on_window_destroy)

        self.stp_ptn_release= os.path.join(IMAGEDIR, 'un_stop.png')
        self.stp_ptn_pressed= os.path.join(IMAGEDIR, 'stop.png')
        self.estopped = True
        
        self.colors = Color()
        self.set_style()
        self.connect_signals()
        self.update()
        self.show()


# ==========================================================
# Set style
# ==========================================================
    def set_style(self):    
        try:    
            self.widgets.window3.set_title("Main Keyboard")
            layouts = self.widgets.get_list(gtk.Layout)
            for lyt in layouts: 
                lyt.modify_bg(gtk.STATE_NORMAL, self.colors.dgray)

            leds = self.widgets.get_list(gladevcp.led.HAL_LED)
            for led in leds: 
                led.modify_bg(gtk.STATE_NORMAL, self.colors.dgray)
        except:
            print ("Problem with style settings of KeyboardMain")


# ==========================================================
# Update
# ==========================================================
    def update (self, data = None):
        if chek_mode(linuxcnc.MODE_MDI):
            self.widgets.ld11.set_active(False)
            self.widgets.ld31.set_active(True)
            self.widgets.ld41.set_active(False)
        elif chek_mode(linuxcnc.MODE_AUTO):
            self.widgets.ld11.set_active(False)
            self.widgets.ld31.set_active(False)
            self.widgets.ld41.set_active(True)
        elif chek_mode(linuxcnc.MODE_MANUAL):
            self.widgets.ld11.set_active(True)
            self.widgets.ld31.set_active(False)
            self.widgets.ld41.set_active(False)
        else:
            self.widgets.ld11.set_active(False)
            self.widgets.ld31.set_active(False)
            self.widgets.ld41.set_active(False)

# ==========================================================
# Connect signals
# ==========================================================

    def connect_signals(self):
#        try:        
            self.widgets.mkb11.connect('clicked', self.on_mkb11_clicked)
            self.widgets.mkb12.connect('clicked', self.on_mkb12_clicked)
            self.widgets.mkb13.connect('clicked', self.on_mkb13_clicked)
            self.widgets.mkb18.connect('clicked', self.on_mkb18_clicked)
            self.widgets.mkb19.connect('clicked', self.on_mkb19_clicked)
        
            self.widgets.mkb21.connect('clicked', self.on_mkb21_clicked)
            self.widgets.mkb22.connect('clicked', self.on_mkb22_clicked)
            self.widgets.mkb23.connect('clicked', self.on_mkb23_clicked)
            self.widgets.mkb27.connect('clicked', self.on_mkb27_clicked)
            self.widgets.mkb28.connect('clicked', self.on_mkb28_clicked)
            self.widgets.mkb29.connect('clicked', self.on_mkb29_clicked)
    
            self.widgets.mkb31.connect('clicked', self.on_mkb31_clicked)
            self.widgets.mkb32.connect('clicked', self.on_mkb32_clicked)
            self.widgets.mkb33.connect('clicked', self.on_mkb33_clicked)
            self.widgets.mkb37.connect('clicked', self.on_mkb37_clicked)
            self.widgets.mkb38.connect('clicked', self.on_mkb38_clicked)
    
    
            self.widgets.mkb41.connect('clicked', self.on_mkb41_clicked)
            self.widgets.mkb42.connect('clicked', self.on_mkb42_clicked)
            self.widgets.mkb43.connect('clicked', self.on_mkb43_clicked)
            self.widgets.mkb49.connect('clicked', self.on_mkb49_clicked)
    
            self.widgets.mkb50.connect('clicked', self.on_mkb50_clicked)
            self.widgets.mkb51.connect('clicked', self.on_mkb51_clicked)
            self.widgets.mkb52.connect('clicked', self.on_mkb52_clicked)
            self.widgets.mkb53.connect('clicked', self.on_mkb53_clicked)
            self.widgets.mkb57.connect('clicked', self.on_mkb57_clicked)
            self.widgets.mkb58.connect('clicked', self.on_mkb58_clicked)
            self.widgets.mkb59.connect('clicked', self.on_mkb59_clicked)
            self.widgets.mkb60.connect('clicked', self.on_mkb60_clicked)
            self.widgets.mkb61.connect('clicked', self.on_mkb61_clicked)
            self.widgets.mkb62.connect('clicked', self.on_mkb62_clicked)
            self.widgets.mkb63.connect('clicked', self.on_mkb63_clicked)
            self.widgets.stp_btn_box.connect('button-press-event', self.on_stp_btn_clicked)
    
#        except:
#            print ("Signal connection of Keyboard Main: could not connect ")


# ==========================================================
# On key pressed
# ==========================================================

    def on_stp_btn_clicked(self, data = None, data2 = None):
        if estop_clicked:
            if self.estopped:
                self.estopped = False
                self.widgets.stp_btn.set_from_file(self.stp_ptn_release)
                print("un STOP")
            else: 
                self.estopped = True
                self.widgets.stp_btn.set_from_file(self.stp_ptn_pressed)
                print("STOP")

    def on_mkb11_clicked(self, widget, data=None):
        if set_mode(linuxcnc.MODE_MANUAL): print ("JOG %r"% manual_ok())
        self.update()
    def on_mkb12_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb13_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb18_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb19_clicked(self, widget, data=None):
        print ("OK")

    def on_mkb21_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb22_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb23_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb27_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb28_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb29_clicked(self, widget, data=None):
        print ("OK")

    def on_mkb31_clicked(self, widget, data=None):
        if set_mode(linuxcnc.MODE_MDI): print ("MDI")
        self.update()
    def on_mkb32_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb33_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb37_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb38_clicked(self, widget, data=None):
        print ("OK")

    def on_mkb41_clicked(self, widget, data=None):
        if set_mode(linuxcnc.MODE_AUTO): print ("AUTO")
        self.update()
    def on_mkb42_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb43_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb49_clicked(self, widget, data=None):
        print ("OK")

    def on_mkb50_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb51_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb52_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb53_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb57_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb58_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb59_clicked(self, widget, data=None):
        print ("OK")
    def on_mkb60_clicked(self, widget, data=None):
        if chek_mode(linuxcnc.MODE_MANUAL):
            spindle(linuxcnc.SPINDLE_OFF)
            self.widgets.ld60.set_active(True)
            self.widgets.ld61.set_active(False)
            print ("stop_spindle")
#            self.update()
    def on_mkb61_clicked(self, widget, data=None):
        if chek_mode(linuxcnc.MODE_MANUAL):
            spindle(linuxcnc.SPINDLE_FORWARD)
            self.widgets.ld60.set_active(False)
            self.widgets.ld61.set_active(True)
            print ("start_spindle")
#            self.update()
    def on_mkb62_clicked(self, widget, data=None):
        if chek_mode(linuxcnc.MODE_MANUAL):
            jog(linuxcnc.JOG_STOP, 2)
            self.widgets.ld62.set_active(True)
            self.widgets.ld63.set_active(False)
            print ("OK")
    def on_mkb63_clicked(self, widget, data=None):
        if chek_mode(linuxcnc.MODE_MANUAL):
            jog(linuxcnc.JOG_CONTINUOUS, 2, 100)
            self.widgets.ld62.set_active(False)
            self.widgets.ld63.set_active(True)
            print ("OK")

# ==========================================================
# Emmit signals
# ==========================================================
    def _emit_signal(self, data):
        if data:
            self.data = data
        else: self.data = ""
        self.emit('key_press_keyboard_main')
# ==========================================================
# Show the keyboard
# ==========================================================

    def show(self):
        self.widgets.window3.show()

    def on_window_destroy(self, widget):
        self.widgets.window3.destroy()

# ==========================================================
# Creating signal
# ==========================================================
#gobject.type_register(Keyboard)
gobject.signal_new("key_press_keyboard_main", Keyboardmain, gobject.SIGNAL_RUN_FIRST,
    gobject.TYPE_NONE, ())

