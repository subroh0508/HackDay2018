from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import sleep
from joblib import Parallel, delayed
import pickle


QUERY_ROOT = "https://www.irasutoya.com/search"


def crawl(start, max_results=20):
    params = dict()
    params["q"] = "*"
    params["updated-max"] = "2018-12-10T17:00:00-08:00"
    params["start"] = start
    params["max-results"] = max_results
    params["by-date"] = "false"
    conditions = ["=".join([str(k), str(v)]) for k, v in params.items()]
    conditions_joined = "&".join(conditions)

    query = "?".join((QUERY_ROOT, conditions_joined))

    # Selenium settings
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(chrome_options=options)

    # get a HTML response
    driver.get(query)

    # results
    try:
        # parse the response
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "lxml")
        result_bodies = soup.find_all("div", class_="box")

    except Exception:
        # Try again only once
        sleep(2)
        # parse the response
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "lxml")
        result_bodies = soup.find_all("div", class_="box")

    # Close browser
    driver.close()
    driver.quit()

    results = list()

    for body in result_bodies:
        content = body.find("div", class_="boxim")
        image = content.find("img")
        alt, src = image.get("alt"), image.get("src")
        results.append({"name": alt, "url": src})

    print("Scraped {} to {}".format(start, start+max_results-1))

    return results


def crawl_all(start=1, page_max=10000, span=20):
    results_list = Parallel(n_jobs=-1, verbose=0, timeout=None)\
        ([delayed(crawl)(i) for i in range(start, page_max, span)])

    # Parse to 1 dimension
    result = list()
    for results in results_list:
        result += results

    return result


def main():
    result = crawl_all(page_max=20700)

    with open('irasutoya_contents.pickle', 'wb') as f:
        pickle.dump(result, f)


if __name__ == '__main__':
    main()
