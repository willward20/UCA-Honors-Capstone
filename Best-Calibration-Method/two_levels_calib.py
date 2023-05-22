#############################################################################
# Script Name: two_levels_calib.py
# Written by: Will Ward (willward20)

# Python script for calibrating an MPU-9250 accelerometer for more accurate 
# displacement estiamtes using least-squares optimzation of model parameters.

# First, the acceleration models are optimized in order of complexity to reduce
# the computational load. Only the third model, misalignment_model, is actually
# used in the calibration process. After calibrating the first set of test data, 
# the data is integrated over time to calcualte the displacement. Next, the
# displacement model is optimized to fit the calucated displacement data using
# least-squares optimization. Finally, the second set of test data is calibrated
# using the optimized acceleration model, integrated for displacement, and
# calibrated again using the optimized displacement model. 
##############################################################################

import sys
sys.path.append('../')
import numpy as np   
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
from scipy.integrate import cumtrapz    


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

def misalignment_model_2(measured_accel, bias, scale_f_matrix):
    # Accelerometer Output Model -- Bias and Scale Factor Matrix (includes misalignment)
    # measured_accel = true_accel*scale_f_matrix + bias
    # true_accel = (measured_accel - bias)*(scale_f_matrix)^-1
    true_accel = np.array([np.dot((measured_accel[0]-bias), np.linalg.inv(scale_f_matrix))])
    
    for ii in range(1, np.shape(measured_accel)[0]):
        true_accel = np.append(true_accel, [np.dot((measured_accel[ii]-bias), np.linalg.inv(scale_f_matrix))], axis=0)
   
    return (true_accel)

def disp_model(times, q0, q1, q2):
    # Error in displacement model
    return (0.5*q2*times*times + q1*times + q0) # equals calculated displacement



def integrate_data(times, acceleration):

    # Split up each axis
    a_x = acceleration[:,0]
    a_y = acceleration[:,1]
    a_z = acceleration[:,2]

    # Integrate data twice over time
    vel_x = np.append(0.0, cumtrapz(a_x,x=times))    # outputs an array of velocity values over time
    vel_y = np.append(0.0, cumtrapz(a_y,x=times)) 
    vel_z = np.append(0.0, cumtrapz(a_z,x=times))  

    dis_x = np.append(0.0, cumtrapz(vel_x, x=times))    # outputs an array of displacement values over time
    dis_y = np.append(0.0, cumtrapz(vel_y, x=times))    
    dis_z = np.append(0.0, cumtrapz(vel_z, x=times))  

    return dis_x, dis_y, dis_z


def graph_data(times, x, y, z, Y_AXIS, TITLE, FILENAME):   
    
    # Graph x, y, and z data on one plot.

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.plot(times, x, color='r', label='x')
    plt.plot(times, y, color='b', label='y')
    plt.plot(times, z, color='g', label='z')
    axs.set_ylabel(Y_AXIS)
    axs.set_xlabel('Time (seconds)')
    axs.set_title(TITLE)
    axs.legend()
    fig.savefig(FILENAME)

    return





if __name__ == '__main__':
    
    ##########################################################
    # Read all of the six-position data from CSV file
    ##########################################################

    # Read six-position data from CSV file
    file = open("data/final_trial/six_position_data.csv") 
    read_data = np.loadtxt(file, skiprows = 1, delimiter=",", dtype=float) 
    
    # Divide data into seperate arrays
    x_true = read_data[:, 0]  # true x acceleration (gravity)
    x_mean = read_data[:, 1]  # mean x measured acceleration
    x_std  = read_data[:, 2]  # standard deviation of each meaurement -- NOT the SDOM of x_mean!!!!
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
    print('X Parameters')
    params, covar = curve_fit(bias_model, x_true, x_mean, sigma=x_std)
    b_x1 = params.item()
    #print("Parameters: ", params, " Uncertainties (%): ", np.sqrt(np.diag(covar))/params * 100) # extract diagonal components (variances) and square them to get std dev

    params, covar = curve_fit(scale_factor_model, x_true, x_mean, p0=(b_x1, 1), sigma=x_std)
    b_x2, Sxx2 = params[0].item(), params[1].item()
    #print("Parameters: ", params, " Uncertainties (%): ", np.sqrt(np.diag(covar))/params * 100)

    params, covar = curve_fit(misalignment_model, true, x_mean, p0=(b_x2, Sxx2, 0, 0), sigma=x_std)
    b_x3, Sxx3, Sxy3, Sxz3 = params[0].item(), params[1].item(), params[2].item(), params[3].item()
    print("Parameters: ", params, " Uncertainties (%): ", np.sqrt(np.diag(covar))/params * 100) 
    print('')
    

    # Optimize Parameters for Y
    print('Y Parameters')
    params, covar = curve_fit(bias_model, y_true, y_mean, sigma=y_std)
    b_y1 = params.item()
    #print("Parameters: ", params, " Uncertainties (%): ", np.sqrt(np.diag(covar))/params * 100)

    params, covar = curve_fit(scale_factor_model, y_true, y_mean, p0=(b_y1, 1), sigma=y_std)
    b_y2, Syy2 = params[0].item(), params[1].item()
    #print("Parameters: ", params, " Uncertainties (%): ", np.sqrt(np.diag(covar))/params * 100)

    params, covar = curve_fit(misalignment_model, true, y_mean, p0=(b_y2, -0.0039, Syy2, 0.0083), sigma=y_std)
    b_y3, Syx3, Syy3, Syz3 = params[0].item(), params[1].item(), params[2].item(), params[3].item()
    print("Parameters: ", params, " Uncertainties (%): ", np.sqrt(np.diag(covar))/params * 100) 
    print('')


    # Optimize Parameters for Z
    print('Z Parameters')
    params, covar = curve_fit(bias_model, z_true, z_mean, sigma=z_std)
    b_z1 = params.item()
    #print("Parameters: ", params, " Uncertainties (%): ", np.sqrt(np.diag(covar))/params * 100)

    params, covar = curve_fit(scale_factor_model, z_true, z_mean, p0=(b_z1, 1), sigma=z_std)
    b_z2, Szz2 = params[0].item(), params[1].item()
    #print("Parameters: ", params, " Uncertainties (%): ", np.sqrt(np.diag(covar))/params * 100) 

    params, covar = curve_fit(misalignment_model, true, z_mean, p0=(b_z2, -0.0089, -0.0048, Szz2), sigma=z_std)
    b_z3, Szx3, Szy3, Szz3 = params[0].item(), params[1].item(), params[2].item(), params[3].item()
    print("Parameters: ", params, " Uncertainties (%): ", np.sqrt(np.diag(covar))/params * 100)

    


    ###############################################
    # Calibrate the test data using Model 3
    ###############################################
    
    # Read acceleration data from CSV file
    file = open("data/final_trial/six_position_test_data.csv")    # containts raw acceleration data collected 179 Hz over one minute
    accel_data = np.loadtxt(file, skiprows = 2, delimiter=",", dtype=float) 
    time_array = accel_data[:, 0]    # time stamps for integrating
    accels = accel_data[:,1:]    # three columns  of acceleration [g] (x, y, z)

    # Calibrate using Model 3
    bias = np.array([b_x3, b_y3, b_z3])    # extract optimized biases
    scale_f = (np.array([[Sxx3, Sxy3, Sxz3],    # extract optimized scale factors, including misalignments
                           [Syx3, Syy3, Syz3],
                           [Szx3, Szy3, Szz3]])).T
    accel_calib = misalignment_model_2(accels, bias, scale_f)    # calibrate using Model 3


    ###############################################
    # Calculate the Displacement over Time from Acc.
    ###############################################

    # Convert from units of g to m/s/s 
    accel_calib = accel_calib * 9.797 

    # Remove gravity from the z data (facing up)
    accel_calib[:,2] = accel_calib[:,2] - 9.797 

    # Integrate raw and calibrated data over time
    cal_dis_x, cal_dis_y, cal_dis_z = integrate_data(time_array, accel_calib)
    print(f"Model 3 Displacement: {cal_dis_x[-1]:0.0f}, {cal_dis_y[-1]:0.0f}, {cal_dis_z[-1]:0.0f}")

    # Graph the displacement over time of each axis after calibrating with misalignments (model 3)
    y_axis_label = "Displacement (m)"
    title = "Displacement (m) - After Calibrating with Misalignment Model"
    image_file_name = "displacement_misalignment.png"
    #graph_data(time_array, cal_dis_x, cal_dis_y, cal_dis_z, Y_AXIS=y_axis_label, TITLE=title, FILENAME=image_file_name)
    

    ###############################################
    # Optimzie the Displacement Error Model
    ###############################################

    # Optimize Parameters for X
    print('X Parameters')
    params, covar = curve_fit(disp_model, time_array, cal_dis_x)
    q0_x, q1_x, q2_x = params[0].item(), params[1].item(), params[2].item()
    print("Parameters: ", params, " Uncertainties (%): ", np.sqrt(np.diag(covar))/params * 100) # extract diagonal components (variances) and square them to get std dev

    # Optimize Parameters for Y
    print('Y Parameters')
    params, covar = curve_fit(disp_model, time_array, cal_dis_y)
    q0_y, q1_y, q2_y = params[0].item(), params[1].item(), params[2].item()
    print("Parameters: ", params, " Uncertainties (%): ", np.sqrt(np.diag(covar))/params * 100) # extract diagonal components (variances) and square them to get std dev

    # Optimize Parameters for Z
    print('Z Parameters')
    params, covar = curve_fit(disp_model, time_array, cal_dis_z)
    q0_z, q1_z, q2_z = params[0].item(), params[1].item(), params[2].item()
    print("Parameters: ", params, " Uncertainties (%): ", np.sqrt(np.diag(covar))/params * 100) # extract diagonal components (variances) and square them to get std dev

    """
    ########################################
    # Graph x, y, and z data with trend fit.
    ########################################

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.plot(time_array, cal_dis_x, color='r', label='x_measured')
    plt.plot(time_array, disp_model(time_array, q0_x, q1_x, q2_x), 'r--')
    plt.plot(time_array, cal_dis_y, color='b', label='y_measured')
    plt.plot(time_array, disp_model(time_array, q0_y, q1_y, q2_y), 'b--')
    plt.plot(time_array, cal_dis_z, color='g', label='z_measured')
    plt.plot(time_array, disp_model(time_array, q0_z, q1_z, q2_z), 'g--')
    axs.set_ylabel('Displacement (m)')
    axs.set_xlabel('Times (seconds)')
    #axs.set_ylim([-2,2])
    axs.set_title("Fitting Calculated Displacement to Polynomial")
    axs.legend()
    fig.savefig("disp_fitted.jpg")
    """

    

    ###############################################
    # Calibrate NEW Static Data with Disp. Model
    ###############################################

    # Read acceleration data from CSV file
    file = open("data/final_trial/six_position_final_test_data.csv")    # containts raw acceleration data collected 179 Hz over five minutes
    accel_data = np.loadtxt(file, skiprows = 2, delimiter=",", dtype=float) 
    time_array = accel_data[:60*180, 0]    # time stamps for integrating
    accels = accel_data[:60*180,1:]    # three columns  of acceleration [g] (x, y, z)
    
    # Calibrate using Model 3
    bias = np.array([b_x3, b_y3, b_z3])    # extract optimized biases
    scale_f = (np.array([[Sxx3, Sxy3, Sxz3],    # extract optimized scale factors, including misalignments
                           [Syx3, Syy3, Syz3],
                           [Szx3, Szy3, Szz3]])).T
    accel_calib = misalignment_model_2(accels, bias, scale_f)    # calibrate using Model 3

    # Convert from units of g to m/s/s 
    accel_calib = accel_calib * 9.797 

    # Remove gravity from the z data (facing up)
    accel_calib[:,2] = accel_calib[:,2] - 9.797 

    # Integrate raw and calibrated data over time
    cal_dis_x, cal_dis_y, cal_dis_z = integrate_data(time_array, accel_calib)
    print(f"Model 3 Displacement: {cal_dis_x[-1]:0.0f}, {cal_dis_y[-1]:0.0f}, {cal_dis_z[-1]:0.0f}")

    """
    # Graph new data with trend curves from previous block
    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)
    plt.plot(time_array, cal_dis_x, color='r', label='x_measured')
    plt.plot(time_array, disp_model(time_array, q0_x, q1_x, q2_x), 'r--')
    plt.plot(time_array, cal_dis_y, color='b', label='y_measured')
    plt.plot(time_array, disp_model(time_array, q0_y, q1_y, q2_y), 'b--')
    plt.plot(time_array, cal_dis_z, color='g', label='z_measured')
    plt.plot(time_array, disp_model(time_array, q0_z, q1_z, q2_z), 'g--')
    axs.set_ylabel('Displacement (m)')
    axs.set_xlabel('Times (seconds)')
    axs.set_title("Fitting Calculated Displacement to Polynomial")
    axs.legend()
    fig.savefig("disp_fitted_final_data.jpg")
    """
    
    

    # Calibrate using Disp. Model
    disp_calib_x = cal_dis_x - disp_model(time_array, q0_x, q1_x, q2_x)
    disp_calib_y = cal_dis_y - disp_model(time_array, q0_y, q1_y, q2_y)
    disp_calib_z = cal_dis_z - disp_model(time_array, q0_z, q1_z, q2_z)
    print(f"Final Displacement: {disp_calib_x[-1]:0.0f}, {disp_calib_y[-1]:0.0f}, {disp_calib_z[-1]:0.0f}")


    # Graph the displacement over time of each axis after calibrating with misalignments (model 3)
    y_axis_label = "Displacement (m)"
    title = "Final Calibrated Displacement"
    image_file_name = "displacement_misalignment_plus_new.png"
    graph_data(time_array, disp_calib_x, disp_calib_y, disp_calib_z, Y_AXIS=y_axis_label, TITLE=title, FILENAME=image_file_name)
    

    exit()
    #############################
    # Save Parameters to CSV File
    #############################
    
    file = open('NAME.csv', 'a') # name csv after calibration trial and axis
    file.write('Accelerometer Model Parameters Optimized\n')
    file.write('b_x, b_y, b_z, Sxx, Sxy, Sxz, Syx, Syy, Syz, Szx, Szy, Szz \n')
    file.write(str(b_x1) + ',' + str(b_y1) + ',' + str(b_z1) + '\n')
    file.write(str(b_x2) + ',' + str(b_y2) + ',' + str(b_z2) + ',' + str(Sxx2) + ',' + str(Syy2) + ',' + str(Szz2) + '\n')
    file.write(str(b_x3) + ',' + str(b_y3) + ',' + str(b_z3) + ',' + str(Sxx3) + ',' + str(Sxy3) + ',' + str(Sxz3) + ',' +
                                                                     str(Syx3) + ',' + str(Syy3) + ',' + str(Syz3) + ',' + 
                                                                     str(Szx3) + ',' + str(Szy3) + ',' + str(Szz3) + '\n')
    file.close()
    

    

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
    axs.set_title("Six-Position Calibration Data")
    axs.legend()
    fig.savefig("NAME.jpg")
    

    
    
