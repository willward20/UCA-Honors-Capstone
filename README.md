# Investigating MEMS Accelerometer Calibration Techniques

<img src="https://github.com/willward20/UCA-Honors-Capstone/blob/main/media/connections.jpg" width="270" align="left"/> <img src="https://github.com/willward20/UCA-Honors-Capstone/blob/main/media/Final%20Displacement1024_1.jpg" width="250" /> <img src="https://github.com/willward20/UCA-Honors-Capstone/blob/main/media/IMU_axes.png" width="230" /> <img src="https://github.com/willward20/UCA-Honors-Capstone/blob/main/media/USP_Seal_300.png" width="200" align="right"/> 

### Summary

Collect and calibrate linear acceleration data from an MPU-9250 accelerometer using a Raspberry Pi and simple python scripts. Use the calibrated acceleration to estimate the change in position of the sensor over time. 

### Abstract

Triaxial microelectromechanical systems (MEMS) accelerometers are inertial sensors
that measure linear acceleration along three orthogonal axes. In many robotics applications,
accelerometers help track a robot’s relative displacement. However, displacement estimates
derived from an accelerometer’s raw measurements drift significantly over time from ground
truth values during the derivation process due to accumulated errors in acceleration
measurements. While accelerometers can be combined with other sensors to reduce the effect of
displacement estimation drifting, calibrating accelerometers themselves before use is still
essential, especially for very low-cost applications. This study investigates methods of
calibrating a low-cost MEMS accelerometer using least-squares fitting, primarily concentrated
on removing systematic error from acceleration signals.

### Contents

[Thesis.pdf](https://github.com/willward20/UCA-Honors-Capstone/blob/main/Thesis.pdf) is a PDF of my written thesis, which includes information about the project background, experimental methodology, data analysis, and conclusions.
* **Chapter 1:** Background information about accelerometers, linear displacement estimates, and the need for calibration
* **Chapter 2:** Literature review of calibration techniques including error modeling, least-squares optimization, and data collection procedures
* **Chapter 3:** Methodology, including hardware and software setup, preliminary tests performed, statistical analysis, data collection procedures, and calibration procedures
* **Chapter 4:** Results and analysis
* **Chapter 5:** Project conclusions and error analysis

The [Best-Calibration-Method](https://github.com/willward20/UCA-Honors-Capstone/tree/main/Best-Calibration-Method) folder contains the three programs needed to implement the most successful calibration method I used. In my analysis, I found that a calibration method that removes bias from both the acceleration and displacement data performed better than a calibration method that only removes acceleration bias. The [Preliminary-Tests](https://github.com/willward20/UCA-Honors-Capstone/tree/main/Preliminary-Tests) folder contains code and data of my preliminary tests. These tests were used to ensure that accelerometer calibration was feasible. Finally, the [Six-Position-Test](https://github.com/willward20/UCA-Honors-Capstone/tree/main/Six-Position-Test) folder contains the code and data from my initial calibration experiments. 

This capstone project was completed to fulfill my undergraduate thesis requirement for the [University Scholars Program](https://uca.edu/honors/usp/) at the University of Central Arkansas. I graduated from UCA with a Bachelor's of Science in [Engineering Physics](https://uca.edu/physics/engineering-physics/) in May 2023. 
