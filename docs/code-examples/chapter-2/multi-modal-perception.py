"""
Example: Multi-modal Perception
This code demonstrates how to integrate information from multiple sensory modalities
(visual, auditory, tactile) for humanoid robot perception.
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import random

class MultiModalPerception:
    def __init__(self):
        self.visual_data = {'objects': [], 'scene': None}
        self.auditory_data = {'sounds': [], 'directions': []}
        self.tactile_data = {'forces': [], 'contacts': []}

        # Confidence levels for each modality
        self.confidence = {
            'visual': 0.8,
            'auditory': 0.6,
            'tactile': 0.9
        }

    def sense_visual(self, objects_in_view):
        """Simulate visual sensing"""
        self.visual_data['objects'] = objects_in_view
        self.visual_data['scene'] = "indoor_environment"  # Simplified scene representation
        return self.visual_data

    def sense_auditory(self, sound_signals):
        """Simulate auditory sensing"""
        processed_sounds = []
        directions = []

        for signal in sound_signals:
            # Process the sound signal to extract features
            # Find peaks to identify distinct sounds
            peaks, _ = find_peaks(signal, height=0.5)

            for peak_idx in peaks:
                # Estimate direction (simplified)
                direction = random.uniform(0, 360)  # Random direction in degrees
                processed_sounds.append({
                    'amplitude': signal[peak_idx],
                    'frequency': random.uniform(200, 2000),  # Hz
                    'timestamp': peak_idx
                })
                directions.append(direction)

        self.auditory_data['sounds'] = processed_sounds
        self.auditory_data['directions'] = directions
        return self.auditory_data

    def sense_tactile(self, contact_forces):
        """Simulate tactile sensing"""
        processed_contacts = []

        for force in contact_forces:
            if force > 0.1:  # Threshold for contact detection
                processed_contacts.append({
                    'location': random.choice(['left_hand', 'right_hand', 'left_foot', 'right_foot']),
                    'force': force,
                    'pressure': force * random.uniform(0.8, 1.2)  # Simulated pressure
                })

        self.tactile_data['forces'] = contact_forces
        self.tactile_data['contacts'] = processed_contacts
        return self.tactile_data

    def fuse_perception(self):
        """Fuse information from all modalities"""
        fused_perception = {
            'environment': {},
            'objects_of_interest': [],
            'events': [],
            'confidence_map': {}
        }

        # Process visual information
        for obj in self.visual_data['objects']:
            fused_perception['objects_of_interest'].append({
                'type': 'visual',
                'data': obj,
                'confidence': self.confidence['visual']
            })

        # Process auditory information
        for i, sound in enumerate(self.auditory_data['sounds']):
            fused_perception['events'].append({
                'type': 'auditory',
                'data': sound,
                'direction': self.auditory_data['directions'][i] if i < len(self.auditory_data['directions']) else None,
                'confidence': self.confidence['auditory']
            })

        # Process tactile information
        for contact in self.tactile_data['contacts']:
            fused_perception['events'].append({
                'type': 'tactile',
                'data': contact,
                'confidence': self.confidence['tactile']
            })

        # Create confidence-weighted environment model
        # This is a simplified fusion approach
        total_confidence = sum(self.confidence.values())
        avg_confidence = total_confidence / len(self.confidence)

        fused_perception['environment']['confidence'] = avg_confidence
        fused_perception['environment']['modalities_present'] = [
            'visual' if self.visual_data['objects'] else None,
            'auditory' if self.auditory_data['sounds'] else None,
            'tactile' if self.tactile_data['contacts'] else None
        ]
        fused_perception['environment']['modalities_present'] = [m for m in fused_perception['environment']['modalities_present'] if m]

        return fused_perception

def simulate_environment():
    """Simulate a multi-modal environment"""
    # Simulate visual objects
    visual_objects = [
        {'name': 'cup', 'position': [1.0, 0.5, 0.8], 'size': 'medium'},
        {'name': 'book', 'position': [0.8, 0.2, 0.1], 'size': 'large'},
        {'name': 'ball', 'position': [1.5, 1.0, 0.3], 'size': 'small'}
    ]

    # Simulate auditory signals (simplified as amplitude over time)
    time_points = np.linspace(0, 1, 100)
    auditory_signals = []
    for _ in range(2):  # Two different sound sources
        # Create a signal with some peaks
        signal = np.random.normal(0, 0.1, 100)
        # Add some peaks to simulate sounds
        peak_positions = np.random.choice(100, 3, replace=False)
        signal[peak_positions] += np.random.uniform(0.5, 1.0, 3)
        auditory_signals.append(signal)

    # Simulate tactile forces
    tactile_forces = [random.uniform(0, 2) for _ in range(10)]  # 10 sensors

    return visual_objects, auditory_signals, tactile_forces

def main():
    perception_system = MultiModalPerception()

    # Simulate sensing in environment
    visual_objects, auditory_signals, tactile_forces = simulate_environment()

    # Process each modality
    visual_result = perception_system.sense_visual(visual_objects)
    auditory_result = perception_system.sense_auditory(auditory_signals)
    tactile_result = perception_system.sense_tactile(tactile_forces)

    # Fuse all perceptions
    fused_result = perception_system.fuse_perception()

    # Print results
    print("Multi-modal Perception Results:")
    print(f"Objects of interest: {len(fused_result['objects_of_interest'])}")
    print(f"Events detected: {len(fused_result['events'])}")
    print(f"Environment confidence: {fused_result['environment']['confidence']:.2f}")
    print(f"Active modalities: {fused_result['environment']['modalities_present']}")

    # Visualization
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Visualize objects
    if visual_objects:
        obj_positions = np.array([[obj['position'][0], obj['position'][1]] for obj in visual_objects])
        axes[0, 0].scatter(obj_positions[:, 0], obj_positions[:, 1])
        axes[0, 0].set_title('Visual Objects')
        axes[0, 0].set_xlabel('X Position')
        axes[0, 0].set_ylabel('Y Position')
        axes[0, 0].grid(True)

    # Visualize auditory signals
    if auditory_signals:
        for i, signal in enumerate(auditory_signals):
            axes[0, 1].plot(signal, label=f'Source {i+1}')
        axes[0, 1].set_title('Auditory Signals')
        axes[0, 1].set_xlabel('Time')
        axes[0, 1].set_ylabel('Amplitude')
        axes[0, 1].legend()
        axes[0, 1].grid(True)

    # Visualize tactile forces
    if tactile_forces:
        axes[1, 0].bar(range(len(tactile_forces)), tactile_forces)
        axes[1, 0].set_title('Tactile Forces')
        axes[1, 0].set_xlabel('Sensor Index')
        axes[1, 0].set_ylabel('Force (N)')
        axes[1, 0].grid(True)

    # Visualize confidence levels
    modalities = list(perception_system.confidence.keys())
    confidences = list(perception_system.confidence.values())
    axes[1, 1].bar(modalities, confidences)
    axes[1, 1].set_title('Perception Confidence by Modality')
    axes[1, 1].set_ylabel('Confidence')
    axes[1, 1].set_ylim(0, 1)
    axes[1, 1].grid(True, axis='y')

    plt.tight_layout()
    plt.show()

    print("\nFusion complete! Multi-modal perception system successfully integrated visual, auditory, and tactile information.")

if __name__ == "__main__":
    main()