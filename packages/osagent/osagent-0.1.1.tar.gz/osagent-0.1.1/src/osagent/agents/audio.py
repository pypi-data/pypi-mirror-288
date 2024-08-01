import sounddevice as sd
import numpy as np
from scipy.io import wavfile
from openai import OpenAI

RATE = 44100
CHANNELS = 1

is_recording = False
recorded_audio = []


def start_recording():
    global is_recording, recorded_audio
    print("* Recording started.")
    is_recording = True
    recorded_audio = []

    def callback(indata, frames, time, status):
        if status:
            print(status)
        if is_recording:
            recorded_audio.append(indata.copy())

    stream = sd.InputStream(samplerate=RATE, channels=CHANNELS, callback=callback)
    stream.start()
    return stream


def stop_recording(stream, filename):
    global is_recording
    is_recording = False
    stream.stop()
    stream.close()
    print("* Recording stopped.")

    # Convert list of numpy arrays to a single numpy array
    audio_data = np.concatenate(recorded_audio, axis=0)

    # Normalize audio data to 16-bit range
    audio_data = (audio_data * np.iinfo(np.int16).max).astype(np.int16)

    # Write audio data to file
    wavfile.write(filename, RATE, audio_data)

    print(f"* Audio saved to {filename}")


def transcribe_audio(filename):
    client = OpenAI()

    with open(filename, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    return transcription.text


from pathlib import Path
from openai import OpenAI
import pygame


def text_to_speech(text: str, voice: str = "nova", model: str = "tts-1") -> Path:
    speech_file_path = Path(__file__).parent / "speech.mp3"
    client = OpenAI()
    response = client.audio.speech.create(
        model=model,
        voice=voice,
        input=text
    )
    response.stream_to_file(speech_file_path)
    return speech_file_path


def play_audio(file_path: Path):
    pygame.mixer.init()
    pygame.mixer.music.load(str(file_path))
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


def text_to_speech_and_play(text: str, voice: str = "alloy", model: str = "tts-1"):
    file_path = text_to_speech(text, voice, model)
    play_audio(file_path)
