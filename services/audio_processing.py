import whisper

import base64
import io
import librosa
import numpy as np
import torch


class AudioProcessor:
    def __init__(self, model_path='small'):
        self.model = whisper.load_model(model_path)
        print("Whisper model loaded successfully!")

    def process_audio(self, audio_data):              # Assuming `audio_data` is a valid audio file buffer (WAV/MP3)
        # Decode the base64 audio data into binary
        audio_data = base64.b64decode(audio_data)
        # Create an in-memory file-like object using the decoded data
        audio_file = io.BytesIO(audio_data)

        audio, sr = librosa.load(audio_file, sr=None)  # sr=None keeps the original sample rate
        # Convert the audio data to a PyTorch tensor
        audio_tensor = torch.from_numpy(audio)


        result = self.model.transcribe(audio_tensor, language='ar')
        text = result['text']
        print("audio text returned !")
        return text
