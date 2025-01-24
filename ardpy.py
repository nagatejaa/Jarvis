import serial
from HEAD.ear import listen  # Importing the function to listen to voice commands
from HEAD.mouth import speak  # Importing the function to convert text to speech

# Set up serial communication with Arduino
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)  # Adjust COM port as needed

# Function to process commands
def process_command(command):
    command = command.lower()
    
    if "led on" in command:
        arduino.write(b'LED_ON\n')
        speak("Turning on the LED")
    elif "led off" in command:
        arduino.write(b'LED_OFF\n')
        speak("Turning off the LED")
    elif "turn on fan" in command:
        arduino.write(b'FAN_ON\n')
        speak("Turning on the fan")
    elif "turn off fan" in command:
        arduino.write(b'FAN_OFF\n')
        speak("Turning off the fan")
    elif "activate robot" in command:
        arduino.write(b'ROBOT_ACTIVATE\n')
        speak("Activating the robot")
    elif "deactivate robot" in command:
        arduino.write(b'ROBOT_DEACTIVATE\n')
        speak("Deactivating the robot")
    else:
        speak("I didn't understand that command. Please try again.")

# Main loop
def main():
    speak("System is ready. Please give a command.")
    while True:
        command = listen()  # Capture voice input
        if command:
            process_command(command)

if __name__ == "__main__":
    main()
