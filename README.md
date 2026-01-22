# Crypto-Treasury-Pipeline

기업의 **암호화폐(ETH) 보유량**을 실시간으로 추적하여, **mNAV**와 **괴리율**을 계산하는 AI 파이프라인입니다.

## 특징
- **AI 기반 분석:** Google 뉴스 검색 결과를 **ChatGPT(GPT-4o-mini)**가 분석하여, 최신 ETH 보유량을 스스로 찾아냅니다.
- **실시간 데이터:** `yfinance`와 `CoinGecko` API를 통해 주가와 코인 가격을 실시간으로 반영합니다.
- **자동 리포트:** 분석 결과와 투자 지표(Premium %)가 담긴 깔끔한 HTML 리포트를 생성합니다.
<img width="885" height="724" alt="image" src="https://github.com/user-attachments/assets/6f903a07-aaf6-49ca-9bc5-17caac1f296f" />


## 기술 스택
- **Language:** Python
- **AI:** OpenAI API (GPT-4o-mini)
- **Libs:** yfinance, curl_cffi, BeautifulSoup4

## 설치 및 실행
```bash
pip install -r requirements.txt
python main.py
