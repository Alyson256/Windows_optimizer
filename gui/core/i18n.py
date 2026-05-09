import json
import os

class I18n:
    def __init__(self, lang="pt"):
        self.lang = lang
        self.translations = {}
        self.load_language(lang)

    def load_language(self, lang):
        self.lang = lang
        locales_dir = os.path.join(os.path.dirname(__file__), "..", "locales")
        file_path = os.path.join(locales_dir, f"{lang}.json")
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            # Fallback to English if file not found
            if lang != "en":
                self.load_language("en")

    def get(self, key, default=""):
        keys = key.split('.')
        value = self.translations
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
