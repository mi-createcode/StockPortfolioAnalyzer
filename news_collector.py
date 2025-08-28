import yfinance as yf
from datetime import datetime
import json

def get_stock_news_correct(ticker):
    """올바른 뉴스 가져오기 함수 - content 구조 반영"""
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        
        processed_news = []
        for article in news[:5]:  # 최신 5개만
            # content 안에 실제 데이터가 들어있음
            content = article.get('content', {})
            
            title = content.get('title', '제목 없음')
            summary = content.get('summary', '요약 없음')
            description = content.get('description', '')
            
            # summary가 비어있으면 description 사용
            if not summary or summary == '요약 없음':
                summary = description if description else '내용 없음'
            
            # 시간 파싱 (ISO 형식)
            pub_date_str = content.get('pubDate') or content.get('displayTime')
            if pub_date_str:
                try:
                    # ISO 형식 파싱: "2025-08-27T16:42:47Z"
                    published = datetime.fromisoformat(pub_date_str.replace('Z', '+00:00'))
                except:
                    published = datetime.now()
            else:
                published = datetime.now()
            
            # URL 가져오기
            canonical_url = content.get('canonicalUrl', {})
            link = canonical_url.get('url', '') if canonical_url else ''
            
            processed_news.append({
                'title': title,
                'summary': summary,
                'link': link,
                'published': published,
                'provider': content.get('provider', {}).get('displayName', 'Unknown')
            })
        
        return processed_news
        
    except Exception as e:
        print(f"뉴스 가져오기 에러: {e}")
        return []

# 테스트 코드
if __name__ == "__main__":
    print("📰 수정된 뉴스 테스트!")
    
    news = get_stock_news_correct('AAPL')
    
    if news:
        print(f"✅ 뉴스 {len(news)}개 수집 완료!\n")
        
        for i, article in enumerate(news, 1):
            print(f"🔥 {i}. {article['title']}")
            print(f"   📅 발행일: {article['published'].strftime('%Y-%m-%d %H:%M')}")
            print(f"   🏢 출처: {article['provider']}")
            
            # 요약 길면 자르기
            summary = article['summary']
            if len(summary) > 150:
                print(f"   📝 요약: {summary[:150]}...")
            else:
                print(f"   📝 요약: {summary}")
                
            if article['link']:
                print(f"   🔗 링크: {article['link']}")
            print("-" * 60)
    else:
        print("❌ 뉴스 가져오기 실패")