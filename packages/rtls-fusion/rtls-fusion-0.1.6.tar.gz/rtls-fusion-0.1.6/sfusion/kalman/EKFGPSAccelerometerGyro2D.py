# sfusion/kalman/EKFGPSAccelerometerGyro2D.py

import numpy as np

class EKFGPSAccelerometerGyro2D:
    def __init__(self, initial_state, initial_covariance, process_noise, measurement_noise):
        """
        Initialize the Extended Kalman Filter for 2D GPS with accelerometer and gyroscope input.

        :param initial_state: Initial state vector [x_position, y_position, x_velocity, y_velocity, orientation].
        :param initial_covariance: Initial covariance matrix.
        :param process_noise: Process noise covariance matrix.
        :param measurement_noise: Measurement noise covariance matrix.
        """
        self.state = np.array(initial_state)  # State vector [x_position, y_position, x_velocity, y_velocity, orientation]
        self.covariance = np.array(initial_covariance)  # Covariance matrix
        self.process_noise = np.array(process_noise)  # Process noise covariance matrix
        self.measurement_noise = np.array(measurement_noise)  # Measurement noise covariance matrix

    def predict(self, dt, control_input):
        x, y, vx, vy, theta = self.state
        ax, ay, omega = control_input

        # Update orientation
        theta_pred = theta + omega * dt

        # Convert local accelerations to global coordinates
        ax_global = ax * np.cos(theta) - ay * np.sin(theta)
        ay_global = ax * np.sin(theta) + ay * np.cos(theta)

        # State prediction using the process model
        x_pred = x + vx * dt + 0.5 * ax_global * dt**2
        y_pred = y + vy * dt + 0.5 * ay_global * dt**2
        vx_pred = vx + ax_global * dt
        vy_pred = vy + ay_global * dt

        self.state = np.array([x_pred, y_pred, vx_pred, vy_pred, theta_pred])

        # Jacobian of the process model
        F = np.array([
            [1, 0, dt, 0, -0.5 * dt**2 * (ax * np.sin(theta) + ay * np.cos(theta))],
            [0, 1, 0, dt,  0.5 * dt**2 * (ax * np.cos(theta) - ay * np.sin(theta))],
            [0, 0, 1, 0, -dt * (ax * np.sin(theta) + ay * np.cos(theta))],
            [0, 0, 0, 1,  dt * (ax * np.cos(theta) - ay * np.sin(theta))],
            [0, 0, 0, 0, 1]
        ])

        # Predicted covariance
        self.covariance = F @ self.covariance @ F.T + self.process_noise
    

    def update(self, measurement):
        """
        Update the state and covariance with the new measurement.
        
        :param measurement: New measurement for [x_position, y_position].
        """
        # Measurement matrix (Jacobian of the measurement model)
        H = np.array([[1, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0]])

        # Measurement residual
        Z = np.array(measurement)
        y = Z - H @ self.state

        # Residual covariance
        S = H @ self.covariance @ H.T + self.measurement_noise

        # Kalman gain
        K = self.covariance @ H.T @ np.linalg.inv(S)

        # Updated state
        self.state = self.state + K @ y

        # Updated covariance
        self.covariance = (np.eye(5) - K @ H) @ self.covariance
