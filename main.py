#!/usr/bin/env python3
"""
BiliVagent - Bilibili Video Analysis Agent
Main entry point for the application
"""
import argparse
import sys
from bilivagent.agents.bilivagent import BiliVagent


def main():
    parser = argparse.ArgumentParser(
        description="BiliVagent - Bilibili视频智能分析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py BV1xx411c7mD
  python main.py https://www.bilibili.com/video/BV1xx411c7mD
  
注意:
  1. 请先配置 .env 文件中的 SILICONFLOW_API_KEY
  2. 如需语音识别功能，请下载 Vosk 模型并配置 VOSK_MODEL_PATH
  3. 视频下载需要安装 yt-dlp
        """
    )
    
    parser.add_argument(
        "video",
        help="Bilibili视频链接或BV号"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="输出目录（默认: ./output）",
        default=None
    )
    
    parser.add_argument(
        "--no-download",
        help="跳过视频下载（仅分析评论和弹幕）",
        action="store_true"
    )
    
    args = parser.parse_args()
    
    try:
        # Create agent
        agent = BiliVagent()
        
        # Analyze video
        report = agent.analyze_video(args.video)
        
        # Print report
        agent.print_report(report)
        
        print("\n✓ 分析完成!")
        
    except ValueError as e:
        print(f"配置错误: {e}", file=sys.stderr)
        print("请检查 .env 文件配置", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
