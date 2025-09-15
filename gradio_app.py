# gradio_app.py

import os
import gradio as gr
from dotenv import load_dotenv
load_dotenv()

# Import your custom modules
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_elevenlabs

# Define system prompt
system_prompt = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
What's in this image?. Do you find anything wrong with it medically? 
If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
Donot say 'In the image I see' but say 'With what I see, I think you have ....'
Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
Keep your answer concise (max 2 sentences). No preamble, start your answer right away please."""


# Main processing function
def process_inputs(audio_filepath, image_filepath):
    print(f"🎤 Audio path: {audio_filepath}")
    print(f"🖼️ Image path: {image_filepath}")

    # Step 1: Transcribe speech
    transcription = transcribe_with_groq(
        GROQ_API_KEY=os.environ.get("GROQ_API_KEY"),
        audio_filepath=audio_filepath,
        stt_model="whisper-large-v3"
    )

    print(f"📝 Transcription result: {transcription}")

    if not transcription:
        return "❌ Transcription failed. Try again.", "", None

    # Step 2: Analyze image if provided
    if image_filepath:
        query = system_prompt + transcription
        encoded_img = encode_image(image_filepath)

        doctor_response = analyze_image_with_query(
            query=query,
            encoded_image=encoded_img,
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        )
    else:
        doctor_response = "⚠️ No image provided for me to analyze."

    print(f"💬 Doctor Response: {doctor_response}")

    # Step 3: Convert doctor's response to speech
    output_voice_path = "final.mp3"
    try:
        text_to_speech_with_elevenlabs(
            input_text=doctor_response,
            output_filepath=output_voice_path
        )
    except Exception as e:
        print(f"❌ TTS failed: {e}")
        output_voice_path = None

    return transcription, doctor_response, output_voice_path


# Gradio interface
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="🎤 Record Your Voice"),
        gr.Image(type="filepath", label="🖼️ Upload Image (X-ray, etc.)")
    ],
    outputs=[
        gr.Textbox(label="📝 Transcription"),
        gr.Textbox(label="🧠 Doctor's Response"),
        gr.Audio(label="🔊 Voice of the Doctor", type="filepath")
    ],
    title="🧠 AI Doctor with Vision and Voice"
)

# Launch app
iface.launch(debug=True)
