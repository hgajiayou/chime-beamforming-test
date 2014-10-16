### Ephemeris double-checker for CHIME ###
# NTD
# input: Source RA and DEC and the exact time to begin simulating
# output: the alt and az of the object
    # may include time-evolution and therefore need a timestamp.

### Import Statements
import sys
import numpy as np
from datetime import *
from dateutil.tz import tzutc, tzlocal

### CHIME parameters
CHI_lat  = 49.32
CHI_long = -119.62

##### Test Changes #####
CHI_lat  = 45
CHI_long = -120
########################

### Parameters of the output - move to insertion via CLI later on
delta_t = 1.e-2 #The time resolution of the output, in decimal hours
sim_time = 1 #Total time to simulate after the supplied start time, in hours

if len(sys.argv) != 4:
    print "Usage: python ephemeris.py SOURCE_RA SOURCE_DEC TIME_[YYYY][MM][DD]T[HH][MM][SS]Z"

# We assume: RA in decimal hours, DEC in decimal degrees. May convert if needed

### Conversions involving ISO-formatted UTC:
# 2013 11 18 T 01 41 27 Z
# YYYY MM DD   HH MM SS

else:
    source_ra  = float(sys.argv[1])
    source_dec = float(sys.argv[2])
    time_start = sys.argv[3]

    # setting the time constants
    time_J2000_epoch = datetime(2000, 01, 01, 11, 58, 55, 816000, tzinfo=tzutc()) 
    time_per_step = timedelta(0,3600*delta_t)

    # converts input time to the datetime object
    time_current = datetime(int(time_start[:4]),int(time_start[4:6]),int(time_start[6:8]),int(time_start[9:11]),int(time_start[11:13]),int(time_start[13:15]),0,tzinfo=tzutc())

    for i in np.linspace(0, sim_time, sim_time/delta_t):

        alt = 0
        az  = 0

        #Get days since the J2000.0 epoch //(UT - offset)/some factor?
        #Calculate LST from base+_d_+UT, then % to [0,360] in degrees
        #Calc. hour angle = LST-RA, then % to [0,360] in degrees (only concern is <0)
        # Then, nasty trig:
            #sin(ALT) = sin(DEC)*sin(LAT)+cos(DEC)*cos(LAT)*cos(HA)
            #cos(AZ) = (sin(DEC) - sin(ALT)*sin(LAT))/(cos(ALT)*cos(LAT))
        # Reverse trig, output.

        tc=time_current
        print str(tc.year).zfill(4)+str(tc.month).zfill(2)+str(tc.day).zfill(2)+"T"+str(tc.hour).zfill(2)+str(tc.minute).zfill(2)+str(tc.second).zfill(2)+"Z,"+ str(i) +","+ str(alt) +","+ str(az)

        time_current += time_per_step
