#!/usr/bin/env python
# 
# Functions for communication with linuxcnc kernel
#
# Copyright (c) 2017  Maksym Kotelnikov <nemovit.mk@gmail.com>
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

import sys
import linuxcnc


try:
    c = linuxcnc.command()
    s = linuxcnc.stat() # create a connection to the status channel
    e = linuxcnc.error_channel()
except linuxcnc.error, detail:
    print "error", detail
    sys.exit(1)


####################################################
#   MAIN COMMANDS
####################################################

def check_mode():
    print("mode")

def set_auto():
    print("mode")

def set_mdi():
    print("mode")

def set_auto():
    print("mode")

def set_single_block():
    print("mode")

def make_reset():
    print("mode")

def cycle_stop():
    print("mode")

def cycle_start():
    print("mode")

def inc_1():
    print("mode")

def inc_10():
    print("mode")

def inc_100():
    print("mode")

def inc_100():
    print("mode")

def inc_10000():
    print("mode")

def inc_var():
    print("mode")

def set_repos():
    print("mode")

def set_ref_point():
    print("mode")

def set_pls_z():
    print("mode")

def set_mns_z():
    print("mode")

def set_pls_x():
    print("mode")

def set_mns_x():
    print("mode")

def set_pls_y():
    print("mode")

def set_mns_y():
    print("mode")

def rapid():
    print("mode")

def wcs_mcs():
    print("mode")

def spindle_start():
    print("mode")

def spindle_stop():
    print("mode")

def feed_start():
    print("mode")

def feed_stop():
    print("mode")

def set_spindlerate():
    print("mode")

def set_feedrate():
    print("mode")

def keyswitch_on():
    print("mode")

def keyswitch_off():
    print("mode")

def estop_press():
    print("mode")

def estop_release():
    print("mode")




####################################################
#   End of MAIN COMMANDS Section
####################################################

# Stat


#    s.poll() # get current values
#for x in dir(s):
#    if not x.startswith('_'):
#        print x, getattr(s,x)

## Error

#error = e.poll()
#if error:
#    kind, text = error
#    if kind in (linuxcnc.NML_ERROR, linuxcnc.OPERATOR_ERROR):
#        typus = "error"
#    else:
#        typus = "info"
#        print typus, text




#if ok_for_mdi():
#   c.mode(linuxcnc.MODE_MDI)
#   c.wait_complete() # wait until mode switch executed
#   c.mdi("G0 X10 Y20 Z30")


####################################################
#   Connecting linuxcnc modules
####################################################



####################################################
#   Get data from linuxcnc / Update
####################################################


####################################################
#   Get errors from linuxcnc
####################################################


####################################################
#   Check mode
####################################################
# If LinuxCNC is in one of the modes given, return True
def chek_mode(m, *p):
    s.poll()
    if s.task_mode == m or s.task_mode in p: return True
    else: return False

####################################################
#   Set mode
####################################################
# If LinuxCNC is not already in the given mode, switch it to it
def set_mode(m):
    s.poll()
    if s.task_mode == m : return True
    if running(do_poll=False): return False
    c.mode(m)
    c.wait_complete()
    return True

####################################################
#   Ensure mode
####################################################
# If LinuxCNC is not already in one of the modes given, switch it to the
# first mode
def ensure_mode(m, *p):
    s.poll()
    if s.task_mode == m or s.task_mode in p: return True
    if running(do_poll=False): return False
    c.mode(m)
    c.wait_complete()
    return True

####################################################
#   Is running
####################################################
# If LinuxCNC is in RUN, return True
def running(do_poll=True):
    if do_poll: s.poll()
    return s.task_mode == linuxcnc.MODE_AUTO and s.interp_state != linuxcnc.INTERP_IDLE


####################################################
#   Manual OK
####################################################
def manual_ok(do_poll=True):
    """warning: deceptive function name.
This function returns TRUE when not running a program, i.e., when a user-
initiated action (whether an MDI command or a jog) is acceptable.
This means this function returns True when the mdi tab is visible."""
    max_number = 0
    if do_poll: s.poll()
    if s.task_state != linuxcnc.STATE_ON: return False
    return s.interp_state == linuxcnc.INTERP_IDLE or (s.task_mode == linuxcnc.MODE_MDI and s.queued_mdi_commands < max_number)



####################################################
#   ESTOP
####################################################
def estop_clicked(event=None):
        s.poll()
        if s.task_state == linuxcnc.STATE_ESTOP:
            c.state(linuxcnc.STATE_ESTOP_RESET)
        else:
            c.state(linuxcnc.STATE_ESTOP)
        c.wait_complete()
        return True

####################################################
#   ON / OFF
####################################################
def onoff_clicked(event=None):
        s.poll()
        if s.task_state == linuxcnc.STATE_ESTOP_RESET:
            c.state(linuxcnc.STATE_ON)
        else:
            c.state(linuxcnc.STATE_OFF)

####################################################
#   AUTO - Step, Run, Stop, Pause
####################################################
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def task_run(*event):
        if run_warn(): return

        global program_start_line, program_start_line_last
        program_start_line_last = program_start_line;
        ensure_mode(linuxcnc.MODE_AUTO)
        c.auto(linuxcnc.AUTO_RUN, program_start_line)
        program_start_line = 0
        t.tag_remove("ignored", "0.0", "end")
        o.set_highlight_line(None)

def task_step(*event):
        if s.task_mode != linuxcnc.MODE_AUTO or s.interp_state != linuxcnc.INTERP_IDLE:
            o.set_highlight_line(None)
            if run_warn(): return
        ensure_mode(linuxcnc.MODE_AUTO)
        c.auto(linuxcnc.AUTO_STEP)

def task_pause(*event):
        if s.task_mode != linuxcnc.MODE_AUTO or s.interp_state not in (linuxcnc.INTERP_READING, linuxcnc.INTERP_WAITING):
            return
        ensure_mode(linuxcnc.MODE_AUTO)
        c.auto(linuxcnc.AUTO_PAUSE)

def task_resume(*event):
        s.poll()
        if not s.paused:
            return
        if s.task_mode not in (linuxcnc.MODE_AUTO, linuxcnc.MODE_MDI):
            return
        ensure_mode(linuxcnc.MODE_AUTO, linuxcnc.MODE_MDI)
        c.auto(linuxcnc.AUTO_RESUME)

def task_pauseresume(*event):
        if s.task_mode not in (linuxcnc.MODE_AUTO, linuxcnc.MODE_MDI):
            return
        ensure_mode(linuxcnc.MODE_AUTO, linuxcnc.MODE_MDI)
        s.poll()
        if s.paused:
            c.auto(linuxcnc.AUTO_RESUME)
        elif s.interp_state != linuxcnc.INTERP_IDLE:
            c.auto(linuxcnc.AUTO_PAUSE)

def task_stop(*event):
        if s.task_mode == linuxcnc.MODE_AUTO and vars.running_line.get() != 0:
            o.set_highlight_line(vars.running_line.get())
        c.abort()
        c.wait_complete()


####################################################
#   PAUSE / RESUME
####################################################

####################################################
#   MDI
####################################################
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def mdi_up_cmd(*args):
        if args and args[0].char: return   # e.g., for KP_Up with numlock on
        global mdi_history_index
        if widgets.mdi_command.cget("state") == "disabled":
            return
        if mdi_history_index != -1:
            if mdi_history_index > 0:
                mdi_history_index -= 1
            else:
                mdi_history_index = widgets.mdi_history.size() - 1
            widgets.mdi_history.selection_clear(0, "end")
            widgets.mdi_history.see(mdi_history_index)
            if mdi_history_index != (widgets.mdi_history.size() - 1):
                widgets.mdi_history.selection_set(mdi_history_index, mdi_history_index)
            vars.mdi_command.set(widgets.mdi_history.get(mdi_history_index))
            widgets.mdi_command.selection_range(0, "end")

def mdi_down_cmd(*args):
        if args and args[0].char: return   # e.g., for KP_Up with numlock on
        global mdi_history_index
        if widgets.mdi_command.cget("state") == "disabled":
            return
        history_size = widgets.mdi_history.size()
        if mdi_history_index != -1:
            if mdi_history_index < (history_size - 1):
                mdi_history_index += 1
            else:
                mdi_history_index = 0
            widgets.mdi_history.selection_clear(0, "end")
            widgets.mdi_history.see(mdi_history_index)
            if mdi_history_index != (widgets.mdi_history.size() - 1):
                widgets.mdi_history.selection_set(mdi_history_index, mdi_history_index)
            vars.mdi_command.set(widgets.mdi_history.get(mdi_history_index))
            widgets.mdi_command.selection_range(0, "end")

def send_mdi(*event):
        if not manual_ok(): return "break"
        command = vars.mdi_command.get()
        commands.send_mdi_command(command)
        return "break"

def send_mdi_command(command):
        global mdi_history_index, mdi_history_save_filename
        if command != "":
            command= command.lstrip().rstrip()
            vars.mdi_command.set("")
            ensure_mode(linuxcnc.MODE_MDI)
            widgets.mdi_history.selection_clear(0, "end")
            ## check if input is already in list. If so, then delete old element
            #idx = 0
            #for ele in widgets.mdi_history.get(0, "end"):
            #    if ele == command:
            #        widgets.mdi_history.delete(idx)
            #        break
            #    idx += 1
            history_size = widgets.mdi_history.size()
            new_entry = 1
            if history_size > 1 and widgets.mdi_history.get(history_size - 2) == command:
                new_entry = 0
            if new_entry != 0:
                # if command is already at end of list, don't add it again
                widgets.mdi_history.insert(history_size - 1, "%s" % command)
                history_size += 1
            widgets.mdi_history.see(history_size - 1)
            if history_size > (mdi_history_max_entries + 1):
                widgets.mdi_history.delete(0, 0)
                history_size= (mdi_history_max_entries + 1)
            # pdb.set_trace()
            mdi_history_index = widgets.mdi_history.index("end") - 1
            c.mdi(command)
            o.tkRedraw()
            commands.mdi_history_write_to_file(mdi_history_save_filename, history_size)

def ok_for_mdi():
    s.poll()
    return not s.estop and s.enabled and s.homed and (s.interp_state == linuxcnc.INTERP_IDLE)
####################################################
#   JOG
####################################################
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def from_internal_linear_unit(v, unit=None):
    if unit is None:
        unit = s.linear_units
    lu = (unit or 1) * 25.4
    return v*lu

# returns units/sec
def get_jog_speed(a):
#    if vars.joint_mode.get():
#        # World Mode
#        if a in (0,1,2,6,7,8): # XYZUVW
#            speed = vars.jog_speed.get()/60. 
#        else: # ABC
#            speed = vars.jog_aspeed.get()/60.  
#    else:
        # Joint Mode
        ini_joint = "JOINT_%d" % a
        jnt_type = inifile.find(ini_joint, "TYPE")
        if (jnt_type == "LINEAR"):
             speed = 50
#            speed = vars.jog_speed.get()/60.
        elif (inifile.find(ini_joint, "TYPE") == "ANGULAR"):
#            speed = vars.jog_aspeed.get()/60.
             speed = 50
        else:
            print >>sys.stderr, "Unknown %s.TYPE" % ini_joint
            speed = 0.
    # print >>sys.stderr, "DEBUG: get_jog_speed(): j[%d] speed(%f), jog_speed(%f) jog_aspeed(%f)" \
    #                     % (a, speed, vars.jog_speed.get(),  vars.jog_aspeed.get())
        return speed
    
def get_max_jog_speed(a):
    if vars.joint_mode.get():
        # World Mode
        if a in (0,1,2,6,7,8): # XYZUVW
            speed = vars.max_speed.get()    # unit/sec
        else: # ABC
            speed = vars.max_aspeed.get()   # unit/sec
    else:
        # Joint Mode
        ini_joint = "JOINT_%d" % a
        jnt_type = inifile.find(ini_joint, "TYPE")
        if (jnt_type == "LINEAR"):
            speed = vars.max_speed.get()    # unit/sec
        elif (inifile.find(ini_joint, "TYPE") == "ANGULAR"):
            speed = vars.max_aspeed.get()   # unit/sec
        else:
            print >>sys.stderr, "Unknown %s.TYPE" % ini_joint
            speed = 0.
    return speed


def jog(*args):
#    if not manual_ok(): return
    if not chek_mode(linuxcnc.MODE_MANUAL): return
#    if not manual_tab_visible(): return
#    ensure_mode(linuxcnc.MODE_MANUAL)
    c.jog(*args)

# function extract from TCL command
def jog_plus(axis, incr=False):
#    a = vars.current_axis.get()
    if isinstance(a, (str, unicode)):
        a = "xyzabcuvws".index(a)
    speed = get_jog_speed(a)
    jog_on(a, speed)

def jog_minus(axis, incr=False):
#    a = vars.current_axis.get()
    if isinstance(a, (str, unicode)):
        a = "xyzabcuvws".index(a)
    speed = get_jog_speed(a)
    jog_on(a, -speed)

def jog_stop(event=None):
    jog_off(vars.current_axis.get())

# XXX correct for machines with more than six axes
jog_after = [None] * 9
jog_cont  = [False] * 9
jogging   = [0] * 9
def jog_on(a, b):
    if not manual_ok(): return
#    if not manual_tab_visible(): return
    if isinstance(a, (str, unicode)):
        a = "xyzabcuvws".index(a)
    if a < 3:
#        if vars.metric.get(): b = b / 25.4
        b = b / 25.4
        b = from_internal_linear_unit(b)
    if jog_after[a]:
        root_window.after_cancel(jog_after[a])
        jog_after[a] = None
        return
    b = b*vars.feedrate.get()/100.0
    jogincr = widgets.jogincr.get()
    if s.motion_mode == linuxcnc.TRAJ_MODE_TELEOP:
        if jogincr != _("Continuous"):
            jogging[a] = 0
            print "WARNING: do not allow incremental jogging in TELEOP mode"
        else:
            jogging[a] = b
        jog_cont[a] = True
        cartesian_only=jogging[:6]
        c.teleop_vector(*cartesian_only)
    else:
        if jogincr != _("Continuous"):
            s.poll()
            if s.state != 1: return
            distance = parse_increment(jogincr)
            jog(linuxcnc.JOG_INCREMENT, a, b, distance)
            jog_cont[a] = False
        else:
            jog(linuxcnc.JOG_CONTINUOUS, a, b)
            jog_cont[a] = True
            jogging[a] = b

def jog_off(a):
    if isinstance(a, (str, unicode)):
        a = "xyzabcuvws".index(a)
    if jog_after[a]: return
    jog_after[a] = root_window.after_idle(lambda: jog_off_actual(a))

def jog_off_actual(a):
    if not manual_ok(): return
    activate_axis(a)
    jog_after[a] = None
    jogging[a] = 0
    if s.motion_mode == linuxcnc.TRAJ_MODE_TELEOP:
        cartesian_only=jogging[:6]
        c.teleop_vector(*cartesian_only)
    else:
        if jog_cont[a]:
            jog(linuxcnc.JOG_STOP, a)

def jog_off_all():
    for i in range(6):
        if jogging[i]:
            jog_off_actual(i)



####################################################
#   Shpindle
####################################################
def spindle(event=None):
#        if not manual_ok(): return
#        ensure_mode(linuxcnc.MODE_MANUAL)
        c.spindle(event)


def spindle_forward_toggle(*args):
        if not manual_ok(): return
        s.poll()
        if s.spindle_direction == 0:
            c.spindle(1)
        else:
            c.spindle(0)

def spindle_backward_toggle(*args):
        if not manual_ok(): return "break"
        s.poll()
        if s.spindle_direction == 0:
            c.spindle(-1)
        else:
            c.spindle(0)
        return "break" # bound to F10, don't activate menu


def spindle_increase(event=None):
        if not manual_ok(): return
        ensure_mode(linuxcnc.MODE_MANUAL)
        c.spindle(linuxcnc.SPINDLE_INCREASE)
def spindle_decrease(event=None):
        if not manual_ok(): return
        ensure_mode(linuxcnc.MODE_MANUAL)
        c.spindle(linuxcnc.SPINDLE_DECREASE)

def spindle_constant(event=None):
        if not manual_ok(): return
        ensure_mode(linuxcnc.MODE_MANUAL)
        c.spindle(linuxcnc.SPINDLE_CONSTANT)

####################################################
#   Set shpindle rate
def set_spindlerate(newval):
        global spindlerate_blackout
        try:
            value = int(newval)
        except ValueError: return
        value = value / 100.
        c.spindleoverride(value)
        spindlerate_blackout = time.time() + 1

####################################################
#   Feed
####################################################

####################################################
#   Set feed rate
def set_feedrate(newval):
        global feedrate_blackout
        try:
            value = int(newval)
        except ValueError: return
        value = value / 100.
        c.feedrate(value)
        feedrate_blackout = time.time() + 1


####################################################
#   Update tool table
####################################################



####################################################
#   HOME
####################################################

def home_all_axes(event=None):
        if not manual_ok(): return
        ensure_mode(linuxcnc.MODE_MANUAL)
        isHomed=True
        for i,h in enumerate(s.homed):
            if s.axis_mask & (1<<i):
                isHomed=isHomed and h
        doHoming=True
        if isHomed:
            doHoming=prompt_areyousure(_("Warning"),_("Axis is already homed, are you sure you want to re-home?"))
        if doHoming:
            c.home(-1)

def unhome_all_axes(event=None):
        if not manual_ok(): return
        ensure_mode(linuxcnc.MODE_MANUAL)
        c.unhome(-1)

def home_axis(axisName):
        if not manual_ok(): return
        doHoming=True
        if s.homed["xyzabcuvws".index(axisName)]:
            doHoming=prompt_areyousure(_("Warning"),_("This axis is already homed, are you sure you want to re-home?"))
        if doHoming:
            ensure_mode(linuxcnc.MODE_MANUAL)
            c.home("xyzabcuvws".index(axisName))

def unhome_axis(axisName):
        if not manual_ok(): return
        ensure_mode(linuxcnc.MODE_MANUAL)
        c.unhome("xyzabcuvws".index(axisName))

def home_axis_number(num):
        ensure_mode(linuxcnc.MODE_MANUAL)
        c.home(num)

def unhome_axis_number(num):
        ensure_mode(linuxcnc.MODE_MANUAL)
        c.unhome(num)

####################################################
#   OFFSET
####################################################


def clear_offset(num):
        ensure_mode(linuxcnc.MODE_MDI)
        s.poll()
        if num == "G92":
            clear_command = "G92.1"
        else:
            clear_command = "G10 L2 P%c R0" % num
            for i, a in enumerate("XYZABCUVW"):
                if s.axis_mask & (1<<i): clear_command += " %c0" % a
        c.mdi(clear_command)
        c.wait_complete()
        ensure_mode(linuxcnc.MODE_MANUAL)
        s.poll()
        o.tkRedraw()
        reload_file(False)

def touch_off(event=None, new_axis_value = None):
        global system
        if not manual_ok(): return
        if joints_mode(): return
        offset_axis = "xyzabcuvws".index(vars.current_axis.get())
        if new_axis_value is None:
            new_axis_value, system = prompt_touchoff(_("Touch Off"),
                _("Enter %s coordinate relative to %%s:")
                        % vars.current_axis.get().upper(), 0.0, vars.touch_off_system.get())
        else:
            system = vars.touch_off_system.get()
        if new_axis_value is None: return
        vars.touch_off_system.set(system)
        ensure_mode(linuxcnc.MODE_MDI)
        s.poll()

        linear_axis = vars.current_axis.get() in "xyzuvw"
        if linear_axis and vars.metric.get(): scale = 1/25.4
        else: scale = 1

        if linear_axis and 210 in s.gcodes:
            scale *= 25.4

        if system.split()[0] == "T":
            lnum = 10 + vars.tto_g11.get()
            offset_command = "G10 L%d P%d %c[%s*%.12f]" % (lnum, s.tool_in_spindle, vars.current_axis.get(), new_axis_value, scale)
            c.mdi(offset_command)
            c.wait_complete()
            c.mdi("G43")
            c.wait_complete()
        else:
            offset_command = "G10 L20 %s %c[%s*%.12f]" % (system.split()[0], vars.current_axis.get(), new_axis_value, scale)
            c.mdi(offset_command)
            c.wait_complete()

        ensure_mode(linuxcnc.MODE_MANUAL)
        s.poll()
        o.tkRedraw()
        reload_file(False)

def set_axis_offset(event=None):
        commands.touch_off(new_axis_value=0.)


def toggle_override_limits(*args):
        s.poll()
        if s.interp_state != linuxcnc.INTERP_IDLE: return
        if s.joint[0]['override_limits']:
            ensure_mode(linuxcnc.MODE_AUTO)
        else:
            ensure_mode(linuxcnc.MODE_MANUAL)
            c.override_limits()


####################################################
#   Brake
####################################################
def brake(event=None):
        if not manual_ok(): return
        ensure_mode(linuxcnc.MODE_MANUAL)
        c.brake(event)


def brake_on(*args):
        if not manual_ok(): return
        c.brake(1)
def brake_off(*args):
        if not manual_ok(): return
        c.brake(0)
####################################################
#   Flood
####################################################
def flood(event=None):
        if not manual_ok(): return
        ensure_mode(linuxcnc.MODE_MANUAL)
        c.flood(event)

def flood_toggle(*args):
        if not manual_ok(): return
        s.poll()
        c.flood(not s.flood)
####################################################
#   Mist
####################################################
def mist(event=None):
        if not manual_ok(): return
        ensure_mode(linuxcnc.MODE_MANUAL)
        c.mist(event)

def mist_toggle(*args):
        if not manual_ok(): return
        s.poll()
        c.mist(not s.mist)







#def update(self):
#        if not self.running.get():
#            return
#        try:
#            self.stat.poll()
#        except linuxcnc.error, detail:
#            print "error", detail
#            del self.stat
#            return
#        self.after = self.win.after(update_ms, self.update)

#        self.win.set_current_line(self.stat.id or self.stat.motion_line)

#        speed = self.stat.current_vel

#        limits = soft_limits()

#        if (self.logger.npts != self.lastpts
#                or limits != o.last_limits
#                or self.stat.actual_position != o.last_position
#                or self.stat.joint_actual_position != o.last_joint_position
#                or self.stat.homed != o.last_homed
#                or self.stat.g5x_offset != o.last_g5x_offset
#                or self.stat.g92_offset != o.last_g92_offset
#                or self.stat.g5x_index != o.last_g5x_index
#                or self.stat.rotation_xy != o.last_rotation_xy
#                or self.stat.limit != o.last_limit
#                or self.stat.tool_table[0] != o.last_tool
#                or self.stat.motion_mode != o.last_motion_mode
#                or abs(speed - self.last_speed) > .01):
#            o.redraw_soon()
#            o.last_limits = limits
#            o.last_limit = self.stat.limit
#            o.last_homed = self.stat.homed
#            o.last_position = self.stat.actual_position
#            o.last_g5x_offset = self.stat.g5x_offset
#            o.last_g92_offset = self.stat.g92_offset
#            o.last_g5x_index = self.stat.g5x_index
#            o.last_rotation_xy = self.stat.rotation_xy
#            o.last_motion_mode = self.stat.motion_mode
#            o.last_tool = self.stat.tool_table[0]
#            o.last_joint_position = self.stat.joint_actual_position
#            self.last_speed = speed
#            self.lastpts = self.logger.npts

#        root_window.update_idletasks()
#        vupdate(vars.exec_state, self.stat.exec_state)
#        vupdate(vars.interp_state, self.stat.interp_state)
#        vupdate(vars.queued_mdi_commands, self.stat.queued_mdi_commands)
#        if hal_present == 1 :
#            set_manual_mode = comp["set-manual-mode"]
#            if self.set_manual_mode != set_manual_mode:
#                 self.set_manual_mode = set_manual_mode
#                 if self.set_manual_mode:
#                     root_window.tk.eval(pane_top + ".tabs raise manual")
#            notifications_clear = comp["notifications-clear"]
#            if self.notifications_clear != notifications_clear:
#                 self.notifications_clear = notifications_clear
#                 if self.notifications_clear:
#                     notifications.clear()
#            notifications_clear_info = comp["notifications-clear-info"]
#            if self.notifications_clear_info != notifications_clear_info:
#                 self.notifications_clear_info = notifications_clear_info
#                 if self.notifications_clear_info:
#                     notifications.clear("info")
#            notifications_clear_error = comp["notifications-clear-error"]
#            if self.notifications_clear_error != notifications_clear_error:
#                 self.notifications_clear_error = notifications_clear_error
#                 if self.notifications_clear_error:
#                     notifications.clear("error")
#        vupdate(vars.task_mode, self.stat.task_mode)
#        vupdate(vars.task_state, self.stat.task_state)
#        vupdate(vars.task_paused, self.stat.task_paused)
#        vupdate(vars.taskfile, self.stat.file)
#        vupdate(vars.interp_pause, self.stat.paused)
#        vupdate(vars.mist, self.stat.mist)
#        vupdate(vars.flood, self.stat.flood)
#        vupdate(vars.brake, self.stat.spindle_brake)
#        vupdate(vars.spindledir, self.stat.spindle_direction)
#        vupdate(vars.motion_mode, self.stat.motion_mode)
#        vupdate(vars.optional_stop, self.stat.optional_stop)
#        vupdate(vars.block_delete, self.stat.block_delete)
#        if time.time() > spindlerate_blackout:
#            vupdate(vars.spindlerate, int(100 * self.stat.spindlerate + .5))
#        if time.time() > feedrate_blackout:
#            vupdate(vars.feedrate, int(100 * self.stat.feedrate + .5))
#        if time.time() > maxvel_blackout:
#            m = to_internal_linear_unit(self.stat.max_velocity)
#            if vars.metric.get(): m = m * 25.4
#            vupdate(vars.maxvel_speed, float(int(600 * m)/10.0))
#            root_window.tk.call("update_maxvel_slider")
#        vupdate(vars.override_limits, self.stat.joint[0]['override_limits'])
#        on_any_limit = 0
#        for l in self.stat.limit:
#            if l:
#                on_any_limit = True
#                break
#        vupdate(vars.on_any_limit, on_any_limit)
#        global current_tool
#        current_tool = self.stat.tool_table[0]
#        if current_tool:
#            tool_data = {'tool': current_tool[0], 'zo': current_tool[3], 'xo': current_tool[1], 'dia': current_tool[10]}
#        if current_tool is None:
#            vupdate(vars.tool, _("Unknown tool %d") % self.stat.tool_in_spindle)
#        elif tool_data['tool'] == 0 or tool_data['tool'] == -1:
#            vupdate(vars.tool, _("No tool"))
#        elif current_tool.xoffset == 0 and not lathe:
#            vupdate(vars.tool, _("Tool %(tool)d, offset %(zo)g, diameter %(dia)g") % tool_data)
#        else:
#            vupdate(vars.tool, _("Tool %(tool)d, zo %(zo)g, xo %(xo)g, dia %(dia)g") % tool_data)
#        active_codes = []
#        for i in self.stat.gcodes[1:]:
#            if i == -1: continue
#            if i % 10 == 0:
#                active_codes.append("G%d" % (i/10))
#            else:
#                active_codes.append("G%(ones)d.%(tenths)d" % {'ones': i/10, 'tenths': i%10})

#        for i in self.stat.mcodes[1:]:
#            if i == -1: continue
#            active_codes.append("M%d" % i)

#        feed_str = "F%.1f" % self.stat.settings[1]
#        if feed_str.endswith(".0"): feed_str = feed_str[:-2]
#        active_codes.append(feed_str)
#        active_codes.append("S%.0f" % self.stat.settings[2])

#        codes = " ".join(active_codes)
#        widgets.code_text.configure(state="normal")
#        widgets.code_text.delete("0.0", "end")
#        widgets.code_text.insert("end", codes)
#        widgets.code_text.configure(state="disabled")

#        user_live_update()






def set_maxvel(newval):
        newval = float(newval)
        if vars.metric.get(): newval = newval / 25.4
        newval = from_internal_linear_unit(newval)
        global maxvel_blackout
        c.maxvel(newval / 60.)
        maxvel_blackout = time.time() + 1

def reload_tool_table(*args):
        c.load_tool_table()


def set_first_line(lineno):
        if not manual_ok(): return
        set_first_line(lineno)

## mouse wheel deferred functions

#def wheel_up_deferred():
#    global recentUp , is_wheel_up
#    jog_plus()
#    while recentUp==1:
#        recentUp = 0
#        time.sleep(0.1)
#    jog_stop()
#    is_wheel_up=0
#    return
#    

#def wheel_down_deferred():
#    global recentDown, is_wheel_down
#    jog_minus()
#    while recentDown==1:
#        recentDown = 0
#        time.sleep(0.1)
#    jog_stop()
#    is_wheel_down=0
#    return


#while s.joints == 0:
#    print "waiting for s.joints"
#    time.sleep(.01)
#    statfail+=1
#    statwait *= 2
#    if statfail > 8:
#        raise SystemExit, (
#            "A configuration error is preventing LinuxCNC from starting.\n"
#            "More information may be available when running from a terminal.")
#s.poll()

