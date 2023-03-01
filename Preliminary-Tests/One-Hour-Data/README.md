# One Hour Processing
Data collected over one hour while the sensor is at rest on a roughly level surface. (This is the first hour of the 15-Hours-Data)

## Centered Histogram Plots
A histogram is created for each axis of the one hour data to show the spread. The histogram is centered (mean subtracted from all values) because the accelerometer was not on a perfectly level table. Therefore the mean is meaningless because we have no reliable point of reference to compare it to. It serves only as way to compare orders of magnitude with the SDOM.

## ***Plots***
***This folder contains plots of the data integrated over time, after bias (mean) and sometimes noise are removed. Bias is removed by subtracting the mean of the data from every acceleration point. Noise is eliminated by replacing every datapoint with the mean*** **I don't think this should be included in the capstone because it is not a good way of removing noise.**