### CHIME Test Beamformer
# NTD
# input: list of the delays required to beamform, baseband data file
# output: visibilities from correlation of delayed timestreams


### Import statements
import numpy as np
import sys

### Constants 

# location of delay file
delay_file = "example_delays.dat"

# location of baseband packet file
baseband_data_file = ""

# save location for output files
output_prefix = "./corr_data/correlated-visibility-"
output_suffix = ".dat"

# constants related to packet structure
header_length_bytes = 58
data_size_bytes     = 8192
packet_size_bytes   = 9296
frames_per_packet   = 4
frame_length        = 2048

# constants related to baseband file structure
packets_in_file = 64*1024

# constants related to the CHIME layout 
n_elements = 16


### Main Program
if len(sys.argv) != 1:
    sys.exit("Usage: python beamforming.py")

# read in list of delay times
#   ensure that units are consistent

# read in data from the baseband packet files

# apply the delays in terms of time-steps (units of 1/800MHz)
#   interpolate? round? do some n-step function?

# correlate the delayed timestreams to generate visibilities

# output "[r]\t[i]\t[mag]\t[phase]" for each visibility
