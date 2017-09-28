#!/usr/bin/python

import sys,os,subprocess
def _print_help():
            print """ Gscreen a customizable operator screen for linuxcnc based on pyGTK / GLADE.\n
        It is usually loaded from linuxcnc's INI file under the [DISPLAY] HEADER
        eg. DISPLAY = gscreen\n
        Options:
        --INI.................Designates the configuration file path for linuxcnc
        -c....................Loads an optional skin for Gscreen
        -d....................Debug mode
        -v....................Verbose debug mode
        -F....................Prints documentation of internal functions to standard output
        """
            sys.exit(0)

for num,temp in enumerate(sys.argv):
        if temp == '-h' or temp == '--help' or len(sys.argv) == 1:
            _print_help()

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

#import widget
#import data
#import color

from widget import Widgets
from color import Color
from data import Data
from screenlabels import ScrnLbl


#--------------------------------------------------------
# limit number of times err msgs are displayed
excepthook_msg_ct = 0
excepthook_msg_ct_max = 10

update_spindle_bar_error_ct = 0
update_spindle_bar_error_ct_max = 3
#--------------------------------------------------------

# try to add a notify system so messages use the
# nice intergrated pop-ups
# Ubuntu kinda wrecks this be not following the
# standard - you can't set how long the message stays up for.
# I suggest fixing this with a PPA off the net
# https://launchpad.net/~leolik/+archive/leolik?field.series_filter=lucid
try:
    NOTIFY_AVAILABLE = False
    import pynotify
    if not pynotify.init("Gscreen"):
        print "**** GSCREEN INFO: There was a problem initializing the pynotify module"
    else:
        NOTIFY_AVAILABLE = True
except:
    print "**** GSCREEN INFO: You don't seem to have pynotify installed"

# try to add ability for audio feedback to user.
try:
    _AUDIO_AVAILABLE = False
    import pygst
    pygst.require("0.10")
    import gst
    _AUDIO_AVAILABLE = True
    print "**** GSCREEN INFO: audio available!"
except:
    print "**** GSCREEN INFO: no audio alerts available - PYGST libray not installed?"

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

class myGUI:

    	def __init__(self):

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
		self.builder.add_from_file(gladefile2)	
		self.builder.add_from_file(gladefile3)
	
#		Need to correct connection

#       	self.builder.connect_signals(self)

	        self.widgets = Widgets(self.builder)
	
#		self.window = self.builder.get_object("window1")

#		self.widgets.window1.connect('window_delete_evet', self.on_window_delete_event)
		self.widgets.window1.set_title("Sinumeric 840D")
		self.widgets.window2.set_title("Alfa-Numeric Keyboard")
		self.widgets.window3.set_title("Main Keyboard")
	
		self.widgets.window1.connect('destroy', self.on_window_delete_event)
		self.widgets.window2.connect('destroy', self.on_window_delete_event)
		self.widgets.window3.connect('destroy', self.on_window_delete_event)

		self.set_style()
		self.set_labels(self.data.screenName.index("Main"))
		self.error_channel = linuxcnc.error_channel()

#		gtk.EventBox.modify_bg(gtk.STATE_NORMAL, lgray)

        	self.connect_signals()
	
#		# Check for messages
#		try:
#        		message = self.error_channel.poll()
#			if message:
#        	    		self._show_message(message)
#		except:
#        	    	print ("Problem with error chanel")

		# timers for display updates
#        	temp = self.inifile.find("DISPLAY","CYCLE_TIME")
#        	if not temp:
#            		self.add_alarm_entry(_("CYCLE_TIME in [DISPLAY] of INI file is missing: defaulting to 100ms"))
#            		temp = 100
#        	elif float(temp) < 50:
#            		self.add_alarm_entry(_("CYCLE_TIME in [DISPLAY] of INI file is too small: defaulting to 100ms"))
#            		temp = 100
#        	print _("timeout %d" % int(temp))
#        	if "timer_interrupt" in dir(self.handler_instance):
#            		gobject.timeout_add(int(temp), self.handler_instance.timer_interrupt)
#        	else:
#            		gobject.timeout_add(int(temp), self.timer_interrupt)
		temp = 100
		gobject.timeout_add(int(temp), self.timer_interrupt)
#		self.widgets = Widgets(self.xml)

		# Finally, show the window 
#        	self.window.show()
		self.widgets.window1.show()
		self.widgets.window2.show()
		self.widgets.window3.show()

    	# check linuxcnc for status, error and then update the readout
    	def timer_interrupt(self):		
#        	self.emc.mask()
#	        self.emcstat = linuxcnc.stat()
#        	self.emcerror = linuxcnc.error_channel()
#        	self.emcstat.poll()
#        	self.data.task_mode = self.emcstat.task_mode 
#        	self.status.periodic()
#        	self.data.system = self.status.get_current_system()
#        	e = self.emcerror.poll()
#        	if e:
#        	    kind, text = e
#            	print kind,text
#            	if "joint" in text:
#                	for letter in self.data.axis_list:
#                		axnum = "xyzabcuvws".index(letter)
#                    		text = text.replace( "joint %d"%axnum,"Axis %s"%letter.upper() )
#            	if kind in (linuxcnc.NML_ERROR, linuxcnc.OPERATOR_ERROR):
#                	self.notify(_("Error Message"),text,ALERT_ICON,3)
#            	elif kind in (linuxcnc.NML_TEXT, linuxcnc.OPERATOR_TEXT):
#                	self.notify(_("Message"),text,INFO_ICON,3)
#            	elif kind in (linuxcnc.NML_DISPLAY, linuxcnc.OPERATOR_DISPLAY):
#                	self.notify(_("Message"),text,INFO_ICON,3)
#        	self.emc.unmask()
#        	if "periodic" in dir(self.handler_instance):
#            		self.handler_instance.periodic()
#        	else:
#            		self.update_position()
		# Check for messages
		try:
        		message = self.error_channel.poll()
			if message:
        	    		self._show_message(message)
		except:
			pass
#        	    	print ("Problem with error chanel")
        	return True

    # Format Info & Error messages and display at bottom of screen, terminal
    	def _show_message(self, message):
        	kind, text = message # Unpack
	
#       	if "joint" in text:
#            	# Replace "joint N" with "L axis"
#            	for axis in self.axis_letter_list:
#                	joint = 'XYZABCUVWS'.index(axis)
#                	text = text.replace("joint {0}".format(joint), "{0} axis".format(axis))
#            	text = text.replace("joint -1", "all axes")

        	if text == "" or text is None:
            		text = "Unknown error!"

        	# Print to terminal and display at bottom of screen
        	if kind in (linuxcnc.NML_ERROR, linuxcnc.OPERATOR_ERROR, 'ERROR'):
#            		if kind != "ERROR":
#                		log.error(text)
            		kind = "ERROR"
            		color = 'red'
#            		self.hal['error'] = True
            		# flash the border in the message area
#            		self.set_animation('error_image', 'error_flash.gif')
#            		self.new_error = True
        	elif kind in (linuxcnc.NML_TEXT, linuxcnc.OPERATOR_TEXT, 'INFO'):
#            		if kind != "INFO":
#                		log.info(text)
            		kind = "INFO"
            		color = 'blue'
        	elif kind in (linuxcnc.NML_DISPLAY, linuxcnc.OPERATOR_DISPLAY, 'MSG'):
#            		if kind != "MSG":
#                		log.info(text)
            		kind = "MSG"
            		color = 'blue'
        	elif kind == 'WARN':
            		kind = "WARNING"
            		color = 'orange'
        	else:
            		kind == "ERROR"
            		color = 'red'
#            		log.error(text)

#        	msg = '<span size=\"11000\" weight=\"bold\" foreground=\"{0}\">{1}:' \
#        	'</span> {2}'.format(color, kind, text)
		msg = kind + text
        	self.widgets.lbl4.set_markup(msg)

    	def set_labels(self, screan):	
		self.widgets.lblX1.set_label(self.data.labelX_JOG[screan][0])
		self.widgets.lblX2.set_label(self.data.labelX_JOG[screan][1])	
		self.widgets.lblX3.set_label(self.data.labelX_JOG[screan][2])
		self.widgets.lblX4.set_label(self.data.labelX_JOG[screan][3])
		self.widgets.lblX5.set_label(self.data.labelX_JOG[screan][4])
		self.widgets.lblX6.set_label(self.data.labelX_JOG[screan][5])
		self.widgets.lblX7.set_label(self.data.labelX_JOG[screan][6])
		self.widgets.lblX8.set_label(self.data.labelX_JOG[screan][7])
	
		self.widgets.lblY1.set_label(self.data.labelY_JOG[screan][0])
		self.widgets.lblY2.set_label(self.data.labelY_JOG[screan][1])	
		self.widgets.lblY3.set_label(self.data.labelY_JOG[screan][2])
		self.widgets.lblY4.set_label(self.data.labelY_JOG[screan][3])
		self.widgets.lblY5.set_label(self.data.labelY_JOG[screan][4])
		self.widgets.lblY6.set_label(self.data.labelY_JOG[screan][5])
		self.widgets.lblY7.set_label(self.data.labelY_JOG[screan][6])
		self.widgets.lblY8.set_label(self.data.labelY_JOG[screan][7])
	
    	def set_style(self):	
		try:		    	
#			self.widgets.layout3.modify_bg(gtk.STATE_NORMAL, dgray)
#			self.widgets.layout2.modify_bg(gtk.STATE_NORMAL, dgray)
#			self.widgets.layout4.modify_bg(gtk.STATE_NORMAL, dgray)
#			self.widgets.layout21.modify_bg(gtk.STATE_NORMAL, dgray)
#			self.widgets.layout22.modify_bg(gtk.STATE_NORMAL, dgray)
#			self.widgets.layout31.modify_bg(gtk.STATE_NORMAL, dgray)
#			self.widgets.layout32.modify_bg(gtk.STATE_NORMAL, dgray)
#			self.widgets.layout33.modify_bg(gtk.STATE_NORMAL, dgray)
#			self.widgets.layout34.modify_bg(gtk.STATE_NORMAL, dgray)
#			self.widgets.layout35.modify_bg(gtk.STATE_NORMAL, dgray)
		
#			self.widgets.lineX.modify_bg(gtk.STATE_NORMAL, dgray)
#			self.widgets.ld11.modify_bg(gtk.STATE_NORMAL, dgray)
#			self.widgets.eventbox2.modify_bg(gtk.STATE_NORMAL, lgray)
			layouts = self.widgets.get_list(gtk.Layout)
			for lyt in layouts: 
				lyt.modify_bg(gtk.STATE_NORMAL, self.colors.dgray)
	
			labels = self.widgets.get_list(gtk.Label)
			for lbl in labels: 
				lbl.modify_font(pango.FontDescription('dejavusans condensed 10'))
			
			leds = self.widgets.get_list(gladevcp.led.HAL_LED)
			for led in leds: 
				led.modify_bg(gtk.STATE_NORMAL, self.colors.dgray)
	
			boxs = self.widgets.get_list(gtk.EventBox)
			for box in boxs: 
				box.modify_bg(gtk.STATE_NORMAL, self.colors.lblue)

			boxs = self.widgets.get_list(gtk.EventBox, self.widgets["lineX"])
			for box in boxs: 
				box.modify_bg(gtk.STATE_NORMAL, self.colors.gray)

			boxs = self.widgets.get_list(gtk.EventBox, self.widgets["lineY"])
			for box in boxs: 
				box.modify_bg(gtk.STATE_NORMAL, self.colors.gray)
#				print ("items %r"% led.__class__)
#				self.widgets[lbl].modify_bg(gtk.STATE_NORMAL, lgray)
			self.widgets["eventboxBig"].modify_bg(gtk.STATE_NORMAL, self.colors.lgray)
		except:
        	    	print ("Problem with style settings ")

	def soft_key_pressed(self, soft_key):
		if "X" in soft_key:
			key = self.data.labelX_JOG[self.data.screenName.index(self.data.CURRENTSCREEN)][int(soft_key[1])]
		elif "Y" in soft_key:
			key = self.data.labelY_JOG[self.data.screenName.index(self.data.CURRENTSCREEN)][int(soft_key[1])]
		else:
			key = None
		if self.data.CURRENTSCREEN == "Main":
			if key == "Machining":
				self.change_screen("Auxiliary")
			elif key == "Parameters":
				self.change_screen("Tool offset")
			elif key == "Programs":
				self.change_screen("Workpiece")
			elif key == "Services":
				print("OK")
			elif key == "Diagnosis":
				print("OK")
			elif key == "Auto":
				print("OK")
			elif key == "Cycles":
				print("OK")
			elif key == "AUTO":
				print("OK")
			elif key == "MDI":
				print("OK")
			elif key == "JOG":
				print("OK")
			elif key == "REPOS":
				print("OK")
			elif key == "REF":
				print("OK")
			elif key == "SBL\nExecute":
				print("OK")

		elif self.data.CURRENTSCREEN == "Auxiliary":
			if key == "Pre-\nsetting":
				self.change_screen("Presetting")
			elif key == "Handwheel":
				self.change_screen("Handwheel")
			elif key == "Increment":
				print("OK")
			elif key == "G fct.+\ntransf.":
				self.change_screen("G fct")
			elif key == "Auxiliary\nfunction":
				self.change_screen("Auxiliary")
			elif key == "Spindles":
				self.change_screen("Spindles")
			elif key == "Axis\nfeedrate":
				print("OK")
			elif key == "Zoom\nact.val":
				print("OK")
			elif key == "WCS":
				self.change_screen("WCS")

		elif self.data.CURRENTSCREEN == "Correct Program":
			if key == "Close":
				print("OK")
			
		elif self.data.CURRENTSCREEN == "MDI":
			if key == "OK":
				print("OK")
			
		elif self.data.CURRENTSCREEN == "Program Control":
			if key == "OK":
				print("OK")

		elif self.data.CURRENTSCREEN == "G fct":
			if key == "Pre-\nsetting":
				self.change_screen("Presetting")
			elif key == "Handwheel":
				self.change_screen("Handwheel")
			elif key == "Increment":
				print("OK")
			elif key == "G fct":
				self.change_screen("G fct")
			elif key == "Auxiliary\nfunction":
				self.change_screen("Auxiliary")
			elif key == "Spindles":
				self.change_screen("Spindles")
			elif key == "Axis\nfeedrate":
				print("OK")
			elif key == "Zoom\nact.val":
				print("OK")
			elif key == "WCS":
				self.change_screen("WCS")
			
		elif self.data.CURRENTSCREEN == "Handwheel":
			if key == "OK":
				print("OK")
			
		elif self.data.CURRENTSCREEN == "Presetting":
			if key == "OK":
				print("OK")

		elif self.data.CURRENTSCREEN == "Spindles":
			if key == "Pre-\nsetting":
				self.change_screen("Presetting")
			elif key == "Handwheel":
				self.change_screen("Handwheel")
			elif key == "Increment":
				print("OK")
			elif key == "G fct.+\ntransf.":
				self.change_screen("G fct")
			elif key == "Auxiliary\nfunction":
				self.change_screen("Auxiliary")
			elif key == "Spindles":
				self.change_screen("Spindles")
			elif key == "Axis\nfeedrate":
				print("OK")
			elif key == "Zoom\nact.val":
				print("OK")
			elif key == "WCS":
				self.change_screen("WCS")

		elif self.data.CURRENTSCREEN == "WCS":
			if key == "Pre-\nsetting":
				self.change_screen("Presetting")
			elif key == "Get Comp.":
				self.change_screen("getComp")
			elif key == "Handwheel":
				self.change_screen("Handwheel")
			elif key == "Increment":
				print("OK")
			elif key == "G fct.+\ntransf.":
				self.change_screen("G fct")
			elif key == "Auxiliary\nfunction":
				self.change_screen("Auxiliary")
			elif key == "Spindles":
				self.change_screen("Spindles")
			elif key == "Axis\nfeedrate":
				print("OK")
			elif key == "Zoom\nact.val":
				print("OK")
			elif key == "WCS":
				self.change_screen("WCS")
			
		elif self.data.CURRENTSCREEN == "getComp":
			if key == "Abort":
				print("OK")
			elif key == "OK":
				print("OK")
			
		elif self.data.CURRENTSCREEN == "new Tool":
			if key == "Abort":
				print("OK")
			elif key == "OK":
				print("OK")

		elif self.data.CURRENTSCREEN == "Rvar":
			if key == "Tool\noffset":
				self.change_screen("Tool offset")
			elif key == "R\nvariables":
				self.change_screen("Rvar")
			elif key == "Setting\ndata":
				print("OK")
			elif key == "Work\noffset":
				self.change_screen("Work offset")
			elif key == "User\ndata":
				print("OK")
			elif key == "Determine\ncompens.":
				print("OK")
			elif key == "Delete\nselect":
				print("OK")
			elif key == "Delete\nAll":
				print("OK")
			elif key == "Search":
				print("OK")

		elif self.data.CURRENTSCREEN == "Tool offset":
			if key == "Tool\noffset":
				self.change_screen("Tool offset")
			elif key == "R\nvariables":
				self.change_screen("Rvar")
			elif key == "Setting\ndata":
				print("OK")
			elif key == "Work\noffset":
				self.change_screen("Work offset")
			elif key == "User\ndata":
				self.change_screen("")
			elif key == "Determine\ncompens.":
				print("OK")
			elif key == "T no +":
				print("OK")
			elif key == "T no -":
				print("OK")
			elif key == "D no +":
				print("OK")
			elif key == "D no -":
				print("OK")
			elif key == "Delete":
				print("OK")
			elif key == "Details":
				print("OK")
			elif key == "Overview":
				print("OK")
			elif key == "New\ntool":
				print("OK")

		elif self.data.CURRENTSCREEN == "Work offset":
			if key == "Tool\noffset":
				self.change_screen("Tool offset")
			elif key == "R\nvariables":
				self.change_screen("Rvar")
			elif key == "Setting\ndata":
				print("OK")
			elif key == "Work\noffset":
				self.change_screen("Work offset")
			elif key == "User\ndata":
				print("OK")
			elif key == "Variables\nshow":
				print("OK")
			elif key == "ZO +":
				print("OK")
			elif key == "ZO -":
				print("OK")
			elif key == "EFFBASI":
				print("OK")
			elif key == "OVERVIEW":
				print("OK")
			elif key == "LOCATION":
				print("OK")
			elif key == "DELETE":
				print("OK")
			elif key == "STORE":
				print("OK")

		elif self.data.CURRENTSCREEN in "part Programs, stranot Cycles, sub Programs, user Cycles, Workpiece":
			if key == "Workpiece":
				self.change_screen("Workpiece")
			elif key == "Part\nprograms":
				self.change_screen("part Programs")
			elif key == "Sub\nprograms":
				self.change_screen("sub Programs")
			elif key == "Strand\ncycles":
				self.change_screen("stranot Cycles")
			elif key == "User\ncycles":
				self.change_screen("user Cycles")
			elif key == "Manufact.\nCycles":
				print("OK")
			elif key == "Memory\ninformation":
				print("OK")
			elif key == "New":
				print("OK")
			elif key == "Copy":
				print("OK")
			elif key == "Insert":
				print("OK")
			elif key == "Delete":
				print("OK")
			elif key == "Rename":
				print("OK")
			elif key == "Alter\nenable":
				print("OK")
			elif key == "Program\nselect":
				print("OK")

	def highliteLBL(self, label = None, oldLabel = None):
		print("change lbl color")
		if label:
			box = self.widgets[label].get_parent()
			box.modify_bg(gtk.STATE_NORMAL, self.colors.orange)
		if oldLabel and oldLabel != label:
			box = self.widgets[oldLabel].get_parent()
			box.modify_bg(gtk.STATE_NORMAL, self.colors.white)

	def highliteBTN(self, button = None, oldButton = None):
		if button:
			box = self.widgets[button].get_parent()
			box.modify_bg(gtk.STATE_NORMAL, self.colors.blue)
			print("lbl %r blue"% button)
		if oldButton and oldButton != button:
			box = self.widgets[oldButton].get_parent()
			box.modify_bg(gtk.STATE_NORMAL, self.colors.lgray)
			print("lbl %r gray"% oldButton)


	def set_screen(self,screen):
		oldLabel = self.data.screenParams[self.data.screenName.index(self.data.CURRENTSCREEN)][3]
		#oldLabel = ""
		oldButton = self.data.screenParams[self.data.screenName.index(self.data.CURRENTSCREEN)][4]
		print("btn old %r "% oldButton)
		print("screen %r "% self.data.CURRENTSCREEN)

		self.data.PARENTSCREEN = self.data.screenParams[self.data.screenName.index(screen)][0]	
		notebook = self.data.screenParams[self.data.screenName.index(screen)][1]
		change_act = self.data.screenParams[self.data.screenName.index(screen)][2]
		self.data.CURRENTLABEL = self.data.screenParams[self.data.screenName.index(screen)][3]
		button = self.data.screenParams[self.data.screenName.index(screen)][4]

		self.highliteLBL(self.data.CURRENTLABEL, oldLabel)
		self.highliteBTN(button, oldButton)	

		self.data.CURRENTSCREEN = screen
		if notebook:
			self.widgets["mainscreen"].set_current_page(int(notebook))
			print ("set notebook page")
		if change_act:
			self.change_view(change_act)

	def change_view(self, state):
		print ("change view")

	def change_screen(self,screan):
		self.set_labels(self.data.screenName.index(screan))
		self.set_screen(screan)
		print("OK")

	def place_sign(self, sign):
		if self.data.CURRENTLABEL:
			if self.data.editMode == "INSERT":
				text = self.widgets[self.data.CURRENTLABEL].get_text()
				if not self.data.editPosition: self.data.editPosition = len(text)
				text = text[:self.data.editPosition] + sign + text[self.data.editPosition:]
				self.data.editPosition = self.data.editPosition + 1
				self.widgets[self.data.CURRENTLABEL].set_text(text)
			elif  self.data.editMode == "SELECT":
				print("OK")
	
	def check_text(self):
		print("OK")

	def move_key(self, direction):
		lbl = self.data.CURRENTLABEL
		if lbl:
			st1, tbl, st3 = lbl.split('_')			
			lblLst = getattr(self.scrnlbl, tbl)
			maxY = len(lblLst) - 1
			y = 0
			for lst in lblLst:
				print("list %r"% lst)						
				try: 	
					print("lbl %r"% lbl)
					x = lst.index(lbl)
					print("x is  %r"% x)
				except:
					x = None
				if x != None: 											
					maxX = len(lst) - 1
					break
				y = y + 1			
			if direction == "LEFT":
				while True:
					newX = x - 1
					if newX < 0: 
						newX = maxX
						newY = y - 1
						if newY < 0:
							newY = maxY
					else: newY = y
					if lblLst[newY][newX]: break									
			elif direction == "RIGHT":
				print("OK")
			elif direction == "UP":
				print("OK")
			elif direction == "DOWN":
				print("OK")
			newLbl = lblLst[newY][newX]
			if self.data.CURRENTLABEL != newLbl:
				self.highliteLBL(newLbl, self.data.CURRENTLABEL)
				self.data.CURRENTLABEL = newLbl
				self.data.editPosition = ""
		print("OK")

	def page_key(self, direction):
		print("OK")


	def channel_key(self):
		print("OK")
	def alarm_cancel_key(self):
		print("OK")
	def help_key(self):
		print("OK")

	def next_win_key(self):
		print("OK")
	def backspace_key(self):
		print("OK")

	def select_key(self):
		print("OK")
	def insert_key(self):
		print("OK")
	def end_key(self):
		print("OK")
	def input_key(self):
		print("OK")


	# this installs local signals unless overriden by custom handlers
	# HAL pin signal call-backs are covered in the HAL pin initilization functions
	def connect_signals(self):
		try:		
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
	
			self.widgets.kb11.connect('clicked', self.on_kb11_clicked)
			self.widgets.kb12.connect('clicked', self.on_kb12_clicked)
			self.widgets.kb13.connect('clicked', self.on_kb13_clicked)
			self.widgets.kb14.connect('clicked', self.on_kb14_clicked)
			self.widgets.kb15.connect('clicked', self.on_kb15_clicked)
			self.widgets.kb21.connect('clicked', self.on_kb21_clicked)
			self.widgets.kb22.connect('clicked', self.on_kb22_clicked)
			self.widgets.kb23.connect('clicked', self.on_kb23_clicked)
			self.widgets.kb24.connect('clicked', self.on_kb24_clicked)
			self.widgets.kb25.connect('clicked', self.on_kb25_clicked)
			self.widgets.kb31.connect('clicked', self.on_kb31_clicked)
			self.widgets.kb32.connect('clicked', self.on_kb32_clicked)
			self.widgets.kb33.connect('clicked', self.on_kb33_clicked)
			self.widgets.kb34.connect('clicked', self.on_kb34_clicked)
			self.widgets.kb35.connect('clicked', self.on_kb35_clicked)
			self.widgets.kb41.connect('clicked', self.on_kb41_clicked)
			self.widgets.kb42.connect('clicked', self.on_kb42_clicked)
			self.widgets.kb43.connect('clicked', self.on_kb43_clicked)
			self.widgets.kb44.connect('clicked', self.on_kb44_clicked)
			self.widgets.kb45.connect('clicked', self.on_kb45_clicked)
			self.widgets.kb51.connect('clicked', self.on_kb51_clicked)
			self.widgets.kb52.connect('clicked', self.on_kb52_clicked)
			self.widgets.kb53.connect('clicked', self.on_kb53_clicked)
			self.widgets.kb54.connect('clicked', self.on_kb54_clicked)
			self.widgets.kb55.connect('clicked', self.on_kb55_clicked)
			self.widgets.kb61.connect('clicked', self.on_kb61_clicked)
			self.widgets.kb62.connect('clicked', self.on_kb62_clicked)
			self.widgets.kb63.connect('clicked', self.on_kb63_clicked)
			self.widgets.kb64.connect('clicked', self.on_kb64_clicked)
			self.widgets.kb65.connect('clicked', self.on_kb65_clicked)
			self.widgets.kb71.connect('clicked', self.on_kb71_clicked)
			self.widgets.kb72.connect('clicked', self.on_kb72_clicked)
			self.widgets.kb73.connect('clicked', self.on_kb73_clicked)
			self.widgets.kb74.connect('clicked', self.on_kb74_clicked)
			self.widgets.kb75.connect('clicked', self.on_kb75_clicked)
			self.widgets.kb81.connect('clicked', self.on_kb81_clicked)
			self.widgets.kb82.connect('clicked', self.on_kb82_clicked)
			self.widgets.kb83.connect('clicked', self.on_kb83_clicked)
			self.widgets.kb84.connect('clicked', self.on_kb84_clicked)
			self.widgets.kb85.connect('clicked', self.on_kb85_clicked)
	
			self.widgets.btnX1.connect('clicked', self.on_btnX1_clicked)
			self.widgets.btnX2.connect('clicked', self.on_btnX2_clicked)
			self.widgets.btnX3.connect('clicked', self.on_btnX3_clicked)
			self.widgets.btnX4.connect('clicked', self.on_btnX4_clicked)
			self.widgets.btnX5.connect('clicked', self.on_btnX5_clicked)
			self.widgets.btnX6.connect('clicked', self.on_btnX6_clicked)
			self.widgets.btnX7.connect('clicked', self.on_btnX7_clicked)
			self.widgets.btnX8.connect('clicked', self.on_btnX8_clicked)
	
			self.widgets.btnY1.connect('clicked', self.on_btnY1_clicked)
			self.widgets.btnY2.connect('clicked', self.on_btnY2_clicked)
			self.widgets.btnY3.connect('clicked', self.on_btnY3_clicked)
			self.widgets.btnY4.connect('clicked', self.on_btnY4_clicked)
			self.widgets.btnY5.connect('clicked', self.on_btnY5_clicked)
			self.widgets.btnY6.connect('clicked', self.on_btnY6_clicked)
			self.widgets.btnY7.connect('clicked', self.on_btnY7_clicked)
			self.widgets.btnY8.connect('clicked', self.on_btnY8_clicked)
	
			self.widgets.btn_recall.connect('clicked', self.on_btn_recall_clicked)
			self.widgets.btn_machine.connect('clicked', self.on_btn_machine_clicked)
			self.widgets.btn_etc.connect('clicked', self.on_btn_etc_clicked)
			self.widgets.btn_menu.connect('clicked', self.on_btn_menu_clicked)
        	except:
        	    print ("Dirrect connection: could not connect ")

	def on_mkb11_clicked(self, widget, data=None):
		print ("OK")
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
		print ("OK")
	def on_mkb32_clicked(self, widget, data=None):
		print ("OK")
	def on_mkb33_clicked(self, widget, data=None):
		print ("OK")
	def on_mkb37_clicked(self, widget, data=None):
		print ("OK")
	def on_mkb38_clicked(self, widget, data=None):
		print ("OK")

	def on_mkb41_clicked(self, widget, data=None):
		print ("OK")
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
		print ("OK")
	def on_mkb61_clicked(self, widget, data=None):
		print ("OK")
	def on_mkb62_clicked(self, widget, data=None):
		print ("OK")
	def on_mkb63_clicked(self, widget, data=None):
		print ("OK")
	#FIRST ROW
	def on_kb11_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("A")
		else: self.place_sign("7")
	def on_kb12_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("B")
		else: self.place_sign("8")
	def on_kb13_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("C")
		else: self.place_sign("9")
	def on_kb14_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("D")
		else: self.place_sign("/")
	def on_kb15_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("E")
		else: self.place_sign("(")
	#SECOND ROW
	def on_kb21_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("F")
		else: self.place_sign("4")
	def on_kb22_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("G")
		else: self.place_sign("5")
	def on_kb23_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("H")
		else: self.place_sign("6")
	def on_kb24_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("I")
		else: self.place_sign("*")
	def on_kb25_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("J")
		else: self.place_sign(")")
	#THIRD ROW
	def on_kb31_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("K")
		else: self.place_sign("1")
	def on_kb32_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("L")
		else: self.place_sign("2")
	def on_kb33_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("M")
		else: self.place_sign("3")
	def on_kb34_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("N")
		else: self.place_sign("-")
	def on_kb35_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("O")
		else: self.place_sign("[")
	#FOURTH ROW
	def on_kb41_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("P")
		else: self.place_sign("=")
	def on_kb42_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("Q")
		else: self.place_sign("0")
	def on_kb43_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("R")
		else: self.place_sign(".")
	def on_kb44_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("S")
		else: self.place_sign("+")
	def on_kb45_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("T")
		else: self.place_sign("]")
	#FIFTH ROW
	def on_kb51_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("U")
		else: self.place_sign("\\")
	def on_kb52_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("V")
		else: self.place_sign(",")
	def on_kb53_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("W")
		else: self.channel_key() 
	def on_kb54_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("X")
		else: self.alarm_cancel_key()
	def on_kb55_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("Y")
		else: self.help_key()
	#Sixth row
	def on_kb61_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("Z")
		else: self.place_sign(";")
	def on_kb62_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("?")
		else: self.next_win_key()
	def on_kb63_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("!")
		else: self.move_key("UP")
	def on_kb64_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("\'")
		else: self.page_key("DOWN")
	def on_kb65_clicked(self, widget, data=None):
		self.backspace_key()
	#Seventh row
	def on_kb71_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("_")
		else: self.place_sign(" ")
	def on_kb72_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("<")
		else: self.move_key("LEFT")
	def on_kb73_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign(">")
		else: self.select_key()
	def on_kb74_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("\"")
		else: self.move_key("RIGHT")
	def on_kb75_clicked(self, widget, data=None):
		self.insert_key()

	def on_kb81_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.data.SHIFTED = False
		else: self.data.SHIFTED = True
	def on_kb82_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign(":")
		else: self.end_key()
	def on_kb83_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("$")
		else: self.move_key("DOWN")
	def on_kb84_clicked(self, widget, data=None):
		if self.data.SHIFTED:
			self.place_sign("%")
		else: self.page_key("DOWN")
	def on_kb85_clicked(self, widget, data=None):
		self.input_key()

	def on_btnX1_clicked(self, widget, data=None):
		self.soft_key_pressed("X0")
	def on_btnX2_clicked(self, widget, data=None):
		self.soft_key_pressed("X1")
	def on_btnX3_clicked(self, widget, data=None):
		self.soft_key_pressed("X2")
	def on_btnX4_clicked(self, widget, data=None):
		self.soft_key_pressed("X3")
	def on_btnX5_clicked(self, widget, data=None):
		self.soft_key_pressed("X4")
	def on_btnX6_clicked(self, widget, data=None):
		self.soft_key_pressed("X5")
	def on_btnX7_clicked(self, widget, data=None):
		self.soft_key_pressed("X6")
	def on_btnX8_clicked(self, widget, data=None):
		self.soft_key_pressed("X7")

	def on_btnY1_clicked(self, widget, data=None):
		self.soft_key_pressed("Y0")
	def on_btnY2_clicked(self, widget, data=None):
		self.soft_key_pressed("Y1")
	def on_btnY3_clicked(self, widget, data=None):
		self.soft_key_pressed("Y2")
	def on_btnY4_clicked(self, widget, data=None):
		self.soft_key_pressed("Y3")
	def on_btnY5_clicked(self, widget, data=None):
		self.soft_key_pressed("Y4")
	def on_btnY6_clicked(self, widget, data=None):
		self.soft_key_pressed("Y5")
	def on_btnY7_clicked(self, widget, data=None):
		self.soft_key_pressed("Y6")
	def on_btnY8_clicked(self, widget, data=None):
		self.soft_key_pressed("Y7")

	def on_btn_recall_clicked(self, widget, data=None):
		self.change_screen(self.data.PARENTSCREEN)
	def on_btn_machine_clicked(self, widget, data=None):
		self.change_screen("Auxiliary")
	def on_btn_etc_clicked(self, widget, data=None):
		print ("etc")
	def on_btn_menu_clicked(self, widget, data=None):
		self.change_screen("Main")

#	    def on_kb11_clicked(self, widget, data=None):
#		self.widgets.lblX1.set_text("New Text from 1")
##		self.widgets.label2.set_text("New Text from 1")

#	    def on_kb12_clicked(self, widget, data=None):
##		self.widgets.lblX3.set_text(" 2")
#		self.widgets.lblX2.set_text("2nd")

## =========================================================
## BEGIN - Helper functions
## =========================================================

    # Handle window exit button press
    	def on_window_delete_event(self, widget, data=None):
		self.close_window()
##      	message = "Are you sure you want \n to close LinuxCNC?"
##        	exit_hazzy = self.yes_no_dialog.run(message)
##        	if exit_hazzy:
        

#        return True  # If does not return True will close window without popup!

    # Exit steps
    	def close_window(self):
	 	gtk.main_quit()

#        	self.set_state(linuxcnc.STATE_OFF)
#        	self.set_state(linuxcnc.STATE_ESTOP)
        


def main():
    gtk.main()

if __name__ == "__main__":
    ui = myGUI()
    main()
