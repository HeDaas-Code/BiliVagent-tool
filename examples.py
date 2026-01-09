#!/usr/bin/env python3
"""
示例脚本：演示如何使用 BiliVagent 的各个组件

注意：此脚本仅作为示例，实际使用请运行 main.py
"""

import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def example_1_parse_bv():
    """示例 1: 解析 BV 号"""
    print("="*60)
    print("示例 1: 解析 BV 号")
    print("="*60)
    
    from bilivagent.utils.bilibili import BilibiliParser
    
    parser = BilibiliParser()
    
    # 从不同格式提取 BV 号
    test_cases = [
        "BV1xx411c7mD",
        "https://www.bilibili.com/video/BV1xx411c7mD",
        "https://www.bilibili.com/video/BV1xx411c7mD?spm_id_from=333.999.0.0"
    ]
    
    for test in test_cases:
        try:
            bv = parser.parse_bv_number(test)
            print(f"✓ {test[:50]}... => {bv}")
        except Exception as e:
            print(f"✗ {test[:50]}... => Error: {e}")


def example_2_text_processing():
    """示例 2: 文本处理"""
    print("\n" + "="*60)
    print("示例 2: 文本处理")
    print("="*60)
    
    from bilivagent.utils.text import TextProcessor
    
    processor = TextProcessor()
    
    # 脱敏示例
    text = "我的手机是13800138000，邮箱是test@example.com"
    desensitized = processor.desensitize_text(text)
    print(f"\n原文: {text}")
    print(f"脱敏: {desensitized}")
    
    # 关键词提取示例
    sample_text = """
    这个视频真的太精彩了！UP主讲解得很清楚，内容丰富，
    画质也很好。学到了很多知识，强烈推荐大家观看。
    希望UP主能出更多这样的教程视频。
    """
    
    keywords = processor.extract_keywords(sample_text, top_k=5)
    print(f"\n示例文本关键词:")
    for word, weight in keywords:
        print(f"  - {word}: {weight:.4f}")
    
    # 情感分析示例
    sentiment = processor.analyze_sentiment_keywords(sample_text)
    print(f"\n情感分析:")
    for key, count in sentiment.items():
        print(f"  - {key}: {count}")


def example_3_siliconflow_client():
    """示例 3: SiliconFlow API 客户端（需要配置 API Key）"""
    print("\n" + "="*60)
    print("示例 3: SiliconFlow API 客户端")
    print("="*60)
    
    try:
        from bilivagent.utils.siliconflow import SiliconFlowClient
        from bilivagent.config import Config
        
        # 检查是否配置了 API Key
        if not Config.SILICONFLOW_API_KEY or Config.SILICONFLOW_API_KEY == "your_api_key_here":
            print("\n⚠ 未配置 SILICONFLOW_API_KEY，跳过此示例")
            print("  请在 .env 文件中配置 API Key")
            return
        
        client = SiliconFlowClient()
        
        # 简单的对话示例
        messages = [
            {"role": "system", "content": "你是一个友好的助手"},
            {"role": "user", "content": "用一句话介绍 Bilibili"}
        ]
        
        print("\n发送请求到 SiliconFlow API...")
        response = client.chat_completion(messages, max_tokens=100)
        print(f"\n回复: {response}")
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")


def example_4_video_info():
    """示例 4: 获取视频信息（需要网络连接）"""
    print("\n" + "="*60)
    print("示例 4: 获取视频信息")
    print("="*60)
    
    try:
        from bilivagent.utils.bilibili import BilibiliParser
        
        parser = BilibiliParser()
        
        # 使用一个示例 BV 号
        # 注意：实际使用时请替换为真实的 BV 号
        bv = "BV1xx411c7mD"
        
        print(f"\n尝试获取视频信息: {bv}")
        print("注意: 这需要网络连接到 Bilibili")
        
        # 实际项目中这里会调用 API
        print("\n⚠ 示例跳过实际 API 调用")
        print("  完整功能请运行: python main.py BV号")
        
    except Exception as e:
        print(f"\n✗ 错误: {e}")


def main():
    """运行所有示例"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "BiliVagent 功能示例" + " "*24 + "║")
    print("╚" + "="*58 + "╝")
    
    examples = [
        example_1_parse_bv,
        example_2_text_processing,
        example_3_siliconflow_client,
        example_4_video_info,
    ]
    
    for example_func in examples:
        try:
            example_func()
        except KeyboardInterrupt:
            print("\n\n用户中断")
            break
        except Exception as e:
            print(f"\n✗ 示例执行出错: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("示例运行完成")
    print("="*60)
    print("\n要运行完整的视频分析，请使用:")
    print("  python main.py <BV号或视频链接>")
    print("\n更多信息请查看:")
    print("  - README.md: 完整文档")
    print("  - QUICKSTART.md: 快速开始指南")
    print("  - DEVELOPMENT.md: 开发指南")
    print()


if __name__ == "__main__":
    main()
