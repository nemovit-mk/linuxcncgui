#!/usr/bin/python

import sys,os,subprocess
#def _print_help():
#            print """ Gscreen a customizable operator screen for linuxcnc based on pyGTK / GLADE.\n
#        It is usually loaded from linuxcnc's INI file under the [DISPLAY] HEADER
#        eg. DISPLAY = gscreen\n
#        Options:
#        --INI.................Designates the configuration file path for linuxcnc
#        -c....................Loads an optional skin for Gscreen
#        -d....................Debug mode
#        -v....................Verbose debug mode
#        -F....................Prints documentation of internal functions to standard output
#        """
#            sys.exit(0)

#for num,temp in enumerate(sys.argv):
#        if temp == '-h' or temp == '--help' or len(sys.argv) == 1:
#            _print_help()

import pygtk
pygtk.require("2.0")
import gtk
import gtk.glade
import gobject
import hal
import errno
import gladevcp.makepins
from gladevcp.gladebuilder import GladeBuilder
import pango
import traceback
import atexit
import vte
import time
from time import strftime,localtime
import hal_glib
import gobject
#import linuxcnc

#import widget
#import data
#import color

from widget import Widgets
from color import Color
from data import Data
from screenlabels import ScrnLbl

from modules.keyboard.keyboard import Keyboard
from modules.keyboardmain.keyboardmain import Keyboardmain


#--------------------------------------------------------
## limit number of times err msgs are displayed
#excepthook_msg_ct = 0
#excepthook_msg_ct_max = 10

#update_spindle_bar_error_ct = 0
#update_spindle_bar_error_ct_max = 3
##--------------------------------------------------------

# BASE is the absolute path to linuxcnc base
# libdir is the path to Gscreen python files
# datadir is where the standarad GLADE files are
# imagedir is for icons
# themedir is path to system's GTK2 theme folder
#BASE = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), ".."))
#libdir = os.path.join(BASE, "lib", "python")
#datadir = os.path.join(BASE, "share", "linuxcnc")
#imagedir = os.path.join(BASE, "share","gscreen","images")
#SKINPATH = os.path.join(BASE, "share","gscreen","skins")
#sys.path.insert(0, libdir)
#themedir = "/usr/share/themes"
#userthemedir = os.path.join(os.path.expanduser("~"), ".themes")

#xmlname = os.path.join(datadir,"gscreen.glade")
#xmlname2 = os.path.join(datadir,"gscreen2.glade")
#ALERT_ICON = os.path.join(imagedir,"applet-critical.png")
#INFO_ICON = os.path.join(imagedir,"std_info.gif")

# Setup paths to files
BASE = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), ".."))
#INIFILE = sys.argv[2]                               # Path to .ini file
#CONFIGDIR = os.path.dirname(INIFILE)                # Path to config dir

# We use __file__ to get the file dir so we can run from any location
MYDIR = os.path.dirname(os.path.realpath(__file__))
IMAGEDIR = MYDIR
#os.path.join(MYDIR, 'images')
#MODULEDIR = os.path.join(MYDIR, 'modules')
MAINDIR = os.path.dirname(MYDIR)

# Set system path so we can find our own modules
sys.path.insert(1, MYDIR)

# internationalization and localization
import locale, gettext


# path to TCL for external programs eg. halshow
try:
    TCLPATH = os.environ['LINUXCNC_TCL_DIR']
except:
    pass
# path to the configuration the user requested
# used to see if the is local GLADE files to use
try:
    CONFIGPATH = os.environ['CONFIG_DIR']
except:
    pass
import linuxcnc


from linuxcnc_actions import *



class myGUI(gobject.GObject):

    def __init__(self):

        self.__gobject_init__()

        #add data 
        self.data = Data()
        self.colors = Color()
        self.scrnlbl = ScrnLbl()

        # Glade setup
        gladefile = os.path.join(IMAGEDIR, 'images/840D.glade')
        gladefile2 = os.path.join(IMAGEDIR, 'modules/keyboard/ui/keyboard.glade')
        gladefile3 = os.path.join(IMAGEDIR, 'modules/keyboardmain/ui/keyboardmain.glade')
        self.builder = gtk.Builder()
        self.builder.add_from_file(gladefile)
#        self.builder.add_from_file(gladefile2)    
#        self.builder.add_from_file(gladefile3)
    
#        Need to correct connection

#           self.builder.connect_signals(self)

        self.widgets = Widgets(self.builder)
    
#        self.window = self.builder.get_object("window1")

#        self.widgets.window1.connect('window_delete_evet', self.on_window_delete_event)
        self.widgets.window1.set_title("Sinumeric 840D")
    
#        self.widgets.window2.connect('destroy', self.on_window_delete_event)
#        self.widgets.window3.connect('destroy', self.on_window_delete_event)



        self.set_style()
#        self.set_labels(self.data.screenName.index("Main"))
        self.error_channel = linuxcnc.error_channel()

#        gtk.EventBox.modify_bg(gtk.STATE_NORMAL, lgray)

        self.connect_signals()

        self.widgets.window2 = Keyboard()
#        self.widgets.window2.connect('destroy', self.on_window_delete_event)
        self.widgets.window2.connect('key_press_keyboard', self.on_keyboard_signal)
#        self.widgets.window2.set_destroy_with_parent(True)
        
        self.action = Actions()
        self.action.connect("time_to_update", self.update)

        self.widgets.window3 = Keyboardmain(self.action)
#        self.widgets.window2.connect('destroy', self.on_window_delete_event)
        self.widgets.window3.connect('key_press_keyboard_main', self.on_main_kayboard_signal)
#        self.widgets.window3.set_destroy_with_parent(True)
        
        self.cnc_stat = linuxcnc.stat()

        self.data.CURRENTSCREEN = "main_screen"
        self.set_screen()
#        self.highliteBTN()

#        self.widgets = Widgets(self.xml)

        # Finally, show the window 
#            self.window.show()

        self.widgets.window1.connect('destroy', self.on_window_delete_event)
        self.widgets.window1.show()

# ==========================================================
# Callbacks
# ==========================================================

    def on_main_kayboard_signal(self, keyboard):
        parent = None
        md = gtk.MessageDialog(parent, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
            gtk.BUTTONS_CLOSE, str(self.action.number))
        md.run()
        print("Signal from main keyboard")

    def on_keyboard_signal(self, keyboard):
#        print("some %r"% some)
        print("data %r"% keyboard.data)
        self.widgets[self.data.CURRENTSCREEN].on_key_pressed(keyboard.data)
#        self.widgets.vcp_mdihistory840d.on_my_signal(keyboard.data)

    def show_msg(self, msg):
        parent = None
        md = gtk.MessageDialog(parent, 
            gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
            gtk.BUTTONS_CLOSE, str(msg))
        md.run()

#   Update callback from linuxcnc_actions
    def update(self, action):
        # Update keyboard info
        self.widgets.window3.update()
        # Update current screen info
        if self.data.CURRENTSCREEN != None:
            self.widgets[self.data.CURRENTSCREEN].update()

        #Operating area
        self.widgets.lbl1a.set_label(self.action.operating_area)
        #Channel
        self.widgets.lbl1b.set_label(self.action.channel)
        #Mode
        self.widgets.lbl1c.set_label(self.action.mode)
        #File path (program name)
        self.widgets.lbl1d.set_label(self.action.program_name)
        #Channel status
        self.widgets.lbl2a.set_label(self.action.channel_status)
        #Channel message
        self.widgets.lbl2b.set_label(self.action.channel_message[len(self.action.channel_message)-1])
        #Program status
        self.widgets.lbl3a.set_label(self.action.program_status)
        #Flags
        self.widgets.lbl3b.set_label(self.action.flags)
        #Alarm message line
        self.widgets.lbl4.set_label(self.action.alarm_message[len(self.action.alarm_message)-1])

#    def on_change_screen_signal(self, screen):
#        self.data.CURRENTSCREEN = screen.new_screen
#        self.set_screen()
#        self.widgets[self.data.CURRENTSCREEN]('change-screen', self.on_change_screen_signal)
#        self.widgets[self.data.CURRENTSCREEN]('change-labels', self.set_labels)
#        self.highliteBTN()
#        print("change-screen")

# ==========================================================
# Functions
# ==========================================================

    def set_labels(self, data = None):
        for n in range (0, 8):
            self.widgets["lblX"+str(n+1)].set_label(self.widgets[self.data.CURRENTSCREEN].labelX[n][0])
            self.widgets["lblY"+str(n+1)].set_label(self.widgets[self.data.CURRENTSCREEN].labelY[n][0])
            oldLghtLBL = self.data.LGHTLABEL
            self.data.LGHTLABEL = self.widgets[self.data.CURRENTSCREEN].lght_btn
            self.highliteBTN(oldLghtLBL)
#            if self.widgets[self.data.CURRENTSCREEN].lght_btn !=
#            self.data.LGHTLABEL = self.widgets[self.data.CURRENTSCREEN].lght_btn
    
    def set_style(self):    
#        try:                
#            self.widgets.layout3.modify_bg(gtk.STATE_NORMAL, dgray)
#            self.widgets.layout2.modify_bg(gtk.STATE_NORMAL, dgray)
#            self.widgets.layout4.modify_bg(gtk.STATE_NORMAL, dgray)
#            self.widgets.layout21.modify_bg(gtk.STATE_NORMAL, dgray)
#            self.widgets.layout22.modify_bg(gtk.STATE_NORMAL, dgray)
#            self.widgets.layout31.modify_bg(gtk.STATE_NORMAL, dgray)
#            self.widgets.layout32.modify_bg(gtk.STATE_NORMAL, dgray)
#            self.widgets.layout33.modify_bg(gtk.STATE_NORMAL, dgray)
#            self.widgets.layout34.modify_bg(gtk.STATE_NORMAL, dgray)
#            self.widgets.layout35.modify_bg(gtk.STATE_NORMAL, dgray)
        
#            self.widgets.lineX.modify_bg(gtk.STATE_NORMAL, dgray)
#            self.widgets.ld11.modify_bg(gtk.STATE_NORMAL, dgray)
#            self.widgets.eventbox2.modify_bg(gtk.STATE_NORMAL, lgray)

            boxs = self.widgets.get_list(gtk.EventBox)
            for box in boxs: 
                box.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)

            for i in self.widgets["window1"].get_children():
                if isinstance(i, gtk.Layout):
                    i.modify_bg(gtk.STATE_NORMAL, self.colors.dgray)
                if isinstance(i, gtk.Notebook):
                    i.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
                if isinstance(i, gtk.Label):
                    i.modify_font(pango.FontDescription('dejavusans condensed 10'))
                if isinstance(i, gtk.EventBox):
                    i.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)

            boxs = self.widgets.get_list(gtk.EventBox, self.widgets["lineX"])
            for box in boxs: 
                box.modify_bg(gtk.STATE_NORMAL, self.colors.gray)

            boxs = self.widgets.get_list(gtk.EventBox, self.widgets["lineY"])
            for box in boxs: 
                box.modify_bg(gtk.STATE_NORMAL, self.colors.gray)

            self.widgets["eventboxBig"].modify_bg(gtk.STATE_NORMAL, self.colors.lgray)

            layouts = self.widgets.get_list(gtk.Layout)
            for lyt in layouts: 
                lyt.modify_bg(gtk.STATE_NORMAL, self.colors.dgray)

            labels = self.widgets.get_list(gtk.Label)
            for lbl in labels: 
                lbl.modify_font(pango.FontDescription('dejavusans condensed 10'))        
                        
#            leds = self.widgets.get_list(gladevcp.led.HAL_LED)
#            for led in leds: 
#                led.modify_bg(gtk.STATE_NORMAL, self.colors.dgray)

#            ntbks = self.widgets.get_list(gtk.Notebook)
#            for ntbk in ntbks: 
#                ntbk.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
            
#            vprts = self.widgets.get_list(gtk.Viewport)
#            for vprt in vprts: 
#                vprt.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)

#            scrls = self.widgets.get_list(gtk.ScrolledWindow)
#            for scrl in scrls: 
#                scrl.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)
    
    
#            for header in self.scrnlbl.headers:
#                self.widgets[header].modify_bg(gtk.STATE_NORMAL, self.colors.blue)

#                print ("items %r"% led.__class__)
#                self.widgets[lbl].modify_bg(gtk.STATE_NORMAL, lgray)
#        except:
#                    print ("Problem with style settings ")

    def highliteBTN(self, oldButton = None):
#        button = self.widgets[self.data.CURRENTSCREEN].lght_btn
        if self.data.LGHTLABEL:
            box = self.widgets[self.data.LGHTLABEL].get_parent()
            box.modify_bg(gtk.STATE_NORMAL, self.colors.blue)
#            print("lbl %r blue"% self.data.LGHTLABEL)
        if oldButton and oldButton != self.data.LGHTLABEL:
            box = self.widgets[oldButton].get_parent()
            box.modify_bg(gtk.STATE_NORMAL, self.colors.lgray)
#            print("lbl %r gray"% oldButton)


#    def on_change_screen_signal(self, screen):
#        self.data.CURRENTSCREEN = screen.new_screen
##        self.set_screen()
#        self.widgets[self.data.CURRENTSCREEN]('change-screen', self.on_change_screen_signal)
#        self.widgets[self.data.CURRENTSCREEN]('change-labels', self.set_labels)
#        self.highliteBTN()
#        print("change-screen")


    def set_screen(self, screen = None):
        if screen == None: 
            self.data.CURRENTSCREEN = "main_screen"
#            renew = False
        else: 
#            if self.data.CURRENTSCREEN != screen.crnt_screen:
#                renew = True
#            else: renew = False
            self.data.CURRENTSCREEN = screen.crnt_screen
#        if renew:
#        self.widgets[self.data.CURRENTSCREEN].actions_on_enter()
        self.widgets[self.data.CURRENTSCREEN].action = self.action
        if self.data.CURRENTSCREEN=="screen_gfile" and self.widgets["screen_open_file"].path_to_file != None:
            self.widgets[self.data.CURRENTSCREEN].gfile.filename = self.widgets["screen_open_file"].path_to_file
            self.widgets[self.data.CURRENTSCREEN].gfile.read_file()
        self.set_labels()
        page_num = self.widgets["mainscreen"].page_num(self.widgets[self.data.CURRENTSCREEN])
        self.widgets["mainscreen"].set_current_page(page_num)
        self.widgets[self.data.CURRENTSCREEN].connect('change-screen', self.set_screen)
        self.widgets[self.data.CURRENTSCREEN].connect('change-labels', self.set_labels)
#        self.set_labels()
#        self.highliteBTN()

#    def check_text(self):

#        print("OK")

####################################################
#   Jog keys
####################################################
    def on_keycall_ABORT(self,state,SHIFT,CNTRL,ALT):
        """Calls a gladevcp hal action to abort a linuxcnc run.
           action widget is assumed to be named hal_action_stop.
           The action will emit signal 'activate'
           This is part of the default key call routine
        """
        if state: # only activate when pushed not when released
            self.widgets.hal_action_stop.emit("activate")
            return True
    def on_keycall_ESTOP(self,state,SHIFT,CNTRL,ALT):
        """Calls a gladevcp toggle button to estop linuxcnc.
           button widget is assumed to be named button_estop
           The button will emit signal 'clicked'
           This is part of the default key call routine
        """
        if state:
            self.widgets.button_estop.emit('clicked')
            return True
    def on_keycall_POWER(self,state,SHIFT,CNTRL,ALT):
        """Calls a gladevcp toggle button to power linuxcnc.
           button widget is assumed to be named button_estop
           The button will emit signal 'clicked'
           This is part of the default key call routine
        """
        if state:
            self.widgets.button_machine_on.emit('clicked')
            return True
    def on_keycall_XPOS(self,state,SHIFT,CNTRL,ALT):
        """This calls check_mode() for manual mode
           if in manual mode, jogs X axis positively
           by calling do_key_jog()
           It will ether start or stop the jog based on 'state'
        """
        if self.data._MAN in self.check_mode(): # manual mode required
            self.do_key_jog(_X,1,state)
            return True
    def on_keycall_XNEG(self,state,SHIFT,CNTRL,ALT):
        """This calls check_mode() for manual mode
           if in manual mode, jogs X axis negatively
           by calling do_key_jog()
           It will ether start or stop the jog based on 'state'
        """
        if self.data._MAN in self.check_mode(): # manual mode required
            self.do_key_jog(_X,0,state)
            return True


    def on_keycall_INCREMENTS(self,state,SHIFT,CNTRL,ALT):
        """This calls check_mode() for manual mode
           if in manual mode, it will increase or decrease jog increments
           by calling set_jog_increments(index_dir = )
           It will ether increase or decrease the increments based on 'SHIFT'
        """
        if state and self.data._MAN in self.check_mode(): # manual mode required
            if SHIFT:
                self.set_jog_increments(index_dir = -1)
            else:
                self.set_jog_increments(index_dir = 1)
        return True

####################################################
#   Button cycle start
####################################################


    def on_cycle_start_changed(self,hal_object):
        """This is Gscreen's cycle start HAL pin callback function.
            If Gscreen is in AUTO mode it will cycle start.
            If Gscreen is in MDI mode it will submit the MDI entry.
            GScreen mode is from data.mode_oder[0]
            Requires a run toogle action widget called hal_toogleaction_run
            Requires a MDI widget called hal_mdihistory
            adds button press entries to the alarm page
        """
        print "cycle start change"
        h = self.halcomp
        if not h["cycle-start"]: return
        if self.data.mode_order[0] == self.data._AUTO:
            self.add_alarm_entry(_("Cycle start pressed in AUTO mode"))
            self.widgets.hal_toggleaction_run.emit('activate')
        elif self.data.mode_order[0] == self.data._MDI:
            self.add_alarm_entry(_("Cycle start pressed in MDI mode"))
        self.widgets.hal_mdihistory.submit()


####################################################
#   Abort and feed
####################################################

    def on_abort_changed(self,hal_object):
        """This is Gscreen's abort HAL pin callback function.
            Requires a action stop widget called hal_action_stop
        """
        print "abort change"
        h = self.halcomp
        if not h["abort"]: return
        self.widgets.hal_action_stop.emit("activate")

    def on_feed_hold_changed(self,hal_object):
        """This is Gscreen's feedhold HAL pin callback function.
            Requires a toogle action pause widget called hal_action_stop
        """
        print "feed-hold change"
        h = self.halcomp
        self.widgets.hal_toggleaction_pause.set_active(h["feed-hold"])


####################################################
#   Tool
####################################################


    # Here we create a manual tool change dialog
    # This can be overridden in a handler file
    def on_tool_change(self,widget):
        """This is a callback function to launch a default manual tool change dialog.
            This also manupulates the tool change pins:
            change-tool
            tool-number
            tool-changed
        """
        h = self.halcomp
        c = h['change-tool']
        n = h['tool-number']
        cd = h['tool-changed']
        print "tool change",c,cd,n
        if c:
            message =  _("Please change to tool # %s, then click OK."% n)
            self.data.tool_message = self.notify(_("INFO:"),message,None)
            self.warning_dialog(message, True,pinname="TOOLCHANGE")
        else:
            h['tool-changed'] = False


    # dialog for manually calling a tool
    def on_index_tool(self,*args):
        """This is a callback to launch a manual toolchange dialog.
        """
        if self.data.index_tool_dialog: return
        self.data.index_tool_dialog = gtk.Dialog(_("Manual Tool Index Entry"),
                   self.widgets.window1,
                   gtk.DIALOG_DESTROY_WITH_PARENT,
                   (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                    gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        label = gtk.Label(_("Manual Tool Index Entry"))
        label.modify_font(pango.FontDescription("sans 20"))
        self.data.index_tool_dialog.vbox.pack_start(label)
        calc = gladevcp.Calculator()
        self.data.index_tool_dialog.vbox.add(calc)
        calc.set_value("")
        calc.set_property("font","sans 20")
        calc.set_editable(True)
        calc.entry.connect("activate", lambda w : self.data.index_tool_dialog.emit('response',gtk.RESPONSE_ACCEPT))
        self.data.index_tool_dialog.parse_geometry("400x400")
        self.data.index_tool_dialog.show_all()
        calc.num_pad_only(True)
        calc.integer_entry_only(True)
        self.data.index_tool_dialog.connect("response", self.on_index_tool_return,calc)

    def on_index_tool_return(self,widget,result,calc):
        """This is a callbck function from the maunal toolchange dialog.
        """
        if result == gtk.RESPONSE_ACCEPT:
            raw = calc.get_value()
            try:
                tool = abs(int((raw)))
                self.mdi_control.index_tool(tool)
            except:
                return
        widget.destroy()
        self.data.index_tool_dialog = None

####################################################
#   Update info
####################################################
    def update_tool_label(self):
        # corodinate system:
        systemlabel = (_("Machine"),"G54","G55","G56","G57","G58","G59","G59.1","G59.2","G59.3")
        tool = str(self.data.tool_in_spindle)
        if tool == None: tool = "None"
        self.widgets.system.set_text(("Tool %s     %s"%(tool,systemlabel[self.data.system])))


    def update_coolant_leds(self):
        # coolant
        self.widgets.led_mist.set_active(self.data.mist)
        self.widgets.led_flood.set_active(self.data.flood)

    def update_estop_led(self):
        # estop
        self.widgets.led_estop.set_active(self.data.estopped)

    def update_machine_on_led(self):
        self.widgets.led_on.set_active(self.data.machine_on)

    def update_limit_override(self):
        # ignore limts led
        self.widgets.led_ignore_limits.set_active(self.data.or_limits)

    def update_override_label(self):
        # overrides
        self.widgets.fo.set_text("FO: %d%%"%(round(self.data.feed_override,2)*100))
        self.widgets.so.set_text("SO: %d%%"%(round(self.data.spindle_override,2)*100))
        self.widgets.mv.set_text("VO: %d%%"%(round((self.data.velocity_override),2) *100))


    # we need to check if the current units is in the basic machine units - convert if nesassary.
    # then set the display according to the current display units.
    def update_jog_rate_label(self):
        rate = round(self.status.convert_units(self.data.jog_rate),2)
        if self.data.dro_units == self.data._MM:
            text = "%4.2f mm/min"% (rate)
        else:
            text = "%3.2f IPM"% (rate)
        self.widgets.jog_rate.set_text(text)
        try:
            text = "%4.2f DPM"% (self.data.angular_jog_rate)
            self.widgets.angular_jog_rate.set_text(text)
        except:
            pass

    def update_mode_label(self):
        # Mode / view
        modenames = self.data.mode_labels
        time = strftime("%a, %d %b %Y  %I:%M:%S %P    ", localtime())
        self.widgets.mode_label.set_label( "%s   View -%s               %s"% (modenames[self.data.mode_order[0]],self.data.plot_view[0],time) )

####################################################
#   Spindle
####################################################

    def on_spindle_speed_adjust(self,widget):
        """ this is a callback function for spindle increase /decrease controls.
            Checks if MDI is busy or in AUTO mode - notifies as info.
            requires calling widget to be call spindle_increase or spindle_decrease.
            calls spindle_adjustment()
        """
        if self.mdi_control.mdi_is_reading():
            self.notify(_("INFO:"),_("Can't start spindle manually while MDI busy"),INFO_ICON)
            return
        elif self.data.mode_order[0] == self.data._AUTO:
            self.notify(_("INFO:"),_("can't start spindle manually in Auto mode"),INFO_ICON)
            return
        if widget == self.widgets.spindle_increase:
            self.spindle_adjustment(True,True)
        elif widget == self.widgets.spindle_decrease:
            self.spindle_adjustment(False,True)

    # start the spindle according to preset rpm and direction buttons, unless interp is busy
    def on_spindle_control_clicked(self,*args):
        """this is a callback function that will start the spindle manually.
            Checks if MDI is busy or in AUTO mode - notifies as info.
            direction is based on state of widget s_display_fwd toggle button.
            speed is based on data.spindle_preset.
            calls adjust_spindle_rpm()
        """
        if self.mdi_control.mdi_is_reading():
            self.notify(_("INFO:"),_("Can't start spindle manually while MDI busy"),INFO_ICON)
            return
        elif self.data.mode_order[0] == self.data._AUTO:
            self.notify(_("INFO:"),_("can't start spindle manually in Auto mode"),INFO_ICON)
            return
        if not self.data.spindle_speed == 0:
            self.emc.spindle_off(1)
            return
        if not self.widgets.s_display_fwd.get_active() and not self.widgets.s_display_rev.get_active():
            self.notify(_("INFO:"),_("No direction selected for spindle"),INFO_ICON)
            return
        if self.widgets.s_display_fwd.get_active():
            self.adjust_spindle_rpm(self.data.spindle_preset,1)
        else:
            self.adjust_spindle_rpm(self.data.spindle_preset,-1)

    # dialog for setting the spindle preset speed
    def on_preset_spindle(self,*args):
        """This is a callback function to launch a spindle preset speed dialog.
        """
        if self.data.preset_spindle_dialog: return
        label = gtk.Label(_("Spindle Speed Preset Entry"))
        label.modify_font(pango.FontDescription("sans 20"))
        self.data.preset_spindle_dialog = gtk.Dialog(_("Spindle Speed Preset Entry"),
                   self.widgets.window1,
                   gtk.DIALOG_DESTROY_WITH_PARENT,
                   (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
                    gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        calc = gladevcp.Calculator()
        self.data.preset_spindle_dialog.vbox.pack_start(label)
        self.data.preset_spindle_dialog.vbox.add(calc)
        calc.set_value("")
        calc.set_property("font","sans 20")
        calc.set_editable(True)
        calc.entry.connect("activate", lambda w : self.data.preset_spindle_dialog.emit('response',gtk.RESPONSE_ACCEPT))
        self.data.preset_spindle_dialog.parse_geometry("400x400")
        self.data.preset_spindle_dialog.set_decorated(False)
        self.data.preset_spindle_dialog.show_all()
        self.data.preset_spindle_dialog.connect("response", self.on_preset_spindle_return,calc)


    # from prefererence page
    def set_spindle_start_rpm(self,widget):
        """This is a callbck function to set the preset spindle speed.
            requires the calling widget to return a float value.
            calls preset_spindle_speed() function
        """
        data = widget.get_value()
        self.data.spindle_start_rpm = data
        self.prefs.putpref('spindle_start_rpm', data,float)
        self.preset_spindle_speed(data)


    # manual spindle control
    # TODO fix direct reference just use 'widget'
    def on_s_display_fwd_toggled(self,widget):
        """This is a callback to manually set the spindle fwd.
            If the spindle is running backward it will stop.
            It also toggles the reverse button
        """
        if widget.get_active():
            if self.widgets.s_display_fwd.get_active():
                self.emc.spindle_off(1)
                self.block("s_display_rev")
                self.widgets.s_display_rev.set_active(False)
                self.unblock("s_display_rev")
        else:
            self.block("s_display_fwd")
            widget.set_active(True)
            self.unblock("s_display_fwd")
 
    # manual spindle control
    # TODO fix direct reference just use 'widget'
    def on_s_display_rev_toggled(self,widget):
        """This is a callback to manually set the spindle reverse.
            If the spindle is running forward it will stop.
            it also toggles the fwd button
        """
        if widget.get_active():
            if self.widgets.s_display_fwd.get_active():
                self.emc.spindle_off(1)
                self.block("s_display_fwd")
                self.widgets.s_display_fwd.set_active(False)
                self.unblock("s_display_fwd")
        else:
            self.block("s_display_rev")
            widget.set_active(True)
            self.unblock("s_display_rev")


####################################################
#   Change mode
####################################################
    def on_mode_clicked(self,widget,event):
        """This is a callback function to change modes in Gscreen.
            Requires a button called 'button_mode' with a label
            calls mode_changed()
        """
        # only change machine modes on click
        if event.type == gtk.gdk.BUTTON_PRESS:
            a,b,c = self.data.mode_order
            self.data.mode_order = b,c,a
            label = self.data.mode_labels
            self.widgets.button_mode.set_label(label[self.data.mode_order[0]])
            self.mode_changed(self.data.mode_order[0])


    def on_button_jog_mode_clicked(self,widget):
        """This is a callback function to set jog mode
            It calls jog_mode()
        """
        self.jog_mode()


    # adjust sensitivity and labels of buttons
    def jog_mode(self):
        print "jog mode:",self.widgets.button_jog_mode.get_active()
        # if muliple axis selected - unselect all of them
        if len(self.data.active_axis_buttons) > 1 and self.widgets.button_jog_mode.get_active():
            for i in self.data.axis_list:
                self.widgets["axis_%s"%i].set_active(False)
        if self.widgets.button_jog_mode.get_active():
            self.widgets.button_move_to.set_label("Goto Position")
            self.emc.set_manual_mode()
        else:
            self.widgets.button_move_to.set_label("")
        self.update_hal_jog_pins()
        self.update_hal_override_pins()




####################################################
#   Home, unhome
####################################################
    # Horizontal buttons
    def on_button_home_all_clicked(self,widget):
        """This is a callback function to home all axis
            It calls home_all()
        """
        self.home_all()
    def on_button_unhome_all_clicked(self,widget):
        """This is a callback function to unhome all axis
            It calls unhome_all()
        """
        self.unhome_all()
    def on_button_home_axis_clicked(self,widget):
        """This is a callback function to home selected axis
            It calls home_selected()
        """
        self.home_selected()
    def on_button_unhome_axis_clicked(self,widget):
        """This is a callback function to unhome selected axis
            It calls unhome_selected()
        """
        self.unhome_selected()


    def unhome_all(self):
        self.emc.unhome_all(1)

    def home_all(self):
        self.emc.home_all(1)

    # do some checks first the home the selected axis
    def home_selected(self):
        print "home selected"
        if len(self.data.active_axis_buttons) > 1:
            self.notify(_("INFO:"),_("Can't home multiple axis - select HOME ALL instead"),INFO_ICON)
            print self.data.active_axis_buttons
        elif self.data.active_axis_buttons[0][0] == None:
            self.notify(_("INFO:"),_("No axis selected to home"),INFO_ICON)
        else:
            print "home axis %s" % self.data.active_axis_buttons[0][0]
            self.emc.home_selected(self.data.active_axis_buttons[0][1])

    def unhome_selected(self):
        if len(self.data.active_axis_buttons) > 1:
            self.notify(_("INFO:"),_("Can't unhome multiple axis"),INFO_ICON)
            print self.data.active_axis_buttons
        elif self.data.active_axis_buttons[0][0] == None:
            self.notify(_("INFO:"),_("No axis selected to unhome"),INFO_ICON)
        else:
            print "unhome axis %s" % self.data.active_axis_buttons[0][0]
            self.emc.unhome_selected(self.data.active_axis_buttons[0][1])


####################################################
#   Zero Axis
####################################################

    # Touchoff the axis zeroing it
    # reload the plot to update the display
    def zero_axis(self):
        if self.data.active_axis_buttons[0][0] == None:
            self.notify(_("INFO:"),_("No axis selected for origin zeroing"),INFO_ICON)
        # if an axis is selected then set it
        for i in self.data.axis_list:
            if self.widgets["axis_%s"%i].get_active():
                print "zero %s axis" %i
                self.mdi_control.set_axis(i,0)
                self.reload_plot()


####################################################
#   On ESTOP
####################################################
    def on_estop_clicked(self,*args):
        """This is a callback function for a click of the estop button
            It will togle between estop/machine off and enabled/machine on.
            Requires a button widget with a label named on_label
            Adds an alarm entry message on each toggle. 
        """
        if self.data.estopped:
            self.emc.estop_reset(1)
        elif not self.data.machine_on:
            self.emc.machine_on(1)
            self.widgets.on_label.set_text("Machine On")
            self.add_alarm_entry(_("Machine powered on"))
        else:
            self.emc.machine_off(1)
            self.emc.estop(1)
            self.widgets.on_label.set_text("Machine Off")
            self.add_alarm_entry(_("Machine Estopped!"))


####################################################
#   Feed rate
####################################################


    def set_feed_override(self,percent_rate,absolute=False):
        if absolute:
            rate = percent_rate
        else:
            rate = self.data.feed_override + percent_rate
        if rate > self.data.feed_override_max: rate = self.data.feed_override_max
        self.emc.feed_override(rate)

    def set_rapid_override(self,percent_rate,absolute=False):
        if absolute:
            rate = percent_rate
        else:
            rate = self.data.rapid_override + percent_rate
        if rate > self.data.rapid_override_max: rate = self.data.rapid_override_max
        self.emc.rapid_override(rate)


####################################################
#   Feed speed label
####################################################


    def update_feed_speed_label(self):
        data = self.data.velocity
        if self.data.IPR_mode:
            try:
                data = data/abs(self.halcomp["spindle-readout-in"])
            except:
                data = 0
        if self.data.dro_units == self.data._MM:
            text = "%.2f"% (data)
        else:
            text = "%.3f"% (data)
        self.widgets.active_feed_speed_label.set_label("F%s    S%s   V%s"% (self.data.active_feed_command,
                            self.data.active_spindle_command,text))


####################################################
#   Spindle and velocity rate
####################################################
    def set_spindle_override(self,percent_rate,absolute=False):
        if absolute:
            rate = percent_rate
        else:
            rate = self.data.spindle_override + percent_rate
        if rate > self.data.spindle_override_max: rate = self.data.spindle_override_max
        elif rate < self.data.spindle_override_min: rate = self.data.spindle_override_min
        self.emc.spindle_override(rate)

    def set_velocity_override(self,percent_rate,absolute=False):
        if absolute:
            rate = percent_rate
        else:
            rate = self.data.velocity_override + percent_rate
        if rate > 1.0: rate = 1.0
        self.emc.max_velocity(rate * self.data._maxvelocity)


    # spindle control
    def spindle_adjustment(self,direction,action):
        if action and not self.widgets.s_display_fwd.get_active() and not self.widgets.s_display_rev.get_active():
            self.notify(_("INFO:"),_("No direction selected for spindle"),INFO_ICON)
            return
        if direction and action:
            if self.data.spindle_speed:
                self.emc.spindle_faster(1)
            elif self.widgets.s_display_fwd.get_active():
               self.emc.spindle_forward(1,self.data.spindle_start_rpm)
            else:
                self.emc.spindle_reverse(1,self.data.spindle_start_rpm)
            print direction,action
        elif not direction and action:
            if self.data.spindle_speed:
                if self.data.spindle_speed >100:
                    self.emc.spindle_slower(1)
                else:
                    self.emc.spindle_off(1)


    def adjust_spindle_rpm(self, rpm, direction=None):
            # spindle control
             if direction == None:
                direction = self.data.spindle_dir
             if direction > 0:
                print "forward"
                self.emc.spindle_forward(1, float(rpm))
             elif direction < 0:
                print "reverse"
                self.emc.spindle_reverse(1, float(rpm))
             else:
                self.emc.spindle_off(1)


####################################################
#   Jog rate
####################################################

    def set_jog_rate(self,step=None,absolute=None):
        if self.data.angular_jog_adjustment_flag:
            j_rate = "angular_jog_rate"
        else:
            j_rate = "jog_rate"
        # in units per minute
        print "jog rate =",step,absolute,self.data[j_rate]
        if not absolute == None:
            rate = absolute
        elif not step == None:
            rate = self.data[j_rate] + step
        else:return
        if rate < 0: rate = 0
        if rate > self.data[j_rate+"_max"]: rate = self.data[j_rate+"_max"]
        rate = round(rate,1)
        if self.data.angular_jog_adjustment_flag:
            self.emc.continuous_jog_velocity(None,rate)
        else:
            self.emc.continuous_jog_velocity(rate,None)
        self.data[j_rate] = rate


####################################################
#   Jog increnets
####################################################

    # This sets the jog increments -there are three ways
    # ABSOLUTE:
    # set absolute to the absolute increment wanted
    # INDEX from INI:
    # self.data.jog_increments holds the increments from the INI file
    # do not set absolute variable
    # index_dir = 1 or -1 to set the rate higher or lower from the list
    def set_jog_increments(self,vector=None,index_dir=None,absolute=None):
        print "set jog incr"
        if self.data.angular_jog_adjustment_flag:
            incr = "angular_jog_increments"
            incr_index = "current_angular_jogincr_index"
        else:
            incr = "jog_increments"
            incr_index = "current_jogincr_index"

        if not absolute == None:
            distance = absolute
            self.widgets[incr].set_text("%f"%distance)
            self.halcomp["jog-increment-out"] = distance
            print "index jog increments",distance
            return
        elif not index_dir == None:
            next = self.data[incr_index] + index_dir
        elif not vector == None:
            next = vector
        else: return
        end = len(self.data[incr])-1
        if next < 0: next = 0
        if next > end: next = end
        self.data[incr_index] = next
        jogincr = self.data[incr][next]
        try:
            if 'angular' in incr and not jogincr == 'continuous':
                label = jogincr + ' Degs'
            else:
                label = jogincr
            self.widgets[incr].set_text(label)
        except:
            self.show_try_errors()
        if jogincr == ("continuous"):
            distance = 0
        else:
            distance = self.parse_increment(jogincr)
        print "index jog increments",jogincr,distance
        self.halcomp["jog-increment-out"] = distance


####################################################
#   Do JOG
####################################################

    # do some checks then jog selected axis or start spindle
    def do_jog(self,direction,action):
        # if manual mode, if jogging
        # if only one axis button pressed
        # jog positive  at selected rate
        if self.data.mode_order[0] == self.data._MAN:
            if len(self.data.active_axis_buttons) > 1:
                self.notify(_("INFO:"),_("Can't jog multiple axis"),INFO_ICON)
                print self.data.active_axis_buttons
            elif self.data.active_axis_buttons[0][0] == None:
                self.notify(_("INFO:"),_("No axis selected to jog"),INFO_ICON)
            else:
                print "Jog axis %s" % self.data.active_axis_buttons[0][0]
                if not self.data.active_axis_buttons[0][0] == "s":
                    if not action: cmd = 0
                    elif direction: cmd = 1
                    else: cmd = -1
                    self.emc.jogging(1)
                    if self.data.active_axis_buttons[0][0] in('a','b','c'):
                        jogincr = self.data.angular_jog_increments[self.data.current_angular_jogincr_index]
                    else:
                        jogincr = self.data.jog_increments[self.data.current_jogincr_index]
                    print jogincr
                    if jogincr == ("continuous"): # continuous jog
                        print "active axis jog:",self.data.active_axis_buttons[0][1]
                        self.emc.continuous_jog(self.data.active_axis_buttons[0][1],cmd)
                    else:
                        print "jog incremental"
                        if cmd == 0: return # don't want release of button to stop jog
                        distance = self.parse_increment(jogincr)
                        self.emc.incremental_jog(self.data.active_axis_buttons[0][1],cmd,distance)


    def do_key_jog(self,axis,direction,action):
        if self.data._JOG in self.check_mode(): # jog mode active:
                    if not action: cmd = 0
                    elif direction: cmd = 1
                    else: cmd = -1
                    self.emc.jogging(1)
                    print self.data.jog_increments[self.data.current_jogincr_index]
                    if self.data.jog_increments[self.data.current_jogincr_index] == ("continuous"): # continuous jog
                        print "active axis jog:",axis
                        self.emc.continuous_jog(axis,cmd)
                    else:
                        print "jog incremental"
                        if cmd == 0: return # don't want release of button to stop jog
                        self.mdi_control.mdi.emcstat.poll()
                        if self.mdi_control.mdi.emcstat.state != 1: return
                        jogincr = self.data.jog_increments[self.data.current_jogincr_index]
                        distance = self.parse_increment(jogincr)
                        self.emc.incremental_jog(axis,cmd,distance)


    # feeds to a position (while in manual mode)
    def do_jog_to_position(self,data):
        if len(self.data.active_axis_buttons) > 1:
            self.notify(_("INFO:"),_("Can't jog multiple axis"),INFO_ICON)
            print self.data.active_axis_buttons
        elif self.data.active_axis_buttons[0][0] == None:
            self.notify(_("INFO:"),_("No axis selected to move"),INFO_ICON)
        else:
            if not self.data.active_axis_buttons[0][0] == "s":
                if self.data.active_axis_buttons[0][0] in('a','b','c'):
                    rate = self.data.angular_jog_rate
                    pos = self.get_qualified_input(data,switch=_DEGREE_INPUT)
                else:
                    rate = self.data.jog_rate
                    pos = self.get_qualified_input(data)
                self.mdi_control.go_to_position(self.data.active_axis_buttons[0][0],pos,rate)



    # move axis to a position (while in manual mode)
    def move_to(self,data):
        if self.data.mode_order[0] == self.data._MAN:# if in manual mode
            if self.widgets.button_jog_mode.get_active(): # jog mode active
                print "jog to position"
                self.do_jog_to_position(data)

####################################################
#   Optional STOP
####################################################
    def set_optional_stop(self,data):
        self.prefs.putpref('opstop', data, bool)
        self.data.op_stop = data
        self.emc.opstop(data)

####################################################
#   Additional Functions (mist, flood, ignore limits)
####################################################

    def toggle_mist(self):
        if self.data.mist:
            self.emc.mist_off(1)
        else:
            self.emc.mist_on(1)

    def toggle_flood(self):
        if self.data.flood:
            self.emc.flood_off(1)
        else:
            self.emc.flood_on(1)

    def toggle_ignore_limits(self,*args):
        print "over ride limits"
        self.emc.override_limits(1)


####################################################
#   On mode change
####################################################

    # adjust the screen as per each mode toggled 
    def mode_changed(self,mode):

        if mode == self.data._MAN: 
            self.widgets.vmode0.show()
            self.widgets.vmode1.hide()
            self.widgets.notebook_mode.hide()
            self.widgets.hal_mdihistory.hide()
            self.widgets.button_homing.show()
            self.widgets.dro_frame.show()
            self.widgets.spare.hide()
        elif mode == self.data._MDI:
            if self.widgets.button_homing.get_active():
                self.widgets.button_homing.emit("clicked")
            if self.data.plot_hidden:
                self.toggle_offset_view()
            self.emc.set_mdi_mode()
            self.widgets.hal_mdihistory.show()
            self.widgets.vmode0.show()
            self.widgets.vmode1.hide()
            self.widgets.notebook_mode.hide()
        elif mode == self.data._AUTO:
            self.widgets.vmode0.hide()
            self.widgets.vmode1.show()
            if self.data.full_graphics:
                self.widgets.notebook_mode.hide()
            else:
                self.widgets.notebook_mode.show()
            self.widgets.hal_mdihistory.hide()
        if not mode == self.data._MAN:
            self.widgets.button_jog_mode.set_active(False)
            self.widgets.button_homing.set_active(False)
            self.widgets.button_homing.hide()
            self.widgets.spare.show()
        for i in range(0,3):
            if i == mode:
                self.widgets["mode%d"% i].show()
            else:
                self.widgets["mode%d"% i].hide()


####################################################
#   Check LinuxCNC status and update display
####################################################

    # check linuxcnc for status, error and then update the readout
    def timer_interrupt(self):
        self.emc.mask()
        self.emcstat = linuxcnc.stat()
        self.emcerror = linuxcnc.error_channel()
        self.emcstat.poll()
        self.data.task_mode = self.emcstat.task_mode 
        self.status.periodic()
        self.data.system = self.status.get_current_system()
        e = self.emcerror.poll()
        if e:
            kind, text = e
            print kind,text
            if "joint" in text:
                for letter in self.data.axis_list:
                    axnum = "xyzabcuvws".index(letter)
                    text = text.replace( "joint %d"%axnum,"Axis %s"%letter.upper() )
            if kind in (linuxcnc.NML_ERROR, linuxcnc.OPERATOR_ERROR):
                self.notify(_("Error Message"),text,ALERT_ICON,3)
            elif kind in (linuxcnc.NML_TEXT, linuxcnc.OPERATOR_TEXT):
                self.notify(_("Message"),text,INFO_ICON,3)
            elif kind in (linuxcnc.NML_DISPLAY, linuxcnc.OPERATOR_DISPLAY):
                self.notify(_("Message"),text,INFO_ICON,3)
        self.emc.unmask()
        if "periodic" in dir(self.handler_instance):
            self.handler_instance.periodic()
        else:
            self.update_position()
        return True

    # update the whole display
    def update_position(self,*args):
        self.update_mdi_spindle_button()
        self.update_spindle_bar()
        self.update_dro()
        self.update_active_gcodes()
        self.update_active_mcodes()
        self.update_aux_coolant_pins()
        self.update_feed_speed_label()
        self.update_tool_label()
        self.update_coolant_leds()
        self.update_estop_led()
        self.update_machine_on_led()
        self.update_limit_override()
        self.update_override_label()
        self.update_jog_rate_label()
        self.update_mode_label()
        self.update_units_button_label()



####################################################
#   G codes list
####################################################

    def update_active_gcodes(self):
        # active codes
        active_g = " ".join(self.data.active_gcodes)
        self.widgets.active_gcodes_label.set_label("%s   "% active_g)

    def update_active_mcodes(self):
        self.widgets.active_mcodes_label.set_label(" ".join(self.data.active_mcodes))

####################################################
#   Conncet signals
####################################################

    # this installs local signals unless overriden by custom handlers
    # HAL pin signal call-backs are covered in the HAL pin initilization functions
    def connect_signals(self):
        try:        
            self.widgets.btnX1.connect('clicked', self.on_btnX_clicked, 0)
            self.widgets.btnX2.connect('clicked', self.on_btnX_clicked, 1)
            self.widgets.btnX3.connect('clicked', self.on_btnX_clicked, 2)
            self.widgets.btnX4.connect('clicked', self.on_btnX_clicked, 3)
            self.widgets.btnX5.connect('clicked', self.on_btnX_clicked, 4)
            self.widgets.btnX6.connect('clicked', self.on_btnX_clicked, 5)
            self.widgets.btnX7.connect('clicked', self.on_btnX_clicked, 6)
            self.widgets.btnX8.connect('clicked', self.on_btnX_clicked, 7)
    
            self.widgets.btnY1.connect('clicked', self.on_btnY_clicked, 0)
            self.widgets.btnY2.connect('clicked', self.on_btnY_clicked, 1)
            self.widgets.btnY3.connect('clicked', self.on_btnY_clicked, 2)
            self.widgets.btnY4.connect('clicked', self.on_btnY_clicked, 3)
            self.widgets.btnY5.connect('clicked', self.on_btnY_clicked, 4)
            self.widgets.btnY6.connect('clicked', self.on_btnY_clicked, 5)
            self.widgets.btnY7.connect('clicked', self.on_btnY_clicked, 6)
            self.widgets.btnY8.connect('clicked', self.on_btnY_clicked, 7)
            

            self.widgets.btn_recall.connect('clicked', self.on_btn_recall_clicked)
            self.widgets.btn_machine.connect('clicked', self.on_btn_machine_clicked)
            self.widgets.btn_etc.connect('clicked', self.on_btn_etc_clicked)
            self.widgets.btn_menu.connect('clicked', self.on_btn_menu_clicked)
        except:
            print ("Dirrect connection: could not connect ")

    def on_btnX_clicked(self, widget, data=None):
        soft_key = self.widgets[self.data.CURRENTSCREEN].labelX[data][0]
        self.widgets[self.data.CURRENTSCREEN].on_soft_key_pressed(soft_key)
#        oldButton = self.widgets[self.data.CURRENTSCREEN].lght_btn
#        if screen != "" and screen != None: 
#            self.data.CURRENTSCREEN = self.widgets[self.data.CURRENTSCREEN].crnt_screen
##            self.set_screen()
#            self.highliteBTN(oldButton)


    def on_btnY_clicked(self, widget, data=None):
        soft_key = self.widgets[self.data.CURRENTSCREEN].labelY[data][0]
        self.widgets[self.data.CURRENTSCREEN].on_soft_key_pressed(soft_key)
#        soft_key = self.widgets[self.data.CURRENTSCREEN].labelY[data][0]
#        oldButton = self.widgets[self.data.CURRENTSCREEN].lght_btn
#        if screen != "" and screen != None: 
#            self.widgets[self.data.CURRENTSCREEN].on_soft_key_pressed(soft_key)
#            self.data.CURRENTSCREEN = self.widgets[self.data.CURRENTSCREEN].crnt_screen
#            self.set_screen()
#            self.highliteBTN(oldButton)
#        screen = self.widgets[self.data.CURRENTSCREEN].labelY[data][1]
#        oldButton = self.widgets[self.data.CURRENTSCREEN].lght_btn
#        if screen != "" and screen != None: 
#            self.data.CURRENTSCREEN = screen
#            self.set_screen()
#            self.highliteBTN(oldButton)


    def on_btn_recall_clicked(self, widget, data=None):
        self.change_screen(self.data.PARENTSCREEN)
    def on_btn_machine_clicked(self, widget, data=None):
        self.set_screen()
        self.widgets[self.data.CURRENTSCREEN].on_soft_key_pressed("Machining")

#        oldButton = self.widgets[self.data.CURRENTSCREEN].lght_btn
#        self.data.CURRENTSCREEN = "main_screen"
#        self.set_screen()
#        self.highliteBTN(oldButton)
    def on_btn_etc_clicked(self, widget, data=None):
        print ("etc")
    def on_btn_menu_clicked(self, widget, data=None):
        self.set_screen()
        self.widgets[self.data.CURRENTSCREEN].on_soft_key_pressed("MENU")
#        oldButton = self.widgets[self.data.CURRENTSCREEN].lght_btn
#        self.data.CURRENTSCREEN = "main_screen"
#        self.set_screen()
#        self.highliteBTN(oldButton)


## =========================================================
## BEGIN - Helper functions
## =========================================================

    # Handle window exit button press
    def on_window_delete_event(self, widget, data=None):
            self.close_window()
##          message = "Are you sure you want \n to close LinuxCNC?"
##            exit_hazzy = self.yes_no_dialog.run(message)
##            if exit_hazzy:
#        return True  # If does not return True will close window without popup!

    # Exit steps
    def close_window(self):
        print "estopping"
        try:
            self.emc.machine_off(1)
            self.emc.estop(1)
        except:
            pass
        time.sleep(2)
        gtk.main_quit()

#            self.set_state(linuxcnc.STATE_OFF)
#            self.set_state(linuxcnc.STATE_ESTOP)
def main():
    gtk.main()

if __name__ == "__main__":
    ui = myGUI()
    main()
