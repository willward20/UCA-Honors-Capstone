# Six-Position Calibration Method

(Describe this method of collecting data and calibrating. Point out what each of the scripts do.)

### Statistical Analysis
Each trial test data (taken after collecting parameter fitting data) is calibrated using the parameters derived from the respective trial. (Test data from Trial 1 is calibrated using parameters derived from Trial 1). The test data is calibrated using each of the three error models to compare their performances. After calibrating, the mean and standard deviation of the datasets (including the raw, uncalibrated data) are derived. The results are shown below. 

Since the data was taken at rest, we expect the mean acceleration of each axis to be zero (after gravity is removed from the z-axis). In every trial, the error in the mean decreased after calibrating with the bias-only accelerometer model. For the x and y axis, calibrating next with bias and scale factor did not noticeably improve the mean, but it significantly imrpvoed the error in the z-axis (by at least a factor of 10). Finally, when data was calibrated using the model with bias, scale factor, and misalignment, the mean of the x and y axis decreased closer to zero, while the z axis was mostly unaffected. 

When calibrating with the six-position method, the best error model to use for least squares fitting is clearly the model that includes bias, scale factor, and misalignment. 

**Notice how after calibrating with misalignements, in every trial the standard deviation (uncertaitny in one acceleration measurement) is now larger than the mean of the data.** This might have a significant impact on displacement drift, due to high oscillation. ***I'm curious how much the displacment error would improve if noise was removed.***

#### Trial 1
|    Calibration Method Used     | x (mean, stand. dev) | y (mean, stand. dev) | z (mean, stand. dev) |
| :---------------------------:  | :-----------------:  | :-----------------:  | :------------------: |
| Uncalibrated Data   (m/s/s)    |  (0.9617, 0.0258)    |  (0.6050, 0.0549)    |  (-2.2238, 0.0416)   |     
| Bias Calibrated     (m/s/s)    |  (0.0638, 0.0258)    |  (0.1411, 0.0549)    |   (0.2296, 0.0416)   |  
| Add Scale Factors   (m/s/s)    |  (0.0638, 0.0258)    |  (0.1411, 0.0549)    |   (0.0140, 0.0407)   |  
| Add Misalignments   (m/s/s)    | (-0.0252, 0.0258)    |  (0.0367, 0.0549)    |   (0.0139, 0.0407)   | 
  
#### Trial 2
|    Calibration Method Used     | x (mean, stand. dev) | y (mean, stand. dev) | z (mean, stand. dev) |
| :---------------------------:  | :-----------------:  | :-----------------:  | :------------------: |
| Uncalibrated Data (m/s/s)      |  (0.9485, 0.0356)    |  (0.6009, 0.0530)    |  (-2.2028, 0.0437)   |
| Bias Calibrated   (m/s/s)      |  (0.0573, 0.0356)    |  (0.1422, 0.0530)    |   (0.2411, 0.0437)   |
| Add Scale Factors (m/s/s)      |  (0.0573, 0.0356)    |  (0.1421, 0.0530)    |   (0.0261, 0.0427)   |
| Add Misalignments (m/s/s)      | (-0.0194, 0.0356)    |  (0.0355, 0.0529)    |   (0.0261, 0.0427)   |

#### Trial 3
|    Calibration Method Used     | x (mean, stand. dev) | y (mean, stand. dev) | z (mean, stand. dev) |
| :---------------------------:  | :-----------------:  | :-----------------:  | :------------------: |
| Uncalibrated Data (m/s/s)      |  (0.9461, 0.0379)    |  (0.5946, 0.0481)    |  (-2.2079, 0.0425)   |
| Bias Calibrated   (m/s/s)      |  (0.0621, 0.0379)    |  (0.1385, 0.0481)    |   (0.2248, 0.0425)   |
| Add Scale Factors (m/s/s)      |  (0.0621, 0.0379)    |  (0.1385, 0.0481)    |   (0.0056, 0.0416)   |
| Add Misalignments (m/s/s)      | (-0.0165, 0.0379)    |  (0.0335, 0.0482)    |   (0.0056, 0.0416)   |


### Integrating Test Data Over Time

#### Trial 1
|    Calibration Method Used     | x displacement | y displacement | z displacement |
| :---------------------------:  | :-----------:  | :-----------:  | :------------: |
| Uncalibrated Data (m)          |  1731          | 1089           | -4002          |
| Bias Calibrated (m)            |   115          |  254           |   413          |
| Add Scale Factors (m)          |   115          |  254           |    25          |
| Add Misalignments (m)          |   -45          |   66           |    25          |

#### Trial 2
|    Calibration Method Used     | x displacement | y displacement | z displacement |
| :---------------------------:  | :-----------:  | :-----------:  | :------------: |
| Uncalibrated Data (m)          |  1707          | 1081           | -3965          |
| Bias Calibrated (m)            |   103          |  255           |   433          |
| Add Scale Factors (m)          |   103          |  255           |    47          |
| Add Misalignments (m)          |   -35          |   63           |    47          |

#### Trial 3
|    Calibration Method Used     | x displacement | y displacement | z displacement |
| :---------------------------:  | :-----------:  | :-----------:  | :------------: |
| Uncalibrated Data (m)          |  1704          | 1072           | -3974          |
| Bias Calibrated (m)            |   113          |  251           |   404          |
| Add Scale Factors (m)          |   113          |  251           |    10          |
| Add Misalignments (m)          |   -29          |   62           |    10          |


