import keyboard
import pyautogui
from datetime import datetime
import os
from google import genai
from PIL import Image
import APIs

client = genai.Client(api_key=APIs.API_KEY)

if not os.path.exists("screenshots"):
    os.makedirs("screenshots")

def capture_and_analyze():
    print("\n[+] F2 Pressed: Capturing screenshot...")
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = f"screenshots/screenshot_{timestamp}.png"
    
    screenshot = pyautogui.screenshot()
    screenshot.save(filepath)
    print(f"[+] Saved locally as: {filepath}")
    
    print("[+] Sending image to Gemini for location analysis. Please wait...")
    try:
        image = Image.open(filepath)
        
        prompt = (
            "Analyze this image and determine the location depicted in it. "
            "Look for landmarks, architecture, geography, signs, language, or any other clues. "
            "Be as specific as possible. "
            "And the position on the map as if I don't know where to look for on the map. "
        )
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[image, prompt]
        )
        
        print("\n" + "="*40)
        print("Result")
        print("="*40)
        print(response.text)
        print("="*40 + "\n")
        
    except Exception as e:
        print(f"[-] An error occurred while connecting Gemini: {e}")

print("Script is running! F2 to capture and analyze. (ESC to stop)")

keyboard.add_hotkey('f2', capture_and_analyze)

keyboard.wait('esc')