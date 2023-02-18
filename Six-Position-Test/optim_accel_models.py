##################################################################
# Program Name: optim_accel_models.py
# Written by: Will Ward
# 
# Optimize parameters in three accelerometer output models to fit
# the six-position data. Save the model parameters to a CSV file.  
# Use least-squares fitting (scipy.optimize.curve_fit)
#
# Function:
#     1. Load raw acceleration data from CSV file
#     2. Optimize parameters in model one
#     3. Optimize parameters in model two 
#     4. Optimize parameters in model three
#     5. Graph data and save params to CSV 
###################################################################


import sys
sys.path.append('../')
import numpy as np   
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt


def bias_model(true_accel, bias):
    # Acceleromet Output Model -- Bias Only
    # measured_accel = true_accel + bias
    return (true_accel + bias) # equals measured accel

def scale_factor_model(true_accel, bias, scale_factor):
    # Accelerometer Output Model -- Bias and Scale Factor Vector
    # measured_accel = scale_factor * true_accel + bias
    return (scale_factor * true_accel + bias) # equals measured accel

def misalignment_model(true_accel, bias, s1, s2, s3):
    # Accelerometer Output Model -- Bias and Scale Factor Matrix (includes misalignment)
    # measured_accel = scale_factor_matrix * true_accel + bias
    return (true_accel[0]*s1 + true_accel[1]*s2 + true_accel[2]*s3 + bias)




if __name__ == '__main__':

    # Read data from CSV file
    file = open("data/trial_3/six_position_data_3.csv") 
    read_data = np.loadtxt(file, skiprows = 1, delimiter=",", dtype=float) 
    
    # Divide data into seperate arrays
    x_true = read_data[:, 0]  # true x acceleration (gravity)
    x_mean = read_data[:, 1]  # mean x measured acceleration
    x_std  = read_data[:, 2]  # standard deviation of measured x
    y_true = read_data[:, 3]  # y
    y_mean = read_data[:, 4]  # y
    y_std  = read_data[:, 5]  # y
    z_true = read_data[:, 6]  # z
    z_mean = read_data[:, 7]  # z
    z_std  = read_data[:, 8]  # z
    
    true = np.stack((x_true, y_true, z_true), axis = 0) # combine all truth data, for convenience


    ##########################################################
    # Optimize the paramters in all three accelerometer models
    ##########################################################

    # Optimize Parameters for X
    params, covar = curve_fit(bias_model, x_true, x_mean)
    b_x1 = params.item()
    print(b_x1)
    params, covar = curve_fit(scale_factor_model, x_true, x_mean, p0=(b_x1, 1))
    b_x2, Sxx2 = params[0].item(), params[1].item()
    print(b_x2, Sxx2)
    params, covar = curve_fit(misalignment_model, true, x_mean, p0=(b_x2, Sxx2, 0, 0))
    b_x3, Sxx3, Sxy3, Sxz3 = params[0].item(), params[1].item(), params[2].item(), params[3].item()
    print(b_x3, Sxx3, Sxy3, Sxz3)

    # Optimize Parameters for Y
    params, covar = curve_fit(bias_model, y_true, y_mean)
    b_y1 = params.item()
    print(b_y1)
    params, covar = curve_fit(scale_factor_model, y_true, y_mean, p0=(b_y1, 1))
    b_y2, Syy2 = params[0].item(), params[1].item()
    print(b_y2, Syy2)
    params, covar = curve_fit(misalignment_model, true, y_mean, p0=(b_y2, 0, Syy2, 0))
    b_y3, Syx3, Syy3, Syz3 = params[0].item(), params[1].item(), params[2].item(), params[3].item()
    print(b_y3, Syy3, Syx3, Syz3)

    # Optimize Parameters for Z
    params, covar = curve_fit(bias_model, z_true, z_mean)
    b_z1 = params.item()
    print(b_z1)
    params, covar = curve_fit(scale_factor_model, z_true, z_mean, p0=(b_z1, 1))
    b_z2, Szz2 = params[0].item(), params[1].item()
    print(b_z2, Szz2)
    params, covar = curve_fit(misalignment_model, true, z_mean, p0=(b_z2, 0, 0, Szz2))
    b_z3, Szx3, Szy3, Szz3 = params[0].item(), params[1].item(), params[2].item(), params[3].item()
    print(b_z3, Szz3, Szx3, Szy3)
    
    
    #exit()


    #############################
    # Save Parameters to CSV File
    #############################
    
    file = open('optim_params_3.csv', 'a') # name csv after calibration trial and axis
    file.write('Accelerometer Model Parameters Optimized - Trial 3.\n')
    file.write('b_x, b_y, b_z, Sxx, Sxy, Sxz, Syx, Syy, Syz, Szx, Szy, Szz \n')
    file.write(str(b_x1) + ',' + str(b_y1) + ',' + str(b_z1) + '\n')
    file.write(str(b_x2) + ',' + str(b_y2) + ',' + str(b_z2) + ',' + str(Sxx2) + ',' + str(Syy2) + ',' + str(Szz2) + '\n')
    file.write(str(b_x3) + ',' + str(b_y3) + ',' + str(b_z3) + ',' + str(Sxx3) + ',' + str(Sxy3) + ',' + str(Sxz3) + ',' +
                                                                     str(Syx3) + ',' + str(Syy3) + ',' + str(Syz3) + ',' + 
                                                                     str(Szx3) + ',' + str(Szy3) + ',' + str(Szz3) + '\n')
    file.close()


    exit()

    ########################################
    # Graph x, y, and z data with trend fit.
    ########################################

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.scatter(x_true, x_mean, color='r', label='x')
    plt.plot(x_true, misalignment_model(true, b_x3, Sxx3, Sxy3, Sxz3), color='r')
    plt.scatter(y_true, y_mean, color='b', label='y')
    plt.plot(y_true, misalignment_model(true, b_y3, Syx3, Syy3, Syz3), color='b')
    plt.scatter(z_true, z_mean, color='g', label='z')
    plt.plot(z_true, misalignment_model(true, b_z3, Szx3, Szy3, Szz3), color='g')
    axs.set_ylabel('Measured Gravity [g]')
    axs.set_xlabel('True Gravity [g]')
    #axs.set_ylim([-2,2])
    axs.set_title("Six-Position Calibration Data - Trial 3")
    axs.legend()
    fig.savefig("six_position_optim_3.jpg")
    

    
    
