from langchain_community.vectorstores import FAISS
from langchain.schema import Document
from langchain_huggingface import HuggingFaceEmbeddings  # 수정된 import

def create_simple_vectorstore():
    """간단한 벡터 저장소 만들기 (HuggingFace 로컬 임베딩)"""
    try:
        print("🤖 HuggingFace 모델 다운로드 중... (첫 실행시 시간 소요)")
        
        # HuggingFace 임베딩 모델 초기화
        model_name = "sentence-transformers/all-MiniLM-L6-v2"  # 가볍고 빠름
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},  # CPU 사용 명시
            encode_kwargs={'normalize_embeddings': True}  # 정규화
        )
        
        print("✅ 모델 로드 완료!")

        # 샘플 문서들 - 주식/투자 관련으로 변경
        sample_texts = [
            "애플의 아이폰 판매가 증가하고 있으며 주가 상승 요인으로 작용하고 있습니다.",
            "테슬라의 전기차 배터리 기술 발전으로 투자자들의 관심이 높아지고 있습니다.", 
            "삼성전자의 반도체 사업이 호조를 보이며 메모리 반도체 수요가 급증하고 있습니다.",
            "엔비디아의 AI 칩 수요 급증으로 주식 시장에서 큰 주목을 받고 있습니다.",
            "애플 주식의 기술적 분석 결과 상승 추세가 지속될 것으로 전망됩니다."
        ]

        print("📝 샘플 문서 임베딩 중...")

        # Document 객체로 변환
        documents = []
        for i, text in enumerate(sample_texts):
            doc = Document(
                page_content=text, 
                metadata={
                    'id': i, 
                    'topic': 'stock_analysis',
                    'source': 'sample_data'
                }
            )
            documents.append(doc)

        # FAISS 벡터 저장소 생성
        vectorstore = FAISS.from_documents(documents, embeddings)
        print("✅ 벡터 저장소 생성 완료!")

        return vectorstore

    except Exception as e:
        print(f"❌ 임베딩 에러: {e}")
        print("💡 해결 방법:")
        print("1. 인터넷 연결 확인 (모델 다운로드 필요)")
        print("2. pip install sentence-transformers 실행")
        return None


def test_search(vectorstore):
    """검색 테스트 함수"""
    queries = [
        "AI 관련 투자",
        "전기차 주식",
        "애플 주가 전망",
        "반도체 투자 기회",
        "기술적 분석"
    ]

    for query in queries:
        print(f"\n🔍 '{query}' 검색 결과:")
        results = vectorstore.similarity_search(query, k=2)

        for i, doc in enumerate(results, 1):
            print(f"  {i}. {doc.page_content}")
            print(f"     메타데이터: {doc.metadata}")


# 테스트 코드
if __name__ == "__main__":
    print("🧠 HuggingFace 무료 임베딩 테스트 시작!")
    print("💰 비용: 완전 무료!")

    vectorstore = create_simple_vectorstore()

    if vectorstore:
        print("\n🎉 성공! 무료 벡터 저장소 완성!")
        test_search(vectorstore)

        # 벡터 저장소 저장
        print("\n💾 벡터 저장소 로컬 저장 중...")
        vectorstore.save_local("portfolio_vectorstore_free")
        print("✅ 저장 완료: portfolio_vectorstore_free 폴더")
        
        print("\n🚀 내일은 이 벡터 저장소를 FastAPI와 연결할 예정!")

    else:
        print("❌ 벡터 저장소 생성 실패")