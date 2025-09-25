from pathlib import Path
import os
from elevenlabs.client import ElevenLabs
from elevenlabs import VoiceSettings
import uuid

from dotenv import load_dotenv
load_dotenv()

elevenlabs_ai_key = os.getenv("ELEVENLABS_API_KEY", None)
if not elevenlabs_ai_key:
    raise ValueError("ELEVENLABS_API_KEY not found in environment variables.")

def generate_podcast_from_script(outline, out_name):
    elevenlabs = ElevenLabs(
        api_key=elevenlabs_ai_key,
    )
    audio = elevenlabs.text_to_speech.convert(
        text=outline,
        voice_id="MzqUf1HbJ8UmQ0wUsx2p",
        language_code="en",
        seed=1234,
        output_format="mp3_22050_32",
        model_id="eleven_flash_v2_5",
        apply_text_normalization="on",
        voice_settings=VoiceSettings(
            stability=.5,
            similarity_boost=.75,
            style=0.0,
            use_speaker_boost=False,
            speed=1.0,
        ),
    )

    speech_file_name = f"podcast-{out_name}-{uuid.uuid4()}.mp3"
    speech_file_path = Path(__file__).parent.parent / "out" / speech_file_name
    with open(speech_file_path, "xb") as f:
        for chunk in audio:
            if chunk:
                f.write(chunk)
    return speech_file_path