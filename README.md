# UCA-Honors-Capstone

For my undergradaute honors thesis, I investigated calibrating a MEMS accelerometer using six-position data collection to improve the sensor's measurements. This GitHub repository contains all of the code used to collect and calibrate data using an MPU-9250 accelerometer and a Raspberry Pi 4. Overall, the method used to calibrate the sensor signifcantly reduced the amount of drift in displacement calculations over a 60 second period, even though error in acceleration measurements will always exist. For a complete analysis of the project results, a PDF of my thesis is included in this repository. The capstone was completed in partial fulfillment of the requirements for the University Scholars Program at the University of Central Arkansas. I graduated from UCA with a Bachelor's of Science in Engineering Physics in May 2023. 

**Abstract**: Triaxial microelectromechanical systems (MEMS) accelerometers are inertial sensors
that measure linear acceleration along three orthogonal axes. In many robotics applications,
accelerometers help track a robot’s relative displacement. However, displacement estimates
derived from an accelerometer’s raw measurements drift significantly over time from ground
truth values during the derivation process due to accumulated errors in acceleration
measurements. While accelerometers can be combined with other sensors to reduce the effect of
displacement estimation drifting, calibrating accelerometers themselves before use is still
essential, especially for very low-cost applications. This study investigates methods of
calibrating a low-cost MEMS accelerometer using least-squares fitting, primarily concentrated
on removing systematic error from acceleration signals.

# Contents

The Preliminary-Tests and Six-Position-Test folders contain all of the code used to collect calibration testing data during the project. The folders also contain all plots generated for my thesis document (Thesis.pdf). In my analysis, I found that a calibration method that removes bias from both the acceleration and displacement data performed better than the other methods I tested. The Best-Calibration-Method folder contains the code used in implementing this method.