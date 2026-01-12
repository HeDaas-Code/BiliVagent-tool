"""Video and audio processing utilities"""
import os
import random
import glob
from typing import List, Optional, Tuple
from moviepy import VideoFileClip
import cv2
from bilivagent.config import Config


class VideoProcessor:
    """Process video files"""
    
    def extract_audio(self, video_path: str, output_path: Optional[str] = None) -> str:
        """
        Extract audio from video.
        If video has no audio track, try to find a separate audio file.
        """
        if output_path is None:
            output_path = video_path.rsplit(".", 1)[0] + ".wav"
        
        # If output already exists, return it
        if os.path.exists(output_path):
            Config.debug_print(f"[DEBUG] Audio already exists: {output_path}")
            return output_path

        video = None
        try:
            video = VideoFileClip(video_path)

            # Check if video has audio
            if video.audio is not None:
                Config.debug_print(f"[DEBUG] Extracting audio from video...")
                video.audio.write_audiofile(
                    output_path,
                    codec='pcm_s16le',
                    fps=16000,
                    nbytes=2,
                    buffersize=2000,
                    ffmpeg_params=["-ac", "1"]  # Force mono audio
                )
                video.close()
                Config.debug_print(f"[DEBUG] Audio extracted to: {output_path}")
                return output_path
            else:
                Config.debug_print("[DEBUG] Video has no audio track, looking for separate audio file...")
                video.close()
                video = None
        except Exception as e:
            Config.debug_print(f"[DEBUG] Error extracting audio from video: {e}")
            if video:
                video.close()

        # Try to find separate audio file (yt-dlp creates .m4a files)
        audio_path = self._find_separate_audio(video_path)
        if audio_path:
            Config.debug_print(f"[DEBUG] Found separate audio file: {audio_path}")
            # Convert m4a to wav using moviepy
            return self._convert_audio_to_wav(audio_path, output_path)

        raise ValueError(f"Cannot extract audio: video has no audio track and no separate audio file found for {video_path}")

    def _find_separate_audio(self, video_path: str) -> Optional[str]:
        """Find separate audio file that corresponds to the video"""
        video_dir = os.path.dirname(video_path)
        video_basename = os.path.basename(video_path)

        # Extract BV number from filename (e.g., BV1CxByBoE9r.f100026.mp4 -> BV1CxByBoE9r)
        bv_match = video_basename.split('.')[0]

        # Look for audio files with the same BV number
        audio_extensions = ['.m4a', '.aac', '.mp3', '.opus', '.ogg']

        for ext in audio_extensions:
            # Check for patterns like BV1CxByBoE9r.f30280.m4a
            pattern = os.path.join(video_dir, f"{bv_match}*{ext}")
            matches = glob.glob(pattern)
            if matches:
                return matches[0]

        return None

    def _convert_audio_to_wav(self, audio_path: str, output_path: str) -> str:
        """Convert audio file to WAV format (mono, 16kHz, 16-bit PCM)"""
        from moviepy import AudioFileClip

        audio = AudioFileClip(audio_path)

        # Ensure mono by setting nchannels=1
        audio.write_audiofile(
            output_path,
            codec='pcm_s16le',
            fps=16000,
            nbytes=2,
            buffersize=2000,
            ffmpeg_params=["-ac", "1"]  # Force mono audio
        )
        audio.close()

        return output_path
    
    def extract_random_frames(self, video_path: str, num_frames: int = 3, output_dir: Optional[str] = None) -> List[str]:
        """Extract random frames from video"""
        if output_dir is None:
            output_dir = os.path.dirname(video_path)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Open video
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        if total_frames <= 0:
            cap.release()
            raise ValueError("Cannot read video frames")
        
        # Select random frame indices
        frame_indices = sorted(random.sample(range(0, total_frames), min(num_frames, total_frames)))
        
        frame_paths = []
        base_name = os.path.splitext(os.path.basename(video_path))[0]
        
        for i, frame_idx in enumerate(frame_indices):
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
            ret, frame = cap.read()
            
            if ret:
                frame_path = os.path.join(output_dir, f"{base_name}_frame_{i+1}.jpg")
                cv2.imwrite(frame_path, frame)
                frame_paths.append(frame_path)
        
        cap.release()
        return frame_paths
