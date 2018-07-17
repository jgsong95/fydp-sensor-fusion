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

# compute H
# def calculate_jacobian(px, py, pz, THRESH = 0.0001, ZERO_REPLACEMENT = 0.0001):
#     """
#       Calculates the Jacobian given for four state variables
#       Args:
#         px, py, pz : floats - 3 state variables
#         THRESH - minimum value of squared distance to return a non-zero matrix
#         ZERO_REPLACEMENT - value to replace zero to avoid division by zero error
#       Returns:
#         H : the jacobian matrix expressed as a 3 x 3 numpy matrix with float values
#     """
#
#     d_squared = px * px + py*py + pz* pz
#     d = sqrt(d_squared)
#     d_cubed = d_squared * d
#
#     if d_squared < THRESH:
#         H = np.matrix(np.zeros(3, 3))
#
#
#     else:
#
#         r11 = px / d
#         r12 = py / d
#         r13 = py / d
#
#         r21 = -py / d_squared
#         r22 = px / d_squared
#         r23 =
#
#         r31 = py * (vx * py - vy * px) / d_cubed
#         r32 = px * (vy * px - vx * py) / d_cubed
#         r33 = pz * ()
#
#         H = np.matrix([[r11, r12, 0, 0],
#                        [r21, r22, 0, 0],
#                        [r31, r32, r11, r12]])
#
#     return H

class FusionEKF(EKF):

    def __init__(self, dt):
        EKF.__init__(self, 3, 3)
        self.dt = dt

    def predict(self):
        return 0

    def update(self):
        return 0
