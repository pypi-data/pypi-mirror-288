# sfusion/particle/PFGPSAccelerometerGyro2D.py

import numpy as np

class PFGPSAccelerometerGyro2D:
    def __init__(self, initial_state, initial_covariance, process_noise, measurement_noise, num_particles=1000):
        """
        Initialize the Particle Filter for 2D GPS with accelerometer and gyroscope input.

        :param initial_state: Initial state vector [x_position, y_position, x_velocity, y_velocity, orientation].
        :param initial_covariance: Initial covariance matrix.
        :param process_noise: Process noise covariance matrix.
        :param measurement_noise: Measurement noise covariance matrix.
        :param num_particles: Number of particles.
        """
        self.num_particles = num_particles
        self.particles = np.random.multivariate_normal(initial_state, initial_covariance, num_particles)
        self.weights = np.ones(num_particles) / num_particles
        self.process_noise = process_noise
        self.measurement_noise = measurement_noise

    def predict(self, dt, control_input):
        """
        Predict the next state for each particle.
        
        :param dt: Time step.
        :param control_input: Control input (acceleration and angular velocity) [x_acceleration, y_acceleration, angular_velocity].
        """
        ax, ay, omega = control_input

        for i in range(self.num_particles):
            x, y, vx, vy, theta = self.particles[i]

            theta += omega * dt

            ax_global = ax * np.cos(theta) - ay * np.sin(theta)
            ay_global = ax * np.sin(theta) + ay * np.cos(theta)

            x += vx * dt + 0.5 * ax_global * dt**2
            y += vy * dt + 0.5 * ay_global * dt**2
            vx += ax_global * dt
            vy += ay_global * dt

            self.particles[i] = np.array([x, y, vx, vy, theta]) + np.random.multivariate_normal([0, 0, 0, 0, 0], self.process_noise)

    def update(self, measurement):
        """
        Update the weights of the particles based on the new measurement.
        
        :param measurement: New measurement for [x_position, y_position].
        """
        for i in range(self.num_particles):
            x, y, _, _, _ = self.particles[i]
            predicted_measurement = np.array([x, y])
            self.weights[i] = self.gaussian_likelihood(measurement, predicted_measurement, self.measurement_noise)
        
        self.weights += 1.e-300  # Avoid division by zero
        self.weights /= sum(self.weights)  # Normalize

        self.resample()

    def gaussian_likelihood(self, measurement, predicted_measurement, measurement_noise):
        """
        Calculate the likelihood of a measurement given the predicted measurement and measurement noise.
        
        :param measurement: Actual measurement.
        :param predicted_measurement: Predicted measurement.
        :param measurement_noise: Measurement noise covariance matrix.
        """
        error = measurement - predicted_measurement
        return np.exp(-0.5 * np.dot(error.T, np.dot(np.linalg.inv(measurement_noise), error))) / np.sqrt(np.linalg.det(2 * np.pi * measurement_noise))

    def resample(self):
        """
        Resample particles based on their weights.
        """
        cumulative_sum = np.cumsum(self.weights)
        cumulative_sum[-1] = 1.  # Avoid rounding errors
        indexes = np.searchsorted(cumulative_sum, np.random.rand(self.num_particles))

        self.particles[:] = self.particles[indexes]
        self.weights.fill(1.0 / self.num_particles)

    def get_state(self):
        """
        Get the estimated state as the mean of the particles.
        """
        return np.average(self.particles, weights=self.weights, axis=0)
