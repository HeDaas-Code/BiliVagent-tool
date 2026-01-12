"""Video and audio processing utilities"""
import os
import random
from typing import List, Optional
from moviepy.editor import VideoFileClip
import cv2


class VideoProcessor:
    """Process video files"""
    
    def extract_audio(self, video_path: str, output_path: Optional[str] = None) -> str:
        """Extract audio from video"""
        if output_path is None:
            output_path = video_path.rsplit(".", 1)[0] + ".wav"
        
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(output_path, codec='pcm_s16le', fps=16000, nbytes=2, buffersize=2000)
        video.close()
        
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
