#!/usr/bin/python

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
