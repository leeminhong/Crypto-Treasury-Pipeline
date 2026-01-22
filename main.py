import yaml
from data_fetcher import DataFetcher
from calculator import Calculator
from storage import Storage
from reporter import Reporter
from datetime import datetime

def main():
    # 설정 로드
    with open('config.yaml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    fetcher = DataFetcher(config)
    calculator = Calculator()
    storage = Storage()
    reporter = Reporter()

    today = datetime.now().strftime('%Y-%m-%d')

    for company in config['companies']:
        name = company['name']
        ticker = company['ticker']
        default_shares = company['default_shares']
        default_holdings = company['default_holdings']
        pr_url = company['pr_url']

        # 데이터 수집
        stock_price, crypto_price, shares_out = fetcher.get_market_data(ticker, default_shares, name)
        holdings = fetcher.get_holdings_from_news(pr_url, default_holdings)

        if stock_price and crypto_price:
            # 계산
            mnav = calculator.calculate_mnav(holdings, crypto_price, shares_out)
            premium_pct, mnav_ratio = calculator.calculate_premium(stock_price, mnav)

            # 저장
            storage.save_history(today, name, premium_pct, mnav_ratio)
            storage.save_source(today, name, holdings, pr_url)

            # 리포트
            chart_file = reporter.generate_chart(name)
            html_file = reporter.generate_html_report(
                name, stock_price, crypto_price, shares_out, holdings, mnav, premium_pct, mnav_ratio, chart_file
            )

            print(f"Report generated for {name}: {html_file}")

if __name__ == "__main__":
    main()