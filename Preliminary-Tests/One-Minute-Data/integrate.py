
import sys
sys.path.append('../')
import numpy as np  
import matplotlib.pyplot as plt 
from scipy.integrate import cumtrapz    


def integrate_data(times, acceleration):

    # Integrate data twice over time

    print("Integrating Acceleration")   # status update
    velocity = np.append(0.0, cumtrapz(acceleration,x=times))   # outputs an array of velocity values over time

    print("Integrating Velocity")   # status update
    displacement = np.append(0.0, cumtrapz(velocity, x=times))  # outputs an array of displacement values over time
    
    print("Finished Integrating")   # status update
    
    return time_array, velocity, displacement



def graph_data(x_times, y_times, z_times, x, y, z, Y_AXIS, TITLE, FILENAME):   
    
    # Graph x, y, and z data on one plot. Each axis gets its own time value, in case data was filtered

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.plot(x_times, x, color='r', label='x')
    plt.plot(y_times, y, color='b', label='y')
    plt.plot(z_times, z, color='g', label='z')
    axs.set_ylabel(Y_AXIS)
    axs.set_xlabel('Time (seconds)')
    #axs.set_ylim([#, #])
    axs.set_title(TITLE)
    axs.legend()
    fig.savefig(FILENAME)

    return





if __name__ == '__main__':

    # Read data from CSV file
    file = open("one_min_raw_data.csv") # containts raw acceleration data collected 179 Hz over one hour (stationary)
    read_data = np.loadtxt(file, skiprows = 2, delimiter=",", dtype=float) 
    
    # Divide data into seperate arrays
    time_array = read_data[:, 0]
    x_accels = read_data[:, 1]
    y_accels = read_data[:, 2]
    z_accels = read_data[:, 3] 

    # convert from g to m/s/s
    x_accels *= 9.797
    y_accels *= 9.797
    z_accels *= 9.797
    z_accels -= 9.797

    # Integrate the raw data
    x_time, x_vel, x_dis = integrate_data(time_array, x_accels)
    y_time, y_vel, y_dis = integrate_data(time_array, y_accels)
    z_time, z_vel, z_dis = integrate_data(time_array, z_accels)
    
    # Graph the displacement over time of raw integrated data
    y_axis_label = "Displacement (m)"
    title = "Displacement (m) - Raw Accel Data"
    image_file_name = "one_min_raw_dis.png"
    graph_data(x_time, y_time, z_time, x_dis, y_dis, z_dis, Y_AXIS=y_axis_label, TITLE=title, FILENAME=image_file_name)


    

    # Remove bias by subtracting the mean
    x_accels -= np.mean(x_accels)
    y_accels -= np.mean(y_accels)
    z_accels -= np.mean(z_accels)

    # Integrate the bias corrected data
    x_time, x_vel_cor, x_dis_cor = integrate_data(time_array, x_accels)
    y_time, y_vel_cor, y_dis_cor = integrate_data(time_array, y_accels)
    z_time, z_vel_cor, z_dis_cor = integrate_data(time_array, z_accels)

    # DATASET 2 - graph displacement
    y_axis_label = "Displacement (m)"
    title = "Displacement (m) - Bias Corrected Accel Data"
    image_file_name = "one_min_no_bias_dis.png"
    graph_data(x_time, y_time, z_time, x_dis_cor, y_dis_cor, z_dis_cor, Y_AXIS=y_axis_label, TITLE=title, FILENAME=image_file_name)
    


    """
    # Remove all noise -- Create a dataset where every value is the mean 
    x_no_noise = np.empty(len(time_array))
    x_no_noise.fill(np.mean(x_accels))
    y_no_noise = np.empty(len(time_array))
    y_no_noise.fill(np.mean(y_accels))
    z_no_noise = np.empty(len(time_array))
    z_no_noise.fill(np.mean(z_accels))

    # Integrate the idealized noise rremoved data
    x_time, x_vel_no_noise, x_dis_no_noise = integrate_data(time_array, x_no_noise)
    y_time, y_vel_no_noise, y_dis_no_noise = integrate_data(time_array, y_no_noise)
    z_time, z_vel_no_noise, z_dis_no_noise = integrate_data(time_array, z_no_noise)

    # DATASET 3 - graph displacement
    y_axis_label = "Displacement (m)"
    title = "Displacement (m) - Bias and Noise Corrected Accel Data"
    image_file_name = "one_min_no_noise_dis.png"
    graph_data(x_time, y_time, z_time, x_dis_no_noise, y_dis_no_noise, z_dis_no_noise, Y_AXIS=y_axis_label, TITLE=title, FILENAME=image_file_name)  
    """
    
    

