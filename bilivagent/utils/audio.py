"""Audio processing and speech recognition"""
import os
import json
import wave
from typing import Optional
from vosk import Model, KaldiRecognizer


class SpeechRecognizer:
    """Speech to text using Vosk"""
    
    def __init__(self, model_path: str):
        if not os.path.exists(model_path):
            raise ValueError(f"Vosk model not found at: {model_path}")
        
        self.model = Model(model_path)
    
    def transcribe(self, audio_path: str) -> str:
        """Transcribe audio to text"""
        wf = wave.open(audio_path, "rb")
        
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() not in [8000, 16000, 32000, 48000]:
            raise ValueError("Audio file must be WAV format mono PCM")
        
        rec = KaldiRecognizer(self.model, wf.getframerate())
        rec.SetWords(True)
        
        transcription = []
        
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if "text" in result:
                    transcription.append(result["text"])
        
        # Get final result
        final_result = json.loads(rec.FinalResult())
        if "text" in final_result:
            transcription.append(final_result["text"])
        
        wf.close()
        
        return " ".join(transcription)
