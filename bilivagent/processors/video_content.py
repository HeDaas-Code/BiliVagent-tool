"""Video content processor"""
import os
from typing import Dict, List
from bilivagent.utils.video import VideoProcessor
from bilivagent.utils.audio import SpeechRecognizer
from bilivagent.utils.siliconflow import SiliconFlowClient
from bilivagent.config import Config


class VideoContentProcessor:
    """Process video content: extract audio, transcribe, and analyze"""
    
    def __init__(self):
        self.video_processor = VideoProcessor()
        self.speech_recognizer = None
        self.client = SiliconFlowClient()
        
        # Initialize speech recognizer if model exists
        if os.path.exists(Config.VOSK_MODEL_PATH):
            self.speech_recognizer = SpeechRecognizer(Config.VOSK_MODEL_PATH)
    
    def process(self, video_path: str, bv_number: str) -> Dict:
        """Process video content"""
        result = {
            "transcription": "",
            "summary": "",
            "keywords": [],
            "frames": [],
            "video_style": ""
        }
        
        # Extract audio
        print("Extracting audio from video...")
        audio_path = self.video_processor.extract_audio(
            video_path, 
            os.path.join(Config.TEMP_DIR, f"{bv_number}.wav")
        )
        
        # Transcribe audio to text
        if self.speech_recognizer and os.path.exists(audio_path):
            print("Transcribing audio to text...")
            try:
                transcription = self.speech_recognizer.transcribe(audio_path)
                result["transcription"] = transcription
                
                # Generate summary using LLM
                if transcription:
                    print("Generating summary from transcription...")
                    summary = self._generate_summary(transcription)
                    result["summary"] = summary
                    
                    # Extract keywords
                    keywords = self._extract_keywords(transcription)
                    result["keywords"] = keywords
            except Exception as e:
                print(f"Error in speech recognition: {e}")
                result["transcription"] = "语音识别失败"
        else:
            print("Speech recognizer not available, skipping transcription")
            result["transcription"] = "未进行语音识别（需要Vosk模型）"
        
        # Extract and analyze video frames
        print("Extracting video frames...")
        try:
            frame_paths = self.video_processor.extract_random_frames(
                video_path, 
                num_frames=3,
                output_dir=Config.TEMP_DIR
            )
            result["frames"] = frame_paths
            
            # Analyze video style from frames
            if frame_paths:
                print("Analyzing video style...")
                video_style = self._analyze_video_style(frame_paths)
                result["video_style"] = video_style
        except Exception as e:
            print(f"Error extracting frames: {e}")
        
        return result
    
    def _generate_summary(self, text: str) -> str:
        """Generate summary from text using LLM"""
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的内容分析助手。请根据提供的文本生成简洁的概述。"
            },
            {
                "role": "user",
                "content": f"请为以下内容生成一个100字以内的概述：\n\n{text[:3000]}"
            }
        ]
        
        summary = self.client.chat_completion(messages, max_tokens=500)
        return summary
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text using LLM"""
        messages = [
            {
                "role": "system",
                "content": "你是一个关键词提取专家。请从文本中提取最重要的10个关键词。"
            },
            {
                "role": "user",
                "content": f"请从以下内容中提取10个最重要的关键词，用逗号分隔：\n\n{text[:2000]}"
            }
        ]
        
        keywords_str = self.client.chat_completion(messages, max_tokens=200)
        keywords = [k.strip() for k in keywords_str.split('，') if k.strip()]
        return keywords[:10]
    
    def _analyze_video_style(self, frame_paths: List[str]) -> str:
        """Analyze video style from frames using vision model"""
        if not frame_paths:
            return "无法分析"
        
        # Use the first frame for analysis
        prompt = "请分析这个视频画面的风格特点，包括画面质量、色彩、构图等。请用简洁的语言描述（50字以内）。"
        
        style = self.client.vision_analysis(frame_paths[0], prompt)
        return style if style else "未知风格"
