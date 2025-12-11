"""
Example: Specialized Applications
This code demonstrates humanoid robot applications in specialized domains
such as healthcare, manufacturing, and service industries.
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import random
from typing import List, Dict, Tuple

class ApplicationDomain(Enum):
    """Specialized application domains for humanoid robots"""
    HEALTHCARE = "healthcare"
    MANUFACTURING = "manufacturing"
    SERVICE = "service"
    RESEARCH = "research"

@dataclass
class TaskRequirement:
    """Requirements for a specific task"""
    safety_level: int  # 1-10 scale
    precision_level: int  # 1-10 scale
    social_interaction: bool
    physical_strength: float  # 0-100 N
    dexterity: int  # 1-10 scale

class HealthcareRobot:
    """Specialized robot for healthcare applications"""
    def __init__(self):
        self.patient_data = {}
        self.safety_protocols = ["no_sharp_objects", "gentle_touch", "hygiene_compliance"]
        self.tasks = ["monitor_vitals", "assist_walking", "medication_reminder", "social_companionship"]

    def monitor_patient_vitals(self, patient_id: str) -> Dict[str, float]:
        """Monitor patient vital signs"""
        vitals = {
            'heart_rate': random.uniform(60, 100),
            'temperature': random.uniform(36.0, 37.5),
            'blood_pressure_systolic': random.uniform(110, 140),
            'blood_pressure_diastolic': random.uniform(70, 90),
            'oxygen_saturation': random.uniform(95, 100)
        }
        self.patient_data[patient_id] = vitals
        return vitals

    def assist_with_mobility(self, patient_id: str) -> str:
        """Assist patient with walking or movement"""
        # Check patient's condition first
        if patient_id in self.patient_data:
            heart_rate = self.patient_data[patient_id].get('heart_rate', 80)
            if heart_rate > 95:
                return "Patient heart rate too high for mobility exercise"

        # Provide assistance
        assistance_types = ["walking_support", "balance_assistance", "transfer_help"]
        return f"Providing {random.choice(assistance_types)} to patient {patient_id}"

    def medication_reminder(self, patient_id: str, medication: str) -> str:
        """Remind patient to take medication"""
        return f"Reminder: Time for {medication} for patient {patient_id}"

class ManufacturingRobot:
    """Specialized robot for manufacturing applications"""
    def __init__(self):
        self.quality_standards = {
            'precision': 0.1,  # mm tolerance
            'repeatability': 0.999,  # 99.9% success rate
            'throughput': 100  # items per hour
        }
        self.safety_protocols = ["cage_protection", "speed_limiting", "emergency_stop"]
        self.assigned_tasks = ["assembly", "quality_inspection", "material_handling"]

    def perform_assembly(self, part_a: str, part_b: str) -> bool:
        """Perform precise assembly task"""
        # Simulate precision assembly
        success_rate = 0.98
        return random.random() < success_rate

    def quality_inspection(self, item: str) -> Dict[str, bool]:
        """Perform quality inspection"""
        inspection_results = {
            'dimension_check': random.random() > 0.02,  # 2% defect rate
            'visual_inspection': random.random() > 0.03,  # 3% defect rate
            'functional_test': random.random() > 0.01,  # 1% defect rate
            'overall_pass': True
        }
        inspection_results['overall_pass'] = all([
            inspection_results['dimension_check'],
            inspection_results['visual_inspection'],
            inspection_results['functional_test']
        ])
        return inspection_results

    def handle_material(self, item: str, destination: str) -> str:
        """Handle material transportation"""
        return f"Transported {item} to {destination} successfully"

class ServiceRobot:
    """Specialized robot for service industry applications"""
    def __init__(self):
        self.customer_interaction_modes = ["greeting", "wayfinding", "assistance", "entertainment"]
        self.safety_protocols = ["collision_avoidance", "soft_contacts", "predictable_behavior"]
        self.service_tasks = ["greeting_customers", "answering_questions", "guiding", "cleaning"]

    def greet_customer(self, customer_id: str) -> str:
        """Greet and welcome customer"""
        greetings = [
            f"Welcome! How can I assist you today, customer {customer_id}?",
            f"Hello {customer_id}! I'm here to help.",
            f"Good day! What brings you here today?"
        ]
        return random.choice(greetings)

    def provide_wayfinding(self, destination: str) -> str:
        """Provide directions to destination"""
        directions = [
            f"The {destination} is straight ahead, then turn right.",
            f"You can find {destination} on your left side.",
            f"Go straight for 50 meters, then look for signs to {destination}."
        ]
        return random.choice(directions)

    def customer_assistance(self, request: str) -> str:
        """Provide customer assistance"""
        if "restroom" in request.lower():
            return "Restrooms are located to your right, just past the information desk."
        elif "help" in request.lower() or "where" in request.lower():
            return "I'd be happy to help! Could you please specify what you're looking for?"
        else:
            return f"I can help with that. Let me connect you with the appropriate service for '{request}'."

class ApplicationManager:
    """Manages specialized applications and task allocation"""
    def __init__(self):
        self.healthcare_robot = HealthcareRobot()
        self.manufacturing_robot = ManufacturingRobot()
        self.service_robot = ServiceRobot()

        self.domain_requirements = {
            ApplicationDomain.HEALTHCARE: TaskRequirement(
                safety_level=9, precision_level=7, social_interaction=True,
                physical_strength=20, dexterity=8
            ),
            ApplicationDomain.MANUFACTURING: TaskRequirement(
                safety_level=7, precision_level=9, social_interaction=False,
                physical_strength=50, dexterity=7
            ),
            ApplicationDomain.SERVICE: TaskRequirement(
                safety_level=8, precision_level=5, social_interaction=True,
                physical_strength=10, dexterity=6
            )
        }

    def allocate_task(self, domain: ApplicationDomain, task_details: str) -> str:
        """Allocate task to appropriate specialized robot"""
        if domain == ApplicationDomain.HEALTHCARE:
            return self.handle_healthcare_task(task_details)
        elif domain == ApplicationDomain.MANUFACTURING:
            return self.handle_manufacturing_task(task_details)
        elif domain == ApplicationDomain.SERVICE:
            return self.handle_service_task(task_details)
        else:
            return f"Domain {domain} not supported"

    def handle_healthcare_task(self, task_details: str) -> str:
        """Handle healthcare-specific tasks"""
        if "monitor" in task_details.lower():
            patient_id = "P001"
            vitals = self.healthcare_robot.monitor_patient_vitals(patient_id)
            return f"Patient {patient_id} vitals: {vitals}"
        elif "assist" in task_details.lower():
            patient_id = "P001"
            return self.healthcare_robot.assist_with_mobility(patient_id)
        elif "medication" in task_details.lower():
            patient_id = "P001"
            return self.healthcare_robot.medication_reminder(patient_id, "Aspirin")
        else:
            return "Healthcare task not recognized"

    def handle_manufacturing_task(self, task_details: str) -> str:
        """Handle manufacturing-specific tasks"""
        if "assembly" in task_details.lower():
            return f"Assembly completed: {self.manufacturing_robot.perform_assembly('part_A', 'part_B')}"
        elif "inspection" in task_details.lower():
            return f"Quality results: {self.manufacturing_robot.quality_inspection('widget_123')}"
        elif "transport" in task_details.lower():
            return self.manufacturing_robot.handle_material('component_X', 'station_5')
        else:
            return "Manufacturing task not recognized"

    def handle_service_task(self, task_details: str) -> str:
        """Handle service-specific tasks"""
        if "greet" in task_details.lower():
            return self.service_robot.greet_customer("C001")
        elif "direction" in task_details.lower() or "where" in task_details.lower():
            return self.service_robot.provide_wayfinding("information_desk")
        elif "assist" in task_details.lower():
            return self.service_robot.customer_assistance(task_details)
        else:
            return "Service task not recognized"

class SpecializedApplicationSimulator:
    """Simulates specialized applications in different domains"""
    def __init__(self):
        self.app_manager = ApplicationManager()
        self.performance_metrics = {
            ApplicationDomain.HEALTHCARE: [],
            ApplicationDomain.MANUFACTURING: [],
            ApplicationDomain.SERVICE: []
        }

    def simulate_healthcare_scenario(self) -> List[str]:
        """Simulate healthcare application scenario"""
        scenario_results = []
        scenario_results.append(self.app_manager.allocate_task(
            ApplicationDomain.HEALTHCARE, "monitor patient vitals"))
        scenario_results.append(self.app_manager.allocate_task(
            ApplicationDomain.HEALTHCARE, "assist with mobility"))
        scenario_results.append(self.app_manager.allocate_task(
            ApplicationDomain.HEALTHCARE, "medication reminder"))
        return scenario_results

    def simulate_manufacturing_scenario(self) -> List[str]:
        """Simulate manufacturing application scenario"""
        scenario_results = []
        scenario_results.append(self.app_manager.allocate_task(
            ApplicationDomain.MANUFACTURING, "assembly task"))
        scenario_results.append(self.app_manager.allocate_task(
            ApplicationDomain.MANUFACTURING, "quality inspection"))
        scenario_results.append(self.app_manager.allocate_task(
            ApplicationDomain.MANUFACTURING, "transport component"))
        return scenario_results

    def simulate_service_scenario(self) -> List[str]:
        """Simulate service application scenario"""
        scenario_results = []
        scenario_results.append(self.app_manager.allocate_task(
            ApplicationDomain.SERVICE, "greet customer"))
        scenario_results.append(self.app_manager.allocate_task(
            ApplicationDomain.SERVICE, "provide directions"))
        scenario_results.append(self.app_manager.allocate_task(
            ApplicationDomain.SERVICE, "assist with purchase"))
        return scenario_results

def main():
    print("Specialized Applications Demonstration")
    print("=" * 50)

    simulator = SpecializedApplicationSimulator()

    print("\n1. Healthcare Application Scenario:")
    healthcare_results = simulator.simulate_healthcare_scenario()
    for i, result in enumerate(healthcare_results, 1):
        print(f"  {i}. {result}")

    print("\n2. Manufacturing Application Scenario:")
    manufacturing_results = simulator.simulate_manufacturing_scenario()
    for i, result in enumerate(manufacturing_results, 1):
        print(f"  {i}. {result}")

    print("\n3. Service Application Scenario:")
    service_results = simulator.simulate_service_scenario()
    for i, result in enumerate(service_results, 1):
        print(f"  {i}. {result}")

    # Demonstrate domain-specific requirements
    print("\n4. Domain-Specific Requirements:")
    manager = ApplicationManager()
    for domain, reqs in manager.domain_requirements.items():
        print(f"\n  {domain.value.upper()}:")
        print(f"    Safety Level: {reqs.safety_level}/10")
        print(f"    Precision Level: {reqs.precision_level}/10")
        print(f"    Social Interaction Required: {reqs.social_interaction}")
        print(f"    Physical Strength: {reqs.physical_strength}N")
        print(f"    Dexterity: {reqs.dexterity}/10")

    # Visualization
    plt.figure(figsize=(15, 5))

    # Domain characteristics comparison
    domains = ['Healthcare', 'Manufacturing', 'Service']
    safety_levels = [9, 7, 8]
    precision_levels = [7, 9, 5]
    social_interaction = [1, 0, 1]  # 1 for yes, 0 for no

    plt.subplot(1, 3, 1)
    plt.bar(domains, safety_levels)
    plt.title('Safety Level Requirements')
    plt.ylabel('Safety Level (1-10)')
    plt.xticks(rotation=45)

    plt.subplot(1, 3, 2)
    plt.bar(domains, precision_levels)
    plt.title('Precision Requirements')
    plt.ylabel('Precision Level (1-10)')
    plt.xticks(rotation=45)

    plt.subplot(1, 3, 3)
    plt.bar(domains, social_interaction)
    plt.title('Social Interaction Required')
    plt.ylabel('Yes (1) / No (0)')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    print(f"\nSpecialized applications demonstration complete!")
    print("Key takeaways:")
    print("- Different domains have distinct requirements and constraints")
    print("- Specialized robots are optimized for specific application areas")
    print("- Safety and precision requirements vary significantly across domains")

if __name__ == "__main__":
    main()