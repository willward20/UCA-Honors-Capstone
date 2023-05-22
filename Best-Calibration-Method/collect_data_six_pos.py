#############################################################################
# Script Name: collect_data_six_pos.py
# Written by: Will Ward (willward20)

# Python script for colleting acceleration data from an MPU-9250 IMU.

# Data is collected after rotating the IMU to six static positions: 
# (1) x-up,  (2) x-down,  (3) y-up,  (4) y-down,  (5) z-up,  (6) z-down.
# Then, an additional one minute of data is collected for calibration tests.

# The accelerometer should be placed on a level surface at all times. 
# Collect data in a stable surface that will not vibrate or wobble. 
##############################################################################


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
    
    # Collect acceleration over time.
    # Iteratively save to a CSV file. 
    
    start_time = time.time()    # initialize start time
    while (time.time() - start_time) < total_time:    # collect data for total_time seconds

        x_accel, y_accel, z_accel ,_,_,_ = mpu9250_i2c.mpu6050_conv()    # retrieve acceleration measurement
        elapsed_time = time.time() - start_time     # record a time stamp
        
        # Save data and time stamp to CSV
        file = open(FILENAME, 'a')
        file.write(str(elapsed_time) + ',' + str(x_accel) + ',' + str(y_accel) + ',' + str(z_accel) + '\n')
        file.close()

    return


def accel_mean_std(
        total_time):

    # Read acceleration from the IMU. 
    # Calculate mean and standard deviation

    start_time = time.time()    # initialize start time
    x_data = []    # x_axis acceleration
    y_data = []    # y_axis acceleration
    z_data = []    # z_axis acceleration

    while (time.time() - start_time) < total_time:    # collect data for total_time seconds

        x_accel, y_accel, z_accel ,_,_,_ = mpu9250_i2c.mpu6050_conv()    # retrieve acceleration measurements
        x_data.append(x_accel)    # append measurement to array
        y_data.append(y_accel)    # append measurement to array
        z_data.append(z_accel)    # append measurement to array

    data = [[np.mean(x_data), np.std(x_data)],    # store mean and standard deviation of x measurements
            [np.mean(y_data), np.std(y_data)],    # store mean and standard deviation of y measurements
            [np.mean(z_data), np.std(z_data)]]    # store mean and standard deviation of z measurements

    return data


def save_csv(
        csv_file, measured, true):

    # Save true acceleration, 
    # mean measured acceleration, 
    # and standard deviation to a CSV file.

    file = open(csv_file, 'a')        # means                     # standard devs
    file.write(str(true[0]) + ',' + str(measured[0][0]) + ',' + str(measured[0][1]) + ',' + # x
               str(true[1]) + ',' + str(measured[1][0]) + ',' + str(measured[1][1]) + ',' + # y
               str(true[2]) + ',' + str(measured[2][0]) + ',' + str(measured[2][1]) + '\n') # z
    file.close()

    return





if __name__ == '__main__':
    
    # Open a CSV file for saving six-position data.
    # CSV will save true acceleration, mean acceleration
    # and standard deviation for each accelerometer axis.
    six_position_csv = 'six_position_data.csv'    # CSV file name
    file = open(six_position_csv, 'a') 
    file.write('x_true (g)' + ',' + 'x_mean (g)' + ',' + 'x_std' + ',' + 
               'y_true (g)' + ',' + 'y_mean (g)' + ',' + 'y_std' + ',' +
               'z_true (g)' + ',' + 'z_mean (g)' + ',' + 'z_std' + '\n')    # label each column
    file.close()


    # Collect acceleration data for six IMU orientations.
    # Collect data at 180 Hz for 30 seconds. Then save the 
    # groudn truth and measured data to CSV file.
    print("Six Position Static Data Collection")    # status update

    # Orientation 1: Z-axis facing up
    input("\t1. Rotate Z up and press enter.")    # pause for user input
    measured_data = accel_mean_std(total_time=30)    # collect over 30 seconds
    true_data = [0.0, 0.0, 1.0] # ground truth acceleration
    save_csv(six_position_csv, measured_data, true_data)

    # Orientation 2: Z-axis facing down
    input("\t2. Rotate Z down and press enter.")
    measured_data = accel_mean_std(total_time=30)    
    true_data = [0.0, 0.0, -1.0]    
    save_csv(six_position_csv, measured_data, true_data)

    # Orientation 3: Y-axis facing up
    input("\t3. Rotate Y up and press enter.")
    measured_data = accel_mean_std(total_time=30) 
    true_data = [0.0, 1.0, 0.0] 
    save_csv(six_position_csv, measured_data, true_data)

    # Orientation 4: Y-axis facing down
    input("\t4. Rotate Y down and press enter.")
    measured_data = accel_mean_std(total_time=30) 
    true_data = [0.0, -1.0, 0.0] 
    save_csv(six_position_csv, measured_data, true_data)

    # Orientation 5: X-axis facing up
    input("\t5. Rotate X up and press enter.")
    measured_data = accel_mean_std(total_time=30) 
    true_data = [1.0, 0.0, 0.0] 
    save_csv(six_position_csv, measured_data, true_data)

    # Orientation 6: X-axis facing down
    input("\t6. Rotate X down and press enter.")
    measured_data = accel_mean_std(total_time=30) 
    true_data = [-1.0, 0.0, 0.0] 
    save_csv(six_position_csv, measured_data, true_data)




    # Finally, collect data for one minute while the Z-axis
    # faces up. Save full, unprocessed data to a CSV file.
    input("Collect Test Data. Rotate Z up and press enter.")
    test_csv = 'six_position_test_data.csv'    # CSV file for saving data
    file = open(test_csv, 'a') 
    file.write('Acceleration Data Collected on Level Surface. Z up.' + '\n' + 
                'time (s)' + 'x (g)' + ',' + 'y (g)' + ',' + 'z (g)' + '\n')    # label each column
    file.close()
    
    accel_cal(total_time=60, FILENAME=test_csv)    # collect data for 1 minute and save to CSV


    print("Finished.")