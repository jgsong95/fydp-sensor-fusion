import numpy as np
from math import sin, cos, sqrt
from filterpy.kalman import ExtendedKalmanFilter as EKF


#  x - state vector
#  P - uncertainty covariance matrix of state x (process covariance)
#  z - measurement vector
#  R - uncertainty covariance matrix of sensor that produces z (measurement covariance)
#  F - update matrix - used to get predicted x - based on time elapsed and assumed dynamic model being tracked
#  H - extraction matrix - used to extract the hypothetical measurement if state x is correct and the sensor is perfect
#  Q - noise covariance matrix - adds uncertainty to the process covariance
#  S - 'innovation' covariance that combines process covariance and measurement covariance
#  y - difference between the actual measurement and the predicted measurement
#  K - Kalman gain - contains information on how much weight to place on the current prediction and current observed measurement
#    - that will result the final fused updated state vector and process covariance matrix
#    - computed from P (process covariance), H (extraction), R (measurement covariance)

class FusionEKF:



    def __init__(self):
        self.dt = 0.5
        self.proccess_error = 0.05
        self.ekf = EKF(3, 3)
        self.ekf.Q = np.array([[0, 0, 0],
                               [0, 0, 0],
                               [0, 0, 0]])


    def run(self, data):

        true_position = []

        for i in range(int(20/self.dt)):
            z = data

            self.ekf.update(np.asarray([z.lidar.data]), self.H_of, self.hx, R=self.hx(self.ekf.x)*self.proccess_error)
            self.ekf.predict()

            self.ekf.update(np.asarray([z.camera.data]), self.H_of, self.hx, R=self.hx(self.ekf.x)*self.proccess_error)
            self.ekf.predict()

            true_position.append(self.ekf.x)

    def H_of(self, x):
        return 0


    def hx(self, x):
        return 0


    def fx(self, x):
        return np.dot(self.efk.F, x)




    # Set intial guess to first data input, camera or lidar

