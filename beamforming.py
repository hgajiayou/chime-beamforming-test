### CHIME Test Beamformer
# NTD
# input: list of the delays required to beamform, baseband data file
# output: sum of phase-delayed timestreams



### Import statements
import numpy as np
import sys



### Constants 

# location of delay file
delay_file = "example_delays.dat"

# location of baseband packet file
baseband_data_file = "/mnt/CHIMEdata/baseband_data/B0329/1000.dat"

# save location for output files
output_file = "./corr_data/beamformed-result.dat"

# constants related to file and packet structure
header_length_bytes = 58
packet_size_bytes   = 9296
frames_per_packet   = 4
frame_length        = 2048
n_elements          = 16
n_frequencies       = 128
packets_in_file     = 64*1024

# frequency information
max_freqency_ghz = 0.8
min_freqency_ghz = 0.4
frequency_array = np.linspace(min_freqency_ghz, max_freqency_ghz, n_frequencies)
    # if frequencies reversed, swap start/stop


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
# shape of data cube is (timestep, element, frequency)

data_file = open(baseband_data_file, "rb")

# read in data from the baseband packet files
for i in range(packets_in_file):
    data_file.seek(i*packet_size_bytes + header_length_bytes, 0)
    for k in range(frames_per_packet):
        read_data = np.fromstring(data_file.read(frame_length),dtype=np.uint8)
        data_real = ((read_data >> 4).astype(np.int32) - 8)
        data_imag = ((read_data & 0xf).astype(np.int32) - 8)
        data_complex = data_real + 1.0j*data_imag
        del data_real, data_imag
        data_complex = data_complex.reshape((n_elements, n_frequencies), order='F')
        raw_baseband_data.append(data_complex)

delay_phases = delay_times*2*np.pi
# to convert to true delay, multiply by (frequency / 1GHz) - so 0.4 through 0.8

beamformed_data = []

for i in range(packets_in_file*frames_per_packet): #for each timestep
    beamformed_data.append([])
    for k in range(n_frequencies): #for each frequency
        summed_beam = 0.
        for l in range(n_elements): #for each element
            phase=-1.0j*delay_phases[l]*frequency_array[k]
            summed_beam +=  raw_baseband_data[i][l][k]*np.exp(phase)
        beamformed_data[i].append(summed_beam)

np.savetxt(output_file, beamformed_data, fmt = '%s\t'*n_frequencies)
