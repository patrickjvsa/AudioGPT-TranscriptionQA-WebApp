"""
Este archivo contiene clases y funciones para cargar, procesar documentos de audio y transcribirlos.
Fue programado teniendo en mente su utilización en aplicaciones de IA.

Autor: Patrick Vásquez <pvasquezs@fen.uchile.cl>
Ultima actualización: 05/11/2023
"""

# Import modules

from abc import ABC, abstractmethod

# Format Extracter
class ExtractDocumentFormat:
    def __init__(self, file_path):
        self.file_path = file_path

    def extract_extension(file_path):
        """
        Extrae la extensión del archivo. La api de openai soporta m4a, mp3, mp4, mpeg, mpga, wav y webm.
        :return: La extensión del archivo.
        """
        import os
        name, extension = os.path.splitext(file_path)
        return extension

# Audio transcriber

class TranscribeAudio(ABC):

    @abstractmethod
    def transcribe_audio():
        pass

class OpenAITranscribeAudio(TranscribeAudio):

    def __init__(self, api_key):
        self.api_key = api_key

    def transcribe_audio(self, file_path, model="whisper-1"):
        import openai
        file = open(file_path, "rb")
        transcription = openai.Audio.transcribe(model, file)
        return transcription

# Future updates: chunk audio files