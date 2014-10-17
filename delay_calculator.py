### CHIME Feed-Delay Calculator
# NTD
# input: source alt and az, feed layout and cable delay files
# output: list of the delays required to beamform

### Import statements
import sys
import numpy as np

### Constants 

# CHIME rotation from celestial north - in radians, clockwise from above
chime_offset_clockwise = 0*(np.pi/180.)

# inverse of speed of light - in nanoseconds per meter
one_over_c = 3.3356

# Location of file containing feed positions in [x]\t[y]\n format, in m
feed_config_file = "/home/denman/chime_proc/chime_layout_8ch_old.dat"

# Location of file containing cable delays in [t]\n format, in ns
cable_delay_file = "/home/denman/chime_proc/chime_cable_delays.dat"

### TEST CHANGES ###
#feed_config_file = "test_grid.dat"
####################

if len(sys.argv) != 3:
    print "Usage: python delay_calculator.py SOURCE_ALT SOURCE_AZ"

else:
    source_alt = float(sys.argv[1])*np.pi/180.
    source_az  = float(sys.argv[2])*np.pi/180.
    # assuming input in degrees, convert to radians for ease of use

    alt_correction_term = np.cos(source_alt)

    # read feed data from appropriate config files
    feed_positions = np.loadtxt(feed_config_file)
    cable_delays = np.loadtxt(cable_delay_file)
    feed_delays = []

    #NOTE: We assume here that all files list the feeds in the same order

    for i in range(len(feed_positions)):
        projection_angle = np.arctan2(feed_positions[i][1],feed_positions[i][0])
        offset_distance  = alt_correction_term*np.sqrt(feed_positions[i][0]*feed_positions[i][0] + feed_positions[i][1]*feed_positions[i][1])
        effective_angle  = projection_angle - (source_az - chime_offset_clockwise)

        feed_delays.append(np.sin(effective_angle)*offset_distance*one_over_c + cable_delays[i]) 
        print feed_delays[i]
