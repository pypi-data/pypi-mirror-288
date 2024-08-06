# sfusion/kalman/EKFGPSPolar2D.py

import numpy as np

class EKFGPSPolar2D:
    def __init__(self, initial_state, initial_covariance, process_noise, measurement_noise):
        """
        Initialize the Extended Kalman Filter for 2D GPS in polar coordinates.

        :param initial_state: Initial state vector [x_position, y_position, s_velocity, theta_angle].
        :param initial_covariance: Initial covariance matrix.
        :param process_noise: Process noise covariance matrix.
        :param measurement_noise: Measurement noise covariance matrix.
        """
        self.state = np.array(initial_state)  # State vector [x_position, y_position, s_velocity, theta_angle]
        self.covariance = np.array(initial_covariance)  # Covariance matrix
        self.process_noise = np.array(process_noise)  # Process noise covariance matrix
        self.measurement_noise = np.array(measurement_noise)  # Measurement noise covariance matrix

    def predict(self, dt):
        """
        Predict the next state and covariance.
        
        :param dt: Time step.
        """
        # State transition function
        x, y, s, theta = self.state
        x_pred = x + s * np.cos(theta) * dt
        y_pred = y + s * np.sin(theta) * dt
        s_pred = s
        theta_pred = theta

        self.state = np.array([x_pred, y_pred, s_pred, theta_pred])

        # Jacobian of the state transition function
        F = np.array([[1, 0, np.cos(theta) * dt, -s * np.sin(theta) * dt],
                      [0, 1, np.sin(theta) * dt,  s * np.cos(theta) * dt],
                      [0, 0, 1, 0],
                      [0, 0, 0, 1]])

        # Predicted covariance
        self.covariance = F @ self.covariance @ F.T + self.process_noise

    def update(self, measurement):
        """
        Update the state and covariance with the new measurement.
        
        :param measurement: New measurement for [x_position, y_position].
        """
        # Measurement matrix
        H = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0]])

        # Measurement residual
        y = measurement - H @ self.state

        # Residual covariance
        S = H @ self.covariance @ H.T + self.measurement_noise

        # Kalman gain
        K = self.covariance @ H.T @ np.linalg.inv(S)

        # Updated state
        self.state = self.state + K @ y

        # Updated covariance
        self.covariance = (np.eye(4) - K @ H) @ self.covariance
