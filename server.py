from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from chat_engine import PortfolioChatBot

# 서버 만들기
app = FastAPI(title="포트폴리오 분석봇", version="1.0")

# 챗봇 인스턴스 생성 (서버 시작할 때 한 번만)
chatbot = PortfolioChatBot()

# 대화 요청 형식 정의
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

# 기본 페이지
@app.get("/")
def home():
    return {"message": "🚀 포트폴리오 분석봇이 준비되었습니다!"}

# 주식 정보 API
@app.get("/stock/{ticker}")
def get_stock_info(ticker: str):
    from data_collector import get_stock_price
    
    stock_data = get_stock_price(ticker)
    if stock_data:
        return {"success": True, "data": stock_data}
    else:
        return {"success": False, "error": "주식 정보를 가져올 수 없습니다"}

# 대화 API 🆕
# 대화 API에서 이 부분만 변경
@app.post("/chat")
def chat_with_bot(request: ChatRequest):
    try:
        # 기존: response = chatbot.chat(request.message)
        response = chatbot.chat_with_context(request.message, request.session_id)  # 🆕 변경
        return {
            "success": True,
            "response": response,
            "session_id": request.session_id
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"대화 처리 중 오류: {str(e)}"
        }

# 서버 실행 함수
if __name__ == "__main__":
    print("🔥 포트폴리오 분석봇 서버 시작!")
    print("📍 주소: http://localhost:8000")
    print("📖 API 문서: http://localhost:8000/docs")
    print("💬 대화 테스트: http://localhost:8000/docs 에서 /chat 엔드포인트 사용")
    uvicorn.run(app, host="0.0.0.0", port=8000)