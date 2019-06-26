'''
A simple python module to scan Stock Ticker symbols.
'''

import datetime
import json
import logging
import requests


from src import logger 
from src import task
from src import worker


log = logger.getLogger(__name__)
# logger.getLogger("requests").setLevel(logging.WARNING)
# logger.getLogger("urllib").setLevel(logging.WARNING)

class StockTask(task.Task):
    FIN_DATA_URL='https://www.alphavantage.co'
    API_KEY='XXXX'
    FIN_DATA_TYPE='TIME_SERIES_DAILY_ADJUSTED'

    def __init__(self, tckr='TSLA'):
        super(StockTask, self).__init__()
        self.tckr = tckr
        self.data = None
        self.date = datetime.datetime.now().strftime("%Y-%m-%d")

    def build_url(self):
        self.url = '%s/query?apikey=%s&function=%s&symbol=%s' % (
                self.FIN_DATA_URL,
                self.API_KEY,
                self.FIN_DATA_TYPE,
                self.tckr)

    def _run(self):
        try:
            self.build_url()
            r = requests.get(self.url)
            if r.status_code == 200:
                self.data = json.loads(r.text)

            opening = self.open_today()
            log.info("%s opened at : %s", self.tckr, opening)

        except Exception as err:
            _ = err

    def open_today(self):
        if not self.data:
            return None

        return self.data["Time Series (Daily)"][self.date]["1. open"]

def simple():


    data = ['VMW', 'AAPL', 'GOOG', 'TSLA', 'CRWD'] 
    tasks = [StockTask(tckr=x) for x in data]
    with worker.ThreadPool(2) as tpool:
        _ = [tpool.append_task(t) for t in tasks]

    open_today = [(x.tckr, x.open_today() if x.data else None) for x in tasks]

    log.info("Open today : %s", open_today)

def get_next_tckr():
    alphas = [chr(i).upper() for i in range(97, 97 + 26)]

    for i in ['_'] + alphas:
        for j in alphas:
            for k in alphas:
                for l in alphas:
                    tckr = j + k + l
                    tckr = tckr if i == '_' else i + tckr
                    yield tckr
def scrapper():
    log.info("======================")
    log.info("    Start Scrapping  ")
    log.info("======================")
    with worker.ThreadPool(2) as tpool:
        for tckr in get_next_tckr():
            task = StockTask(tckr)
            tpool.append_task(task)




if __name__ == '__main__':
    simple()
