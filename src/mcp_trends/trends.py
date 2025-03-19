import requests
import logging
from typing import Any, List

import pandas as pd
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError

logger = logging.getLogger("mcp-trends")

class Trends():
    def __init__(
            self,
            proxy: str = 'https://34.203.233.13:80',
            hl: str ='en-US',
            retries: int=2,
            verify_ssl: bool =False
    ):
        self.proxy = proxy
        self.timeout=(10, 25)
        self.retries = retries
        self.hl = hl
        self.tz=360
        self.backoff_factor=0.1
        self.verify_ssl = verify_ssl

        self.trend = TrendReq(proxies=['https://34.203.233.13:80',])

        logger.debug(f"Trends client initialized with proxy={proxy}")

    def get_interest_by_region(self, keywords: List) -> str:
        logger.info(f"Getting interest by region with keywords: {keywords}")
        try:
            keywords_list=[]
            if "," in keywords:
                keywords_list = [keyword.strip() for keyword in keywords.split(",")]
            else:
                keywords_list = [keywords]
    
                self.trend.build_payload(kw_list=keywords_list)
                df = self.trend.interest_by_region()
                print(df.head(10))
                return df.head(10)
        except TooManyRequestsError as e:
            logger.error(f"Rate limit exceeded: {e}")
            return f"Error: Rate limit exceeded. Please try again later. ({e})"
        except Exception as e:
            print(f"Error: {e}")
            

'''
if __name__ == "__main__":
    trends = Trends()
    res = trends.get_interest_by_region("gen ai")
    print(res)
'''





