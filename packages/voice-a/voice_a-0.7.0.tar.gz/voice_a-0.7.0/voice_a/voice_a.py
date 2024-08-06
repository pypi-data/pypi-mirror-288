from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import threading
import time
import requests
import base64
import os 
from virtual_aide.assistreq_pws import set_env_vars
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pvporcupine
import pyaudio
import struct
from playsound import playsound
from typing import List, Optional 


#Hotword

class HotwordDetector:
    def __init__(self, keywords: List[str] = ['picovoice', 'terminator', 'americano', 'hey siri', 'bumblebee', 'ok google', 'blueberry', 'jarvis', 'pico clock', 'porcupine', 'grapefruit', 'hey google', 'alexa'], 
                 activation_sound_path: Optional[str] = None,
                 deactivation_sound_path: Optional[str] = None,
                 prints: bool = False) -> None:
        self.keywords = keywords
        self.activation_sound_path = activation_sound_path
        self.deactivation_sound_path = deactivation_sound_path
        self.prints = prints

        self.porcupine = pvporcupine.create(keywords=self.keywords)
        self.audio_interface = pyaudio.PyAudio()
        self.audio_stream = self.audio_interface.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
        )

        self._stop_requested = False

    def stop(self) -> None:
        self._stop_requested = True
        if self.prints: print("Hotword detection has been stopped.")

    def listen_for_hotwords(self, stop_event: Optional[object] = None) -> bool:
        try:
            if self.deactivation_sound_path:
                self._play_sound(self.deactivation_sound_path)
            if self.prints: print("Listening for hotwords...")
            while not self._stop_requested and (stop_event is None or not stop_event.is_set()):
                audio_data = self.audio_stream.read(self.porcupine.frame_length)
                audio_data = struct.unpack_from("h" * self.porcupine.frame_length, audio_data)
                keyword_index = self.porcupine.process(audio_data)
                if keyword_index >= 0:
                    detected_keyword = self.keywords[keyword_index]
                    if self.prints: print(f"Hotword detected: {detected_keyword}")
                    if self.activation_sound_path:
                        self._play_sound(self.activation_sound_path)
                    return True  # Return True if a hotword is detected

        finally:
            self._cleanup()

    def _play_sound(self, sound_path: Optional[str]) -> None:
        if sound_path: playsound(sound_path)
        if self.prints: print(f"Playing sound: {sound_path}")
            

    def _cleanup(self) -> None:
        if self.prints: print("Cleaning up resources...")
        if self.porcupine is not None:
            self.porcupine.delete()
        if self.audio_stream is not None:
            self.audio_stream.close()
        if self.audio_interface is not None:
            self.audio_interface.terminate()
        if self.prints: print("Resources have been cleaned up.")
    
if __name__ == "__main__":
    detector = HotwordDetector(prints=True)
    hotword_detected = detector.listen_for_hotwords()

    if hotword_detected:
        print("Executing actions for detected hotword.........")

###################################################################################################

#Stop_word

def play_audio_Event(file_path: str, stop_event: threading.Event, prints: bool = False) -> None:
  
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    if prints: print(f"Playing audio: {file_path}")
    
    while pygame.mixer.music.get_busy() and not stop_event.is_set():
        time.sleep(0.1)  
    
    if stop_event.is_set():
        pygame.mixer.music.stop()
        if prints: print("Audio playback stopped.")
    
    pygame.mixer.quit()
    if prints: print("Pygame mixer quit.")

def detect_hotword(detector: HotwordDetector, stop_event: threading.Event, prints: bool = False) -> None:
    
    hotword_detected = detector.listen_for_hotwords()
    if hotword_detected:
        stop_event.set()
        if prints: print("Hotword detected, Setting Stop Event.")

def play_audio(audio_file_path: str = "asset\output_audio.mp3", prints: bool = False) -> None:
    stop_event = threading.Event()
    detector = HotwordDetector()

    audio_thread = threading.Thread(target=play_audio_Event, args=(audio_file_path, stop_event, prints))
    hotword_thread = threading.Thread(target=detect_hotword, args=(detector, stop_event, prints))

    audio_thread.start()
    hotword_thread.start()

    audio_thread.join()
    detector.stop()
    hotword_thread.join()

    if prints: print("Application exited gracefully.")

set_env_vars()
model_name = os.getenv('MODEL_NAME')
def speak(text: str, model: str = model_name, filename: str = "asset\output_audio.mp3"):
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass

    url = "https://deepgram.com/api/ttsAudioGeneration"
    payload = {"text": text, "model": model}

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() 

        with open(filename, 'wb') as audio_file:
            audio_file.write(base64.b64decode(response.json()['data']))

        play_audio(filename)
        os.remove(filename)
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}") 
    except Exception as err:
        print(f"An error occurred: {err}")  

# if __name__ == "__main__":
    # speak("Thank you for watching! I hope you found this video informative and helpful. If you did, please give it a thumbs up and consider subscribing to my channel for more videos like this")

#SPEECH

class SpeechToTextListener:
    def __init__(
            self, 
            website_path: str = "https://realtime-stt-devs-do-code.netlify.app/", 
            language: str = "en-US",
            wait_time: int = 10):
        
        self.website_path = website_path
        self.language = language
        self.chrome_options = Options()
        self.chrome_options.add_argument("--use-fake-ui-for-media-stream")
        self.chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        self.chrome_options.add_argument("--headless=new")
        self.chrome_options.add_argument("--log-level=3")  
        self.chrome_options.add_argument("--disable-gpu")  
        self.chrome_options.add_argument("--no-sandbox")  
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.wait = WebDriverWait(self.driver, wait_time)
        self.stop_event = threading.Event()

    def stream(self, content: str):
        """Prints the given content to the console, overwriting previous output."""
        print("\rUser Speaking: " + f"{content}", end='', flush=True)

    def get_text(self) -> str:
        """Retrieves the transcribed text from the website."""
        return self.driver.find_element(By.ID, "convert_text").text

    def select_language(self):
        """Selects the language from the dropdown using JavaScript."""
        self.driver.execute_script(
            f"""
            var select = document.getElementById('language_select');
            select.value = '{self.language}';
            var event = new Event('change');
            select.dispatchEvent(event);
            """
        )

    def verify_language_selection(self):
        """Verifies if the language is correctly selected."""
        language_select = self.driver.find_element(By.ID, "language_select")
        selected_language = language_select.find_element(By.CSS_SELECTOR, "option:checked").get_attribute("value")
        return selected_language == self.language

    def main(self) -> Optional[str]:
        try:
            self.driver.get(self.website_path)
            
            self.wait.until(EC.presence_of_element_located((By.ID, "language_select")))
            
            self.select_language()

            if not self.verify_language_selection():
                print(f"Error: Failed to select the correct language. Selected: {self.verify_language_selection()}, Expected: {self.language}")
                return None

            self.driver.find_element(By.ID, "click_to_record").click()

            is_recording = self.wait.until(EC.presence_of_element_located((By.ID, "is_recording")))

            stream_thread = threading.Thread(target=self.update_stream)
            stream_thread.start()

            while True:
                is_recording_text = self.driver.find_element(By.ID, "is_recording").text
                if not is_recording_text.startswith("Recording: True"):
                    self.stop_event.set()  
                    break
                time.sleep(2) 

            stream_thread.join() 
            return self.get_text()
        except Exception as e:
            print(f"Error during main processing: {e}")
            return None

    def update_stream(self):
    
        while not self.stop_event.is_set():
            try:
                text = self.get_text()
                if text:
                    self.stream(text)
                time.sleep(1)  
            except Exception as e:
                print(f"Error during streaming update: {e}")
                break

    def listen(self, prints: bool = False) -> Optional[str]:
        while True:
            result = self.main()
            if result and len(result) != 0:
                print("\r" + " " * (len(result) + 16) + "\r", end="", flush=True)
                if prints: print("\rYOU SAID: " + f"{result}\n")
                break
        return result

# if __name__ == "__main__":
#     listener = SpeechToTextListener(language="en-US") 
#     speech = listener.listen()
#     print("FINAL EXTRACTION: ", speech)