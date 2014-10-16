### CHIME Feed-Delay Calculator
# NTD
# input: source alt and az, feed layout and cable delays
# output: grid of the delays required to beamform

### Import statements
import sys
import numpy as np

### Constants 
# CHIME rotation from celestial north - in radians, clockwise from above
chime_offset_clockwise = 0*(np.pi/180.)
# inverse of speed of light - in nanoseconds per meter
one_over_c = 3.3356
# Location of file containing feed positions in [x]\t[y]\n format, in m
feed_config_file = "/home/qingtang/pulsar/feed_loc_layout27.txt"
# Location of file containing cable delays in [t]\n format, in ns
cable_delay_file = "/home/denman/chime_proc/chime_cable_delays.dat"

if len(sys.argv) != 3:
    print "Usage: python delay_calculator.py SOURCE_ALT SOURCE_AZ"

else:
    source_alt = float(sys.argv[1])*np.pi/180.
    source_az  = float(sys.argv[2])*np.pi/180.
    # assuming input in degrees, convert to radians for ease of use

    # calculate the east-west and north-south angles (from zenith)
    geom_delay_east  = (0.5*np.pi - source_alt)*np.sin(source_az+chime_offset_clockwise)
    geom_delay_north = (0.5*np.pi - source_alt)*np.cos(source_az+chime_offset_clockwise)

    # read feed data from appropriate config files
    feed_positions = np.loadtxt(feed_config_file)
    cable_delays = np.loadtxt(cable_delay_file)

    #NOTE: We assume here that all files list the feeds in the same order

    # Calculate projected seperations for each feed
    #   Convert to a delay in time (microsec? nanosec?) 

    feed_delays = []

    for i in range(len(feed_positions)):
        temp_ew = feed_positions[i][0]*np.sin(geom_delay_east)
        temp_ns = feed_positions[i][1]*np.sin(geom_delay_north)
        feed_delays.append(np.sqrt(temp_ew*temp_ew + temp_ns*temp_ns)*one_over_c + cable_delays[i])

    print feed_delays
