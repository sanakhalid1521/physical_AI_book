"""
Example: Sensor Integration and Data Processing
This code demonstrates how to integrate data from multiple sensors
in a humanoid robot perception system.
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class SensorFusion:
    def __init__(self):
        self.imu_data = {'accel': [0, 0, 0], 'gyro': [0, 0, 0], 'timestamp': None}
        self.camera_data = {'image': None, 'features': [], 'timestamp': None}
        self.lidar_data = {'ranges': [], 'timestamp': None}

        # Kalman filter parameters
        self.state = np.array([0, 0, 0, 0])  # [x, y, vx, vy]
        self.covariance = np.eye(4) * 1000  # Initial uncertainty

    def update_imu(self, accel_data, gyro_data):
        """Update IMU data"""
        self.imu_data['accel'] = accel_data
        self.imu_data['gyro'] = gyro_data
        self.imu_data['timestamp'] = datetime.now()

    def update_camera(self, image_data, features):
        """Update camera data"""
        self.camera_data['image'] = image_data
        self.camera_data['features'] = features
        self.camera_data['timestamp'] = datetime.now()

    def update_lidar(self, ranges):
        """Update LIDAR data"""
        self.lidar_data['ranges'] = ranges
        self.lidar_data['timestamp'] = datetime.now()

    def kalman_predict(self, dt):
        """Predict next state using motion model"""
        # State transition matrix (constant velocity model)
        F = np.array([
            [1, 0, dt, 0],
            [0, 1, 0, dt],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

        # Process noise matrix
        Q = np.eye(4) * 0.1

        # Predict state and covariance
        self.state = F @ self.state
        self.covariance = F @ self.covariance @ F.T + Q

    def kalman_update(self, measurement, sensor_type):
        """Update state with sensor measurement"""
        if sensor_type == 'position':
            # Measurement matrix for position
            H = np.array([[1, 0, 0, 0],
                         [0, 1, 0, 0]])

            # Measurement noise
            R = np.eye(2) * 0.5

            # Innovation
            y = measurement - H @ self.state[:4]

            # Innovation covariance
            S = H @ self.covariance[:4, :4] @ H.T + R

            # Kalman gain
            K = self.covariance[:4, :4] @ H.T @ np.linalg.inv(S)

            # Update state and covariance
            self.state[:4] += K @ y
            self.covariance[:4, :4] -= K @ S @ K.T

    def process_sensor_data(self):
        """Process and fuse sensor data"""
        # This is a simplified example
        # In practice, you'd handle time synchronization, calibration, etc.

        # Simulate getting measurements from different sensors
        # with some noise
        true_position = np.array([1.0, 2.0])
        position_measurement = true_position + np.random.normal(0, 0.1, 2)

        # Update the filter
        self.kalman_update(position_measurement, 'position')

        return self.state[:2]  # Return estimated position

def detect_features(image):
    """Simple feature detection (placeholder)"""
    # In a real system, this would use computer vision algorithms
    features = []
    for i in range(5):  # Simulate finding 5 features
        features.append({
            'x': np.random.randint(0, image.shape[1] if len(image.shape) > 1 else 640),
            'y': np.random.randint(0, image.shape[0] if len(image.shape) > 1 else 480),
            'type': 'corner'
        })
    return features

def main():
    fusion = SensorFusion()

    # Simulate sensor readings over time
    estimated_positions = []
    true_positions = []

    for t in range(100):
        dt = 0.1  # 100ms time step

        # Simulate true motion
        true_pos = np.array([0.01 * t, 0.02 * t])  # Moving diagonally

        # Simulate sensor readings with noise
        accel = [0.01 + np.random.normal(0, 0.01), 0.02 + np.random.normal(0, 0.01), -9.81]
        gyro = [0, 0, 0]
        image = np.random.rand(480, 640)  # Simulated image
        features = detect_features(image)
        lidar_ranges = [5 + np.random.normal(0, 0.1) for _ in range(360)]  # 360 degree scan

        # Update sensors
        fusion.update_imu(accel, gyro)
        fusion.update_camera(image, features)
        fusion.update_lidar(lidar_ranges)

        # Predict and update
        fusion.kalman_predict(dt)
        estimated_pos = fusion.process_sensor_data()

        estimated_positions.append(estimated_pos.copy())
        true_positions.append(true_pos.copy())

    # Plot results
    estimated_positions = np.array(estimated_positions)
    true_positions = np.array(true_positions)

    plt.figure(figsize=(10, 6))
    plt.plot(true_positions[:, 0], true_positions[:, 1], 'g-', label='True Position', linewidth=2)
    plt.plot(estimated_positions[:, 0], estimated_positions[:, 1], 'r--', label='Estimated Position', linewidth=2)
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Sensor Fusion: True vs Estimated Position')
    plt.legend()
    plt.grid(True)
    plt.show()

    print("Sensor fusion simulation completed!")

if __name__ == "__main__":
    main()