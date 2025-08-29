from typing import Dict, List
from datetime import datetime

class ConversationManager:
    def __init__(self):
        # 세션별 대화 히스토리 저장
        self.conversations: Dict[str, List[dict]] = {}
    
    def add_message(self, session_id: str, user_message: str, bot_response: str):
        """대화 히스토리에 메시지 추가"""
        if session_id not in self.conversations:
            self.conversations[session_id] = []
        
        self.conversations[session_id].append({
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "bot": bot_response,
            "turn": len(self.conversations[session_id]) + 1
        })
        
        # 메모리 절약을 위해 최근 10개만 유지
        if len(self.conversations[session_id]) > 10:
            self.conversations[session_id] = self.conversations[session_id][-10:]
    
    def get_context(self, session_id: str, last_n: int = 3) -> str:
        """최근 대화 맥락 가져오기"""
        if session_id not in self.conversations:
            return ""
        
        recent_messages = self.conversations[session_id][-last_n:]
        context = []
        
        for msg in recent_messages:
            context.append(f"사용자: {msg['user']}")
            context.append(f"봇: {msg['bot']}")
        
        return "\n".join(context)
    
    def get_last_mentioned_stocks(self, session_id: str) -> List[str]:
        """최근 대화에서 언급된 주식들 찾기"""
        if session_id not in self.conversations:
            return []
        
        mentioned_stocks = []
        stock_keywords = {
            "애플": "AAPL",
            "aapl": "AAPL", 
            "테슬라": "TSLA",
            "tsla": "TSLA",
            "삼성": "005930.KS",
            "samsung": "005930.KS",
            "엔비디아": "NVDA",
            "nvidia": "NVDA"
        }
        
        # 최근 3개 메시지에서 주식 찾기
        recent_messages = self.conversations[session_id][-3:]
        for msg in recent_messages:
            user_msg = msg['user'].lower()
            for keyword, ticker in stock_keywords.items():
                if keyword in user_msg and ticker not in mentioned_stocks:
                    mentioned_stocks.append(ticker)
        
        return mentioned_stocks[:3]  # 최대 3개만

# 테스트
if __name__ == "__main__":
    cm = ConversationManager()
    
    # 테스트 대화
    cm.add_message("user1", "애플 분석해줘", "애플 주식 분석 결과...")
    cm.add_message("user1", "그 주식 리스크는?", "애플의 주요 리스크는...")
    cm.add_message("user1", "테슬라는 어때?", "테슬라 분석 결과...")
    
    print("📝 대화 맥락:")
    print(cm.get_context("user1"))
    print("\n📊 언급된 주식들:")
    print(cm.get_last_mentioned_stocks("user1"))