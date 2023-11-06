# AudioGPT: Transcriptions with Whisper and QA.

AudioGPT es una aplicación web basada en Streamlit que permite la transcripción de archivos de audio utilizando Whisper. Además, brinda la posibilidad de descargar la transcripción en formato de texto (txt) y realizar preguntas utilizando ChatGPT a través de la biblioteca LangChain y ChromaDB.

## Instalación

Asegúrate de tener Python instalado en tu sistema. Luego, sigue estos pasos:

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tuusuario/AudioGPT.git
   ```

2. Accede al directorio del proyecto:

   ```bash
   cd AudioGPT-TranscriptionQA-WebApp
   ```

3. Crea un entorno virtual (opcional pero recomendado):

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

4. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta la aplicación web:

   ```bash
   streamlit run app.py
   ```

2. Añade tu API Key de OpenAI y sube tu archivo de audio para la transcripción.

3. Una vez que se complete la transcripción, podrás descargar el resultado en formato de texto (txt).

4. También puedes hacer preguntas utilizando ChatGPT a través de la interfaz proporcionada.

## Notas

Me gustaría a futuro añadirle la funcionalidad para descargar y transcribir directamente desde YouTube u otros servidores de hosting.
