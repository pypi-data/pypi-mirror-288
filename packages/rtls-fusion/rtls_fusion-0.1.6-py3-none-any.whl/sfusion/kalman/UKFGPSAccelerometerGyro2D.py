# sfusion/kalman/UKFGPSAccelerometerGyro2D.py

import numpy as np

class UKFGPSAccelerometerGyro2D:
    def __init__(self, initial_state, initial_covariance, process_noise, measurement_noise):
        """
        Initialize the Unscented Kalman Filter for 2D GPS with accelerometer and gyroscope input.

        :param initial_state: Initial state vector [x_position, y_position, x_velocity, y_velocity, orientation].
        :param initial_covariance: Initial covariance matrix.
        :param process_noise: Process noise covariance matrix.
        :param measurement_noise: Measurement noise covariance matrix.
        """
        self.state = np.array(initial_state)
        self.covariance = np.array(initial_covariance)
        self.process_noise = np.array(process_noise, dtype=float)
        self.measurement_noise = np.array(measurement_noise, dtype=float)
        self.alpha = 0.75
        self.beta = 2
        self.kappa = 50
        self.n = self.state.shape[0]
        self.lambda_ = self.alpha**2 * (self.n + self.kappa) - self.n

    def sigma_points(self, state, covariance):
        sigma_points = np.zeros((2 * self.n + 1, self.n))
        sigma_points[0] = state
        sqrt_matrix = np.linalg.cholesky((self.n + self.lambda_) * covariance)
        
        for i in range(self.n):
            sigma_points[i + 1] = state + sqrt_matrix[i]
            sigma_points[self.n + i + 1] = state - sqrt_matrix[i]
        
        return sigma_points

    def predict_sigma_points(self, sigma_points, dt, control_input):
        predicted_sigma_points = np.zeros_like(sigma_points)
        for i, point in enumerate(sigma_points):
            x, y, vx, vy, theta = point
            ax, ay, omega = control_input

            theta_pred = theta + omega * dt

            ax_global = ax * np.cos(theta) - ay * np.sin(theta)
            ay_global = ax * np.sin(theta) + ay * np.cos(theta)

            x_pred = x + vx * dt + 0.5 * ax_global * dt**2
            y_pred = y + vy * dt + 0.5 * ay_global * dt**2
            vx_pred = vx + ax_global * dt
            vy_pred = vy + ay_global * dt

            predicted_sigma_points[i] = [x_pred, y_pred, vx_pred, vy_pred, theta_pred]
        
        return predicted_sigma_points

    def predict(self, dt, control_input):
        sigma_points = self.sigma_points(self.state, self.covariance)
        self.predicted_sigma_points = self.predict_sigma_points(sigma_points, dt, control_input)
        
        weights_mean = np.zeros(2 * self.n + 1)
        weights_cov = np.zeros(2 * self.n + 1)
        weights_mean[0] = self.lambda_ / (self.n + self.lambda_)
        weights_cov[0] = weights_mean[0] + (1 - self.alpha**2 + self.beta)
        for i in range(1, 2 * self.n + 1):
            weights_mean[i] = 1 / (2 * (self.n + self.lambda_))
            weights_cov[i] = weights_mean[i]
        
        self.state = np.sum(weights_mean[:, np.newaxis] * self.predicted_sigma_points, axis=0)
        
        self.covariance = self.process_noise.copy()
        for i in range(2 * self.n + 1):
            diff = self.predicted_sigma_points[i] - self.state
            self.covariance += weights_cov[i] * np.outer(diff, diff)

    def update(self, measurement):
        predicted_measurements = np.zeros((2 * self.n + 1, 2))
        
        for i, point in enumerate(self.predicted_sigma_points):
            x, y, vx, vy, theta = point
            predicted_measurements[i] = [x, y]
        
        weights_mean = np.zeros(2 * self.n + 1)
        weights_cov = np.zeros(2 * self.n + 1)
        weights_mean[0] = self.lambda_ / (self.n + self.lambda_)
        weights_cov[0] = weights_mean[0] + (1 - self.alpha**2 + self.beta)
        for i in range(1, 2 * self.n + 1):
            weights_mean[i] = 1 / (2 * (self.n + self.lambda_))
            weights_cov[i] = weights_mean[i]

        z_pred = np.sum(weights_mean[:, np.newaxis] * predicted_measurements, axis=0)
        
        S = self.measurement_noise.copy()
        for i in range(2 * self.n + 1):
            diff = predicted_measurements[i] - z_pred
            S += weights_cov[i] * np.outer(diff, diff)
        
        cross_covariance = np.zeros((self.n, 2))
        for i in range(2 * self.n + 1):
            state_diff = self.predicted_sigma_points[i] - self.state
            measurement_diff = predicted_measurements[i] - z_pred
            cross_covariance += weights_cov[i] * np.outer(state_diff, measurement_diff)
        
        K = np.dot(cross_covariance, np.linalg.inv(S))
        self.state += np.dot(K, (measurement - z_pred))
        self.covariance -= np.dot(K, np.dot(S, K.T))