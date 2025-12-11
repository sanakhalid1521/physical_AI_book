"""
Example: Human-Robot Interaction
This code demonstrates human-robot interaction systems for humanoid robots,
focusing on natural communication and collaboration.
"""

import re
import random
from datetime import datetime
from enum import Enum

class InteractionMode(Enum):
    """Different modes of human-robot interaction"""
    SPEECH = "speech"
    GESTURE = "gesture"
    TOUCH = "touch"
    MULTIMODAL = "multimodal"

class DialogueManager:
    """Manages conversation with human users"""
    def __init__(self):
        self.context = {}
        self.user_profile = {}
        self.conversation_history = []

    def process_input(self, user_input, user_id="default"):
        """Process user input and generate response"""
        # Update conversation history
        self.conversation_history.append({
            'user_id': user_id,
            'timestamp': datetime.now(),
            'input': user_input
        })

        # Classify intent
        intent = self.classify_intent(user_input)

        # Generate response based on intent
        response = self.generate_response(intent, user_input, user_id)

        # Update context
        self.context['last_intent'] = intent
        self.context['last_input'] = user_input

        return response, intent

    def classify_intent(self, user_input):
        """Classify user intent using simple pattern matching"""
        user_input_lower = user_input.lower()

        # Define patterns for different intents
        patterns = {
            'greeting': [r'hello', r'hi', r'hey', r'good morning', r'good afternoon', r'good evening'],
            'request_move': [r'go to', r'move to', r'walk to', r'go', r'come here', r'follow me'],
            'request_object': [r'bring me', r'give me', r'pick up', r'get', r'hand me', r'fetch'],
            'request_help': [r'help', r'assist', r'can you', r'could you', r'please'],
            'inquiry': [r'what', r'where', r'when', r'who', r'why', r'how'],
            'goodbye': [r'bye', r'goodbye', r'see you', r'thank you', r'thanks'],
            'idle': [r'nothing', r'never mind', r'stop', r'cancel']
        }

        for intent, intent_patterns in patterns.items():
            for pattern in intent_patterns:
                if re.search(pattern, user_input_lower):
                    return intent

        return 'unknown'

    def generate_response(self, intent, user_input, user_id):
        """Generate appropriate response based on intent"""
        responses = {
            'greeting': [
                "Hello! How can I assist you today?",
                "Hi there! What can I do for you?",
                "Good to see you! How may I help?"
            ],
            'request_move': [
                "I'll move to that location for you.",
                "Navigating to the specified location.",
                "On my way to that destination."
            ],
            'request_object': [
                "I'll retrieve that object for you.",
                "Going to get that item now.",
                "Fetching the requested object."
            ],
            'request_help': [
                "I'm here to help. What do you need?",
                "How can I assist you?",
                "I'm ready to help with that task."
            ],
            'inquiry': [
                "That's a good question. Let me think...",
                "I can help you with that inquiry.",
                "Let me provide information about that."
            ],
            'goodbye': [
                "Goodbye! Feel free to call me if you need anything.",
                "See you later! Have a great day.",
                "Thank you for interacting with me!"
            ],
            'idle': [
                "Standing by for further instructions.",
                "I'm here when you need me.",
                "Waiting for your next command."
            ]
        }

        if intent in responses:
            return random.choice(responses[intent])
        else:
            return "I'm not sure I understand. Could you please rephrase that?"

class GestureRecognizer:
    """Recognizes and interprets human gestures"""
    def __init__(self):
        self.gesture_map = {
            'wave': ['wave', 'waving', 'hello gesture'],
            'point': ['point', 'pointing', 'point to', 'over there'],
            'beckon': ['come here', 'beckon', 'beckoning'],
            'stop': ['stop', 'halt', 'wait', 'pause'],
            'thumbs_up': ['good', 'ok', 'yes', 'thumbs up'],
            'thumbs_down': ['bad', 'no', 'dislike', 'thumbs down']
        }

    def recognize_gesture(self, gesture_description):
        """Recognize gesture from description or sensor data"""
        gesture_description_lower = gesture_description.lower()

        for gesture, keywords in self.gesture_map.items():
            for keyword in keywords:
                if keyword in gesture_description_lower:
                    return gesture

        return 'unknown'

    def interpret_gesture(self, gesture, context=None):
        """Interpret the meaning of a gesture in context"""
        interpretations = {
            'wave': "Greeting or getting attention",
            'point': "Directing attention to an object or location",
            'beckon': "Requesting approach or attention",
            'stop': "Requesting halt or pause",
            'thumbs_up': "Approval or positive feedback",
            'thumbs_down': "Disapproval or negative feedback"
        }

        return interpretations.get(gesture, "Unknown gesture meaning")

class SocialBehaviorEngine:
    """Implements social behaviors for natural interaction"""
    def __init__(self):
        self.social_rules = [
            self.maintain_eye_contact,
            self.respect_personal_space,
            self.use_appropriate_gestures,
            self.adjust_speech_to_audience
        ]

    def maintain_eye_contact(self, user_position, robot_position):
        """Simulate eye contact by orienting head toward user"""
        # Calculate direction to user
        dx = user_position[0] - robot_position[0]
        dy = user_position[1] - robot_position[1]

        # Return head orientation command
        return f"orient_head_to({dx}, {dy})"

    def respect_personal_space(self, user_distance):
        """Maintain appropriate distance from user"""
        if user_distance < 0.5:  # Too close
            return "step_back"
        elif user_distance > 2.0:  # Too far for conversation
            return "step_closer"
        else:
            return "maintain_current_distance"

    def use_appropriate_gestures(self, social_context):
        """Select appropriate gestures based on context"""
        if social_context == "formal":
            return ["minimal_gestures", "nodding"]
        elif social_context == "informal":
            return ["natural_gestures", "expressive"]
        else:
            return ["contextual_gestures"]

    def adjust_speech_to_audience(self, audience_characteristics):
        """Adjust speech based on audience (age, familiarity, etc.)"""
        adjustments = []
        if audience_characteristics.get("elderly", False):
            adjustments.append("speak_louder")
        if audience_characteristics.get("child", False):
            adjustments.append("simplify_language")
        if not audience_characteristics.get("familiar", False):
            adjustments.append("use_formal_language")

        return adjustments if adjustments else ["normal_speech"]

class HumanRobotInteractionSystem:
    """Main system integrating all HRI components"""
    def __init__(self):
        self.dialogue_manager = DialogueManager()
        self.gesture_recognizer = GestureRecognizer()
        self.social_engine = SocialBehaviorEngine()
        self.current_interaction_mode = InteractionMode.MULTIMODAL

    def process_multimodal_input(self, speech_input=None, gesture_input=None, context=None):
        """Process multiple input modalities simultaneously"""
        results = {}

        # Process speech
        if speech_input:
            speech_response, intent = self.dialogue_manager.process_input(speech_input)
            results['speech_response'] = speech_response
            results['intent'] = intent

        # Process gesture
        if gesture_input:
            recognized_gesture = self.gesture_recognizer.recognize_gesture(gesture_input)
            gesture_interpretation = self.gesture_recognizer.interpret_gesture(recognized_gesture, context)
            results['gesture'] = recognized_gesture
            results['gesture_interpretation'] = gesture_interpretation

        # Generate social response
        social_response = self.generate_social_response(results, context)
        results['social_response'] = social_response

        return results

    def generate_social_response(self, input_results, context):
        """Generate appropriate social behaviors based on input"""
        social_commands = []

        # Example: If user waves, robot should acknowledge
        if input_results.get('gesture') == 'wave':
            social_commands.append("wave_back")
            social_commands.append("smile_display")

        # Example: If user points to something, robot should look
        if input_results.get('gesture') == 'point':
            social_commands.append("gaze_follow")
            social_commands.append("acknowledge_with_head_nod")

        return social_commands

def simulate_interaction():
    """Simulate a human-robot interaction scenario"""
    hri_system = HumanRobotInteractionSystem()

    # Simulate conversation
    conversation = [
        ("Hello robot!", "wave"),
        ("Can you go to the kitchen?", "point to kitchen"),
        ("Bring me a cup from the table", "point to table"),
        ("Thank you!", "thumbs up"),
        ("Goodbye!", "wave")
    ]

    print("Simulating Human-Robot Interaction:")
    print("=" * 40)

    for i, (speech, gesture) in enumerate(conversation):
        print(f"\nTurn {i+1}:")
        print(f"  Human: {speech}")
        print(f"  Gesture: {gesture}")

        results = hri_system.process_multimodal_input(speech, gesture)

        if 'speech_response' in results:
            print(f"  Robot Response: {results['speech_response']}")
        if 'gesture_interpretation' in results:
            print(f"  Gesture Interpretation: {results['gesture_interpretation']}")
        if 'social_response' in results:
            print(f"  Social Behaviors: {', '.join(results['social_response'])}")

def main():
    print("Human-Robot Interaction Demonstration")
    print("=" * 50)

    # Demonstrate individual components
    print("\n1. Dialogue Manager:")
    dm = DialogueManager()
    test_inputs = ["Hello!", "Please go to the kitchen", "Can you help me?", "Thank you!"]

    for inp in test_inputs:
        response, intent = dm.process_input(inp)
        print(f"  Input: '{inp}' -> Intent: {intent}, Response: '{response}'")

    print("\n2. Gesture Recognition:")
    gr = GestureRecognizer()
    test_gestures = ["waving hello", "pointing to the door", "beckoning me closer", "giving thumbs up"]

    for gesture in test_gestures:
        recognized = gr.recognize_gesture(gesture)
        interpretation = gr.interpret_gesture(recognized)
        print(f"  '{gesture}' -> Recognized: {recognized}, Interpretation: {interpretation}")

    print("\n3. Social Behavior Engine:")
    sb = SocialBehaviorEngine()
    print(f"  Eye contact command: {sb.maintain_eye_contact((1, 1), (0, 0))}")
    print(f"  Personal space response (0.3m): {sb.respect_personal_space(0.3)}")
    print(f"  Appropriate gestures (informal): {sb.use_appropriate_gestures('informal')}")
    print(f"  Speech adjustment (elderly): {sb.adjust_speech_to_audience({'elderly': True})}")

    print("\n4. Complete Interaction Simulation:")
    simulate_interaction()

    print(f"\nHuman-robot interaction demonstration complete!")

if __name__ == "__main__":
    main()