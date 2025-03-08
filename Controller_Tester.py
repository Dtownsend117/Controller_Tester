import subprocess
import sys
import platform
import speech_recognition as sr
import pyttsx3
import pyautogui
import time

def speak(text):
    """Convert text to speech."""
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[1].id)
    engine.setProperty("rate",180)
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    """Listen for a voice command and return the recognized text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for your command...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service.")
            return None

def open_game_controllers():
    """Open the Game Controllers settings based on the operating system."""
    os_type = platform.system()
    
    if os_type == "Windows":
        subprocess.Popen("joy.cpl", shell=True)  
        
    elif os_type == "Darwin":
        subprocess.Popen(["open", "/System/Library/PreferencePanes/Keyboard.prefPane"])
        
    else:
        speak("Unsupported operating system. This module only supports Windows and macOS.")

def list_available_controllers():
    """List available controllers and return them."""
    controllers = ["Controller 1", "Controller 2", "Controller 3", "Controller 4"]
    for index, controller in enumerate(controllers, start=1):
        print(f"{index}: {controller}")
    return controllers

def select_controller(controllers):
    """Allow the user to verbally select a controller by number."""
    speak("Please choose a controller or exit.")
    print("Please choose a controller number or exit.")
    command = listen_for_command()
    
    if command:
        for index, controller in enumerate(controllers, start=1):
            if f"controller {index}" in command:
                speak(f"You selected {controller}.")
                return index  
            elif "exit" in command or "exit tester" in command:
                speak("Exiting the tester.")
                exit_tester()
                return None
        speak("I did not recognize that controller number.")
    return None

def open_controller_properties(index):
    """Open the properties window for the selected controller."""
    
    time.sleep(1)
  
    for _ in range(index - 1):
        pyautogui.press('down')
    
    pyautogui.press('tab')
  
    pyautogui.press('enter')
    speak("Opening properties.")

def exit_tester():
    """Simulate pressing the Esc key twice to exit the tester and exit the program."""
    time.sleep(1) 
    pyautogui.press('esc')
    pyautogui.press('esc')
    speak("Exited the tester.")
    sys.exit() 

if __name__ == "__main__":
    open_game_controllers()
    available_controllers = list_available_controllers()
    
    while True:
        selected_controller_index = select_controller(available_controllers)
        
        if selected_controller_index is not None:
            open_controller_properties(selected_controller_index)
