import json
import time
import http.cookiejar as cjar
import selenium
import selenium.webdriver
import vimeo_dl as vimeo
from pprint import pprint as pp

SITE = 'https://membresia.org/conocimiento'
WAITTIME = 7


def bla(driver, url):
    a = driver.get(url)
    time.sleep(WAITTIME)
    return a

class WebDriver:

    def __init__(self, driver=selenium.webdriver.Chrome(), cookiesFileName='cookies.txt'):
        self.driver = driver
        #self.driver.get = bla
        self.cookiesFileName = cookiesFileName
        self.driver.get(SITE)
        for c in self._load_cookies():
            self.driver.add_cookie(c)

    def __enter__(self):
        return self.driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.quit()

    def _load_cookies(self):
        cookies = []
        cj = cjar.MozillaCookieJar(self.cookiesFileName)
        cj.load()
        for c in cj._cookies:
            for c2 in cj._cookies[c]:
                for c3 in cj._cookies[c][c2]:
                    cookie = cj._cookies[c][c2][c3]
                    cookies += [
                        {'name': cookie.name, 'value': cookie.value, 'domain': cookie.domain, 'path': cookie.path}]
        return cookies


def scrap_vimeo(page, driver):
    pp(page)
    driver.get(page)
    time.sleep(10)
    urls = [ url.get_attribute('href') for url in driver.find_elements_by_xpath('//a[@class="play-icon-wrap hidden-xs"]') ]
    vimeo_list = {}
    for u in urls:
        pp(u)
        driver.get(u)
        time.sleep(WAITTIME)
        title = driver.find_element_by_xpath('//h1').text
        try:
            video = driver.find_element_by_xpath('//iframe').get_attribute('src')
        except selenium.common.exceptions.NoSuchElementException as e:
            video = ''
        vimeo_list[title] = video
    pp(vimeo_list)
    return vimeo_list


with WebDriver() as driver:
    driver.get(SITE)
    time.sleep(WAITTIME)

    names_list = [ n.text for n in driver.find_elements_by_xpath('//div[@class="video-header"]/h3') ]
    video_list = [ href.get_attribute('href') for href in driver.find_elements_by_xpath('//a[@class="see-all"][@href]') ]
    pages = dict(zip(names_list, video_list))

    pp(pages)
    all_videos = {name: scrap_vimeo(url, driver) for name, url in pages.items()}

    with open('urls.txt', 'w') as file:
        file.write(json.dumps(all_videos, indent=4, sort_keys=True))

    pp(all_videos)

