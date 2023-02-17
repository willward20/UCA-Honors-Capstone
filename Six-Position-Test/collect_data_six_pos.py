##################################################################
# Program Name: collect_data_six_pos.py
# Written by: Will Ward 
#  
# Collect acceleration data from the MPU-9250 accelerometer. 
# Rotate the accelerometer to six static positions to collect
# data for error model fitting. 
#           x-up, x-down, y-up, y-down, z-up, z-down
# For each orientation, average 30 seconds of data (180 Hz). Record the mean
# and standard deviation. 
# After collecting at 6 orientations, collect an additional 1 minute of static data
###################################################################



import time,sys
sys.path.append('../')
import numpy as np
import matplotlib.pyplot as plt

# Wait for IMU to connect
t0 = time.time()
start_bool = False # if IMU start fails - stop
while time.time()-t0<5:
    try: 
        import mpu9250_i2c
        start_bool = True
        break
    except:
        continue
time.sleep(2) # wait for MPU to load and settle



def accel_cal(total_time, FILENAME):

    # Collect acceleration over time and iteratively save to CSV
    
    start_time = time.time() # initialize start time

    while (time.time() - start_time) < total_time: # collect data for total_time seconds

        x_accel, y_accel, z_accel ,_,_,_ = mpu9250_i2c.mpu6050_conv() # read and convert accel data (ignore gyro)
        elapsed_time = time.time() - start_time # record a time stamp
        
        # Save analyzed data to CSV
        file = open(FILENAME, 'a')
        file.write(str(elapsed_time) + ',' + str(x_accel) + ',' + str(y_accel) + ',' + str(z_accel) + '\n')
        file.close()

    return


def accel_mean_std(total_time):

    # Read acceleration from the IMU and return the mean and std of each axis over total_tim

    start_time = time.time() # initialize start time
    x_data = []
    y_data = []
    z_data = []

    while (time.time() - start_time) < total_time: # collect data for total_time seconds
        x_accel, y_accel, z_accel ,_,_,_ = mpu9250_i2c.mpu6050_conv() # read and convert accel data (ignore gyro)
        x_data.append(x_accel)
        y_data.append(y_accel)
        z_data.append(z_accel)

    data = [[np.mean(x_data), np.std(x_data)], # x
            [np.mean(y_data), np.std(y_data)], # y
            [np.mean(z_data), np.std(z_data)]] # z

    return data


def save_csv(csv_file, true, measured):

    # Save true acceleration, mean measured acceleration, and standard deviation to CSV file

    file = open(csv_file, 'a') 
    file.write(str(true[0]) + ',' + str(measured[0][0]) + ',' + str(measured[0][1]) + ',' + # x
               str(true[1]) + ',' + str(measured[1][0]) + ',' + str(measured[1][1]) + ',' + # y
               str(true[2]) + ',' + str(measured[2][0]) + ',' + str(measured[2][1]) + '\n') # z
    file.close()





if __name__ == '__main__':

    # Ensure that the IMU is initialized
    if not start_bool:
        print("IMU not Started - Check Wiring and I2C")

    else:
        
        # Open a CSV file for saving six-position data. Label each column
        six_position_csv = 'six_position_data.csv'
        file = open(six_position_csv, 'a') 
        file.write('x_true (g)' + ',' + 'x_mean (g)' + ',' + 'x_std' + ',' + 
                   'y_true (g)' + ',' + 'y_mean (g)' + ',' + 'y_std' + ',' +
                   'z_true (g)' + ',' + 'z_mean (g)' + ',' + 'z_std' + '\n') # label each column
        file.close()

        print("Six Position Static Data Collection")

        # 1
        input("\t1. Rotate Z up and press enter.")
        measured_data = accel_mean_std(total_time=30) # collect over 30 seconds
        true_data = [0.0, 0.0, 1.0] # ground truth acceleration
        save_csv(six_position_csv, measured_data, true_data)

        # 2
        input("\t2. Rotate Z down and press enter.")
        measured_data = accel_mean_std(total_time=30) # collect over 30 seconds
        true_data = [0.0, 0.0, -1.0] # groudn truth acceleration
        save_csv(six_position_csv, measured_data, true_data)

        # 3
        input("\t3. Rotate Y up and press enter.")
        measured_data = accel_mean_std(total_time=30) # collect over 30 seconds
        true_data = [0.0, 1.0, 0.0] # groudn truth acceleration
        save_csv(six_position_csv, measured_data, true_data)

        # 4
        input("\t4. Rotate Y down and press enter.")
        measured_data = accel_mean_std(total_time=30) # collect over 30 seconds
        true_data = [0.0, -1.0, 0.0] # groudn truth acceleration
        save_csv(six_position_csv, measured_data, true_data)

        # 5
        input("\t5. Rotate X up and press enter.")
        measured_data = accel_mean_std(total_time=30) # collect over 30 seconds
        true_data = [1.0, 0.0, 0.0] # groudn truth acceleration
        save_csv(six_position_csv, measured_data, true_data)

        # 6
        input("\t6. Rotate X down and press enter.")
        measured_data = accel_mean_std(total_time=30) # collect over 30 seconds
        true_data = [-1.0, 0.0, 0.0] # groudn truth acceleration
        save_csv(six_position_csv, measured_data, true_data)



        input("Collect Test Data. Rotate Z up and press enter.")

        # Open a CSV file for saving test data. Label each column
        test_csv = 'six_position_test_data.csv'
        file = open(test_csv, 'a') 
        file.write('Acceleration Data Collected on Level Surface. Z up.' + '\n' + 
                   'time (s)' + 'x (g)' + ',' + 'y (g)' + ',' + 'z (g)' + '\n') # label each column
        file.close()
        accel_cal(total_time=60, FILENAME=test_csv)


        print("Finished!") # status update