##################################################################
# Script Name: collect_data.py
# Written by: Will Ward (willward20)
#  
# Python script for colleting acceleration data from an MPU-9250 IMU.
###################################################################


import time,sys
sys.path.append('../')
import numpy as np
import matplotlib.pyplot as plt

# Wait for IMU to connect
t0 = time.time()    # start time
start_bool = False    # if IMU start fails - stop
while (time.time() - t0) < 5:
    try: 
        import mpu9250_i2c    # package for accesing IMU
        start_bool = True
        break
    except:
        continue

# Ensure that the IMU is initialized
if not start_bool:
    print("IMU not Started - Check Wiring and I2C")
    exit()
else:
    print("IMU Started")
    time.sleep(2)    # wait for MPU to load and settle



def accel_cal(
        total_time, FILENAME):

    # Open a CSV file for saving data. Label each column
    file = open(FILENAME, 'a')    # name csv after calibration trial and axis
    file.write('time' + ',' + 'x (g)' + ',' + 'y (g)' + ',' + 'z (g)' + '\n')    # label each column
    file.close()
    
    start_time = time.time()    # initialize start time
    while (time.time() - start_time) < total_time:    # collect data for total_time seconds

        x_accel, y_accel, z_accel ,_,_,_ = mpu9250_i2c.mpu6050_conv()    # retrieve acceleration measurement
        elapsed_time = time.time() - start_time    # record a time stamp
        
        # Save analyzed data to CSV
        file = open(FILENAME, 'a')
        file.write(str(elapsed_time) + ',' + str(x_accel) + ',' + str(y_accel) + ',' + str(z_accel) + '\n')
        file.close()

    return


def graph_data(
        times, x_accels, y_accels, z_accels, TITLE, FILENAME):

    # Graph x, y, and z data on seperate plots.

    fig,axs = plt.subplots(3,1)

    axs[0].scatter(times, x_accels, s=1, color='r')
    axs[1].scatter(times, y_accels, s=1, color='b')
    axs[2].scatter(times, z_accels, s=1, color='g')
    axs[0].set_ylabel('X Accel. [g]')
    axs[1].set_ylabel('Y Accel. [g]')
    axs[2].set_ylabel('Z Accel. [g]')
    axs[2].set_xlabel('Time (hours)')
    axs[0].set_title(TITLE)
    fig.savefig(FILENAME)

    return






if __name__ == '__main__':

    input("Press Enter to Start Collecting")    # prompt user to begin collection
    accel_cal(total_time=60, FILENAME='accel_data.csv')    # collect over time and save to CSV
    print("Finished collecting") 

    # Open the CSV file again and graph the data
    file = open("accel_over_time.csv")
    read_data = np.loadtxt(file, skiprows = 1, delimiter=",", dtype=float)
    time_array = read_data[:, 0] # seperate data into arays
    x_accels = read_data[:, 1]
    y_accels = read_data[:, 2]
    z_accels = read_data[:, 3]

    graph_data(time_array, x_accels, y_accels, z_accels, TITLE="Acceleration over Time", FILENAME="accel_over_time.png")


