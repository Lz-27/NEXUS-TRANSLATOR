from PyQt6.QtCore import QObject
from deep_translator import GoogleTranslator

LANGUAGES_ES = {
    'af': 'Afrikáans', 'sq': 'Albanés', 'am': 'Amárico', 'ar': 'Árabe', 'hy': 'Armenio', 'as': 'Asamés',
    'ay': 'Aimara', 'az': 'Azerbaiyano', 'bm': 'Bambara', 'eu': 'Euskera', 'be': 'Bielorruso', 'bn': 'Bengalí',
    'bho': 'Bhojpuri', 'bs': 'Bosnio', 'bg': 'Búlgaro', 'ca': 'Catalán', 'ceb': 'Cebuano', 'ny': 'Chichewa',
    'zh-CN': 'Chino (Simplificado)', 'zh-TW': 'Chino (Tradicional)', 'co': 'Corso', 'hr': 'Croata', 'cs': 'Checo',
    'da': 'Danés', 'dv': 'Maldivo (Dhivehi)', 'doi': 'Dogri', 'nl': 'Neerlandés', 'en': 'Inglés', 'eo': 'Esperanto',
    'et': 'Estonio', 'ee': 'Ewe', 'tl': 'Filipino', 'fi': 'Finlandés', 'fr': 'Francés', 'fy': 'Frisón',
    'gl': 'Gallego', 'ka': 'Georgiano', 'de': 'Alemán', 'el': 'Griego', 'gn': 'Guaraní', 'gu': 'Guyaratí',
    'ht': 'Criollo Haitiano', 'ha': 'Hausa', 'haw': 'Hawaiano', 'iw': 'Hebreo', 'hi': 'Hindi', 'hmn': 'Hmong',
    'hu': 'Húngaro', 'is': 'Islandés', 'ig': 'Igbo', 'ilo': 'Ilocano', 'id': 'Indonesio', 'ga': 'Irlandés',
    'it': 'Italiano', 'ja': 'Japonés', 'jw': 'Javanés', 'kn': 'Canarés', 'kk': 'Kazajo', 'km': 'Jemer',
    'rw': 'Kinyarwanda', 'gom': 'Konkani', 'ko': 'Coreano', 'kri': 'Krio', 'ku': 'Kurdo (Kurmanji)',
    'ckb': 'Kurdo (Sorani)', 'ky': 'Kirguís', 'lo': 'Lao', 'la': 'Latín', 'lv': 'Letón', 'ln': 'Lingala',
    'lt': 'Lituano', 'lg': 'Luganda', 'lb': 'Luxemburgués', 'mk': 'Macedonio', 'mai': 'Maithili', 'mg': 'Malgache',
    'ms': 'Malayo', 'ml': 'Malayalam', 'mt': 'Maltés', 'mi': 'Maorí', 'mr': 'Maratí', 'mni-Mtei': 'Meitei (Manipuri)',
    'lus': 'Mizo', 'mn': 'Mongol', 'my': 'Birmano', 'ne': 'Nepalí', 'no': 'Noruego', 'or': 'Odia (Oriya)',
    'om': 'Oromo', 'ps': 'Pastún', 'fa': 'Persa', 'pl': 'Polaco', 'pt': 'Portugués', 'pa': 'Panyabí',
    'qu': 'Quechua', 'ro': 'Rumano', 'ru': 'Ruso', 'sm': 'Samoano', 'sa': 'Sánscrito', 'gd': 'Gaélico Escocés',
    'nso': 'Sepedi', 'sr': 'Serbio', 'st': 'Sesoto', 'sn': 'Shona', 'sd': 'Sindhi', 'si': 'Cingalés',
    'sk': 'Eslovaco', 'sl': 'Esloveno', 'so': 'Somalí', 'es': 'Español', 'su': 'Sundanés', 'sw': 'Suajili',
    'sv': 'Sueco', 'tg': 'Tayiko', 'ta': 'Tamil', 'tt': 'Tártaro', 'te': 'Telugu', 'th': 'Tailandés',
    'ti': 'Tigriña', 'ts': 'Tsonga', 'tr': 'Turco', 'tk': 'Turcomano', 'ak': 'Twi', 'uk': 'Ucraniano',
    'ur': 'Urdu', 'ug': 'Uigur', 'uz': 'Uzbeko', 'vi': 'Vietnamita', 'cy': 'Galés', 'xh': 'Xhosa',
    'yi': 'Yidis', 'yo': 'Yoruba', 'zu': 'Zulú'
}

class TranslatorModel(QObject):
    def __init__(self):
        super().__init__()
        # Mantenemos el diccionario original
        self.original_languages_dict = GoogleTranslator().get_supported_languages(as_dict=True)
        
        # Mapear los nombres a Español ordenados alfabéticamente
        spanish_names = list(LANGUAGES_ES.values())
        spanish_names.sort()
        # Add Detectar Idioma at the top
        self.display_langs = ["Detectar Idioma"] + spanish_names
        
        # Crear diccionarios inversos para búsquedas rápidas (Nombre Español -> Código)
        self.name_to_code = {v: k for k, v in LANGUAGES_ES.items()}

    def get_languages(self):
        return self.display_langs

    def translate(self, text, source_lang_es, target_lang_es):
        try:
            if source_lang_es == 'Detectar Idioma':
                source_code = 'auto'
            else:
                source_code = self.name_to_code.get(source_lang_es, 'auto')
                
            target_code = self.name_to_code.get(target_lang_es, 'es')
            
            translator = GoogleTranslator(source=source_code, target=target_code)
            return translator.translate(text)
        except Exception as e:
            return f"Oops, error de conexión: {str(e)}"
