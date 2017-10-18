#!/usr/bin/env python

# This additional help class for Sinumeric 840D GUI.
# This class store labels list make navigation and changes in labels
# of any widget component used it.
#
# Copyright (c) 2017 Maksym Kotelnikov
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

import gtk
import gobject

from widget import Widgets
from color import Color

class LabelList():
    def __init__(self, parameters, box_widget):
        # Unpack parameters
        label_list = parameters[0]
        current_label = parameters[1]
        permissions = parameters[2]
        # Create instanse of class. Set internal values
        self.widget = Widgets(box_widget)
#        labels = self.widget.get_list(gtk.Label)
#        for lbl in labels: 
#            print("lbl - %r"% lbl)
        self.colors = Color()
        self.list = label_list
        self.crnt_lbl = current_label
        self.crnt_plc = len(self.widget[self.crnt_lbl].get_text())
        self.set_permissions (permissions)
        self.get_index()
        self.highlite_lbl()

        # Additional help lists
        self.dirrection = ["LEFT", "RIGHT", "UP", "DOWN"]
        self.actions = ["PAGE_DOWN", "PAGE_UP", "BACKSPACE", "INPUT", "INSERT", "END", "SELECT", "CHANNEL", "ALARM_CANCEL", "NEXT_WIN", "HELP"]
#        self.show_all()

    def highlite_lbl(self, new_lbl = None):
        if new_lbl:
            self.widget[self.crnt_lbl].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.white)
            self.widget[new_lbl].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.orange)
        else:
            for lst in self.list:
                for lbl in lst:
                    if lbl: self.widget[lbl].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.white)
            self.widget[self.crnt_lbl].get_parent().modify_bg(gtk.STATE_NORMAL, self.colors.orange)

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
            self.put_sign(sign)
        elif sign in self.dirrection: self.change_label(sign)
        elif sign in self.actions: self.make_action(sign)

    def put_sign (self, sign):
        text = self.widget[self.crnt_lbl].get_text()
        text = text[:self.crnt_plc] + sign + text[self.crnt_plc:]
        try:
            self.widget[self.crnt_lbl].set_text(text)
            self.crnt_plc = self.crnt_plc + 1
        except:
            pass

    def get_index(self):
        self.maxY = len(self.list) - 1
        self.y = 0
        for lst in self.list:
            try:
                self.x = lst.index(self.crnt_lbl)
            except:
                self.x = None
            if self.x != None:
                self.maxX = len(lst) - 1
                break
            self.y = self.y + 1

    def change_label(self, dirrection):
        if dirrection == "LEFT":
            while True:
                newX = self.x - 1
                if newX < 0: 
                    newX = self.maxX
                    newY = self.y - 1
                    if newY < 0:
                        newY = self.maxY
                else: newY = self.y
                if self.list[newY][newX]:
                    self.x = newX
                    self.y = newY 
                    break
        elif dirrection == "RIGHT":
            while True:
                newX = self.x + 1
                if newX > self.maxX: 
                    newX = 0
                    newY = self.y + 1
                    if newY > self.maxY:
                        newY = 0
                else: newY = self.y
                if self.list[newY][newX]: 
                    self.x = newX
                    self.y = newY 
                    break
        elif dirrection == "UP":
            while True:
                newY = self.y - 1
                if newY < 0: 
                    newY = self.maxY
                    newX = self.x - 1
                    if newX < 0:
                        newX = self.maxX
                else: newX = self.x
                if self.list[newY][newX]: 
                    self.x = newX
                    self.y = newY 
                    break
        elif dirrection == "DOWN":
            while True:
                newY = self.y + 1
                if newY > self.maxY: 
                    newY = 0
                    newX = self.x + 1
                    if newX > self.maxX:
                        newX = 0
                else: newX = self.x
                if self.list[newY][newX]: 
                    self.x = newX
                    self.y = newY 
                    break
        new_lbl = self.list[self.y][self.x]
        if self.crnt_lbl != new_lbl:
            self.highlite_lbl(new_lbl)
            self.crnt_lbl = new_lbl
            self.crnt_plc = len(self.widget[self.crnt_lbl].get_text())

    def make_action(self, action):
        if action == "HELP": print("Help!")
        elif action == "BACKSPACE":
            text = self.widget[self.crnt_lbl].get_text()
            text = text[:self.crnt_plc-1]
            try:
                self.widget[self.crnt_lbl].set_text(text)
                self.crnt_plc = self.crnt_plc -1
            except:
                pass


