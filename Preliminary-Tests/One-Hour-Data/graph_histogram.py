
# This script opens collected data from a file and plots it in histogram

# wait 5-sec for IMU to connect
import sys
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

def graph_hist(accels, c, TITLE, FILENAME, binsize):

    fig = plt.figure()
    axs = fig.add_subplot(1,1,1)
    
    plt.hist(accels, bins = binsize, density = True, alpha=0.6, color=c) 
    plt.title(TITLE)

    #axs.set_ylabel('')
    axs.set_xlabel('Acceleration [m/s/s]')
    axs.set_xlim([-0.2, 0.2])
    fig.savefig(FILENAME)

    return





if __name__ == '__main__':
    
    file = open("one_hour_raw_data.csv")
    read_data = np.loadtxt(file, skiprows = 2, delimiter=",", dtype=float)
    time_array = read_data[:, 0]
    x_accels = read_data[:, 1]
    y_accels = read_data[:, 2]
    z_accels = read_data[:, 3]
    
    print("Total Time (minutes): ", time_array[-1]/60)
    print("Frequency (Hz): ", len(x_accels)/(time_array[-1]))

    print("Means: ", np.mean(x_accels)*9.797, " ", np.mean(y_accels)*9.797, " ", np.mean(z_accels)*9.797)

    # center the data around zero g by subtracting the mean
    x_accels -= np.mean(x_accels)
    y_accels -= np.mean(y_accels)
    z_accels -= np.mean(z_accels)

    # convert from g to m/s/s
    x_accels *= 9.797
    y_accels *= 9.797
    z_accels *= 9.797

    

    # calcualte standard deviations
    x_sd = np.std(x_accels)
    y_sd = np.std(y_accels)
    z_sd = np.std(z_accels)
    print("Std Devs: ", x_sd, " ", y_sd, " ", z_sd)
    print("SDOMs: ", x_sd/np.sqrt(len(time_array)), " ", y_sd/np.sqrt(len(time_array)), " ", z_sd/np.sqrt(len(time_array)))
    exit()
    #graph histograms because normal distribution curve does not fit well
    graph_hist(x_accels, 'r', "Acceleration Over One Hour X-Axis (Standard Dev. = %.3f m/s/s)" % (x_sd), "x_hist_1_hrs_m_s_s.png", binsize=200)
    graph_hist(y_accels, 'b', "Acceleration Over One Hour Y-Axis (Standard Dev. = %.3f m/s/s)" % (y_sd), "y_hist_1_hrs_m_s_s.png", binsize=300)
    graph_hist(z_accels, 'g', "Acceleration Over One Hour Z-Axis (Standard Dev. = %.3f m/s/s)" % (z_sd), "z_hist_1_hrs_m_s_s.png", binsize=300)
    
    
