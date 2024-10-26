import json
import os

def load_surah_data():
    surah_data = {}
    surah_directory = 'surah_data'

    # Load all Surah JSON files
    for filename in os.listdir(surah_directory):
        if filename.endswith('.json'):
            with open(os.path.join(surah_directory, filename), 'r', encoding='utf-8') as f:
                surah = json.load(f)
                surah_data[surah['index']] = surah

    print("Surah data loaded successfully!")
    return surah_data






def load_translation_data():
    with open('translations/translation.json', 'r', encoding='utf-8') as f:
        translations = json.load(f)
        print("Translation data loaded successfully!")
    return translations
