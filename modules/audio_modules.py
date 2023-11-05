"""
Este archivo contiene clases y funciones para cargar, procesar documentos de audio y transcribirlos.
Fue programado teniendo en mente su utilización en aplicaciones de IA.

Autor: Patrick Vásquez <pvasquezs@fen.uchile.cl>
Ultima actualización: 05/11/2023
"""

from abc import ABC, abstractmethod

# Audio transcriber

class TranscribeAudio(ABC):

    @abstractmethod
    def transcribe_audio():
        pass

class OpenAITranscribeAudio(TranscribeAudio):

    def __init__(self, api_key):
        self.api_key = api_key

    def transcribe_audio(self, file_path):
        import openai
        file = open(file_path, "rb")
        transcription = openai.Audio.transcribe("whisper-1", file)
        return transcription
