try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

from jinja2 import Template
import pandas as pd
import os

class Reporter:
    def __init__(self, history_file='history.csv'):
        self.history_file = history_file

    def generate_chart(self, company, output_file='premium_chart.png'):
        """프리미엄 추이 차트 생성"""
        if not MATPLOTLIB_AVAILABLE:
            return None
        # 파일이 없거나 비어있으면 차트 생성 안 함
        if not os.path.exists(self.history_file):
            return None
        
        try:
            df = pd.read_csv(self.history_file)
            if df.empty:
                return None
                
            company_data = df[df['company'] == company]
            if company_data.empty:
                return None

            plt.figure(figsize=(10, 5))
            plt.plot(company_data['date'], company_data['premium_pct'], marker='o')
            plt.title(f'{company} Premium % Trend')
            plt.xlabel('Date')
            plt.ylabel('Premium %')
            plt.grid(True)
            plt.savefig(output_file)
            plt.close()
            return output_file
        except Exception as e:
            print(f"차트 생성 중 오류: {e}")
            return None

    def generate_html_report(self, company, stock_price, crypto_price, shares_out, holdings, mnav, premium_pct, mnav_ratio, chart_file):
        """HTML 리포트 생성"""
        template_str = """
        <html>
        <head>
            <title>{{ company }} mNAV Report</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                h1 { color: #2c3e50; }
                .metric { margin-bottom: 10px; font-size: 1.1em; }
                .label { font-weight: bold; width: 180px; display: inline-block; }
                .value { color: #34495e; }
            </style>
        </head>
        <body>
            <h1>{{ company }} Treasury Report</h1>
            <hr>
            <div class="metric"><span class="label">Stock Price:</span> <span class="value">${{ "{:,.2f}".format(stock_price) }}</span></div>
            <div class="metric"><span class="label">Crypto Price:</span> <span class="value">${{ "{:,.2f}".format(crypto_price) }}</span></div>
            <div class="metric"><span class="label">Shares Outstanding:</span> <span class="value">{{ "{:,.0f}".format(shares_out) }}</span></div>
            <div class="metric"><span class="label">Holdings:</span> <span class="value">{{ "{:,.0f}".format(holdings) }} ETH</span></div>
            <br>
            <div class="metric"><span class="label">mNAV per Share:</span> <span class="value">${{ "{:,.2f}".format(mnav) }}</span></div>
            <div class="metric"><span class="label">mNAV Ratio:</span> <span class="value">{{ "{:,.2f}".format(mnav_ratio) }}x</span></div>
            <div class="metric"><span class="label">Premium:</span> <span class="value" style="color: {{ 'red' if premium_pct > 0 else 'blue' }};">{{ "{:,.2f}".format(premium_pct) }}%</span></div>
            
            {% if chart_file %}
            <br>
            <h3>Premium Trend</h3>
            <img src="{{ chart_file }}" alt="Premium Chart" style="max-width: 600px; border: 1px solid #ccc;">
            {% endif %}
        </body>
        </html>
        """
        template = Template(template_str)
        
        # 값이 None일 경우 0으로 처리하여 에러 방지
        html = template.render(
            company=company,
            stock_price=stock_price or 0,
            crypto_price=crypto_price or 0,
            shares_out=shares_out or 0,
            holdings=holdings or 0,
            mnav=mnav or 0,
            premium_pct=premium_pct or 0,
            mnav_ratio=mnav_ratio or 0,
            chart_file=chart_file
        )
        
        with open('report.html', 'w', encoding='utf-8') as f:
            f.write(html)
        return 'report.html'