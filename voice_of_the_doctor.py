# voice_of_the_doctor.py

from dotenv import load_dotenv
load_dotenv()

import os
import subprocess
import platform
from gtts import gTTS
import elevenlabs
from elevenlabs.client import ElevenLabs

# === Get ElevenLabs API Key from .env ===
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# === Universal audio playback function ===
def play_audio(output_filepath):
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            # Use Start-Process instead of Media.SoundPlayer (which requires WAV)
            subprocess.run(['powershell', '-Command', f'Start-Process "{output_filepath}"'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['ffplay', '-nodisp', '-autoexit', output_filepath])
        else:
            raise OSError("Unsupported operating system")
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")

# === gTTS TTS Function ===
def text_to_speech_with_gtts(input_text, output_filepath):
    language = "en"
    audioobj = gTTS(text=input_text, lang=language, slow=False)
    audioobj.save(output_filepath)
    play_audio(output_filepath)

# === ElevenLabs TTS Function ===
def text_to_speech_with_elevenlabs(input_text, output_filepath):
    if not ELEVENLABS_API_KEY:
        print("❌ ELEVENLABS_API_KEY is missing. Please check your .env file.")
        return

    client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = client.generate(
        text=input_text,
        voice="Aria",
        output_format="mp3_22050_32",
        model="eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)
    play_audio(output_filepath)

# === Run both TTS systems ===
if __name__ == "__main__":
    input_text = "Hi this is AI with Hassan, autoplay testing!"

    # gTTS test
    gtts_output = "gtts_testing_autoplay.mp3"
    text_to_speech_with_gtts(input_text=input_text, output_filepath=gtts_output)

    # ElevenLabs test
    eleven_output = "elevenlabs_testing_autoplay.mp3"
    text_to_speech_with_elevenlabs(input_text=input_text, output_filepath=eleven_output)
