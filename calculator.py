class Calculator:
    @staticmethod
    def calculate_mnav(holdings, crypto_price, shares_out):
        """mNAV 계산"""
        treasury_value = holdings * crypto_price
        mnav = treasury_value / shares_out
        return mnav

    @staticmethod
    def calculate_premium(stock_price, mnav):
        """프리미엄 퍼센트 계산"""
        if mnav == 0:
            return 0.0, 0.0
        ratio = stock_price / mnav
        premium_pct = (ratio - 1) * 100
        return premium_pct, ratio