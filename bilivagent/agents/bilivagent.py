"""Main BiliVagent agent using LangChain"""
import os
import json
from typing import Dict
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.tools import Tool
from langchain_core.prompts import PromptTemplate
from langchain_core.language_models.llms import LLM
from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from typing import Optional, List, Any

from bilivagent.config import Config
from bilivagent.utils.bilibili import BilibiliParser, BilibiliDownloader
from bilivagent.utils.siliconflow import SiliconFlowClient
from bilivagent.processors.video_content import VideoContentProcessor
from bilivagent.processors.text_content import TextContentProcessor


class SiliconFlowLLM(LLM):
    """Custom LLM wrapper for SiliconFlow API"""
    
    client: SiliconFlowClient = None
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = SiliconFlowClient()
    
    @property
    def _llm_type(self) -> str:
        return "siliconflow"
    
    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
        run_manager: Optional[CallbackManagerForLLMRun] = None,
        **kwargs: Any,
    ) -> str:
        messages = [{"role": "user", "content": prompt}]
        return self.client.chat_completion(messages, max_tokens=2000)


class BiliVagent:
    """Main agent for Bilibili video analysis"""
    
    def __init__(self):
        Config.validate()
        
        self.parser = BilibiliParser()
        self.downloader = BilibiliDownloader(Config.TEMP_DIR)
        self.video_processor = VideoContentProcessor()
        self.text_processor = TextContentProcessor()
        self.client = SiliconFlowClient()
    
    def analyze_video(self, url_or_bv: str) -> Dict:
        """Complete video analysis workflow"""
        print("="*60)
        print("BiliVagent - Bilibili Video Analysis")
        print("="*60)
        
        # Step 1: Parse BV number
        print("\n[1/8] Parsing BV number...")
        bv_number = self.parser.parse_bv_number(url_or_bv)
        print(f"BV号: {bv_number}")
        
        # Step 2: Get video info
        print("\n[2/8] Fetching video information...")
        video_info = self.parser.get_video_info(bv_number)
        print(f"标题: {video_info['title']}")
        print(f"分区: {video_info['tname']}")
        
        # Step 3: Download video
        print("\n[3/8] Downloading video...")
        video_path = self.downloader.download_video(bv_number)
        
        if not video_path:
            print("Warning: Video download failed, skipping video analysis")
            video_analysis = {
                "transcription": "视频下载失败",
                "summary": "",
                "keywords": [],
                "frames": [],
                "video_style": "无法分析"
            }
        else:
            print(f"Video saved to: {video_path}")
            
            # Step 4: Process video content
            print("\n[4/8] Processing video content...")
            video_analysis = self.video_processor.process(video_path, bv_number)
        
        # Step 5: Get comments
        print("\n[5/8] Fetching comments...")
        comments = self.parser.get_comments(bv_number, max_count=100)
        print(f"Fetched {len(comments)} comments")
        
        # Step 6: Get danmaku
        print("\n[6/8] Fetching danmaku...")
        danmaku = self.parser.get_danmaku(bv_number, video_info['cid'])
        print(f"Fetched {len(danmaku)} danmaku")
        
        # Step 7: Process text content
        print("\n[7/8] Processing text content (comments and danmaku)...")
        text_analysis = self.text_processor.process(comments, danmaku)
        
        # Step 8: Generate final report
        print("\n[8/8] Generating final report...")
        report = self._generate_report(
            bv_number=bv_number,
            video_info=video_info,
            video_analysis=video_analysis,
            text_analysis=text_analysis
        )
        
        # Save report
        output_path = os.path.join(Config.OUTPUT_DIR, f"{bv_number}_report.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ Report saved to: {output_path}")
        
        return report
    
    def _generate_report(self, bv_number: str, video_info: Dict, video_analysis: Dict, text_analysis: Dict) -> Dict:
        """Generate final analysis report"""
        report = {
            "BV号": bv_number,
            "视频标题": video_info['title'],
            "概述": video_analysis.get('summary', ''),
            "关键词（前十）": video_analysis.get('keywords', []),
            "视频风格": video_analysis.get('video_style', ''),
            "讨论情感": text_analysis.get('sentiment_label', ''),
            "讨论关键词": text_analysis.get('comment_keywords', []),
            "相关讨论": text_analysis.get('discussion_summary', ''),
            "元数据": {
                "分区": video_info['tname'],
                "标签": video_info['tags'],
                "UP主": video_info['owner'],
                "时长": video_info['duration'],
                "评论数": text_analysis.get('total_comments', 0),
                "弹幕数": text_analysis.get('total_danmaku', 0),
            }
        }
        
        return report
    
    def print_report(self, report: Dict):
        """Print formatted report"""
        print("\n" + "="*60)
        print("分析报告")
        print("="*60)
        print(f"\nBV号: {report['BV号']}")
        print(f"视频标题: {report['视频标题']}")
        print(f"\n概述:\n{report['概述']}")
        print(f"\n关键词（前十）:")
        for i, keyword in enumerate(report['关键词（前十）'], 1):
            print(f"  {i}. {keyword}")
        print(f"\n视频风格: {report['视频风格']}")
        print(f"\n讨论情感: {report['讨论情感']}")
        print(f"\n讨论关键词:")
        for i, keyword in enumerate(report['讨论关键词'], 1):
            print(f"  {i}. {keyword}")
        print(f"\n相关讨论:\n{report['相关讨论']}")
        print("\n元数据:")
        print(f"  分区: {report['元数据']['分区']}")
        print(f"  UP主: {report['元数据']['UP主']}")
        print(f"  评论数: {report['元数据']['评论数']}")
        print(f"  弹幕数: {report['元数据']['弹幕数']}")
        print("="*60)
