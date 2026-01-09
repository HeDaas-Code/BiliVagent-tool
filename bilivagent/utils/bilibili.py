"""Bilibili video downloader and parser"""
import re
import os
import json
import subprocess
from typing import Dict, Optional
from bilibili_api import video, sync, comment, Credential
import requests


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
        v = video.Video(bvid=bv_number, credential=self.credential)
        comments = []
        
        try:
            page = 1
            while len(comments) < max_count:
                comment_list = sync(v.get_comments(page_index=page))
                
                if not comment_list or "replies" not in comment_list:
                    break
                
                replies = comment_list.get("replies", [])
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
                
                page += 1
        except Exception as e:
            print(f"Error fetching comments: {e}")
        
        return comments[:max_count]
    
    def get_danmaku(self, bv_number: str, cid: int) -> list:
        """Get video danmaku (弹幕)"""
        v = video.Video(bvid=bv_number, credential=self.credential)
        
        try:
            danmaku_list = sync(v.get_danmakus(cid))
            return [dm.text for dm in danmaku_list]
        except Exception as e:
            print(f"Error fetching danmaku: {e}")
            return []


class BilibiliDownloader:
    """Download Bilibili video"""
    
    def __init__(self, output_dir: str = "./temp"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def download_video(self, bv_number: str) -> Optional[str]:
        """Download video using yt-dlp"""
        url = f"https://www.bilibili.com/video/{bv_number}"
        output_template = os.path.join(self.output_dir, f"{bv_number}.%(ext)s")
        
        try:
            # Use yt-dlp to download video
            cmd = [
                "yt-dlp",
                "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
                "--merge-output-format", "mp4",
                "-o", output_template,
                url
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Find the downloaded file
            video_path = os.path.join(self.output_dir, f"{bv_number}.mp4")
            if os.path.exists(video_path):
                return video_path
            
            # Check for other extensions
            for ext in ["webm", "mkv", "flv"]:
                alt_path = os.path.join(self.output_dir, f"{bv_number}.{ext}")
                if os.path.exists(alt_path):
                    return alt_path
            
            return None
            
        except subprocess.CalledProcessError as e:
            print(f"Error downloading video: {e}")
            return None
