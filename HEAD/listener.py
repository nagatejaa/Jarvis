# import threading
# from HEAD.mouth import speak
# from HEAD.ear import listen  # Import the listen function from ear.py
# from Traning_Model.model import mind  # Assuming your Q&A model is in 'model.py'
#
# # Wake word to listen for
# WAKE_WORD = "jarvis"  # You can change this to whatever wake word you prefer
#
#
# # Function to listen for wake word
# def listen_for_wake_word():
#     while True:
#         print("Listening for the wake word...")
#         recognized_text = listen()  # Use the listen function from ear.py to capture speech
#
#         if recognized_text:  # Ensure recognized_text is not None
#             print(f"Recognized Text: {recognized_text}")
#             if WAKE_WORD in recognized_text.lower():
#                 speak(f"Yes, how can I assist you?")
#                 listen_for_question()  # Listen for a follow-up question
#
#
# # Function to listen for the user's question after the wake word is detected
# def listen_for_question():
#     while True:
#         print("Listening for your question...")
#         question = listen()  # Use the listen function from ear.py to capture speech
#         if question:  # Ensure question is not None
#             print(f"You asked: {question}")
#             # Pass the question to the mind function and speak the answer
#             answer = mind(question)
#             speak(answer)
#
#
# # Function to start the wake word listener in a separate thread
# def start_listener():
#     listener_thread = threading.Thread(target=listen_for_wake_word)
#     listener_thread.daemon = True  # Allow thread to exit when the main program exits
#     listener_thread.start()
#
#
# # Start the listener
# if __name__ == "__main__":
#     start_listener()
#
#     # Run an infinite loop to keep the program running
#     while True:
#         pass  # Keep the program running indefinitely

# import threading
# import time
# from HEAD.mouth import speak
# from HEAD.ear import listen
# from HEAD.brain import mind
#
# # Wake word and commands
# WAKE_WORD = "jarvis"
# QUIT_COMMAND = "jarvis quit"
# STOP_COMMAND = "stop"
#
# # System states
# is_awake = True  # Determines if the system is listening for questions
# is_speaking = False  # Determines if the system is currently speaking
#
# # Lock for handling shared states
# state_lock = threading.Lock()
#
# def listen_for_wake_word():
#     global is_awake
#     while True:
#         if is_awake:
#             print("Listening for the wake word...")
#             recognized_text = listen()
#             if recognized_text:
#                 print(f"Recognized Text: {recognized_text}")
#                 if WAKE_WORD in recognized_text.lower():
#                     with state_lock:
#                         is_awake = True
#                     speak("Yes, how can I assist you?")
#                     time.sleep(0.5)  # Pause before capturing the question
#                     listen_for_question()
#
# def listen_for_question():
#     global is_awake
#     print("Listening for your question...")
#     question = listen()
#     if question:
#         print(f"You asked: {question}")
#         if question.lower() == QUIT_COMMAND:
#             with state_lock:
#                 is_awake = False
#             speak("Going to sleep. Say 'Jarvis' to wake me up.")
#         elif STOP_COMMAND in question.lower():
#             handle_stop_command()
#         else:
#             answer = mind(question)
#             print(f"Answer: {answer}")  # Debugging: log the answer
#             speak(answer)
#
# def handle_stop_command():
#     global is_speaking
#     with state_lock:
#         if is_speaking:
#             speak("OK.")  # Acknowledge the stop command
#             is_speaking = False  # Reset the speaking state
#         listen_for_question()  # Immediately listen for the next question
#
# def speaking_wrapper(text):
#     """Wrapper for speaking to handle the speaking state."""
#     global is_speaking
#     with state_lock:
#         is_speaking = True
#     speak(text)
#     with state_lock:
#         is_speaking = False
#
# def start_listener():
#     listener_thread = threading.Thread(target=listen_for_wake_word)
#     listener_thread.daemon = True
#     listener_thread.start()
#
# if __name__ == "__main__":
#     start_listener()
#     while True:
#         time.sleep(0.1)  # Keep the main thread running


import threading
import time
from HEAD.mouth import speak
from HEAD.ear import listen
from HEAD.brain import mind

# Commands
WAKE_WORD = "jarvis"
QUIT_COMMANDS = ["jarvis quit", "shut up", "quit", "fuck off", "shut the fuck up"]
STOP_COMMAND = "stop"

# System states
is_awake = False  # Initially in "sleep mode"
is_speaking = False  # Tracks if the system is speaking

# Lock for managing shared state
state_lock = threading.Lock()

def listen_for_wake_word():
    """Continuously listens for the wake word when in sleep mode."""
    global is_awake
    while True:
        if not is_awake:
            print("Waiting for the wake word...")
            recognized_text = listen()
            if recognized_text and WAKE_WORD in recognized_text.lower():
                with state_lock:
                    is_awake = True
                speak("Hello sir, how can I assist you?")
                listen_for_question()

def listen_for_question():
    """Continuously listens for user questions when awake."""
    global is_awake
    while is_awake:
        print("Listening for your question...")
        question = listen()
        if question:
            print(f"You asked: {question}")
            # Handle quit commands
            if any(cmd in question.lower() for cmd in QUIT_COMMANDS):
                with state_lock:
                    is_awake = False
                speak("Alright, I'm going to sleep. Say 'Jarvis' to wake me up.")
                break
            # Handle stop command
            elif STOP_COMMAND in question.lower():
                handle_stop_command()
            else:
                # Process the question and respond
                answer = mind(question)
                print(f"Answer: {answer}")
                speaking_wrapper(answer)

def handle_stop_command():
    """Stops the system from speaking and listens for the next question."""
    global is_speaking
    with state_lock:
        if is_speaking:
            is_speaking = False
            speak("OK.")
        listen_for_question()

def speaking_wrapper(text):
    """Handles the speaking state."""
    global is_speaking
    with state_lock:
        is_speaking = True
    speak(text)
    with state_lock:
        is_speaking = False

def start_listener():
    """Starts the wake word listener in a separate thread."""
    listener_thread = threading.Thread(target=listen_for_wake_word)
    listener_thread.daemon = True  # Allow thread to exit with the program
    listener_thread.start()

if __name__ == "__main__":
    start_listener()
    while True:
        time.sleep(0.1)  # Keep the main program running
