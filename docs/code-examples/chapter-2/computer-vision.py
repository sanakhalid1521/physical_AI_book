"""
Example: Computer Vision for Robotics
This code demonstrates computer vision algorithms for humanoid robot applications,
including object detection and tracking.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist

class ObjectDetector:
    def __init__(self):
        self.known_objects = {}  # Database of known objects
        self.tracked_objects = {}  # Currently tracked objects
        self.next_id = 0

    def detect_objects(self, image):
        """Detect objects in an image using traditional computer vision methods"""
        # Convert to grayscale for processing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Use thresholding to segment objects
        _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detections = []
        for contour in contours:
            # Filter by area to remove noise
            if cv2.contourArea(contour) > 100:
                # Get bounding box
                x, y, w, h = cv2.boundingRect(contour)
                center_x = x + w // 2
                center_y = y + h // 2

                # Calculate features for identification
                aspect_ratio = float(w) / h
                extent = float(cv2.contourArea(contour)) / (w * h)

                detection = {
                    'bbox': (x, y, w, h),
                    'center': (center_x, center_y),
                    'aspect_ratio': aspect_ratio,
                    'extent': extent,
                    'area': cv2.contourArea(contour)
                }

                detections.append(detection)

        return detections

    def track_objects(self, detections, max_distance=50):
        """Associate detections with existing tracks"""
        # If no existing tracks, create new ones
        if not self.tracked_objects:
            for detection in detections:
                self.tracked_objects[self.next_id] = {
                    'id': self.next_id,
                    'bbox': detection['bbox'],
                    'center': detection['center'],
                    'history': [detection['center']]
                }
                self.next_id += 1
            return list(self.tracked_objects.values())

        # Get current tracked centers
        tracked_centers = np.array([obj['center'] for obj in self.tracked_objects.values()])

        # Get detection centers
        detection_centers = np.array([det['center'] for det in detections])

        if len(tracked_centers) > 0 and len(detection_centers) > 0:
            # Calculate distances between tracked objects and detections
            distances = cdist(tracked_centers, detection_centers)

            # Associate closest objects within distance threshold
            for i, tracked_obj_id in enumerate(self.tracked_objects.keys()):
                if len(detection_centers) > 0:
                    # Find closest detection to this tracked object
                    closest_det_idx = np.argmin(distances[i])
                    if distances[i, closest_det_idx] < max_distance:
                        # Update tracked object with new detection
                        detection = detections[closest_det_idx]
                        self.tracked_objects[tracked_obj_id]['bbox'] = detection['bbox']
                        self.tracked_objects[tracked_obj_id]['center'] = detection['center']
                        self.tracked_objects[tracked_obj_id]['history'].append(detection['center'])

                        # Remove this detection from consideration
                        detection_centers = np.delete(detection_centers, closest_det_idx, axis=0)
                        detections = [det for j, det in enumerate(detections) if j != closest_det_idx]

        # Create new tracks for unassociated detections
        for detection in detections:
            self.tracked_objects[self.next_id] = {
                'id': self.next_id,
                'bbox': detection['bbox'],
                'center': detection['center'],
                'history': [detection['center']]
            }
            self.next_id += 1

        return list(self.tracked_objects.values())

def simulate_video_sequence():
    """Simulate a video sequence with moving objects"""
    frames = []
    for frame_num in range(50):
        # Create a blank frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)

        # Draw a moving object
        center_x = int(100 + frame_num * 5)  # Move right
        center_y = int(200 + frame_num * 2)  # Move down
        cv2.circle(frame, (center_x, center_y), 30, (0, 255, 0), -1)

        # Draw a stationary object
        cv2.circle(frame, (400, 150), 25, (255, 0, 0), -1)

        frames.append(frame)

    return frames

def main():
    detector = ObjectDetector()
    frames = simulate_video_sequence()

    all_tracked_objects = []

    for i, frame in enumerate(frames):
        # Detect objects in frame
        detections = detector.detect_objects(frame)

        # Track objects across frames
        tracked_objects = detector.track_objects(detections)

        all_tracked_objects.append(tracked_objects)

        # Draw results on frame for visualization
        vis_frame = frame.copy()
        for obj in tracked_objects:
            x, y, w, h = obj['bbox']
            cv2.rectangle(vis_frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(vis_frame, f"ID: {obj['id']}", (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            # Draw trajectory
            for j in range(1, len(obj['history'])):
                cv2.line(vis_frame, obj['history'][j-1], obj['history'][j], (0, 255, 255), 1)

        # For this example, we'll just process a few frames
        if i < 10:  # Only show first 10 frames
            cv2.imshow('Object Detection and Tracking', vis_frame)
            if cv2.waitKey(50) & 0xFF == ord('q'):  # 50ms delay between frames
                break

    cv2.destroyAllWindows()

    # Print summary of tracking
    print(f"Tracked {len(detector.tracked_objects)} objects over {len(frames)} frames")
    for obj_id, obj in detector.tracked_objects.items():
        print(f"Object {obj_id}: {len(obj['history'])} positions recorded")

if __name__ == "__main__":
    main()