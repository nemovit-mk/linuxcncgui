#!/usr/bin/python

# a class for holding data
# here we intialize the data
class ScrnLbl:
	def __init__(self):
		self.headers = ["Header1",
				"Header2",
				"Header3",
				"Header4",
				"Header5",
				"Header6",
				"Header7",
				"Header8",
				"Header9",
				"Header10",
				"Header11",
				"Header12",
				"Header13",
				"Header14",
				"Header15",]
		self.rvar = [ ["lbl_rvar_0", "lbl_rvar_13"],
				["lbl_rvar_1", "lbl_rvar_14"],
				["lbl_rvar_2", "lbl_rvar_15"],
				["lbl_rvar_3", "lbl_rvar_16"],
				["lbl_rvar_4", "lbl_rvar_17"],
				["lbl_rvar_5", "lbl_rvar_18"],
				["lbl_rvar_6", "lbl_rvar_19"],
				["lbl_rvar_7", "lbl_rvar_20"],
				["lbl_rvar_8", "lbl_rvar_21"],
				["lbl_rvar_9", "lbl_rvar_22"],
				["lbl_rvar_10", "lbl_rvar_23"],
				["lbl_rvar_11", "lbl_rvar_24"],
				["lbl_rvar_12", "lbl_rvar_25"],]

	def __getitem__(self, item):
        	return getattr(self, item)
    	def __setitem__(self, item, value):
        	return setattr(self, item, value)
