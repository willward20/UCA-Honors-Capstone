##################################################################
# Program Name: integrate.py
# Written by: Will Ward
#  
# Function:
#     1. Load raw acceleration data from CSV file
#     2. Process the data (calibrate, convert, etc.)
#     3. Integrate the data over time (for velocity and/or distance) 
#     4. Plot the integrated data on a graph
###################################################################


import sys
sys.path.append('../')
import numpy as np  
import matplotlib.pyplot as plt 
from scipy.integrate import cumtrapz    


def bias_model(measured_accel, bias):
    # Acceleromet Output Model -- Bias Only
    # measured_accel = true_accel + bias
    # true_accel = measured_accel - bias
    return (measured_accel - bias) # equals true accel

def scale_factor_model(measured_accel, bias, scale_factor):
    # Accelerometer Output Model -- Bias and Scale Factor Vector
    # measured_accel = scale_factor * true_accel + bias
    # true_accel = (measured_accel - bias) / scale_factor
    return ((measured_accel - bias) / scale_factor) # equals true accel

def misalignment_model(measured_accel, bias, scale_f_matrix):
    # Accelerometer Output Model -- Bias and Scale Factor Matrix (includes misalignment)
    # measured_accel = true_accel*scale_f_matrix + bias
    # true_accel = (measured_accel - bias)*(scale_f_matrix)^-1
    true_accel = np.array([np.dot((measured_accel[0]-bias), np.linalg.inv(scale_f_matrix))])
    for ii in range(1, np.shape(measured_accel)[0]):
        true_accel = np.append(true_accel, [np.dot((measured_accel[ii]-bias), np.linalg.inv(scale_f_matrix))], axis=0)
    return (true_accel)



def integrate_data(times, acceleration):

    # Split up each axis
    a_x = acceleration[:,0]
    a_y = acceleration[:,1]
    a_z = acceleration[:,2]
    # Integrate data twice over time
    vel_x = np.append(0.0, cumtrapz(a_x,x=times))   # outputs an array of velocity values over time
    dis_x = np.append(0.0, cumtrapz(vel_x, x=times))  # outputs an array of displacement values over time
    vel_y = np.append(0.0, cumtrapz(a_y,x=times))   # outputs an array of velocity values over time
    dis_y = np.append(0.0, cumtrapz(vel_y, x=times))  # outputs an array of displacement values over time
    vel_z = np.append(0.0, cumtrapz(a_z,x=times))   # outputs an array of velocity values over time
    dis_z = np.append(0.0, cumtrapz(vel_z, x=times))  # outputs an array of displacement values over time
    
    return dis_x, dis_y, dis_z



def graph_data(times, x, y, z, Y_AXIS, TITLE, FILENAME):   
    
    # Graph x, y, and z data on one plot. Each axis gets its own time value, in case data was filtered

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.plot(times, x, color='r', label='x')
    plt.plot(times, y, color='b', label='y')
    plt.plot(times, z, color='g', label='z')
    axs.set_ylabel(Y_AXIS)
    axs.set_xlabel('Time (seconds)')
    #axs.set_ylim([#, #])
    axs.set_title(TITLE)
    axs.legend()
    fig.savefig(FILENAME)

    return





if __name__ == '__main__':

    # Read acceleration data from CSV file
    file = open("data/trial_3/six_position_test_data_3.csv") # containts raw acceleration data collected 179 Hz over one minute
    accel_data = np.loadtxt(file, skiprows = 2, delimiter=",", dtype=float) 
    time_array = accel_data[:, 0]  # time stamps for integrating
    accels = accel_data[:,1:] # three columns  of acceleration [g] (x, y, z)

    # Read calibration parameters from CSV file
    param_data = open("data/trial_3/optim_params_3.csv")  # contains parameters for three acceleromter error models
    param_data = np.loadtxt(param_data, skiprows = 2, delimiter=",", dtype=float)
    
    # Calibrate data using a pre-optimized error models
    #bias_1 = np.loadtxt(param_data, skiprows = 2, delimiter=",", dtype=float, usecols=(0,1,2), max_rows=1)
    bias_1 = np.array(param_data[0, 0:3])
    accel_calib_1 = bias_model(accels, bias_1)
    
    bias_2 = np.array(param_data[1, 0:3])
    scale_f_2 = np.array(param_data[1, 3:6])
    accel_calib_2 = scale_factor_model(accels, bias_2, scale_f_2)

    bias_3 = np.array(param_data[2, 0:3])
    scale_f_3 = (np.array([param_data[2, 3:6],
                           param_data[2, 6:9],
                           param_data[2, 9:]])).T
    accel_calib_3 = misalignment_model(accels, bias_3, scale_f_3)


    # Convert from units of g to m/s/s
    accels = accels * 9.80665
    accel_calib_1 = accel_calib_1 * 9.80665
    accel_calib_2 = accel_calib_2 * 9.80665
    accel_calib_3 = accel_calib_3 * 9.80665

    # Remove gravity from the z data (facing up)
    accels[:,2] = accels[:,2] - 9.80665
    accel_calib_1[:,2] = accel_calib_1[:,2] - 9.80665
    accel_calib_2[:,2] = accel_calib_2[:,2] - 9.80665
    accel_calib_3[:,2] = accel_calib_3[:,2] - 9.80665

    
    # Statistical analysis
    print("Statistical Analysis")
    print(f"Uncalibrated Data (mean, std): x({np.mean(accels[:,0]):.4f}, {np.std(accels[:,0]):.4f}),",
                                         f"y({np.mean(accels[:,1]):.4f}, {np.std(accels[:,1]):.4f}),",
                                         f"z({np.mean(accels[:,2]):.4f}, {np.std(accels[:,2]):.4f})")
    print(f"Bias Calibrated   (mean, std): x({np.mean(accel_calib_1[:,0]):.4f}, {np.std(accel_calib_1[:,0]):.4f}),",
                                         f"y({np.mean(accel_calib_1[:,1]):.4f}, {np.std(accel_calib_1[:,1]):.4f}),",
                                         f"z({np.mean(accel_calib_1[:,2]):.4f}, {np.std(accel_calib_1[:,2]):.4f})")
    print(f"Add Scale Factors (mean, std): x({np.mean(accel_calib_2[:,0]):.4f}, {np.std(accel_calib_2[:,0]):.4f}),",
                                         f"y({np.mean(accel_calib_2[:,1]):.4f}, {np.std(accel_calib_2[:,1]):.4f}),",
                                         f"z({np.mean(accel_calib_2[:,2]):.4f}, {np.std(accel_calib_2[:,2]):.4f})")
    print(f"Calibrated Data 3 (mean, std): x({np.mean(accel_calib_3[:,0]):.4f}, {np.std(accel_calib_3[:,0]):.4f}),",
                                         f"y({np.mean(accel_calib_3[:,1]):.4f}, {np.std(accel_calib_3[:,1]):.4f}),",
                                         f"z({np.mean(accel_calib_3[:,2]):.4f}, {np.std(accel_calib_3[:,2]):.4f})")
    
    
    # Integrate raw and calibrated data over time
    uncal_dis_x, uncal_dis_y, uncal_dis_z = integrate_data(time_array, accels)
    cal_dis_x_1, cal_dis_y_1, cal_dis_z_1 = integrate_data(time_array, accel_calib_1)
    cal_dis_x_2, cal_dis_y_2, cal_dis_z_2 = integrate_data(time_array, accel_calib_2)
    cal_dis_x_3, cal_dis_y_3, cal_dis_z_3 = integrate_data(time_array, accel_calib_3)
    print(f"Uncalibrated Data: {uncal_dis_x[-1]:0.0f}, {uncal_dis_y[-1]:0.0f}, {uncal_dis_z[-1]:0.0f}")
    print(f"Bias Calibrated:   {cal_dis_x_1[-1]:0.0f}, {cal_dis_y_1[-1]:0.0f}, {cal_dis_z_1[-1]:0.0f}")
    print(f"Add Scale Factors: {cal_dis_x_2[-1]:0.0f}, {cal_dis_y_2[-1]:0.0f}, {cal_dis_z_2[-1]:0.0f}")
    print(f"Add Misalignments: {cal_dis_x_3[-1]:0.0f}, {cal_dis_y_3[-1]:0.0f}, {cal_dis_z_3[-1]:0.0f}")

    
    
    # Graph the displacement over time of each axis after calibrating with misalignments (model 3)
    y_axis_label = "Displacement (m)"
    title = "Trial 3 Displacement (m) - After Calibrating with Misalignments Included"
    image_file_name = "displacement_misalignment_3.png"
    graph_data(time_array, cal_dis_x_3, cal_dis_y_3, cal_dis_z_3, Y_AXIS=y_axis_label, TITLE=title, FILENAME=image_file_name)
    
    

    