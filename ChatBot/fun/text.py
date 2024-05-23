import pyautogui
import keyboard  # Allows for key event detection
import time

# Define a safety limit to avoid infinite loops
MAX_ITERATIONS = 10  # Safeguard to prevent excessive execution

for i in range(MAX_ITERATIONS):
    # Example of key manipulation (simulating toggles)
    pyautogui.press('capslock')
    pyautogui.press('numlock')
    
    # Example of sending text to simulate behavior
    pyautogui.typewrite("This is a simulation for cybersecurity education.")
    
    # Delay to mimic real-world scenarios
    time.sleep(2)
    
    # Break if a specific key is pressed (for safety during demonstration)
    if keyboard.is_pressed('esc'):
        print("Terminating script...")
        break
