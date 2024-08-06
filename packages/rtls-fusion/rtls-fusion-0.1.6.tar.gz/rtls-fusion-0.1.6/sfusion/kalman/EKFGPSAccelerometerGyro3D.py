# sfusion/kalman/EKFGPSAccelerometerGyro3D.py

import numpy as np

class EKFGPSAccelerometerGyro3D:
    def __init__(self, initial_state, initial_covariance, process_noise, measurement_noise):
        """
        Initialize the Extended Kalman Filter for 3D GPS with accelerometer and gyroscope input.

        :param initial_state: Initial state vector [x_position, y_position, z_position, x_velocity, y_velocity, z_velocity, orientation_x, orientation_y, orientation_z].
        :param initial_covariance: Initial covariance matrix.
        :param process_noise: Process noise covariance matrix.
        :param measurement_noise: Measurement noise covariance matrix.
        """
        self.state = np.array(initial_state)  # State vector
        self.covariance = np.array(initial_covariance)  # Covariance matrix
        self.process_noise = np.array(process_noise)  # Process noise covariance matrix
        self.measurement_noise = np.array(measurement_noise)  # Measurement noise covariance matrix

    def predict(self, dt, control_input):
        x, y, z, vx, vy, vz, theta_x, theta_y, theta_z = self.state
        ax, ay, az, omega_x, omega_y, omega_z = control_input

        # Update orientations
        theta_x_pred = theta_x + omega_x * dt
        theta_y_pred = theta_y + omega_y * dt
        theta_z_pred = theta_z + omega_z * dt

        # Convert local accelerations to global coordinates using intrinsic rotations
        R_x = np.array([
            [1, 0, 0],
            [0, np.cos(theta_x), -np.sin(theta_x)],
            [0, np.sin(theta_x), np.cos(theta_x)]
        ])
        
        R_y = np.array([
            [np.cos(theta_y), 0, np.sin(theta_y)],
            [0, 1, 0],
            [-np.sin(theta_y), 0, np.cos(theta_y)]
        ])
        
        R_z = np.array([
            [np.cos(theta_z), -np.sin(theta_z), 0],
            [np.sin(theta_z), np.cos(theta_z), 0],
            [0, 0, 1]
        ])
        
        # Combined rotation matrix
        R = R_z @ R_y @ R_x
        
        # Local acceleration vector
        local_acceleration = np.array([ax, ay, az])
        
        # Global acceleration vector
        global_acceleration = R @ local_acceleration
        
        # # Exclude the gravity component from the global z-component
        # global_acceleration[2] -= 9.81  # Assuming the gravity is 9.81 m/s^2

        ax_global, ay_global, az_global = global_acceleration

        # State prediction using the process model
        x_pred = x + vx * dt + 0.5 * ax_global * dt**2
        y_pred = y + vy * dt + 0.5 * ay_global * dt**2
        z_pred = z + vz * dt + 0.5 * az_global * dt**2
        vx_pred = vx + ax_global * dt
        vy_pred = vy + ay_global * dt
        vz_pred = vz + az_global * dt

        self.state = np.array([x_pred, y_pred, z_pred, vx_pred, vy_pred, vz_pred, theta_x_pred, theta_y_pred, theta_z_pred])

        # Jacobian of the process model
        self.F = jacobian_F(self.state, dt, control_input)

        # Predicted covariance
        self.covariance = self.F @ self.covariance @ self.F.T + self.process_noise

    def update(self, measurement):
        """
        Update the state and covariance with the new measurement.
        
        :param measurement: New measurement for [x_position, y_position, z_position].
        """
        # Measurement matrix (Jacobian of the measurement model)
        H = np.array([[1, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 1, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 1, 0, 0, 0, 0, 0, 0]])

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
        self.covariance = (np.eye(9) - K @ H) @ self.covariance


def jacobian_F(state, dt, control_input):
    _, _, _, vx, vy, vz, theta_x, theta_y, theta_z = state
    ax, ay, az, _, _, _ = control_input

    # Precompute trigonometric functions
    cos_x = np.cos(theta_x)
    sin_x = np.sin(theta_x)
    cos_y = np.cos(theta_y)
    sin_y = np.sin(theta_y)
    cos_z = np.cos(theta_z)
    sin_z = np.sin(theta_z)

    # Compute partial derivatives for ax_global
    dax_global_dtheta_x = ay * (cos_x * sin_y * cos_z + sin_x * sin_z) + az * (-sin_x * sin_y * cos_z + cos_x * sin_z)
    dax_global_dtheta_y = -ax * sin_y * cos_z + ay * (sin_x * cos_y * cos_z) + az * (cos_x * cos_y * cos_z)
    dax_global_dtheta_z = -ax * cos_y * sin_z + ay * (-sin_x * sin_y * sin_z - cos_x * cos_z) + az * (-cos_x * sin_y * sin_z + sin_x * cos_z)

    # Compute partial derivatives for ay_global
    day_global_dtheta_x = ay * (cos_x * sin_y * sin_z - sin_x * cos_z) + az * (-sin_x * sin_y * sin_z - cos_x * cos_z)
    day_global_dtheta_y = -ax * sin_y * sin_z + ay * (sin_x * cos_y * sin_z) + az * (cos_x * cos_y * sin_z)
    day_global_dtheta_z = ax * cos_y * cos_z + ay * (sin_x * sin_y * cos_z - cos_x * sin_z) + az * (cos_x * sin_y * cos_z + sin_x * sin_z)

    # Compute partial derivatives for az_global
    daz_global_dtheta_x = ay * cos_x * cos_y - az * sin_x * cos_y
    daz_global_dtheta_y = -ax * cos_y - ay * sin_x * sin_y - az * cos_x * sin_y
    daz_global_dtheta_z = 0  # az_global does not depend on theta_z

    # Jacobian matrix
    F = np.array([
        [1, 0, 0, dt, 0, 0, 0.5 * dt**2 * dax_global_dtheta_x, 0.5 * dt**2 * dax_global_dtheta_y, 0.5 * dt**2 * dax_global_dtheta_z],
        [0, 1, 0, 0, dt, 0, 0.5 * dt**2 * day_global_dtheta_x, 0.5 * dt**2 * day_global_dtheta_y, 0.5 * dt**2 * day_global_dtheta_z],
        [0, 0, 1, 0, 0, dt, 0.5 * dt**2 * daz_global_dtheta_x, 0.5 * dt**2 * daz_global_dtheta_y, 0.5 * dt**2 * daz_global_dtheta_z],
        [0, 0, 0, 1, 0, 0, dt * dax_global_dtheta_x, dt * dax_global_dtheta_y, dt * dax_global_dtheta_z],
        [0, 0, 0, 0, 1, 0, dt * day_global_dtheta_x, dt * day_global_dtheta_y, dt * day_global_dtheta_z],
        [0, 0, 0, 0, 0, 1, dt * daz_global_dtheta_x, dt * daz_global_dtheta_y, dt * daz_global_dtheta_z],
        [0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1]
    ])
    
    return F
