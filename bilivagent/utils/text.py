"""Text processing and analysis utilities"""
import re
import jieba
import jieba.analyse
from typing import List, Dict
from collections import Counter
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


class TextProcessor:
    """Text processing and analysis"""
    
    def __init__(self):
        # Initialize jieba
        jieba.setLogLevel(jieba.logging.INFO)
    
    def desensitize_text(self, text: str) -> str:
        """Desensitize sensitive information"""
        # Remove phone numbers
        text = re.sub(r'1[3-9]\d{9}', '***', text)
        
        # Remove email addresses
        text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***@***.***', text)
        
        # Remove ID card numbers
        text = re.sub(r'\b\d{17}[\dXx]\b', '***', text)
        
        return text
    
    def extract_keywords(self, text: str, top_k: int = 10) -> List[tuple]:
        """Extract keywords from text"""
        # Use jieba to extract keywords with TF-IDF
        keywords = jieba.analyse.extract_tags(text, topK=top_k, withWeight=True)
        return keywords
    
    def generate_wordcloud(self, text: str, output_path: str) -> str:
        """Generate word cloud image"""
        # Segment text
        words = jieba.cut(text)
        
        # Filter out single characters and common stop words
        stop_words = {'的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
        filtered_words = [w for w in words if len(w) > 1 and w not in stop_words]
        
        text_for_cloud = ' '.join(filtered_words)
        
        # Generate word cloud
        wordcloud = WordCloud(
            font_path='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Fallback font
            width=800,
            height=400,
            background_color='white',
            max_words=100
        ).generate(text_for_cloud)
        
        # Save to file
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig(output_path, bbox_inches='tight', dpi=150)
        plt.close()
        
        return output_path
    
    def analyze_sentiment_keywords(self, text: str) -> Dict[str, int]:
        """Analyze sentiment-related keywords"""
        # Define sentiment word lists
        positive_words = {'好', '棒', '赞', '优秀', '喜欢', '支持', '精彩', '厉害', '牛', '强', '给力', '有趣', '搞笑', '感动', '惊艳'}
        negative_words = {'差', '烂', '垃圾', '无聊', '讨厌', '恶心', '失望', '糟糕', '难看', '不好', '不行', '烦', '吐槽'}
        neutral_words = {'一般', '还行', '可以', '普通', '平常'}
        
        words = list(jieba.cut(text))
        
        sentiment_count = {
            'positive': 0,
            'negative': 0,
            'neutral': 0
        }
        
        for word in words:
            if word in positive_words:
                sentiment_count['positive'] += 1
            elif word in negative_words:
                sentiment_count['negative'] += 1
            elif word in neutral_words:
                sentiment_count['neutral'] += 1
        
        return sentiment_count
