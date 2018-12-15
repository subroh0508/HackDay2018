import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import codecs
from time import sleep
from joblib import Parallel, delayed
from collections import deque
import argparse


class Crawler:
    QUERY_ROOT = "https://www.irasutoya.com/search"

    def __init__(self):
        pass

    def crawl(self, start, update_max="2018-12-10T17:00:00-08:00", max_results=20, by_date="false"):
        params = dict()
        params["q"] = "*"
        params["updated-max"] = update_max
        params["start"] = start
        params["max-results"] = max_results
        params["by-date"] = by_date
        conditions = ["=".join([str(k), str(v)]) for k, v in params.items()]
        conditions_joined = "&".join(conditions)

        query = "?".join((Crawler.QUERY_ROOT, conditions_joined))
        print(query)


def test():
    crlr = Crawler()
    crlr.crawl(start=21)


if __name__ == '__main__':
    test()
