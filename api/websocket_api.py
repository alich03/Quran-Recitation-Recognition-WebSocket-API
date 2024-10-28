from fastapi import FastAPI, WebSocket
import json
from services.audio_processing import AudioProcessor
from services.verse_detection import VerseDetector
from services.translation_service import TranslationService,get_audio_reponse
from utils.json_loader import load_surah_data, load_translation_data

app = FastAPI()

surah_data = load_surah_data()
translations = load_translation_data()

audio_processor = AudioProcessor()
verse_detector = VerseDetector(surah_data)
translation_service = TranslationService(translations)
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    user_translation_preference = None

    while True:
        data = await websocket.receive_text()
        message = json.loads(data)

        if "translation_preference" in message:
            user_translation_preference = message["translation_preference"]
            await websocket.send_text(f"Translation preference set to: {user_translation_preference}")
            continue

        # Process audio and detect verse
        text = audio_processor.process_audio(message["audio_data"])
        print(f"audio_text: {text}")
        verse_info = verse_detector.detect_verse(text)

        if verse_info:                                          #surah index                 #verse number
            translation = translation_service.get_translation(verse_info["surah_index"], verse_info["verse_number"], user_translation_preference)
            audio_reponse = get_audio_reponse(verse_info["surah"],verse_info["verse_number"],translation)
            response = {
                "surah": verse_info["surah"],
                "verse_number": verse_info["verse_number"],
                "verse_text": verse_info["verse_text"],
                "translation": translation,
                "audio_reponse": audio_reponse,
            }
            print("......")
            await websocket.send_text(json.dumps(response))
        else:
            await websocket.send_text(json.dumps({"error": "No verse detected."}))


#end 