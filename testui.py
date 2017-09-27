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

# a class for holding the glade widgets rather then searching for them each time
class Widgets:
    def __init__(self, xml):
        self._xml = xml
    def __getattr__(self, attr):
        r = self._xml.get_object(attr)
        if r is None: raise AttributeError, "No widget %r" % attr
        return r
    def __getitem__(self, attr):
        r = self._xml.get_object(attr)
        if r is None: raise IndexError, "No widget %r" % attr
        return r
    def get_list(self, attr, parent = None):
	l = self._xml.get_objects()
	item_list = []
	for item in l:
	     if isinstance(item, attr): 
		if parent != None:
#			print ("parent %r  %r"% (item.get_parent(), parent))
			if item.get_parent() == parent:			
				item_list.append(item)
	        else: item_list.append(item)
	if len(item_list) < 1: raise IndexError, "No such widgets %r %r" % (type(item),len(l))
        return item_list

# a class for holding data
# here we intialize the data
class Data:
    def __init__(self):
	#screens and label list
	self.CURRENTSCREEN = "Main"
	self.PARENTSCREEN = "Main"
	self.CURRENTLABEL = ""
	self.screenName = [ "Main", 
				"Auxiliary",  
				"Correct Program",  
				"MDI",  
				"Program Control",  
				"G fct",  
				"Handwheel",  
				"Presetting",  
				"Spindles",  
				"WCS",  
				"getComp",  
				"new Tool",  
				"Rvar",  
				"Tool offset",  
				"Work offset",  
				"part Programs",  
				"stranot Cycles",  
				"sub Programs",  
				"user Cycles",  
				"Workpiece"]
	self.screenParams = [ ["Main", "", "", "", ""], 
				["Main", "", "", "", "lblY2"],   
				["Auxiliary", "", "", "", ""],   
				["Auxiliary", "", "", "", ""],   
				["Auxiliary", "", "", "", ""],   
				["Main", "", "", "", "lblY1"],  

				["Main", "", "", "", ""],  
				["Main", "", "", "", ""],  
				["Main", "", "", "", "lblY3"],  
				["Main", "", "", "", ""],  
				["WCS", "", "", "", ""],
 
				["Main", "", "", "", ""],  
				["Main", "", "", "", "lblX2"],  
				["Main", "", "", "", "lblX1"],  
				["Main", "", "", "", "lblX4"],  
				["Main", "", "", "", "lblX2"],  

				["Main", "", "", "", "lblX4"],  
				["Main", "", "", "", "lblX3"],  
				["Main", "", "", "", "lblX5"],  
				["Main", "", "", "", "lblX1"],  ]
	self.labelX_JOG = [
			["Machining", "Parameters", "Programs", "Services", "Diagnosis", "Auto", "Cycles", ""],
			["", "Pre-\nsetting", "", "", "", "Handwheel", "Increment", ""],
			["", "", "", "", "", "", "", ""],
			["", "", "", "", "", "", "", ""],
			["", "", "", "", "", "", "", ""],
			["", "Pre-\nsetting", "", "", "", "Handwheel", "Increment", ""],
			["", "", "", "", "", "", "", ""],
			["", "", "", "", "", "", "", ""],
			["", "Pre-\nsetting", "", "", "", "Handwheel", "Increment", ""],
			["", "Pre-\nsetting", "Get Comp.", "", "", "Handwheel", "Increment", ""],
			["", "", "", "", "", "", "", ""],
			["", "", "", "", "", "", "", ""],
			["Tool\noffset", "R\nvariables", "Setting\ndata", "Work\noffset", "User\ndata", "", "", "Determine\ncompens."],
			["Tool\noffset", "R\nvariables", "Setting\ndata", "Work\noffset", "User\ndata", "", "", "Determine\ncompens."],
			["Tool\noffset", "R\nvariables", "Setting\ndata", "Work\noffset", "User\ndata", "Variables\nshow", "", ""],
			["Workpiece", "Part\nprograms", "Sub\nprograms", "Strand\ncycles", "User\ncycles", "Manufact.\nCycles", "", "Memory\ninformation"],
			["Workpiece", "Part\nprograms", "Sub\nprograms", "Strand\ncycles", "User\ncycles", "Manufact.\nCycles", "", "Memory\ninformation"],
			["Workpiece", "Part\nprograms", "Sub\nprograms", "Strand\ncycles", "User\ncycles", "Manufact.\nCycles", "", "Memory\ninformation"],
			["Workpiece", "Part\nprograms", "Sub\nprograms", "Strand\ncycles", "User\ncycles", "Manufact.\nCycles", "", "Memory\ninformation"],
			["Workpiece", "Part\nprograms", "Sub\nprograms", "Strand\ncycles", "User\ncycles", "Manufact.\nCycles", "", "Memory\ninformation"],]
	self.labelY_JOG = [
			["AUTO", "MDI", "JOG", "REPOS", "REF", "", "", "SBL\nExecute"],
			["G fct.+\ntransf.", "Auxiliary\nfunction", "Spindles", "Axis\nfeedrate", "", "Zoom\nact.val", "WCS", ""],
			["", "", "", "", "", "", "", "Close"],
			["", "", "", "", "", "", "", "OK"],
			["", "", "", "", "", "", "", "OK"],
			["G fct.+ transf.", "Auxiliary\nfunction", "Spindles", "Axis\nfeedrate", "", "Zoom\nact.val", "WCS", ""],
			["", "", "", "", "", "", "", "OK"],
			["", "", "", "", "", "", "", "OK"],
			["G fct.+ transf.", "Auxiliary\nfunction", "Spindles", "Axis\nfeedrate", "", "Zoom\nact.val", "WCS", ""],
			["G fct.+ transf.", "Auxiliary\nfunction", "Spindles", "Axis\nfeedrate", "", "Zoom\nact.val", "WCS", ""],
			["", "", "", "", "", "", "Abort", "OK"],
			["", "", "", "", "", "", "Abort", "OK"],
			["", "", "", "Delete\nselect", "Delete\nAll", "Search", "", ""],
			["T no +", "T no -", "D no +", "D no -", "Delete", "Details", "Overview", "New\ntool"],
			["ZO +", "ZO -", "EFFBASI", "OVERVIEW", "LOCATION", "", "DELETE", "STORE"],
			["New", "Copy", "Insert", "Delete", "Rename", "Alter\nenable", "Program\nselect", ""],
			["New", "Copy", "Insert", "Delete", "Rename", "Alter\nenable", "Program\nselect", ""],
			["New", "Copy", "Insert", "Delete", "Rename", "Alter\nenable", "Program\nselect", ""],
			["New", "Copy", "Insert", "Delete", "Rename", "Alter\nenable", "Program\nselect", ""],
			["New", "Copy", "Insert", "Delete", "Rename", "Alter\nenable", "Program\nselect", ""],]

        # constants for mode idenity
        self._MAN = 0
        self._MDI = 1
        self._AUTO = 2
        self._JOG = 3
        self._MM = 1
#        self._IMPERIAL = 0
        # paths included to give access to handler files
#        self.SKINPATH = SKINPATH
#        self.CONFIGPATH = CONFIGPATH
#        self.BASEPATH = BASE

        self.audio_available = False
        self.use_screen2 = False
        self.theme_name = "Follow System Theme"
        self.abs_textcolor = ""
        self.rel_textcolor = ""
        self.dtg_textcolor = ""
        self.err_textcolor = ""
        self.window_geometry = ""
        self.window_max = ""
        self.axis_list = []
        self.rotary_joints = False
        self.active_axis_buttons = [(None,None)] # axis letter,axis number
        self.abs_color = (0, 65535, 0)
        self.rel_color = (65535, 0, 0)
        self.dtg_color = (0, 0, 65535)
        self.highlight_color = (65535,65535,65535)
        self.highlight_major = False
#        self.display_order = (_REL,_DTG,_ABS)
        self.mode_order = (self._MAN,self._MDI,self._AUTO)
        self.mode_labels = ["Manual Mode","MDI Mode","Auto Mode"]
        self.IPR_mode = False
        self.plot_view = ("p","x","y","y2","z","z2")
        self.task_mode = 0
        self.active_gcodes = []
        self.active_mcodes = []
        for letter in ('x','y','z','a','b','c','u','v','w'):
            self['%s_abs'%letter] = 0.0
            self['%s_rel'%letter] = 0.0
            self['%s_dtg'%letter] = 0.0
            self['%s_is_homed'%letter] = False
        self.spindle_request_rpm = 0
        self.spindle_dir = 0
        self.spindle_speed = 0
        self.spindle_start_rpm = 300
        self.spindle_preset = 300
        self.active_spindle_command = "" # spindle command setting
        self.active_feed_command = "" # feed command setting
        self.system = 1
        self.estopped = True
        self.dro_units = self._MM
        self.machine_units = self._MM
        self.tool_in_spindle = 0
        self.flood = False
        self.mist = False
        self.machine_on = False
        self.or_limits = False
        self.op_stop = False
        self.block_del = False
        self.all_homed = False

        self.jog_rate = 15
        self.jog_rate_inc = 1
        self.jog_rate_max = 60
        self.jog_increments = []
        self.current_jogincr_index = 0
        self.angular_jog_adjustment_flag = False
        self.angular_jog_increments = []
        self.angular_jog_rate = 1800
        self.angular_jog_rate_inc = 60
        self.angular_jog_rate_max = 7200
        self.current_angular_jogincr_index = 0
        self.feed_override = 1.0
        self.feed_override_inc = .05
        self.feed_override_max = 2.0
        self.rapid_override = 1.0
        self.rapid_override_inc = .05
        self.rapid_override_max = 1.0
        self.spindle_override = 1.0
        self.spindle_override_inc = .05
        self.spindle_override_max = 1.2
        self.spindle_override_min = .50
        self.maxvelocity = 1
        self.velocity_override = 1.0
        self.velocity_override_inc = .05
        self.edit_mode = False
        self.full_graphics = False
        self.graphic_move_inc = 20
        self.plot_hidden = False
        self.file = ""
        self.file_lines = 0
        self.line = 0
        self.last_line = 0
        self.motion_line = 0
        self.id = 0
        self.dtg = 0.0
        self.show_dtg = False
        self.velocity = 0.0
        self.delay = 0.0
        self.preppedtool = None
        self.lathe_mode = False
        self.diameter_mode = True
        self.tooleditor = ""
        self.tooltable = ""
        self.alert_sound = "/usr/share/sounds/ubuntu/stereo/bell.ogg"         
        self.error_sound  = "/usr/share/sounds/ubuntu/stereo/dialog-question.ogg"
        self.ob = None
        self.index_tool_dialog = None
        self.keyboard_dialog = None
        self.preset_spindle_dialog = None
        self.spindle_control_dialog = None
        self.entry_dialog = None
        self.restart_dialog = None
        self.key_event_last = None,0
	

    def __getitem__(self, item):
        return getattr(self, item)
    def __setitem__(self, item, value):
        return setattr(self, item, value)

class Color:
	def __init__(self):
		self.dgray = gtk.gdk.Color('#3c3c3c')
		self.gray = gtk.gdk.Color('#dddddd')
		self.lgray = gtk.gdk.Color('#d2d1cf')
		self.lblue = gtk.gdk.Color('#cddddd')
		self.blue = gtk.gdk.Color('#067aa3')
		self.orange = gtk.gdk.Color('#ff7f00')
		self.white = gtk.gdk.Color('#000000')
    	def __getitem__(self, item):
        		return getattr(self, item)
    	def __setitem__(self, item, value):
        		return setattr(self, item, value)

	

class myGUI:

    	def __init__(self):

		#add data 
		self.data = Data()
		self.colors = Color()

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

	def highliteLBL(self, label = None, oldLabel = None, button = None, oldButton = None):
		print("change lbl color")
		if label:
			box = self.widgets[label].get_parent()
			box.modify_bg(gtk.STATE_NORMAL, self.colors.orange)
		if oldLabel and oldLabel != label:
			box = self.widgets[oldLabel].get_parent()
			box.modify_bg(gtk.STATE_NORMAL, self.colors.white)
		if button:
			box = self.widgets[button].get_parent()
			box.modify_bg(gtk.STATE_NORMAL, self.colors.blue)
			print("lbl %r blue"% button)
		if oldButton and oldButton != button:
			box = self.widgets[oldButton].get_parent()
			box.modify_bg(gtk.STATE_NORMAL, self.colors.lgray)
			print("lbl %r gray"% oldButton)

	def set_screen(self,screen):
		oldLabel = self.data.screenParams[self.data.screenName.index(self.data.CURRENTSCREEN)][1]
		oldButton = self.data.screenParams[self.data.screenName.index(self.data.CURRENTSCREEN)][4]
		print("btn old %r "% oldButton)
		print("screen %r "% self.data.CURRENTSCREEN)
		self.data.PARENTSCREEN = self.data.screenParams[self.data.screenName.index(screen)][0]
		self.data.CURRENTLABEL = self.data.screenParams[self.data.screenName.index(screen)][1] 
		notebook = self.data.screenParams[self.data.screenName.index(screen)][2]
		change_act = self.data.screenParams[self.data.screenName.index(screen)][3]
		button = self.data.screenParams[self.data.screenName.index(screen)][4]
		self.highliteLBL(self.data.CURRENTLABEL, oldLabel, button, oldButton)	
		self.data.CURRENTSCREEN = screen
		if notebook:
			print ("set notebook page")
		if change_act:
			self.change_view(change_act)

	def change_view(self, state):
		print ("change view")

	def change_screen(self,screan):
		self.set_labels(self.data.screenName.index(screan))
		self.set_screen(screan)
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
        if self.data.SHIFTED:
            self.place_sign()
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

	def on_kb11_clicked(self, widget, data=None):
		print ("OK")
	def on_kb12_clicked(self, widget, data=None):
		print ("OK")
	def on_kb13_clicked(self, widget, data=None):
		print ("OK")
	def on_kb14_clicked(self, widget, data=None):
		print ("OK")
	def on_kb15_clicked(self, widget, data=None):
		print ("OK")

	def on_kb21_clicked(self, widget, data=None):
		print ("OK")
	def on_kb22_clicked(self, widget, data=None):
		print ("OK")
	def on_kb23_clicked(self, widget, data=None):
		print ("OK")
	def on_kb24_clicked(self, widget, data=None):
		print ("OK")
	def on_kb25_clicked(self, widget, data=None):
		print ("OK")

	def on_kb31_clicked(self, widget, data=None):
		print ("OK")
	def on_kb32_clicked(self, widget, data=None):
		print ("OK")
	def on_kb33_clicked(self, widget, data=None):
		print ("OK")
	def on_kb34_clicked(self, widget, data=None):
		print ("OK")
	def on_kb35_clicked(self, widget, data=None):
		print ("OK")

	def on_kb41_clicked(self, widget, data=None):
		print ("OK")
	def on_kb42_clicked(self, widget, data=None):
		print ("OK")
	def on_kb43_clicked(self, widget, data=None):
		print ("OK")
	def on_kb44_clicked(self, widget, data=None):
		print ("OK")
	def on_kb45_clicked(self, widget, data=None):
		print ("OK")

	def on_kb51_clicked(self, widget, data=None):
		print ("OK")
	def on_kb52_clicked(self, widget, data=None):
		print ("OK")
	def on_kb53_clicked(self, widget, data=None):
		print ("OK")
	def on_kb54_clicked(self, widget, data=None):
		print ("OK")
	def on_kb55_clicked(self, widget, data=None):
		print ("OK")

	def on_kb61_clicked(self, widget, data=None):
		print ("OK")
	def on_kb62_clicked(self, widget, data=None):
		print ("OK")
	def on_kb63_clicked(self, widget, data=None):
		print ("OK")
	def on_kb64_clicked(self, widget, data=None):
		print ("OK")
	def on_kb65_clicked(self, widget, data=None):
		print ("OK")

	def on_kb71_clicked(self, widget, data=None):
		print ("OK")
	def on_kb72_clicked(self, widget, data=None):
		print ("OK")
	def on_kb73_clicked(self, widget, data=None):
		print ("OK")
	def on_kb74_clicked(self, widget, data=None):
		print ("OK")
	def on_kb75_clicked(self, widget, data=None):
		print ("OK")

	def on_kb81_clicked(self, widget, data=None):
		print ("OK")
	def on_kb82_clicked(self, widget, data=None):
		print ("OK")
	def on_kb83_clicked(self, widget, data=None):
		print ("OK")
	def on_kb84_clicked(self, widget, data=None):
		print ("OK")
	def on_kb85_clicked(self, widget, data=None):
		print ("OK")

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
