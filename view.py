from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QPushButton, QLabel, QGraphicsDropShadowEffect, 
                             QFrame, QDialog, QLineEdit, QListWidget, QListWidgetItem,
                             QAbstractItemView, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QCursor, QPainter, QIcon, QPixmap
from PyQt6.QtSvg import QSvgRenderer

# Iconos SVG nítidos y vectoriales integrados
SVGS = {
    "menu": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>""",
    "moon": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>""",
    "sun": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>""",
    "info": """<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>""",
    "swap": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M7 16V4m0 0L3 8m4-4l4 4m6 4v12m0 0l4-4m-4 4l-4-4"/></svg>""",
    "copy": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>""",
    "check": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>""",
    "trash": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>""",
    "volume": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>""",
    "spinner": """<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="2" x2="12" y2="6"></line><line x1="12" y1="18" x2="12" y2="22"></line><line x1="4.93" y1="4.93" x2="7.76" y2="7.76"></line><line x1="16.24" y1="16.24" x2="19.07" y2="19.07"></line><line x1="2" y1="12" x2="6" y2="12"></line><line x1="18" y1="12" x2="22" y2="12"></line><line x1="4.93" y1="19.07" x2="7.76" y2="16.24"></line><line x1="16.24" y1="7.76" x2="19.07" y2="4.93"></line></svg>"""
}

def create_svg_icon(svg_key, color, size=20):
    svg_str = SVGS.get(svg_key, "").format(color=color)
    renderer = QSvgRenderer(svg_str.encode('utf-8'))
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    return QIcon(pixmap)


class LanguageSelectorDialog(QDialog):
    language_selected = pyqtSignal(str)

    def __init__(self, languages, current_lang, is_dark_mode=False, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Seleccionar idioma")
        self.setFixedSize(360, 480)
        self.languages = languages
        self.current_lang = current_lang
        self.is_dark_mode = is_dark_mode
        
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.initUI()
        
    def initUI(self):
        main_frame = QFrame(self)
        main_frame.setObjectName("popupFrame")
        layout = QVBoxLayout(main_frame)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(14)
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(35)
        shadow.setColor(QColor(0, 0, 0, 110 if self.is_dark_mode else 35))
        shadow.setOffset(0, 8)
        main_frame.setGraphicsEffect(shadow)
        
        dialog_layout = QVBoxLayout(self)
        dialog_layout.setContentsMargins(8, 8, 8, 8)
        dialog_layout.addWidget(main_frame)
        
        header_row = QHBoxLayout()
        header_title = QLabel("Seleccionar idioma")
        header_title.setObjectName("popupTitle")
        header_row.addWidget(header_title)
        header_row.addStretch()
        layout.addLayout(header_row)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Buscar idioma...")
        self.search_bar.setObjectName("searchBar")
        self.search_bar.textChanged.connect(self.filter_languages)
        layout.addWidget(self.search_bar)
        
        self.list_widget = QListWidget()
        self.list_widget.setObjectName("langList")
        self.list_widget.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        self.populate_list(self.languages)
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.list_widget)
        
        self.apply_styles()
        
    def populate_list(self, items):
        self.list_widget.clear()
        for lang in items:
            item = QListWidgetItem(lang)
            if lang == self.current_lang:
                font = item.font()
                font.setBold(True)
                item.setFont(font)
            item.setSizeHint(QSize(0, 38))
            self.list_widget.addItem(item)
            
    def filter_languages(self, text):
        filtered = [lang for lang in self.languages if text.lower() in lang.lower()]
        self.populate_list(filtered)
        
    def on_item_clicked(self, item):
        self.language_selected.emit(item.text())
        self.accept()

    def apply_styles(self):
        if self.is_dark_mode:
            self.setStyleSheet("""
                QFrame#popupFrame { 
                    background-color: #161A23; 
                    border-radius: 16px; 
                    border: 1px solid rgba(255, 255, 255, 0.08); 
                }
                QLabel#popupTitle {
                    color: #94A3B8;
                    font-family: 'Segoe UI', system-ui;
                    font-size: 13px;
                    font-weight: 600;
                    letter-spacing: 0.5px;
                }
                QLineEdit#searchBar { 
                    background-color: #0E121A; 
                    border: 1px solid rgba(255, 255, 255, 0.08); 
                    border-radius: 10px; 
                    padding: 8px 14px; 
                    font-family: 'Segoe UI', system-ui; 
                    font-size: 14px; 
                    color: #F1F5F9; 
                }
                QLineEdit#searchBar:focus { 
                    border: 1px solid #3B82F6; 
                    background-color: #121722; 
                }
                QListWidget#langList { 
                    border: none; 
                    background-color: transparent; 
                    outline: none; 
                }
                QListWidget#langList::item { 
                    border-radius: 8px; 
                    padding: 6px 12px; 
                    font-family: 'Segoe UI', system-ui; 
                    font-size: 14px; 
                    color: #CBD5E1; 
                }
                QListWidget#langList::item:hover { 
                    background-color: rgba(59, 130, 246, 0.12); 
                    color: #93C5FD; 
                }
                QListWidget#langList::item:selected { 
                    background-color: #2563EB; 
                    color: #FFFFFF; 
                }
                QScrollBar:vertical { 
                    border: none; 
                    background: transparent; 
                    width: 5px; 
                    border-radius: 2px; 
                }
                QScrollBar::handle:vertical { 
                    background: #334155; 
                    min-height: 25px; 
                    border-radius: 2px; 
                }
                QScrollBar::handle:vertical:hover { 
                    background: #475569; 
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { 
                    border: none; 
                    background: none; 
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame#popupFrame { 
                    background-color: #FFFFFF; 
                    border-radius: 16px; 
                    border: 1px solid rgba(0, 0, 0, 0.08); 
                }
                QLabel#popupTitle {
                    color: #64748B;
                    font-family: 'Segoe UI', system-ui;
                    font-size: 13px;
                    font-weight: 600;
                    letter-spacing: 0.5px;
                }
                QLineEdit#searchBar { 
                    background-color: #F8FAFC; 
                    border: 1px solid #E2E8F0; 
                    border-radius: 10px; 
                    padding: 8px 14px; 
                    font-family: 'Segoe UI', system-ui; 
                    font-size: 14px; 
                    color: #0F172A; 
                }
                QLineEdit#searchBar:focus { 
                    border: 1px solid #2563EB; 
                    background-color: #FFFFFF; 
                }
                QListWidget#langList { 
                    border: none; 
                    background-color: transparent; 
                    outline: none; 
                }
                QListWidget#langList::item { 
                    border-radius: 8px; 
                    padding: 6px 12px; 
                    font-family: 'Segoe UI', system-ui; 
                    font-size: 14px; 
                    color: #334155; 
                }
                QListWidget#langList::item:hover { 
                    background-color: #EFF6FF; 
                    color: #1D4ED8; 
                }
                QListWidget#langList::item:selected { 
                    background-color: #2563EB; 
                    color: #FFFFFF; 
                }
                QScrollBar:vertical { 
                    border: none; 
                    background: transparent; 
                    width: 5px; 
                    border-radius: 2px; 
                }
                QScrollBar::handle:vertical { 
                    background: #CBD5E1; 
                    min-height: 25px; 
                    border-radius: 2px; 
                }
                QScrollBar::handle:vertical:hover { 
                    background: #94A3B8; 
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { 
                    border: none; 
                    background: none; 
                }
            """)


class CustomTitleBar(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setObjectName("customTitleBar")
        self.setFixedHeight(50)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 0, 16, 0)
        layout.setSpacing(10)
        
        logo_container = QHBoxLayout()
        logo_container.setSpacing(8)
        
        self.brand_dot = QFrame()
        self.brand_dot.setFixedSize(8, 8)
        self.brand_dot.setObjectName("brandDot")
        
        self.title_lbl = QLabel("NEXUS TRANSLATOR")
        self.title_lbl.setObjectName("headerLabel")
        
        self.badge_lbl = QLabel("PRO")
        self.badge_lbl.setObjectName("versionBadge")
        
        logo_container.addWidget(self.brand_dot)
        logo_container.addWidget(self.title_lbl)
        logo_container.addWidget(self.badge_lbl)
        
        layout.addLayout(logo_container)
        layout.addStretch()
        
        self.min_btn = QPushButton("—")
        self.min_btn.setObjectName("winBtn")
        self.min_btn.setFixedSize(32, 32)
        self.min_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.min_btn.clicked.connect(self.parent.showMinimized)
        
        self.close_btn = QPushButton("✕")
        self.close_btn.setObjectName("closeBtn")
        self.close_btn.setFixedSize(32, 32)
        self.close_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.close_btn.clicked.connect(self.parent.close)
        
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(6)
        controls_layout.addWidget(self.min_btn)
        controls_layout.addWidget(self.close_btn)
        
        layout.addLayout(controls_layout)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.parent.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self.parent, 'old_pos'):
            delta = event.globalPosition().toPoint() - self.parent.old_pos
            self.parent.move(self.parent.x() + delta.x(), self.parent.y() + delta.y())
            self.parent.old_pos = event.globalPosition().toPoint()


class TranslatorView(QMainWindow):
    text_changed_signal = pyqtSignal()
    swap_requested_signal = pyqtSignal()
    source_lang_changed_signal = pyqtSignal(str)
    target_lang_changed_signal = pyqtSignal(str)
    clear_requested_signal = pyqtSignal()
    copy_requested_signal = pyqtSignal()
    listen_requested_signal = pyqtSignal()

    def __init__(self, languages):
        super().__init__()
        self.languages = languages
        self.is_dark_mode = False
        
        self.setWindowTitle("Nexus Translator")
        self.setMinimumSize(1080, 660)
        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        self.initUI()
        
    def initUI(self):
        base_widget = QWidget()
        self.setCentralWidget(base_widget)
        base_layout = QHBoxLayout(base_widget)
        base_layout.setContentsMargins(18, 18, 18, 18)
        base_layout.setSpacing(14)
        
        # ---------------- BARRA LATERAL (HISTORIAL) ----------------
        self.sidebar = QFrame()
        self.sidebar.setObjectName("sidebarFrame")
        self.sidebar.setFixedWidth(0)
        
        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(18, 18, 18, 18)
        sidebar_layout.setSpacing(14)
        
        sidebar_header = QHBoxLayout()
        sidebar_title = QLabel("Historial")
        sidebar_title.setObjectName("sidebarTitle")
        sidebar_header.addWidget(sidebar_title)
        sidebar_header.addStretch()
        sidebar_layout.addLayout(sidebar_header)
        
        self.history_list = QListWidget()
        self.history_list.setObjectName("historyList")
        self.history_list.setVerticalScrollMode(QAbstractItemView.ScrollMode.ScrollPerPixel)
        sidebar_layout.addWidget(self.history_list)
        
        base_layout.addWidget(self.sidebar)
        
        # ---------------- CONTENEDOR PRINCIPAL ----------------
        self.main_bg = QFrame()
        self.main_bg.setObjectName("mainBg")
        base_layout.addWidget(self.main_bg)
        
        self.window_shadow = QGraphicsDropShadowEffect()
        self.window_shadow.setBlurRadius(40)
        self.window_shadow.setOffset(0, 10)
        self.main_bg.setGraphicsEffect(self.window_shadow)
        
        main_layout = QVBoxLayout(self.main_bg)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)
        
        # Barra superior con botones de navegación
        nav_bar = QFrame()
        nav_bar.setObjectName("navBar")
        nav_layout = QHBoxLayout(nav_bar)
        nav_layout.setContentsMargins(32, 12, 32, 12)
        nav_layout.setSpacing(10)
        
        self.history_btn = QPushButton()
        self.history_btn.setObjectName("toolBtn")
        self.history_btn.setFixedSize(40, 40)
        self.history_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.history_btn.setToolTip("Abrir historial")
        self.history_btn.clicked.connect(self.toggle_sidebar)
        nav_layout.addWidget(self.history_btn)
        
        nav_layout.addStretch()
        
        self.theme_btn = QPushButton()
        self.theme_btn.setObjectName("toolBtn")
        self.theme_btn.setFixedSize(40, 40)
        self.theme_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.theme_btn.setToolTip("Alternar modo oscuro / claro")
        self.theme_btn.clicked.connect(self.toggle_theme)
        nav_layout.addWidget(self.theme_btn)
        
        self.info_btn = QPushButton()
        self.info_btn.setObjectName("toolBtn")
        self.info_btn.setFixedSize(40, 40)
        self.info_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.info_btn.setToolTip("Información del sistema")
        self.info_btn.clicked.connect(self.show_info_dialog)
        nav_layout.addWidget(self.info_btn)
        
        main_layout.addWidget(nav_bar)
        
        # Cuerpo principal
        body_widget = QWidget()
        body_layout = QVBoxLayout(body_widget)
        body_layout.setContentsMargins(32, 8, 32, 32)
        body_layout.setSpacing(0)
        
        content_layout = QHBoxLayout()
        content_layout.setSpacing(18)
        
        # ---------------- TARJETA ORIGEN ----------------
        self.source_frame = QFrame()
        self.source_frame.setObjectName("cardFrame")
        source_layout = QVBoxLayout(self.source_frame)
        source_layout.setContentsMargins(24, 20, 24, 20)
        source_layout.setSpacing(12)
        
        source_top = QHBoxLayout()
        self.source_lang_btn = QPushButton("Detectar Idioma ▾")
        self.source_lang_btn.setObjectName("langSelectBtn")
        self.source_lang_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.source_lang_btn.clicked.connect(self.open_source_selector)
        source_top.addWidget(self.source_lang_btn)
        source_top.addStretch()
        source_layout.addLayout(source_top)
        
        source_sep = QFrame()
        source_sep.setObjectName("cardDivider")
        source_sep.setFixedHeight(1)
        source_layout.addWidget(source_sep)
        
        self.source_text = QTextEdit()
        self.source_text.setPlaceholderText("Escribe o pega el texto a traducir...")
        self.source_text.textChanged.connect(self.text_changed_signal.emit)
        self.source_text.textChanged.connect(self.update_char_count)
        source_layout.addWidget(self.source_text)
        
        source_footer = QHBoxLayout()
        self.char_count_lbl = QLabel("0 caracteres")
        self.char_count_lbl.setObjectName("charCountLbl")
        source_footer.addWidget(self.char_count_lbl)
        source_footer.addStretch()
        
        self.clear_btn = QPushButton()
        self.clear_btn.setObjectName("actionBtn")
        self.clear_btn.setFixedSize(36, 36)
        self.clear_btn.setToolTip("Limpiar texto")
        self.clear_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clear_btn.clicked.connect(self.clear_requested_signal.emit)
        source_footer.addWidget(self.clear_btn)
        
        source_layout.addLayout(source_footer)
        
        self.shadow1 = QGraphicsDropShadowEffect()
        self.shadow1.setBlurRadius(25)
        self.shadow1.setOffset(0, 4)
        self.source_frame.setGraphicsEffect(self.shadow1)
        
        # ---------------- BOTÓN DE INTERCAMBIO (SWAP) ----------------
        swap_layout = QVBoxLayout()
        self.swap_btn = QPushButton()
        self.swap_btn.setObjectName("swapButton")
        self.swap_btn.setFixedSize(50, 50)
        self.swap_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.swap_btn.setToolTip("Intercambiar idiomas")
        self.swap_btn.clicked.connect(self.swap_requested_signal.emit)
        swap_layout.addStretch()
        swap_layout.addWidget(self.swap_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        swap_layout.addStretch()
        
        # ---------------- TARJETA DESTINO ----------------
        self.target_frame = QFrame()
        self.target_frame.setObjectName("cardFrame")
        target_layout = QVBoxLayout(self.target_frame)
        target_layout.setContentsMargins(24, 20, 24, 20)
        target_layout.setSpacing(12)
        
        target_top = QHBoxLayout()
        self.target_lang_btn = QPushButton("Inglés ▾")
        self.target_lang_btn.setObjectName("langSelectBtn")
        self.target_lang_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.target_lang_btn.clicked.connect(self.open_target_selector)
        target_top.addWidget(self.target_lang_btn)
        
        self.status_badge = QLabel("Listo")
        self.status_badge.setObjectName("statusBadge")
        target_top.addStretch()
        target_top.addWidget(self.status_badge)
        target_layout.addLayout(target_top)
        
        target_sep = QFrame()
        target_sep.setObjectName("cardDivider")
        target_sep.setFixedHeight(1)
        target_layout.addWidget(target_sep)
        
        self.target_text = QTextEdit()
        self.target_text.setPlaceholderText("La traducción aparecerá aquí...")
        self.target_text.setReadOnly(True)
        self.target_text.setObjectName("targetText")
        target_layout.addWidget(self.target_text)
        
        target_footer = QHBoxLayout()
        target_footer.addStretch()
        
        self.listen_btn = QPushButton()
        self.listen_btn.setObjectName("actionBtn")
        self.listen_btn.setFixedSize(36, 36)
        self.listen_btn.setToolTip("Escuchar pronunciación")
        self.listen_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.listen_btn.clicked.connect(self.listen_requested_signal.emit)
        
        self.copy_btn = QPushButton()
        self.copy_btn.setObjectName("actionBtn")
        self.copy_btn.setFixedSize(36, 36)
        self.copy_btn.setToolTip("Copiar traducción")
        self.copy_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.copy_btn.clicked.connect(self.copy_requested_signal.emit)
        
        target_footer.addWidget(self.listen_btn)
        target_footer.addWidget(self.copy_btn)
        target_layout.addLayout(target_footer)
        
        self.shadow2 = QGraphicsDropShadowEffect()
        self.shadow2.setBlurRadius(25)
        self.shadow2.setOffset(0, 4)
        self.target_frame.setGraphicsEffect(self.shadow2)
        
        content_layout.addWidget(self.source_frame, 1)
        content_layout.addLayout(swap_layout)
        content_layout.addWidget(self.target_frame, 1)
        
        body_layout.addLayout(content_layout)
        main_layout.addWidget(body_widget)
        
        self.sidebar_animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.sidebar_animation.setDuration(240)
        self.sidebar_animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.sidebar_open = False
        
        self.apply_styles()

    def update_char_count(self):
        chars = len(self.source_text.toPlainText())
        self.char_count_lbl.setText(f"{chars} caracteres")

    def toggle_sidebar(self):
        if self.sidebar_open:
            self.sidebar_animation.setStartValue(280)
            self.sidebar_animation.setEndValue(0)
            self.sidebar.setMaximumWidth(0)
        else:
            self.sidebar.setMaximumWidth(280)
            self.sidebar_animation.setStartValue(0)
            self.sidebar_animation.setEndValue(280)
        
        self.sidebar_animation.start()
        self.sidebar_open = not self.sidebar_open
        
    def refresh_history(self, db_manager):
        self.history_list.clear()
        records = db_manager.get_history(25)
        for r in records:
            source_snippet = r[3].strip()[:35].replace('\n', ' ')
            target_snippet = r[4].strip()[:35].replace('\n', ' ')
            item = QListWidgetItem(f"{r[1]} → {r[2]}\n{source_snippet}\n↳ {target_snippet}")
            item.setToolTip(f"ORIGEN ({r[1]}):\n{r[3]}\n\nTRADUCCIÓN ({r[2]}):\n{r[4]}")
            self.history_list.addItem(item)
            
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.apply_styles()

    def show_info_dialog(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Acerca de Nexus Translator")
        msg.setIcon(QMessageBox.Icon.NoIcon)
        msg.setText("<h3>Nexus Translator</h3>")
        msg.setInformativeText(
            "<p>Traductor de escritorio moderno y minimalista con arquitectura MVC y renderizado adaptativo.</p>"
            "<hr style='border: none; border-top: 1px solid rgba(128,128,128,0.2);'>"
            "<b>Desarrollador:</b> Luis Adrian Castillo Alvarez<br>"
            "<b>Tecnología:</b> Python 3 &bull; PyQt6 &bull; Deep Translator API<br>"
            "<b>Ubicación:</b> Tarapoto, San Martín, Perú"
        )
        
        if self.is_dark_mode:
            msg.setStyleSheet("""
                QMessageBox { background-color: #161A23; border-radius: 14px; }
                QLabel { color: #E2E8F0; font-family: 'Segoe UI', system-ui; font-size: 13px; }
                QPushButton { 
                    background-color: #2563EB; 
                    color: white; 
                    border-radius: 8px; 
                    padding: 8px 22px; 
                    border: none; 
                    font-weight: 600; 
                    font-family: 'Segoe UI', system-ui;
                }
                QPushButton:hover { background-color: #3B82F6; }
            """)
        else:
            msg.setStyleSheet("""
                QMessageBox { background-color: #FFFFFF; border-radius: 14px; }
                QLabel { color: #1E293B; font-family: 'Segoe UI', system-ui; font-size: 13px; }
                QPushButton { 
                    background-color: #2563EB; 
                    color: white; 
                    border-radius: 8px; 
                    padding: 8px 22px; 
                    border: none; 
                    font-weight: 600; 
                    font-family: 'Segoe UI', system-ui;
                }
                QPushButton:hover { background-color: #1D4ED8; }
            """)
        msg.exec()

    def _get_lang_name_from_btn(self, btn):
        text = btn.text()
        if text.endswith(" ▾"):
            text = text[:-2]
        if text.startswith("Detectar Idioma"):
            return "Detectar Idioma"
        return text


    def open_source_selector(self):
        current = self._get_lang_name_from_btn(self.source_lang_btn)
        dialog = LanguageSelectorDialog(self.languages, current, self.is_dark_mode, self)
        pos = self.source_lang_btn.mapToGlobal(self.source_lang_btn.rect().bottomLeft())
        dialog.move(pos.x(), pos.y() + 6)
        dialog.language_selected.connect(self.set_source_language)
        dialog.exec()

    def open_target_selector(self):
        current = self._get_lang_name_from_btn(self.target_lang_btn)
        dialog = LanguageSelectorDialog(self.languages, current, self.is_dark_mode, self)
        pos = self.target_lang_btn.mapToGlobal(self.target_lang_btn.rect().bottomLeft())
        dialog.move(pos.x(), pos.y() + 6)
        dialog.language_selected.connect(self.set_target_language)
        dialog.exec()
        
    def set_source_language(self, lang):
        self.source_lang_btn.setText(f"{lang} ▾")
        self.source_lang_changed_signal.emit(lang)

    def set_target_language(self, lang):
        self.target_lang_btn.setText(f"{lang} ▾")
        self.target_lang_changed_signal.emit(lang)

    def swap_languages(self):
        source_lang = self._get_lang_name_from_btn(self.source_lang_btn)
        target_lang = self._get_lang_name_from_btn(self.target_lang_btn)
        
        self.set_source_language(target_lang)
        self.set_target_language(source_lang)
        
        source_text = self.source_text.toPlainText()
        target_text = self.target_text.toPlainText()
        
        self.source_text.blockSignals(True)
        self.source_text.setPlainText(target_text)
        self.source_text.blockSignals(False)
        self.update_char_count()

    def apply_styles(self):
        if self.is_dark_mode:
            # Paleta Oscura Obsidiana y Azul Eléctrico
            icon_color = "#94A3B8"
            
            self.history_btn.setIcon(create_svg_icon("menu", icon_color, 18))
            self.theme_btn.setIcon(create_svg_icon("sun", icon_color, 18))
            self.info_btn.setIcon(create_svg_icon("info", icon_color, 18))
            self.swap_btn.setIcon(create_svg_icon("swap", "#93C5FD", 20))
            self.clear_btn.setIcon(create_svg_icon("trash", icon_color, 16))
            self.listen_btn.setIcon(create_svg_icon("volume", icon_color, 16))
            self.copy_btn.setIcon(create_svg_icon("copy", icon_color, 16))
            
            self.window_shadow.setColor(QColor(0, 0, 0, 160))
            self.shadow1.setColor(QColor(0, 0, 0, 80))
            self.shadow2.setColor(QColor(0, 0, 0, 80))
            
            self.setStyleSheet("""
                QFrame#sidebarFrame { 
                    background-color: #121620; 
                    border-radius: 16px; 
                    border: 1px solid rgba(255, 255, 255, 0.06); 
                }
                QLabel#sidebarTitle { 
                    color: #F1F5F9; 
                    font-family: 'Segoe UI', system-ui; 
                    font-size: 15px; 
                    font-weight: 700; 
                }
                QListWidget#historyList { 
                    border: none; 
                    background-color: transparent; 
                    outline: none; 
                }
                QListWidget#historyList::item { 
                    color: #94A3B8; 
                    padding: 10px 12px; 
                    border-radius: 8px;
                    margin-bottom: 6px;
                    background-color: rgba(255, 255, 255, 0.02);
                    border: 1px solid rgba(255, 255, 255, 0.04);
                    font-family: 'Segoe UI', system-ui;
                    font-size: 12px;
                }
                QListWidget#historyList::item:hover { 
                    background-color: rgba(59, 130, 246, 0.12); 
                    color: #F8FAFC; 
                    border-color: rgba(59, 130, 246, 0.3);
                }
                
                QFrame#mainBg { 
                    background-color: #0B0E14; 
                    border-radius: 16px; 
                    border: 1px solid rgba(255, 255, 255, 0.07); 
                }
                QFrame#customTitleBar { 
                    background-color: transparent; 
                    border-bottom: 1px solid rgba(255, 255, 255, 0.05); 
                }
                QFrame#brandDot {
                    background-color: #3B82F6;
                    border-radius: 4px;
                }
                QLabel#headerLabel { 
                    color: #F1F5F9; 
                    font-family: 'Segoe UI', system-ui; 
                    font-size: 13px; 
                    font-weight: 700; 
                    letter-spacing: 1.5px; 
                }
                QLabel#versionBadge {
                    background-color: rgba(59, 130, 246, 0.15);
                    color: #60A5FA;
                    font-size: 10px;
                    font-weight: 700;
                    padding: 2px 7px;
                    border-radius: 4px;
                }
                
                QPushButton#winBtn { 
                    background-color: transparent; 
                    color: #64748B; 
                    font-size: 14px; 
                    border: none; 
                    border-radius: 6px; 
                }
                QPushButton#winBtn:hover { 
                    background-color: rgba(255, 255, 255, 0.06); 
                    color: #F1F5F9; 
                }
                QPushButton#closeBtn { 
                    background-color: transparent; 
                    color: #64748B; 
                    font-size: 14px; 
                    border: none; 
                    border-radius: 6px; 
                }
                QPushButton#closeBtn:hover { 
                    background-color: #DC2626; 
                    color: white; 
                }
                
                QFrame#navBar {
                    background-color: transparent;
                }
                QPushButton#toolBtn { 
                    background-color: #121620; 
                    border: 1px solid rgba(255, 255, 255, 0.08); 
                    border-radius: 12px; 
                }
                QPushButton#toolBtn:hover { 
                    background-color: #1A2130; 
                    border-color: rgba(59, 130, 246, 0.4); 
                }
                
                QFrame#cardFrame { 
                    background-color: #121620; 
                    border-radius: 20px; 
                    border: 1px solid rgba(255, 255, 255, 0.07); 
                }
                QFrame#cardDivider {
                    background-color: rgba(255, 255, 255, 0.06);
                }
                
                QPushButton#langSelectBtn { 
                    background-color: transparent; 
                    border: none; 
                    font-family: 'Segoe UI', system-ui; 
                    font-size: 15px; 
                    font-weight: 600; 
                    color: #60A5FA; 
                    text-align: left; 
                    padding: 4px 0px;
                }
                QPushButton#langSelectBtn:hover { 
                    color: #93C5FD; 
                }
                
                QLabel#statusBadge {
                    background-color: rgba(16, 185, 129, 0.12);
                    color: #34D399;
                    font-size: 11px;
                    font-weight: 600;
                    padding: 3px 8px;
                    border-radius: 6px;
                }
                
                QTextEdit { 
                    background-color: transparent; 
                    border: none; 
                    font-family: 'Segoe UI', system-ui; 
                    font-size: 20px; 
                    color: #F1F5F9; 
                    line-height: 1.6; 
                }
                QTextEdit#targetText { 
                    color: #94A3B8; 
                }
                
                QLabel#charCountLbl {
                    color: #475569;
                    font-family: 'Segoe UI', system-ui;
                    font-size: 12px;
                }
                
                QPushButton#actionBtn { 
                    background-color: rgba(255, 255, 255, 0.03); 
                    border: 1px solid rgba(255, 255, 255, 0.06); 
                    border-radius: 10px; 
                }
                QPushButton#actionBtn:hover { 
                    background-color: rgba(255, 255, 255, 0.08); 
                    border-color: rgba(255, 255, 255, 0.15); 
                }
                
                QPushButton#swapButton { 
                    background-color: #1A2130; 
                    border: 1px solid rgba(59, 130, 246, 0.3); 
                    border-radius: 25px; 
                }
                QPushButton#swapButton:hover { 
                    background-color: #2563EB; 
                    border: 1px solid #3B82F6; 
                }
                QPushButton#swapButton:pressed { 
                    background-color: #1D4ED8; 
                }
                
                QScrollBar:vertical { 
                    border: none; 
                    background: transparent; 
                    width: 6px; 
                    border-radius: 3px; 
                }
                QScrollBar::handle:vertical { 
                    background: #252D3D; 
                    min-height: 30px; 
                    border-radius: 3px; 
                }
                QScrollBar::handle:vertical:hover { 
                    background: #3B82F6; 
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { 
                    border: none; 
                    background: none; 
                }
            """)
        else:
            # Paleta Clara Limpia, Aireada y Profesional
            icon_color = "#475569"
            
            self.history_btn.setIcon(create_svg_icon("menu", icon_color, 18))
            self.theme_btn.setIcon(create_svg_icon("moon", icon_color, 18))
            self.info_btn.setIcon(create_svg_icon("info", icon_color, 18))
            self.swap_btn.setIcon(create_svg_icon("swap", "#2563EB", 20))
            self.clear_btn.setIcon(create_svg_icon("trash", icon_color, 16))
            self.listen_btn.setIcon(create_svg_icon("volume", icon_color, 16))
            self.copy_btn.setIcon(create_svg_icon("copy", icon_color, 16))
            
            self.window_shadow.setColor(QColor(0, 0, 0, 35))
            self.shadow1.setColor(QColor(15, 23, 42, 10))
            self.shadow2.setColor(QColor(15, 23, 42, 10))
            
            self.setStyleSheet("""
                QFrame#sidebarFrame { 
                    background-color: #FFFFFF; 
                    border-radius: 16px; 
                    border: 1px solid #E2E8F0; 
                }
                QLabel#sidebarTitle { 
                    color: #0F172A; 
                    font-family: 'Segoe UI', system-ui; 
                    font-size: 15px; 
                    font-weight: 700; 
                }
                QListWidget#historyList { 
                    border: none; 
                    background-color: transparent; 
                    outline: none; 
                }
                QListWidget#historyList::item { 
                    color: #475569; 
                    padding: 10px 12px; 
                    border-radius: 8px;
                    margin-bottom: 6px;
                    background-color: #F8FAFC;
                    border: 1px solid #F1F5F9;
                    font-family: 'Segoe UI', system-ui;
                    font-size: 12px;
                }
                QListWidget#historyList::item:hover { 
                    background-color: #EFF6FF; 
                    color: #1D4ED8; 
                    border-color: #BFDBFE;
                }
                
                QFrame#mainBg { 
                    background-color: #F8FAFC; 
                    border-radius: 16px; 
                    border: 1px solid #E2E8F0; 
                }
                QFrame#customTitleBar { 
                    background-color: transparent; 
                    border-bottom: 1px solid #EEF2F6; 
                }
                QFrame#brandDot {
                    background-color: #2563EB;
                    border-radius: 4px;
                }
                QLabel#headerLabel { 
                    color: #0F172A; 
                    font-family: 'Segoe UI', system-ui; 
                    font-size: 13px; 
                    font-weight: 700; 
                    letter-spacing: 1.5px; 
                }
                QLabel#versionBadge {
                    background-color: #EFF6FF;
                    color: #2563EB;
                    font-size: 10px;
                    font-weight: 700;
                    padding: 2px 7px;
                    border-radius: 4px;
                }
                
                QPushButton#winBtn { 
                    background-color: transparent; 
                    color: #94A3B8; 
                    font-size: 14px; 
                    border: none; 
                    border-radius: 6px; 
                }
                QPushButton#winBtn:hover { 
                    background-color: #F1F5F9; 
                    color: #0F172A; 
                }
                QPushButton#closeBtn { 
                    background-color: transparent; 
                    color: #94A3B8; 
                    font-size: 14px; 
                    border: none; 
                    border-radius: 6px; 
                }
                QPushButton#closeBtn:hover { 
                    background-color: #EF4444; 
                    color: white; 
                }
                
                QFrame#navBar {
                    background-color: transparent;
                }
                QPushButton#toolBtn { 
                    background-color: #FFFFFF; 
                    border: 1px solid #E2E8F0; 
                    border-radius: 12px; 
                }
                QPushButton#toolBtn:hover { 
                    background-color: #F8FAFC; 
                    border-color: #CBD5E1; 
                }
                
                QFrame#cardFrame { 
                    background-color: #FFFFFF; 
                    border-radius: 20px; 
                    border: 1px solid #E2E8F0; 
                }
                QFrame#cardDivider {
                    background-color: #F1F5F9;
                }
                
                QPushButton#langSelectBtn { 
                    background-color: transparent; 
                    border: none; 
                    font-family: 'Segoe UI', system-ui; 
                    font-size: 15px; 
                    font-weight: 600; 
                    color: #2563EB; 
                    text-align: left; 
                    padding: 4px 0px;
                }
                QPushButton#langSelectBtn:hover { 
                    color: #1D4ED8; 
                }
                
                QLabel#statusBadge {
                    background-color: #ECFDF5;
                    color: #059669;
                    font-size: 11px;
                    font-weight: 600;
                    padding: 3px 8px;
                    border-radius: 6px;
                }
                
                QTextEdit { 
                    background-color: transparent; 
                    border: none; 
                    font-family: 'Segoe UI', system-ui; 
                    font-size: 20px; 
                    color: #0F172A; 
                    line-height: 1.6; 
                }
                QTextEdit#targetText { 
                    color: #64748B; 
                }
                
                QLabel#charCountLbl {
                    color: #94A3B8;
                    font-family: 'Segoe UI', system-ui;
                    font-size: 12px;
                }
                
                QPushButton#actionBtn { 
                    background-color: #F8FAFC; 
                    border: 1px solid #E2E8F0; 
                    border-radius: 10px; 
                }
                QPushButton#actionBtn:hover { 
                    background-color: #F1F5F9; 
                    border-color: #CBD5E1; 
                }
                
                QPushButton#swapButton { 
                    background-color: #FFFFFF; 
                    border: 1px solid #E2E8F0; 
                    border-radius: 25px; 
                }
                QPushButton#swapButton:hover { 
                    background-color: #EFF6FF; 
                    border-color: #BFDBFE; 
                }
                QPushButton#swapButton:pressed { 
                    background-color: #DBEAFE; 
                }
                
                QScrollBar:vertical { 
                    border: none; 
                    background: transparent; 
                    width: 6px; 
                    border-radius: 3px; 
                }
                QScrollBar::handle:vertical { 
                    background: #E2E8F0; 
                    min-height: 30px; 
                    border-radius: 3px; 
                }
                QScrollBar::handle:vertical:hover { 
                    background: #CBD5E1; 
                }
                QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { 
                    border: none; 
                    background: none; 
                }
            """)
