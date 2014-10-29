### CHIME Fake Baseband Data Generator
# NTD
# input: list of the delay times
# output: packet-formatted baseband data



### Import statements
import numpy as np
import sys
import random
import scipy.misc

### Constants 

# location of delay file
delay_file = "example_delays.dat"

# location of baseband packet file
baseband_data_file = "./corr_data/fake_data.dat"

# constants related to file and packet structure
header_length_bytes = 58
packet_size_bytes   = 9296
frames_per_packet   = 4
frame_length        = 2048
footer_length_bytes = packet_size_bytes-(header_length_bytes+frames_per_packet*frame_length)
n_elements          = 16
n_frequencies       = 128
packets_in_file     = 64*1024

# frequency information
max_freqency_ghz = 0.8
min_freqency_ghz = 0.4
frequency_array = np.linspace(min_freqency_ghz, max_freqency_ghz, n_frequencies)
    # if frequencies reversed, swap start/stop

# signal-to-noise of the 'pulsar' signal
snr = 3




### TEST CHANGES ###
packets_in_file = 40
snr = 5
####################



### Main Program
if len(sys.argv) != 1:
    sys.exit("Usage: python fake_data_gen.py")

random.seed()

# read in the delay times
delay_times = np.loadtxt(delay_file)
# ensure that units are consistent - currently in nanoseconds


#generate the baseband data using the phase-delays
# for given timestep, element, freq, value should be noise + signal*phase
im_data=np.asarray([])
temp_data = bytearray()
for i in range(packets_in_file):
    temp_data.extend([0]*header_length_bytes)
    for k in range(frames_per_packet):
        for h in range(n_elements):
            for l in frequency_array:
                temp = 8*complex(2*random.random()-1,2*random.random()-1)
                temp += (k/3)*snr*np.exp(1.0j*2*np.pi*delay_times[h]*l)
                temp = np.round(temp)
                imag_part = int(min(max(0, temp.imag+8), 15))
                real_part = int(min(max(0, temp.real+8), 15))
                temp_data.append(16*real_part+imag_part)
                im_data = np.append(im_data, 1.j*(imag_part-8)+(real_part-8))
    temp_data.extend([0]*footer_length_bytes)

# write out the data to a file
data_file = open(baseband_data_file, "wb")
data_file.write(temp_data)
data_file.close()









#data_file = open(baseband_data_file, "rb")
#raw_baseband_data=[]
#for i in range(packets_in_file):
#    data_file.seek(i*frame_length*frames_per_packet,0)
#    for k in range(frames_per_packet):
#        read_data = np.fromstring(data_file.read(frame_length),dtype=np.uint8)
#        data_real = ((read_data >> 4).astype(np.int32) - 8)
#        data_imag = ((read_data & 0xf).astype(np.int32) - 8)
#        data_complex = data_real + 1.0j*data_imag
#        del data_real, data_imag
#        raw_baseband_data.append(data_complex)

#data_file.close()
#raw_baseband_data=np.asarray(raw_baseband_data).reshape(8*2048)
#print raw_baseband_data[:100]
