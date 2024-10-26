from gtts import gTTS
import base64
import re


class TranslationService:
    def __init__(self, translations):
        self.translations = translations

    def get_translation(self, surah_index, verse_number, user_preference="default"):
        
        verse_number_int = int(re.search(r'\d+', verse_number ).group())
        surah_index = str(int(surah_index))
        verse_number = str(verse_number_int)
        # print(f"surah index: {surah_index}")
        # print(f"verse_number: {verse_number}")
        if surah_index in self.translations:
            translation_data = self.translations[surah_index]
            if verse_number in translation_data:
                return translation_data[verse_number]
        return "Translation not found."
    
def get_audio_reponse(surah_name,verse_number,translation):
        
        verse_number_int = int(re.search(r'\d+', verse_number ).group())

        tts = gTTS(f'surah {surah_name} verse number {verse_number_int}.The translation is : {translation}' , lang='en')
        audio_file = "output/reponse.mp3"
        tts.save(audio_file)
        with open(audio_file, "rb") as audio_file:
            encoded_audio = base64.b64encode(audio_file.read()).decode('utf-8')
        print("Audio generated...")
        return encoded_audio
