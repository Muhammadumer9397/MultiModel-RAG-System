import os
import logging
import warnings
import speech_recognition as sr
from io import BytesIO

# ✅ Add ffmpeg to PATH before importing pydub
os.environ["PATH"] += os.pathsep + r"D:\ffmpeg-8.0-essentials_build\bin"

# ✅ Suppress ffmpeg warning
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv.*")

# ✅ Import pydub after setting PATH
from pydub import AudioSegment
from pydub.utils import which

# ✅ Set ffmpeg path manually (optional but safe)
AudioSegment.converter = r"D:\ffmpeg-8.0-essentials_build\bin\ffmpeg.exe"
print("Using ffmpeg from:", which("ffmpeg") or AudioSegment.converter)

# ✅ Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ✅ Load .env
from dotenv import load_dotenv
load_dotenv()

# ✅ Load Groq config
from groq import Groq
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
stt_model = "whisper-large-v3"
audio_filepath = "patient_voice_test_for_patient.mp3"

# ✅ Audio Recording Function
def record_audio(file_path, timeout=20, phrase_time_limit=None):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            # recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")

            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            logging.info(f"Audio saved to: {file_path}")

    except Exception as e:
        logging.error(f"An error occurred while recording: {e}")

# ✅ Transcription Function
def transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY):
    try:
        client = Groq(api_key=GROQ_API_KEY)
        with open(audio_filepath, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model=stt_model,
                file=audio_file,
                language="en"
            )
        print("\n🎧 Transcription:\n", transcription.text)
    except Exception as e:
        logging.error(f"An error occurred during transcription: {e}")

# ✅ Run Everything
record_audio(file_path=audio_filepath)
transcribe_with_groq(stt_model, audio_filepath, GROQ_API_KEY)
