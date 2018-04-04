"""
#   Hot Otter
#       description: screenshot web pages using Chrome
#   author: Alex Herrick - @alxhrck
#   April 2018
#
# Ref:
# https://gist.github.com/rverton/d07a2232f4c0e1c2b9894e9bdb4fa6cf
#
"""

import os
import argparse
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

CHROME_PATH = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
CHROMEDRIVER_PATH = os.path.abspath('chromedriver.exe')
service = None
driver = None


def chrome_configure(window_size):
    try:
        global service
        chrome_options = Options()
        #chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size={size}".format(size=window_size))
        chrome_options.binary_location = CHROME_PATH
        service = webdriver.chrome.service.Service(os.path.abspath(CHROMEDRIVER_PATH))
        service.start()
        return chrome_options
    except WebDriverException as e:
        exit('[!] Error', str(e))


def output_naming(url):
    dt = time.time()
    try:
        o = '{u}-{dt}.png'.format(u=url.split('://')[1], dt=str(dt))
    except IndexError:
        o = '{u}-{dt}.png'.format(u=url, dt=str(dt))
    return o


def make_screenshot(url, chrome_options=None):
    if not url.startswith('http'):
        url = 'http://' + url
        #raise Exception('URLs need to start with "http(s)"')

    output = output_naming(url)
    global driver
    if driver:
        session_id = driver.session_id
    else:
        driver = webdriver.Remote(
            service.service_url,
            desired_capabilities=chrome_options.to_capabilities()
        )
        session_id = driver.session_id

    driver.session_id = session_id
    driver.get(url)
    driver.save_screenshot(output)


if __name__ == '__main__':
    usage = "%(prog)s [-u <url> | -f <file>]"

    parser = argparse.ArgumentParser(usage=usage)
    parser.add_argument('-s', '--size', help="browser windows size (default: 1920,1080)", default='1920,1080')
    parser.add_argument('-u', '--url', help='URLs should start with http(s)')
    parser.add_argument('-f', '--file', help='input file with list of urls')

    args = parser.parse_args()
    opts = chrome_configure(args.size)

    if args.file:
        try:
            with open(args.file, 'rb') as f:
                urls = f.readlines()
            for url in urls:
                print '[+] Screenshot:', url.strip()
                make_screenshot(url.strip(), opts)
        except IOError as e:
            exit('[!] Error: ' + str(e))
    elif args.url:
        make_screenshot(args.url, opts)
    else:
        parser.print_help()

    if driver:
        driver.quit()
