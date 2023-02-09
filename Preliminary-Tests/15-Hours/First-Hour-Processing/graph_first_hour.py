##################################################################
# Program Name: graph_data_and_historgram.py
# Written by: Will Ward
#  
# Function:
#     1.  
###################################################################

# wait 5-sec for IMU to connect
import time,sys
sys.path.append('../')
import numpy as np
import matplotlib.pyplot as plt




def graph_data(times, accels, TITLE, FILENAME, c):

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)

    plt.scatter(times, accels, s=1, color=c)
    axs.set_ylabel('Acceleration [g]')
    axs.set_xlabel('Time (hours)')
    #axs.set_ylim([-2,2])
    axs.set_title(TITLE)
    fig.savefig(FILENAME)

    return

def graph_hist(accels, c, TITLE, FILENAME):

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)
    
    plt.hist(accels, bins = 200, density = True, alpha=0.6, color=c) 
    plt.title(TITLE)

    #axs.set_ylabel('')
    axs.set_xlabel('Acceleration [g]')
    fig.savefig(FILENAME)

    return




if __name__ == '__main__':
    
    file = open("one_hour_raw_data.csv")
    read_data = np.loadtxt(file, skiprows = 2, delimiter=",", dtype=float)
    time_array = read_data[:, 0]
    x_accels = read_data[:, 1]
    y_accels = read_data[:, 2]
    z_accels = read_data[:, 3]
    
    #print("Total Time (hours): ", time_array[-1])
    #print("Frequency (Hz): ", len(x_accels)/(time_array[-1]*60*60))

    #graph_data(time_array, x_accels, "Acceleration over 15 Hours (x-axis)", "x_axis_15_hrs.png", 'r')
    #graph_data(time_array, y_accels, "Acceleration over 15 Hours (y-axis)", "y_axis_15_hrs.png", 'b')
    #graph_data(time_array, z_accels, "Acceleration over 15 Hours (z-axis)", "z_axis_15_hrs.png", 'g')
    
    
    # calculate means
    x_mean = np.mean(x_accels)
    y_mean = np.mean(y_accels)
    z_mean = np.mean(z_accels)
    #print("Means: ", x_mean, " ", y_mean, " ", z_mean)

    # calcualte standard deviations
    x_sd = np.std(x_accels)
    y_sd = np.std(y_accels)
    z_sd = np.std(z_accels)
    #print("Std Devs: ", x_sd, " ", y_sd, " ", z_sd)
    
    #graph histograms because normal distribution curve does not fit well
    graph_hist(x_accels, 'r', "Acceleration Histogram X-Axis: mean = %.4f, std = %.4f" % (x_mean, x_sd), "x_hist_1_hrs.png") 
    graph_hist(y_accels, 'b', "Acceleration Histogram Y-Axis: mean = %.4f, std = %.4f" % (y_mean, y_sd), "y_hist_1_hrs.png") 
    graph_hist(z_accels, 'g', "Acceleration Histogram Z-Axis: mean = %.4f, std = %.4f" % (z_mean, z_sd), "z_hist_1_hrs.png") 
    
    
