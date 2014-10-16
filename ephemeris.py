### Ephemeris double-checker for CHIME
# NTD
# input: Source RA and DEC and the exact time to begin simulating
# output: the alt and az of the object

### Import statements
import sys
import numpy as np
from datetime import *
from dateutil.tz import tzutc, tzlocal

### CHIME parameters
CHI_lat  = 49.32
CHI_long = -119.62

##### Test Changes #####
#CHI_lat  = 49
#CHI_long = -120
########################

### Parameters of the sim
delta_t = 1.e-2 #The time resolution of the output, in decimal hours
sim_time = 1 #Total time to simulate after the supplied start time, in hours

# We assume: RA in decimal hours, DEC in decimal degrees. May convert if needed

### Conversions involving ISO-formatted UTC:
# 2013 11 18 T 01 41 27 Z
# YYYY MM DD   HH MM SS
# Time format: [YYYY][MM][DD]T[HH][MM][SS]Z

# python ephemeris.py 0 0 20131118T014127Z 0.05 24 | less

if len(sys.argv) != 6:
    print "Usage: python ephemeris.py SOURCE_RA SOURCE_DEC TIME DELTA_T SIM_LENGTH"

else:
    source_ra  = float(sys.argv[1])
    source_dec = float(sys.argv[2])
    time_start = sys.argv[3]
    delta_t    = float(sys.argv[4])
    sim_time   = float(sys.argv[5])


    # setting the time constants
    time_J2000_epoch = datetime(2000, 01, 01, 11, 58, 55, 816000, tzinfo=tzutc()) 
    time_per_step = timedelta(0,3600*delta_t)

    # converts input time to the datetime object
    time_current = datetime(int(time_start[:4]),int(time_start[4:6]),int(time_start[6:8]),int(time_start[9:11]),int(time_start[11:13]),int(time_start[13:15]),0,tzinfo=tzutc())

    for i in np.linspace(0, sim_time, sim_time/delta_t):
        days_since_J2000 = time_current - time_J2000_epoch
        decimal_days_since_J2000 = days_since_J2000.days + days_since_J2000.seconds/(24*3600.)

        local_siderial_time = 100.46 + 0.985647*decimal_days_since_J2000 + CHI_long + 15*(time_current.hour+time_current.minute/60.+time_current.second/3600.)
        while(local_siderial_time < 0):
            local_siderial_time += 360.
        while(local_siderial_time > 360):
            local_siderial_time -= 360.

        hour_angle = local_siderial_time - source_ra
        if(hour_angle < 0):
            hour_angle += 360.

        alt = np.sin(source_dec*np.pi/180.)*np.sin(CHI_lat*np.pi/180.)+np.cos(source_dec*np.pi/180.)*np.cos(CHI_lat*np.pi/180.)*np.cos(hour_angle*np.pi/180.)
        alt = np.arcsin(alt)*180/np.pi

        if(np.cos(alt*np.pi/180.) != 0 and np.cos(CHI_lat*np.pi/180.) != 0):
            az = (np.sin(source_dec*np.pi/180.) - np.sin(alt*np.pi/180.)*np.sin(CHI_lat*np.pi/180.))/(np.cos(alt*np.pi/180.)*np.cos(CHI_lat*np.pi/180.))
            az = np.arccos(az)*180/np.pi
        else:
            az = NaN

        if(np.sin(hour_angle*np.pi/180.) >= 0):
            az = 360 - az

        tc=time_current
        sep = "\t"
        print str(tc.year).zfill(4)+str(tc.month).zfill(2)+str(tc.day).zfill(2)+"T"+str(tc.hour).zfill(2)+str(tc.minute).zfill(2)+str(tc.second).zfill(2)+"Z"+sep+ str(i) +sep+ str(alt) +sep+ str(az)

        time_current += time_per_step
