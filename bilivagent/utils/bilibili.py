"""Bilibili video downloader and parser"""
import re
import os
import json
import subprocess
from typing import Dict, Optional
from bilibili_api import video, sync, comment, Credential
import requests
from bilivagent.config import Config


class BilibiliParser:
    """Parse Bilibili video information"""
    
    def __init__(self):
        self.credential = Credential()
    
    def parse_bv_number(self, url_or_bv: str) -> str:
        """Extract BV number from URL or return BV number directly"""
        if url_or_bv.startswith("BV"):
            return url_or_bv
        
        # Extract BV number from URL
        match = re.search(r'BV[a-zA-Z0-9]+', url_or_bv)
        if match:
            return match.group(0)
        
        raise ValueError(f"Cannot extract BV number from: {url_or_bv}")
    
    def get_video_info(self, bv_number: str) -> Dict:
        """Get video information"""
        v = video.Video(bvid=bv_number, credential=self.credential)
        info = sync(v.get_info())
        
        return {
            "bvid": bv_number,
            "title": info.get("title", ""),
            "desc": info.get("desc", ""),
            "owner": info.get("owner", {}).get("name", ""),
            "tags": [tag.get("tag_name", "") for tag in info.get("tags", [])],
            "tname": info.get("tname", ""),  # 分区名称
            "duration": info.get("duration", 0),
            "pubdate": info.get("pubdate", 0),
            "cid": info.get("cid", 0),
        }
    
    def get_comments(self, bv_number: str, max_count: int = 100) -> list:
        """Get video comments"""
        comments = []
        
        try:
            # First get the video info to get the aid (oid for comments)
            v = video.Video(bvid=bv_number, credential=self.credential)
            info = sync(v.get_info())
            aid = info.get('aid')

            if not aid:
                print("Error: Cannot get aid for video")
                return comments

            # Use the comment module's get_comments_lazy function
            offset = ''
            while len(comments) < max_count:
                comment_result = sync(comment.get_comments_lazy(
                    oid=aid,
                    type_=comment.CommentResourceType.VIDEO,
                    offset=offset,
                    credential=self.credential
                ))

                if not comment_result or "replies" not in comment_result:
                    break
                
                replies = comment_result.get("replies", [])
                if not replies:
                    break
                
                for reply in replies:
                    comments.append({
                        "content": reply.get("content", {}).get("message", ""),
                        "like": reply.get("like", 0),
                        "member": reply.get("member", {}).get("uname", ""),
                    })
                    
                    if len(comments) >= max_count:
                        break
                
                # Get offset for next page
                cursor = comment_result.get("cursor", {})
                pagination = cursor.get("pagination_reply", {})
                offset = pagination.get("next_offset", "")
                if not offset:
                    break

        except Exception as e:
            print(f"Error fetching comments: {e}")
        
        return comments[:max_count]
    
    def get_danmaku(self, bv_number: str, cid: int) -> list:
        """Get video danmaku (弹幕)"""
        v = video.Video(bvid=bv_number, credential=self.credential)
        
        try:
            # get_danmakus uses page_index (0-based), cid is optional
            danmaku_list = sync(v.get_danmakus(page_index=0, cid=cid if cid else None))
            return [dm.text for dm in danmaku_list]
        except Exception as e:
            print(f"Error fetching danmaku: {e}")
            return []



class BilibiliDownloader:
    """Download Bilibili video"""
    
    def __init__(self, output_dir: str = "./temp"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.ffmpeg_path = self._find_ffmpeg()

    def _find_ffmpeg(self) -> Optional[str]:
        """
        Find ffmpeg executable path.
        Priority:
        1. Environment PATH (system ffmpeg)
        2. Project folder ./ffmpeg/bin/ffmpeg.exe or ./ffmpeg/ffmpeg.exe
        3. Project folder ./ffmpeg.exe
        """
        import shutil

        # First, check if ffmpeg is in system PATH
        ffmpeg_in_path = shutil.which("ffmpeg")
        if ffmpeg_in_path:
            print(f"Found ffmpeg in PATH: {ffmpeg_in_path}")
            return None  # Return None means use system ffmpeg (no special config needed)

        # Get project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Check possible ffmpeg locations in project folder
        possible_paths = [
            os.path.join(project_root, "ffmpeg", "bin", "ffmpeg.exe"),
            os.path.join(project_root, "ffmpeg", "ffmpeg.exe"),
            os.path.join(project_root, "ffmpeg.exe"),
            # Also check for non-Windows systems
            os.path.join(project_root, "ffmpeg", "bin", "ffmpeg"),
            os.path.join(project_root, "ffmpeg", "ffmpeg"),
        ]

        for path in possible_paths:
            if os.path.isfile(path):
                print(f"Found ffmpeg in project folder: {path}")
                return path

        print("Warning: ffmpeg not found. Video merging may fail.")
        return None

    def download_video(self, bv_number: str) -> Optional[str]:
        """Download video using yt-dlp as Python module"""
        url = f"https://www.bilibili.com/video/{bv_number}"
        output_template = os.path.join(self.output_dir, f"{bv_number}.%(ext)s")
        
        try:
            import yt_dlp
            import glob

            # Check if video already exists
            existing_files = glob.glob(os.path.join(self.output_dir, f"{bv_number}*.mp4"))
            if existing_files:
                Config.debug_print(f"[DEBUG] Video already exists: {existing_files[0]}")
                return existing_files[0]

            # Custom logger class to avoid stdout encoding issues
            class YTDLPLogger:
                def debug(self, msg):
                    if msg.startswith('[download]'):
                        Config.debug_print(f"[DEBUG] {msg}")
                def warning(self, msg):
                    Config.debug_print(f"[DEBUG] Warning: {msg}")
                def error(self, msg):
                    print(f"Error: {msg}")

            # Configure yt-dlp options
            ydl_opts = {
                # Format selection: try merged format first, then separate streams
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': output_template,
                'quiet': True,  # Use quiet mode to avoid stdout encoding issues
                'no_warnings': True,
                'ignoreerrors': False,  # Don't ignore errors, we want to know what went wrong
                'nocheckcertificate': True,  # Skip certificate verification
                'socket_timeout': 30,  # Timeout for network operations
                'logger': YTDLPLogger(),  # Use custom logger
                'progress_hooks': [self._download_progress_hook],  # Progress callback
            }

            # If we found ffmpeg in project folder, configure it
            if self.ffmpeg_path:
                ffmpeg_dir = os.path.dirname(self.ffmpeg_path)
                ydl_opts['ffmpeg_location'] = ffmpeg_dir
                Config.debug_print(f"[DEBUG] Using ffmpeg from: {ffmpeg_dir}")

            print(f"Downloading video: {bv_number}")
            Config.debug_print(f"[DEBUG] URL: {url}")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                error_code = ydl.download([url])
                if error_code != 0:
                    print(f"Download error code: {error_code}")

            # Find the downloaded file
            video_path = os.path.join(self.output_dir, f"{bv_number}.mp4")
            if os.path.exists(video_path):
                print(f"Video downloaded: {video_path}")
                return video_path
            
            # Check for format-specific files that yt-dlp might create
            pattern = os.path.join(self.output_dir, f"{bv_number}*")
            files = glob.glob(pattern)
            video_files = [f for f in files if f.endswith(('.mp4', '.webm', '.mkv', '.flv'))]
            if video_files:
                Config.debug_print(f"[DEBUG] Found video file: {video_files[0]}")
                return video_files[0]

            # List all files found for debugging
            Config.debug_print(f"[DEBUG] Files found matching {bv_number}: {files}")
            return None
            
        except Exception as e:
            import traceback
            print(f"Error downloading video: {e}")
            if Config.DEBUG:
                traceback.print_exc()
            return None

    def _download_progress_hook(self, d):
        """Progress hook for download status"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            Config.debug_print(f"\r[DEBUG] Downloading: {percent} at {speed}", end='')
        elif d['status'] == 'finished':
            Config.debug_print(f"\n[DEBUG] Download finished, merging...")
