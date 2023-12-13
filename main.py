import keyboard
from PIL import ImageGrab
import pytesseract
import pyperclip
import asyncio
import g4f
import re


# Function to extract text between specific symbols from a string
def extract_between_symbols(input_string):
    pattern1 = re.compile(r'§§(.*?)§§')
    pattern2 = re.compile(r'\*\*(.*?)\*\*')

    match1 = pattern1.search(input_string)
    match2 = pattern2.search(input_string)

    if match1:
        return match1.group(1)
    elif match2:
        return match2.group(1)
    else:
        return None


# Set the path to the Tesseract OCR executable (change this based on your installation)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Specify your custom configuration for Tesseract OCR
custom_config = r'--oem 3 --psm 6'


# Function to set text to the clipboard
def set_text_to_clipboard(text):
    pyperclip.copy(text)


# Function to take a screenshot and extract text using Tesseract OCR
def take_screenshot_and_extract_text():
    try:
        # Take a screenshot directly into a PIL Image
        screenshot = ImageGrab.grab()

        # Use pytesseract to perform OCR with the custom configuration
        text = pytesseract.image_to_string(screenshot, config=custom_config)

        return text
    except Exception as e:
        print("Error:", e)


# Function to process text using GPT-4
async def process_text_bing(salt):
    try:
        print(".")
        text = take_screenshot_and_extract_text()
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{"role": "user", "content": salt + text}],
        )

        result = extract_between_symbols(response)
        print(result)
        set_text_to_clipboard(result)
    except Exception as e:
        print("Error:", e)


# Function to process text using GPT-3
async def process_text_gpt3(salt):
    try:
        print(".")
        text = take_screenshot_and_extract_text()
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            provider=g4f.Provider.You,
            messages=[{"role": "user", "content": salt + text}],
        )

        result = extract_between_symbols(response)
        print(result)
        set_text_to_clipboard(result)
    except Exception as e:
        print("Error:", e)


async def process_text_gpt_programming(salt):
    try:
        print(".")
        text = take_screenshot_and_extract_text()
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            provider=g4f.Provider.You,
            messages=[{"role": "user", "content": salt + text}],
        )

        print(response)
        set_text_to_clipboard(response)
    except Exception as e:
        print("Error:", e)

# Add hotkeys
keyboard.add_hotkey('ctrl+alt+1', lambda: asyncio.run(process_text_gpt_programming("This is a text from the screenshot of a programming exam, it's in the Slovak language. There is also text from other stuff than the exam; ignore it. Reply with code written in C++. Do not write anything unnecessary: ")))
keyboard.add_hotkey('ctrl+alt+4', lambda: asyncio.run(process_text_bing("This is a text from the screenshot of a programming exam, it's in the Slovak language. There is also text from other stuff than the exam; ignore it. Reply with code written in C++. Do not write anything unnecessary: ")))
keyboard.add_hotkey('ctrl+alt+2', lambda: asyncio.run(process_text_gpt3("This is a text from the screenshot of a exam. There is also text from other stuff than the exam; ignore it. Provide only the correct answer in format §§answer§§ (for example if question is asking what is 2+2 you answer §§4§§, don not write anything unnecessary: ")))
keyboard.add_hotkey('ctrl+alt+3', lambda: asyncio.run(process_text_gpt3("This is a text from the screenshot of an english exam. There is also text from other stuff than the exam; ignore it. Provide only the correct answer in format §§answer§§ (for example if question is asking what is 2+2 you answer §§4§§, there also might be a question asking to fill in blank space don not write anything unnecessary: ")))
keyboard.add_hotkey('ctrl+alt+5', lambda: asyncio.run(process_text_bing("This is a text from the screenshot of a exam. There is also text from other stuff than the exam; ignore it. Provide only the correct answer in format §§answer§§ (for example if question is asking what is 2+2 you answer §§4§§, don not write anything unnecessary: ")))

# Keep the script running
keyboard.wait('ctrl+alt+0')  # Press the 'esc' key to exit the script
