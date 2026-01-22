import pandas as pd
import os
from datetime import datetime

class Storage:
    def __init__(self, history_file='history.csv', sources_file='sources.csv'):
        self.history_file = history_file
        self.sources_file = sources_file

    def save_history(self, date, company, premium_pct, mnav_ratio):
        """히스토리 저장"""
        data = {
            'date': [date],
            'company': [company],
            'premium_pct': [premium_pct],
            'mnav_ratio': [mnav_ratio]
        }
        df = pd.DataFrame(data)
        if os.path.exists(self.history_file):
            df.to_csv(self.history_file, mode='a', header=False, index=False)
        else:
            df.to_csv(self.history_file, index=False)

    def save_source(self, date, company, holdings, source_url):
        """소스 로그 저장"""
        data = {
            'date': [date],
            'company': [company],
            'holdings': [holdings],
            'source': [source_url]
        }
        df = pd.DataFrame(data)
        if os.path.exists(self.sources_file):
            df.to_csv(self.sources_file, mode='a', header=False, index=False)
        else:
            df.to_csv(self.sources_file, index=False)