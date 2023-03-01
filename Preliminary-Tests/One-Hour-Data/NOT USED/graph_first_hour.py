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


def graph_data_2(x, y, z, x_std, y_std, z_std, TITLE, FILENAME):

    # Graph x, y, and z data on seperate plots.

    fig,axs = plt.subplots(3,1)

    trials = range(60)

    axs[0].errorbar(trials, x, yerr=x_std, color='r')
    axs[1].errorbar(trials, y, yerr=y_std, color='b')
    axs[2].errorbar(trials, z, yerr=z_std, color='g')
    axs[0].set_ylabel('X [g]')
    axs[1].set_ylabel('Y [g]')
    axs[2].set_ylabel('Z [g]')
    axs[2].set_xlabel('Minutes')
    #axs.set_ylim([-2,2])
    axs[0].set_title(TITLE)
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
    print("Means: ", x_mean, " ", y_mean, " ", z_mean)

    # calcualte standard deviations
    x_sd = np.std(x_accels)
    y_sd = np.std(y_accels)
    z_sd = np.std(z_accels)
    #print("Std Devs: ", x_sd, " ", y_sd, " ", z_sd)
    
    #graph histograms because normal distribution curve does not fit well
    #graph_hist(x_accels, 'r', "Acceleration Histogram X-Axis: mean = %.4f, std = %.4f" % (x_mean, x_sd), "x_hist_1_hrs.png") 
    #graph_hist(y_accels, 'b', "Acceleration Histogram Y-Axis: mean = %.4f, std = %.4f" % (y_mean, y_sd), "y_hist_1_hrs.png") 
    #graph_hist(z_accels, 'g', "Acceleration Histogram Z-Axis: mean = %.4f, std = %.4f" % (z_mean, z_sd), "z_hist_1_hrs.png") 
    
    # Split data into individual minutes
    x_means = []
    y_means = []
    z_means = []

    num_minute = int(len(time_array) / 60)
    print(num_minute)
    for ii in range (0, 60):
        x_means.append(np.mean(x_accels[0+num_minute*ii:num_minute+num_minute*ii]))
        y_means.append(np.mean(y_accels[0+num_minute*ii:num_minute+num_minute*ii]))
        z_means.append(np.mean(z_accels[0+num_minute*ii:num_minute+num_minute*ii]))
    
    print("X Means: ", np.mean(x_means))
    print("Y Means: ", np.mean(y_means))
    print("Z Means: ", np.mean(z_means))
    print("X Means Std: ", np.std(x_means))
    print("Y Means Std: ", np.std(y_means))
    print("Z Means Std: ", np.std(z_means))

    graph_data_2(x_means, y_means, z_means, np.std(x_means), np.std(y_means), np.std(z_means)
                        ,  TITLE="Mean (g) of Each One Minute of First Hour", FILENAME="minute_means_first_hour_w_uncertainty.png")