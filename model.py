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
        # Mapear los nombres a Español ordenados alfabéticamente
        spanish_names = list(LANGUAGES_ES.values())
        spanish_names.sort()
        # Add Detectar Idioma at the top
        self.display_langs = ["Detectar Idioma"] + spanish_names
        
        # Crear diccionarios inversos para búsquedas rápidas (Nombre Español -> Código y Código -> Nombre Español)
        self.name_to_code = {v: k for k, v in LANGUAGES_ES.items()}
        self.code_to_name = {k: v for k, v in LANGUAGES_ES.items()}

        # Sesión HTTP persistente con pool de conexiones (reutiliza SSL/TCP para ultra-baja latencia)
        import requests
        self.session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=1)
        self.session.mount('https://', adapter)
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
        })
        
        # Caché en memoria para respuestas instantáneas al reescribir o intercambiar
        self.cache = {}

    def get_languages(self):
        return self.display_langs

    def _translate_mymemory(self, text, source_code, target_code):
        src = 'en' if source_code in ('auto', None, '') else source_code
        tgt = target_code or 'es'
        
        if src == tgt:
            return text, src
            
        params = {
            'q': text,
            'langpair': f"{src}|{tgt}"
        }
        resp = self.session.get('https://api.mymemory.translated.net/get', params=params, timeout=2.5)
        if resp.status_code == 200:
            data = resp.json()
            if 'responseData' in data and data['responseData']:
                translated = data['responseData'].get('translatedText')
                if translated and not translated.startswith("MYMEMORY WARNING"):
                    return translated, src
        raise Exception("MyMemory translation failed")

    def _translate_google_api(self, text, source_code, target_code):
        src = 'auto' if source_code in ('auto', None) else source_code
        tgt = target_code or 'es'
        params = {
            'client': 'gtx',
            'sl': src,
            'tl': tgt,
            'dt': 't',
            'q': text
        }
        resp = self.session.get('https://translate.googleapis.com/translate_a/single', params=params, timeout=2.5)
        if resp.status_code == 200:
            data = resp.json()
            if data and isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                result = "".join([segment[0] for segment in data[0] if segment and segment[0]])
                # Detectar el idioma detectado por Google
                detected_lang = data[2] if len(data) > 2 and isinstance(data[2], str) else src
                if result:
                    return result, detected_lang
        raise Exception(f"Google API error {resp.status_code}")

    def _translate_single(self, text, source_code, target_code):
        if not text or not text.strip():
            return "", source_code

        # Cache check
        cache_key = (text.strip(), source_code, target_code)
        if cache_key in self.cache:
            return self.cache[cache_key]

        # Intento 1: Google GTX API con sesión persistente (latencia ~30-70ms)
        try:
            res, det = self._translate_google_api(text, source_code, target_code)
            self.cache[cache_key] = (res, det)
            return res, det
        except Exception:
            pass

        # Intento 2: deep_translator GoogleTranslator
        try:
            translator = GoogleTranslator(source=source_code, target=target_code)
            res = translator.translate(text)
            self.cache[cache_key] = (res, source_code)
            return res, source_code
        except Exception:
            pass

        # Intento 3: MyMemory API de respaldo
        try:
            res, det = self._translate_mymemory(text, source_code, target_code)
            self.cache[cache_key] = (res, det)
            return res, det
        except Exception:
            pass

        return text, source_code

    def translate(self, text, source_lang_es, target_lang_es):
        try:
            if not text or not text.strip():
                return "", ""

            if source_lang_es.startswith('Detectar Idioma'):
                source_code = 'auto'
            else:
                source_code = self.name_to_code.get(source_lang_es, 'auto')
                
            target_code = self.name_to_code.get(target_lang_es, 'es')
            
            # Si el texto contiene varios párrafos largos, traducirlos concurrentemente
            paragraphs = text.split('\n')
            if len(paragraphs) > 1 and len(text) > 120:
                from concurrent.futures import ThreadPoolExecutor
                
                with ThreadPoolExecutor(max_workers=min(4, len(paragraphs))) as executor:
                    futures = [
                        executor.submit(self._translate_single, p, source_code, target_code) if p.strip() else None
                        for p in paragraphs
                    ]
                    results = []
                    detected = source_code
                    for p, f in zip(paragraphs, futures):
                        if f is not None:
                            translated_part, det = f.result()
                            results.append(translated_part)
                            if det and det != 'auto':
                                detected = det
                        else:
                            results.append(p)
                    
                    detected_name = self.code_to_name.get(detected, detected)
                    return "\n".join(results), detected_name
            else:
                res, detected = self._translate_single(text, source_code, target_code)
                detected_name = self.code_to_name.get(detected, detected)
                return res, detected_name

        except Exception as e:
            return f"Oops, error de conexión: {str(e)}", ""




