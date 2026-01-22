from curl_cffi import requests
import yfinance as yf
from openai import OpenAI
from bs4 import BeautifulSoup
import json
import os
import re
from datetime import datetime

class DataFetcher:
    def __init__(self, config):
        self.config = config
        self.cache_file = "price_cache.json"
        self.cache = self._load_cache()
        
        # [설정] OpenAI 연결
        api_key = config.get('openai_api_key')
        if api_key:
            try:
                self.client = OpenAI(api_key=api_key)
                self.model_name = "gpt-4o-mini" # 가성비 모델
                print(f"🤖 AI(ChatGPT) 감시 모드 작동 중...")
            except Exception as e:
                print(f"⚠️ OpenAI 설정 오류: {e}")
                self.client = None
        else:
            self.client = None

    def _load_cache(self):
        if os.path.exists(self.cache_file):
            try:
                with open(self.cache_file, 'r') as f: return json.load(f)
            except: return {}
        return {}
    
    def _save_cache(self):
        try:
            with open(self.cache_file, 'w') as f: json.dump(self.cache, f, indent=2)
        except: pass

    # =========================================================
    # 1. 시장 데이터 (변동 없음)
    # =========================================================
    def get_market_data(self, ticker, default_shares, company_name=None):
        stock_price = self._get_stock_price(ticker)
        if stock_price is None:
             stock_price = self.cache.get(ticker, {}).get('price', 2.50)

        crypto_price = self._get_crypto_price()
        
        try:
            shares_out = float(default_shares)
        except:
            shares_out = 454862451.0 
            
        try:
            session = requests.Session(impersonate="chrome")
            stock = yf.Ticker(ticker, session=session)
            info = stock.info
            if 'sharesOutstanding' in info and info['sharesOutstanding']:
                shares_out = info['sharesOutstanding']
        except: pass
        
        return stock_price, crypto_price, shares_out

    def _get_stock_price(self, ticker):
        try:
            session = requests.Session(impersonate="chrome")
            stock = yf.Ticker(ticker, session=session)
            hist = stock.history(period="1d")
            if not hist.empty:
                price = float(hist['Close'].iloc[-1])
                self._update_cache(ticker, price)
                return price
        except: return None

    def _get_crypto_price(self):
        try:
            url = "https://api.coingecko.com/api/v3/simple/price"
            session = requests.Session(impersonate="chrome")
            resp = session.get(url, params={"ids": "ethereum", "vs_currencies": "usd"}, timeout=10)
            return float(resp.json()['ethereum']['usd'])
        except: return 3000.0

    # =========================================================
    # 2. 보유량 데이터 (여기가 핵심!)
    # =========================================================
    def get_holdings_from_news(self, pr_url, default_holdings):
        
        print(f"🔍 AI가 최신 뉴스를 검색하고 있습니다...")
        
        # 1. 구글 뉴스 검색 결과 긁어오기
        text_content = ""
        try:
            # 브라우저인 척 위장 (중요)
            session = requests.Session(impersonate="chrome")
            resp = session.get(pr_url, timeout=15)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            # 검색 결과 텍스트만 추출
            text_content = soup.get_text(separator=' ', strip=True)[:6000]
            # print(f"DEBUG: 수집된 텍스트 길이: {len(text_content)}자") 
            
        except Exception as e:
            print(f"⚠️ 검색 접속 실패: {e}")
            return float(default_holdings)

        # 2. ChatGPT에게 분석 시키기
        if self.client:
            try:
                # AI에게 내리는 아주 구체적인 지령
                prompt = f"""
                You are a sophisticated financial data analyst.
                I have provided the text from a Google News search result for 'BitMine Immersion Technologies'.
                
                Your Goal: Find the most recent and largest 'Ethereum (ETH) holdings' number mentioned in the snippets.
                
                Context:
                - The company is known to hold millions of dollars worth of ETH.
                - Look for phrases like "holdings update", "treasury balance", "holds X ETH".
                - Be careful with 'Million' units (e.g., "4.1 Million ETH" means 4,100,000).
                - Ignore trading volumes or unrelated numbers.

                Output Rules:
                - Return ONLY the raw integer number (e.g., 4168000).
                - Do not write "ETH" or "tokens". Just the number.
                - If you absolutely cannot find any holding info, return '0'.

                Search Result Text:
                {text_content}
                """
                
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )
                
                result_text = response.choices[0].message.content.strip()
                print(f"🤖 AI의 판단: {result_text}")

                # 숫자만 추출
                numbers = re.findall(r'\d+', result_text)
                if numbers:
                    val = float("".join(numbers))
                    
                    # 3000 같은 터무니없이 작은 숫자는 무시 (안전장치)
                    if val > 100000: 
                        print(f"✅ AI 검색 성공! 최신 보유량 발견: {val:,.0f} ETH")
                        return val
                    else:
                        print(f"⚠️ AI가 숫자를 찾았으나 너무 작거나 이상함 ({val}). 기본값 사용.")
                else:
                    print("⚠️ AI가 텍스트에서 유의미한 숫자를 못 찾았습니다.")

            except Exception as e:
                print(f"⚠️ ChatGPT 분석 에러: {e}")

        print(f"👉 검색 실패. 설정된 기본값({default_holdings})을 사용합니다.")
        return float(default_holdings)