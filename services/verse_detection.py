from fuzzywuzzy import fuzz

class VerseDetector:
    def __init__(self, surah_data):
        self.surah_data = surah_data
        self.last_detected_verse = None

    def detect_verse(self, audio_text):
        detected_verse = None
        highest_similarity = 50  # Track the best match score
        for surah in self.surah_data.values():
            for verse_key, verse_value in surah['verse'].items():
                if verse_value in audio_text:
                    detected_verse = {
                        "surah": surah['name'],
                        "surah_index": surah['index'],
                        "verse_number": verse_key,
                        "verse_text": verse_value,
                    }
                    # print(f"org_verse :  {verse_value}")
                else:
                    similarity = fuzz.ratio(verse_value, audio_text)
                # If the similarity is above a certain threshold (e.g., 80%), consider it a match
                    if similarity > highest_similarity:
                        detected_verse = {
                            "surah": surah['name'],
                            "surah_index": surah['index'],
                            "verse_number": verse_key,
                            "verse_text": verse_value,
                        }
                        # print(f"org_verse:  {verse_value}")
                        # print(f"sim:  {similarity}")
        if detected_verse:
            # Restart logic: check if the detected verse was the same as the previous one
            if self.last_detected_verse and detected_verse["verse_text"] == self.last_detected_verse["verse_text"]:
                print("Verse restart detected.")
            self.last_detected_verse = detected_verse

        return detected_verse


