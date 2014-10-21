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
baseband_data_file = "/mnt/CHIMEdata/baseband_data/B0329/1000.dat"

# save location for output files
output_prefix = "./corr_data/correlated-visibility-"
output_suffix = ".dat"

# constants related to file and packet structure
header_length_bytes = 58
data_size_bytes     = 8192
packet_size_bytes   = 9296
footer_size_bytes   = packet_size_bytes - (data_size_bytes + header_length_bytes)
frames_per_packet   = 4
frame_length        = 2048
n_elements          = 16
n_frequencies       = 128
packets_in_file     = 64*1024

# length of the timestep for each frame, in nanosec
timestep_in_ns = 1024*(1/800.E6)*1.E9

### TEST CHANGES ###
packets_in_file = 10
####################

### Main Program
if len(sys.argv) != 1:
    sys.exit("Usage: python beamforming.py")

# read in the delay times
delay_times = np.loadtxt(delay_file)
# ensure that units are consistent - currently in nanoseconds

raw_baseband_data = []
# shape of data cube -> (timestep, element, frequency)

data_file = open(baseband_data_file, "rb")

# read in data from the baseband packet files
for i in range(packets_in_file):
    data_file.seek(i*packet_size_bytes + header_length_bytes, 0)
    for j in range(frames_per_packet):
        read_data = np.fromstring(data_file.read(frame_length),dtype=np.uint8)
        data_real = ((read_data >> 4).astype(np.int32) - 8)
        data_imag = ((read_data & 0xf).astype(np.int32) - 8)
        data_complex = data_real + 1.0j*data_imag
        del data_real, data_imag
        data_complex = data_complex.reshape((n_elements, n_frequencies), order='F')
        raw_baseband_data.append(data_complex)

print len(raw_baseband_data)
print len(raw_baseband_data[0])
print len(raw_baseband_data[0][0])

#print raw_baseband_data

# apply the delays in terms of time-steps (units of 1/800MHz)
#   interpolate? round? do some n-step function?

# correlate the delayed timestreams to generate visibilities

# output "[r]\t[i]\t[mag]\t[phase]" for each visibility
