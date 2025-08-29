from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from data_collector import get_stock_price
from news_collector import get_stock_news_correct
from conversation_manager import ConversationManager
import os

class PortfolioChatBot:
    def __init__(self):
        # 기존 코드 유지
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        self.vectorstore = None
        if os.path.exists("portfolio_vectorstore_free"):
            try:
                self.vectorstore = FAISS.load_local(
                    "portfolio_vectorstore_free", 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                print("✅ 기존 벡터 저장소 로드 완료")
            except:
                print("⚠️ 기존 벡터 저장소 로드 실패, 새로 생성합니다")
        
        # 대화 관리자 추가 🆕
        self.conversation_manager = ConversationManager()
    
    def get_stock_analysis(self, ticker):
        """기존 코드 유지"""
        stock_data = get_stock_price(ticker)
        if not stock_data:
            return "❌ 주식 정보를 가져올 수 없습니다"
        
        news = get_stock_news_correct(ticker)
        
        analysis = f"""📊 {stock_data['company_name']} 분석:
💰 현재 가격: ${stock_data['current_price']:.2f}
🏢 섹터: {stock_data['sector']}
📰 최근 뉴스: {len(news)}건"""
        
        if news:
            analysis += f"\n🔥 주요 뉴스: {news[0]['title'][:50]}..."
        
        return analysis.strip()
    
    def chat_with_context(self, user_message, session_id="default"):
        """맥락을 고려한 대화 🆕"""
        user_message_lower = user_message.lower()
        
        # 이전 대화 맥락 가져오기
        context = self.conversation_manager.get_context(session_id, last_n=2)
        last_mentioned_stocks = self.conversation_manager.get_last_mentioned_stocks(session_id)
        
        # 맥락을 고려한 응답 생성
        response = ""
        
        if "리스크" in user_message_lower or "위험" in user_message_lower:
            if last_mentioned_stocks:
                ticker = last_mentioned_stocks[-1]  # 가장 최근 언급된 주식
                response = f"🚨 {ticker} 투자 리스크:\n"
                response += "• 시장 변동성에 민감\n"
                response += "• 기술주 특성상 높은 변동폭\n" 
                response += "• 금리 인상 시 주가 하락 가능성"
            else:
                response = "어떤 주식의 리스크가 궁금하신가요? 먼저 종목을 말씀해주세요."
        
        elif "그" in user_message_lower or "그거" in user_message_lower or "그런데" in user_message_lower:
            if last_mentioned_stocks:
                ticker = last_mentioned_stocks[-1]
                if "전망" in user_message_lower:
                    response = f"📈 {ticker} 전망:\n앞서 분석한 종목 기준으로, 장기적으로는 긍정적이지만 단기 변동성에 주의하세요."
                else:
                    response = f"📊 앞서 말씀드린 {ticker}에 대한 추가 정보가 필요하시다면 구체적으로 물어보세요!"
            else:
                response = "무엇에 대해 더 알고 싶으신가요?"
        
        elif "비교" in user_message_lower:
            if len(last_mentioned_stocks) >= 2:
                response = f"📊 {last_mentioned_stocks[-2]} vs {last_mentioned_stocks[-1]} 비교:\n"
                response += "두 종목 모두 기술주로서 비슷한 특성을 가지지만, 각각의 사업 영역이 다릅니다."
            else:
                response = "비교할 두 종목을 말씀해주세요!"
        
        else:
            # 기존 로직 실행
            response = self.chat_original(user_message)
        
        # 대화 히스토리에 저장
        self.conversation_manager.add_message(session_id, user_message, response)
        
        return response
    
    def chat_original(self, user_message):
        """기존 chat 함수명 변경"""
        user_message_lower = user_message.lower()
        
        if "분석" in user_message_lower or "어때" in user_message_lower:
            tickers = ["애플", "AAPL", "테슬라", "TSLA", "삼성", "005930"]
            for ticker in tickers:
                if ticker.lower() in user_message_lower:
                    if ticker in ["애플", "AAPL"]:
                        return self.get_stock_analysis("AAPL")
                    elif ticker in ["테슬라", "TSLA"]:
                        return self.get_stock_analysis("TSLA")
                    elif ticker in ["삼성", "005930"]:
                        return self.get_stock_analysis("005930.KS")
        
        elif "안녕" in user_message_lower or "hello" in user_message_lower:
            return "👋 안녕하세요! 포트폴리오 분석봇입니다. 어떤 주식에 대해 궁금하신가요?"
        
        elif "포트폴리오" in user_message_lower:
            return "📊 포트폴리오를 분석해드릴게요! '애플 30%, 테슬라 20%' 이런 식으로 말씀해주세요."
        
        else:
            return "🤔 잘 모르겠어요. '애플 분석해줘' 또는 '테슬라 어때?' 같이 물어보세요!"

# 테스트 코드
if __name__ == "__main__":
    print("🤖 멀티턴 챗봇 테스트!")
    
    chatbot = PortfolioChatBot()
    
    # 연속 대화 테스트
    test_conversation = [
        ("user1", "애플 분석해줘"),
        ("user1", "그 주식 리스크는?"),
        ("user1", "테슬라는 어때?"),  
        ("user1", "두 종목 비교해줘")
    ]
    
    for session_id, message in test_conversation:
        print(f"\n👤 사용자: {message}")
        response = chatbot.chat_with_context(message, session_id)
        print(f"🤖 봇: {response}")