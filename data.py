#!/usr/bin/python

# a class for holding data
# here we intialize the data
class Data:
    def __init__(self):
	#screens and label list
	self.SHIFTED = True
	self.CURRENTSCREEN = "Main"
	self.PARENTSCREEN = "Main"
	self.CURRENTLABEL = ""
	self.editPosition = ""
	self.editMode = "INSERT"
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
				["Main", "1", "", "lbl_rvar_0", "lblX2"],  
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
