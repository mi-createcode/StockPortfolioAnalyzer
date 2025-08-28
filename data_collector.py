import yfinance as yf

def get_stock_price(ticker):
    """주식 가격을 가져오는 함수"""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        history = stock.history(period="5d")  # 5일치 데이터
        
        current_price = history['Close'][-1]  # 가장 최근 가격
        
        return {
            'ticker': ticker,
            'current_price': current_price,
            'company_name': info.get('longName', 'Unknown'),
            'sector': info.get('sector', 'Unknown')
        }
    except Exception as e:
        print(f"에러 발생: {e}")
        return None

# 테스트 코드
if __name__ == "__main__":
    print("🚀 주식 데이터 테스트 시작!")
    
    # 애플 주식 정보 가져오기
    apple_data = get_stock_price('AAPL')
    
    if apple_data:
        print(f"✅ {apple_data['company_name']}")
        print(f"현재 가격: ${apple_data['current_price']:.2f}")
        print(f"섹터: {apple_data['sector']}")
    else:
        print("❌ 데이터 가져오기 실패")