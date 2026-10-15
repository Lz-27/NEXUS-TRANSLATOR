import os
import tempfile
import subprocess
from PyQt6.QtCore import QTimer, QThread, pyqtSignal

class AudioWorker(QThread):
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, text, lang_code):
        super().__init__()
        self.text = text
        self.lang_code = lang_code

    def run(self):
        try:
            from gtts import gTTS
            
            tts = gTTS(text=self.text, lang=self.lang_code)
            temp_path = os.path.join(tempfile.gettempdir(), "nexus_translator_tts.mp3")
            
            tts.save(temp_path)
            
            # Reproducir MP3 en Windows de forma nativa sin librerías de terceros (via PowerShell)
            ps_script = f"""
            Add-Type -AssemblyName presentationCore;
            $mediaPlayer = New-Object system.windows.media.mediaplayer;
            $mediaPlayer.Open('{temp_path}');
            $mediaPlayer.Play();
            Start-Sleep -s 1;
            while ($mediaPlayer.Position -lt $mediaPlayer.NaturalDuration.TimeSpan) {{ Start-Sleep -Milliseconds 100 }};
            """
            # CREATE_NO_WINDOW = 0x08000000 ensures no console flashes
            subprocess.run(["powershell", "-Command", ps_script], creationflags=0x08000000)
            
            try:
                os.remove(temp_path)
            except:
                pass
                
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))

class TranslationWorker(QThread):
    result_ready = pyqtSignal(str, str, int)

    def __init__(self, model, text, source, target, request_id):
        super().__init__()
        self.model = model
        self.text = text
        self.source = source
        self.target = target
        self.request_id = request_id

    def run(self):
        result, detected_lang = self.model.translate(self.text, self.source, self.target)
        self.result_ready.emit(result, detected_lang, self.request_id)


class TranslatorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        from database import DatabaseManager
        self.db = DatabaseManager()
        
        self.current_request_id = 0
        self.active_workers = []
        self.audio_worker = None
        
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.start_translation)
        
        self.connect_signals()
        
        # Cargar historial inicial si la sidebar se abre
        self.view.refresh_history(self.db)
        
    def connect_signals(self):
        self.view.text_changed_signal.connect(self.on_text_changed)
        self.view.swap_requested_signal.connect(self.on_swap_requested)
        self.view.source_lang_changed_signal.connect(self.start_translation)
        self.view.target_lang_changed_signal.connect(self.start_translation)
        
        self.view.clear_requested_signal.connect(self.on_clear_requested)
        self.view.copy_requested_signal.connect(self.on_copy_requested)
        self.view.listen_requested_signal.connect(self.on_listen_requested)

    def on_clear_requested(self):
        self.view.source_text.clear()
        self.view.target_text.clear()

    def on_copy_requested(self):
        text = self.view.target_text.toPlainText()
        if text and text != "Traduciendo...":
            from PyQt6.QtWidgets import QApplication
            QApplication.clipboard().setText(text)
            
            from view import create_svg_icon
            icon_color = "#94A3B8" if self.view.is_dark_mode else "#475569"
            check_color = "#10B981"
            self.view.copy_btn.setIcon(create_svg_icon("check", check_color, 16))
            QTimer.singleShot(1500, lambda: self.view.copy_btn.setIcon(create_svg_icon("copy", icon_color, 16)))

    def on_listen_requested(self):
        text = self.view.target_text.toPlainText()
        if not text or text == "Traduciendo...":
            return
            
        target_lang_es = self.view._get_lang_name_from_btn(self.view.target_lang_btn)
        lang_code = self.model.name_to_code.get(target_lang_es, 'es')
        
        self.view.listen_btn.setEnabled(False)
        from view import create_svg_icon
        accent_color = "#3B82F6" if self.view.is_dark_mode else "#2563EB"
        self.view.listen_btn.setIcon(create_svg_icon("spinner", accent_color, 16))
        
        self.audio_worker = AudioWorker(text, lang_code)
        self.audio_worker.finished_signal.connect(self.on_audio_finished)
        self.audio_worker.error_signal.connect(self.on_audio_error)
        self.audio_worker.start()
        
    def on_audio_finished(self):
        self.view.listen_btn.setEnabled(True)
        from view import create_svg_icon
        icon_color = "#94A3B8" if self.view.is_dark_mode else "#475569"
        self.view.listen_btn.setIcon(create_svg_icon("volume", icon_color, 16))
        
    def on_audio_error(self, error_msg):
        self.view.listen_btn.setEnabled(True)
        from view import create_svg_icon
        icon_color = "#94A3B8" if self.view.is_dark_mode else "#475569"
        self.view.listen_btn.setIcon(create_svg_icon("volume", icon_color, 16))
        print(f"Error de Audio: {error_msg}")

    def on_text_changed(self):
        self.timer.start(250)
        
    def on_swap_requested(self):
        self.view.swap_languages()
        self.start_translation()

    def start_translation(self):
        text = self.view.source_text.toPlainText().strip()
        if not text:
            self.view.target_text.clear()
            self.view.status_badge.setText("Listo")
            self.current_request_id += 1 
            return
            
        source_lang = self.view._get_lang_name_from_btn(self.view.source_lang_btn)
        target_lang = self.view._get_lang_name_from_btn(self.view.target_lang_btn)
        
        self.view.status_badge.setText("Traduciendo...")
        self.view.target_text.setPlaceholderText("Traduciendo...")
        
        self.current_request_id += 1
        req_id = self.current_request_id
        
        # Desconectar o terminar trabajadores anteriores no relevantes para liberar carga
        for w in list(self.active_workers):
            try:
                w.result_ready.disconnect()
            except Exception:
                pass

        worker = TranslationWorker(self.model, text, source_lang, target_lang, req_id)
        worker.result_ready.connect(self.on_translation_finished)
        worker.finished.connect(lambda w=worker: self.cleanup_worker(w))
        
        self.active_workers.append(worker)
        worker.start()


    def on_translation_finished(self, translated_text, detected_lang, req_id):
        if req_id == self.current_request_id:
            self.view.target_text.setPlainText(translated_text)
            self.view.status_badge.setText("Listo")
            
            # Si el usuario eligió 'Detectar Idioma', mostrar el idioma detectado en el botón
            current_src_text = self.view.source_lang_btn.text()
            if "Detectar Idioma" in current_src_text and detected_lang:
                self.view.source_lang_btn.setText(f"Detectar Idioma ({detected_lang}) ▾")

            source = self.view.source_text.toPlainText().strip()
            if source and translated_text and "Oops, error" not in translated_text:
                source_lang = self.view._get_lang_name_from_btn(self.view.source_lang_btn)
                target_lang = self.view._get_lang_name_from_btn(self.view.target_lang_btn)
                self.db.add_translation(source_lang, target_lang, source, translated_text)
                self.view.refresh_history(self.db)
            
    def cleanup_worker(self, worker):
        if worker in self.active_workers:
            self.active_workers.remove(worker)

