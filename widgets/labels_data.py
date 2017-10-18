#!/usr/bin/python
#
#
# Copyright (c) 2017  Maksym Kotelnikov
#
# a class for holding data
# here we intialize the data

def labels_X(find):
    if find == "screen_rvar":
        back = [["Tool\noffset", "screen_tool"],
                ["R\nvariables", "screen_rvar"],
                ["Setting\ndata", "screen_gfile"],
                ["Work\noffset", ""],
                ["User\ndata", ""],
                ["", ""],
                ["", ""],
                ["Determine\ncompens.", ""], ] 
    elif find == "screen_tool":
        back = [["Tool\noffset", "screen_tool"],
                ["R\nvariables", "screen_rvar"],
                ["Setting\ndata", "screen_gfile"],
                ["Work\noffset", ""],
                ["User\ndata", ""],
                ["", ""],
                ["", ""],
                ["Determine\ncompens.", ""], ]
    elif find == "main_screen":
        back = [["Machining", "screen_tool"],
                ["Parameters", "screen_rvar"],
                ["Programs", "screen_gfile"],
                ["Services", ""],
                ["Diagnosis", ""],
                ["Auto", ""],
                ["Cycles", ""],
                ["", ""], ]
    elif find == "screen_aux":
        back = [["", "screen_tool"],
                ["Pre-\nsetting", "screen_rvar"],
                ["", "screen_gfile"],
                ["", ""],
                ["", ""],
                ["Handwheel", ""],
                ["Increment", ""],
                ["", ""], ]
    elif find == "screen_open_file":
        back = [["Workpiece", "screen_tool"],
                ["Part\nprograms", "screen_rvar"],
                ["Sub\nprograms", "screen_gfile"],
                ["Strand\ncycles", ""],
                ["User\ncycles", ""],
                ["Manufact.\nCycles", ""],
                ["", ""],
                ["Memory\ninformation", ""], ]
    elif find == "screen_gfile":
        back = [["Workpiece", "screen_tool"],
                ["Part\nprograms", "screen_rvar"],
                ["Sub\nprograms", "screen_gfile"],
                ["Strand\ncycles", ""],
                ["User\ncycles", ""],
                ["Manufact.\nCycles", ""],
                ["", ""],
                ["Memory\ninformation", ""], ]
    elif find == "screen_new_tool":
        back = [["", "screen_tool"],
                ["", "screen_rvar"],
                ["", "screen_gfile"],
                ["", ""],
                ["", ""],
                ["", ""],
                ["", ""],
                ["", ""], ]
    elif find == "screen_gcomp":
        back = [["", "screen_tool"],
                ["", "screen_rvar"],
                ["", "screen_gfile"],
                ["", ""],
                ["", ""],
                ["", ""],
                ["", ""],
                ["", ""], ]
    else: back = ""
    return back

def labels_Y(find):
    if find == "screen_rvar":
        back = [["", ""],
                ["", ""],
                ["", ""],
                ["Delete\nselect", ""],
                ["Delete\nAll", ""],
                ["Search", ""],
                ["", ""],
                ["", ""], ]
    elif find == "screen_tool":
        back = [["T no +", ""],
                ["T no -", ""],
                ["D no +", ""],
                ["D no -", ""],
                ["Delete", ""],
                ["Details", ""],
                ["Overview", ""],
                ["New\ntool", ""], ]
    elif find == "main_screen":
        back = [["AUTO", ""],
                ["MDI", ""],
                ["JOG", ""],
                ["REPOS", ""],
                ["REF", ""],
                ["", ""],
                ["", ""],
                ["SBL\nExecute", ""], ]
    elif find == "screen_aux":
        back = [["G fct.+\ntransf.", "screen_tool"],
                ["Auxiliary\nfunction", "screen_rvar"],
                ["Spindles", "screen_gfile"],
                ["Axis\nfeedrate", ""],
                ["", ""],
                ["Zoom\nact.val", ""],
                ["WCS", ""],
                ["", ""], ]
    elif find == "screen_open_file":
        back = [["New", "screen_tool"],
                ["Copy", "screen_rvar"],
                ["Insert", "screen_gfile"],
                ["Delete", ""],
                ["Rename", ""],
                ["Alter\nenable", ""],
                ["Program\nselect", ""],
                ["", ""], ]
    elif find == "screen_gfile":
        back = [["New", "screen_tool"],
                ["Copy", "screen_rvar"],
                ["Insert", "screen_gfile"],
                ["Delete", ""],
                ["Rename", ""],
                ["Alter\nenable", ""],
                ["Program\nselect", ""],
                ["", ""], ]
    elif find == "screen_new_tool":
        back = [["", "screen_tool"],
                ["", "screen_rvar"],
                ["", "screen_gfile"],
                ["", ""],
                ["", ""],
                ["", ""],
                ["Abort", ""],
                ["OK", ""], ]
    elif find == "screen_gcomp":
        back = [["", "screen_tool"],
                ["", "screen_rvar"],
                ["", "screen_gfile"],
                ["", ""],
                ["", ""],
                ["", ""],
                ["Abort", ""],
                ["OK", ""], ]
    else: back = ""
    return back

#    def __init__(self):
#        self.headers = ["Header1",
#            "Header2",
#            "Header3",
#            "Header4",
#            "Header5",
#            "Header6",
#            "Header7",
#            "Header8",
#            "Header9",
#            "Header10",
#            "Header11",
#            "Header12",
#            "Header13",
#            "Header14",
#            "Header15",]
#        self.rvar = [ ["lbl_rvar_0", "lbl_rvar_13"],
#            ["lbl_rvar_1", "lbl_rvar_14"],
#            ["lbl_rvar_2", "lbl_rvar_15"],
#            ["lbl_rvar_3", "lbl_rvar_16"],
#            ["lbl_rvar_4", "lbl_rvar_17"],
#            ["lbl_rvar_5", "lbl_rvar_18"],
#            ["lbl_rvar_6", "lbl_rvar_19"],
#            ["lbl_rvar_7", "lbl_rvar_20"],
#            ["lbl_rvar_8", "lbl_rvar_21"],
#            ["lbl_rvar_9", "lbl_rvar_22"],
#            ["lbl_rvar_10", "lbl_rvar_23"],
#            ["lbl_rvar_11", "lbl_rvar_24"],
#            ["lbl_rvar_12", "lbl_rvar_25"],]
#    
#    def __getitem__(self, item):
#        return getattr(self, item)
#    def __setitem__(self, item, value):
#        return setattr(self, item, value)
