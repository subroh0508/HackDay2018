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
        self._data = list()

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

        # Selenium settings
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--log-level=3')
        driver = webdriver.Chrome(chrome_options=options)

        # get a HTML response
        driver.get(query)

        # results
        try:
            # Wait processing of javascript
            # sleep(6)
            # parse the response
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html, "lxml")
            result_bodies = soup.find_all("div", class_="box")

        except Exception:
            # Try again only once
            sleep(6)
            # parse the response
            html = driver.page_source.encode('utf-8')
            soup = BeautifulSoup(html, "lxml")
            result_bodies = soup.find_all("div", class_="box")

        # Close browser
        driver.close()
        driver.quit()

        for body in result_bodies:
            content = body.find("div", class_="boxim")
            image = content.find("img")
            alt, src = image.get("alt"), image.get("src")
            self._data.append({"name": alt, "url": src})

        print("Scraped {} to {}".format(start, start+max_results-1))

    def crawl_all(self, page_max=10000, span=20):
        for i in range(1, page_max, span):
            self.crawl(start=i, max_results=span)

        print(self._data)



def test():
    crlr = Crawler()
    crlr.crawl_all(page_max=100)


if __name__ == '__main__':
    test()
