<div align="center">
  
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41CD52?style=flat&logo=qt&logoColor=white)](https://riverbankcomputing.com/software/pyqt/)
[![Architecture](https://img.shields.io/badge/Architecture-MVC-orange?style=flat)](#-architecture--arquitectura)

  <h1>Nexus Translator 🌐</h1>
  <p><strong>Un traductor de escritorio moderno, elegante y súper rápido construido con Python y PyQt6.</strong></p>

<img width="1262" height="764" alt="Image" src="https://github.com/user-attachments/assets/904f03f2-8c37-4035-b81c-bb44e53618ea" />
</div>

<br />

Nexus Translator es una aplicación de escritorio diseñada para ofrecer una experiencia de traducción fluida y visualmente atractiva. Utiliza la robusta librería `deep-translator` para proporcionar traducciones confiables en más de 100 idiomas, todo envuelto en una interfaz minimalista con una arquitectura modular.

## ✨ Características Principales

- **Diseño Moderno y Limpio:** Interfaz futurista con esquinas redondeadas, sombras suaves, y tipografía elegante (Segoe UI).
- **Modo Oscuro / Claro:** Alterna entre una estética luminosa y profesional o un modo nocturno relajante con un solo clic en la barra superior.
- **Detección Automática de Idioma:** No necesitas saber en qué idioma está el texto original, el programa lo detecta automáticamente.
- **Traducción en Tiempo Real:** El texto se traduce automáticamente mientras escribes, gracias a un sistema de *debounce* inteligente.
- **Text-to-Speech (Voz):** Reproduce el audio de la traducción con acento nativo con un solo clic (botón 🔊).
- **Herramientas de Productividad:** Botones dedicados para limpiar texto rápidamente (🗑️) y copiar la traducción al portapapeles (📋).
- **Buscador de Idiomas Integrado:** Panel flotante personalizado con una barra de búsqueda que filtra en tiempo real y lista con scroll suave (100% traducido al español).
- **Botón de Intercambio y Más Información:** Intercambia idiomas de entrada/salida instantáneamente y accede a datos del desarrollador con el botón "¡".

## 🏗️ Arquitectura MVC

Este proyecto ha sido estructurado siguiendo el patrón de diseño **Modelo-Vista-Controlador (MVC)**, garantizando que el código sea escalable, mantenible y profesional:

*   📂 `model.py` **(Modelo):** Gestiona toda la lógica de negocio y se encarga de las peticiones a la API utilizando `GoogleTranslator`.
*   📂 `view.py` **(Vista):** Maneja absolutamente toda la interfaz gráfica en PyQt6, incluyendo la ventana principal y los componentes personalizados como el `LanguageSelectorDialog`.
*   📂 `controller.py` **(Controlador):** Es el cerebro que conecta la interfaz con los datos. Escucha los eventos del usuario (escribir texto, clics) e interactúa con el Modelo para actualizar la Vista.
*   📂 `79.py` **(Main):** El archivo de inicialización principal que instancia y arranca la aplicación.

## 🚀 Guía de Instalación

Sigue estos pasos para ejecutar Nexus Translator en tu entorno local.

### Prerrequisitos

Asegúrate de tener instalado **Python 3.8 o superior**.

### Instalación

1. **Clona este repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/nexus-translator.git
   cd nexus-translator
   ```

2. **Crea un entorno virtual (Recomendado):**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```

3. **Instala las dependencias necesarias:**
   ```bash
   pip install -r requirements.txt
   ```

### Uso

Para iniciar la aplicación, simplemente ejecuta el archivo principal desde tu terminal:

```bash
python 79.py
```

## 🛠️ Tecnologías Utilizadas

*   [Python](https://www.python.org/) - Lenguaje base.
*   [PyQt6](https://riverbankcomputing.com/software/pyqt/intro) - Framework principal para la creación de la Interfaz Gráfica (GUI).
*   [deep-translator](https://github.com/nidhaloff/deep-translator) - Librería encargada del procesamiento de las traducciones.

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Si tienes ideas para mejorar la UI, optimizar el código o añadir nuevas funcionalidades:

1. Haz un Fork del proyecto.
2. Crea tu rama de características (`git checkout -b feature/NuevaCaracteristica`).
3. Haz commit de tus cambios (`git commit -m 'Añadir NuevaCaracteristica'`).
4. Haz push a la rama (`git push origin feature/NuevaCaracteristica`).
5. Abre un Pull Request.

---
*Desarrollado con ❤️ para mejorar la experiencia de traducción en escritorio.*
