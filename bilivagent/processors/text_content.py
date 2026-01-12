"""Text content processor for comments and danmaku"""
from typing import Dict, List
from bilivagent.utils.text import TextProcessor
from bilivagent.utils.siliconflow import SiliconFlowClient


class TextContentProcessor:
    """Process text content from comments and danmaku"""
    
    def __init__(self):
        self.text_processor = TextProcessor()
        self.client = SiliconFlowClient()
    
    def process(self, comments: List[Dict], danmaku: List[str]) -> Dict:
        """Process comments and danmaku"""
        result = {
            "comment_keywords": [],
            "sentiment": {},
            "discussion_summary": "",
            "total_comments": len(comments),
            "total_danmaku": len(danmaku)
        }
        
        # Combine all text
        comment_texts = [c.get("content", "") for c in comments]
        all_texts = comment_texts + danmaku
        
        if not all_texts:
            return result
        
        # Desensitize
        print("Desensitizing text content...")
        desensitized_texts = [self.text_processor.desensitize_text(t) for t in all_texts]
        combined_text = "\n".join(desensitized_texts)
        
        # Extract keywords
        print("Extracting keywords from comments and danmaku...")
        keywords = self.text_processor.extract_keywords(combined_text, top_k=10)
        result["comment_keywords"] = [k[0] for k in keywords]
        
        # Analyze sentiment
        print("Analyzing sentiment...")
        sentiment = self.text_processor.analyze_sentiment_keywords(combined_text)
        result["sentiment"] = sentiment
        
        # Determine overall sentiment
        sentiment_label = self._determine_sentiment_label(sentiment)
        result["sentiment_label"] = sentiment_label
        
        # Generate discussion summary
        print("Generating discussion summary...")
        discussion_summary = self._generate_discussion_summary(combined_text[:5000])
        result["discussion_summary"] = discussion_summary
        
        return result
    
    def _determine_sentiment_label(self, sentiment: Dict[str, int]) -> str:
        """Determine overall sentiment label"""
        total = sum(sentiment.values())
        if total == 0:
            return "中性"
        
        pos_ratio = sentiment.get("positive", 0) / total
        neg_ratio = sentiment.get("negative", 0) / total
        
        if pos_ratio > 0.4:
            return "正面"
        elif neg_ratio > 0.4:
            return "负面"
        else:
            return "中性"
    
    def _generate_discussion_summary(self, text: str) -> str:
        """Generate discussion summary using LLM"""
        if not text.strip():
            return "暂无讨论内容"
        
        messages = [
            {
                "role": "system",
                "content": "你是一个专业的社交媒体分析师。请根据评论和弹幕内容，总结观众的主要讨论点。"
            },
            {
                "role": "user",
                "content": f"请根据以下评论和弹幕内容，总结观众的主要讨论点（150字以内）：\n\n{text}"
            }
        ]
        
        summary = self.client.chat_completion(messages, max_tokens=500)
        return summary if summary else "无法生成讨论总结"
