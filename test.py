import base64
import re
import asyncio
import websockets
import json
import base64
import nest_asyncio
# audio_file = "verse_4.ogg"  #or . wave


def audio_to_base64(audio_file_path):
    with open(audio_file_path, "rb") as audio_file:
        encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')
        # print(encoded_audio)
        return encoded_audio


def base64_to_audio(base64_audio_string,output_file_path):

    audio_data = base64.b64decode(base64_audio_string)
    with open(output_file_path, "wb") as audio_file:
        audio_file.write(audio_data)
    print(f"Audio file saved to {output_file_path}")

    return output_file_path   #returning path



nest_asyncio.apply()

async def send_audio(websocket_url, audio_file_path, translation_preference=None):

    base64_audio_string = audio_to_base64(audio_file_path)

    async with websockets.connect(websocket_url,ping_interval=50) as websocket:
        # Set translation preference if provided
        if translation_preference:
            await websocket.send(json.dumps({
                "translation_preference": translation_preference
            }))
            response = await websocket.recv()
            print(f"Translation preference response: {response}")
        
        await websocket.send(json.dumps({
            "audio_data": base64_audio_string
        }))
        
        
        response = await websocket.recv()
        response = json.loads(response)

        try:
            print(f"Surah Name: {response['surah']}")
            verse_number = int(re.search(r'\d+', response['verse_number'] ).group())
            print(f"Verse Number: {verse_number} ")
            print(f"Verse text: {response['verse_text']}")
            print(f"Verse Translation: {response['translation']}")
            base64_audio = response['audio_reponse']
            saved_path = base64_to_audio(base64_audio,f"output/{response['surah']}_{response['verse_number']}_.mp3")

        except:
            print(f"Received response: {response}")


websocket_url = "ws://127.0.0.1:8000/ws"
audio_file_path = "input/ina.ogg"  # (e.g., an MP3 or WAV of .ogg file)
translation_preference = "arabic"

asyncio.get_event_loop().run_until_complete(
    send_audio(websocket_url, audio_file_path, translation_preference)
)