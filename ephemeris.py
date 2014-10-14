#Ephemeris double-checker for CHIME
#NTD
#input: Source RA and DEC and the exact time to begin simulating
#output: the alt and az of the object
    #may include time-evolution and therefore need a timestamp.


# Import Statements
import sys
import numpy as np

# CHIME parameters
CHI_lat  = 49.32
CHI_long = -119.62



##### Test Changes #####
CHI_lat  = 45
CHI_long = -120
########################



# Parameters of the output - move to insertion via CLI later on
delta_t = 1.e-2 #The time resolution of the output, in decimal hours
sim_time = 1 #Total time to simulate after the initial

if len(sys.argv) != 4:
    print "Usage: python ephemeris.py SOURCE_RA SOURCE_DEC TIME_UTC"

# We assume: RA in decimal hours, DEC in decimal degrees. May convert if needed

else:
    source_ra =  sys.argv[1]
    source_dec = sys.argv[2]
    time_start = sys.argv[3]

    for i in np.linspace(0, sim_time, sim_time/delta_t):
        time_now = time_start + i
        #do calc.   
        print str(i)
