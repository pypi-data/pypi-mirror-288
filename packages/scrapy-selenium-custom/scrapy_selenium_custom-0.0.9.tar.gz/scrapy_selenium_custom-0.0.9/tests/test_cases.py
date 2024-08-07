"""This module contains the base test cases for the ``scrapy_selenium`` package"""

from shutil import which
from unittest import TestCase

import scrapy


class BaseScrapySeleniumTestCase(TestCase):
    """Base test case for the ``scrapy-selenium`` package"""

    class SimpleSpider(scrapy.Spider):
        name = 'simple_spider'
        allowed_domains = ['python.org']
        start_urls = ['http://python.org']

        def parse(self, response):
            pass

    @classmethod
    def setUpClass(cls):
        """Create a scrapy process and a spider class to use in the tests"""

        '''
        cls.settings = {
            'SELENIUM_DRIVER_NAME': 'firefox',
            'SELENIUM_DRIVER_EXECUTABLE_PATH': which('geckodriver'),
            'SELENIUM_DRIVER_ARGUMENTS': ['--headless=new']
        }
        '''
        cls.settings = {
            'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
            'SELENIUM_DRIVER_NAME': 'chrome',
            'SELENIUM_DRIVER_EXECUTABLE_PATH': None,
            # https://www.selenium.dev/blog/2023/headless-is-going-away/
            'SELENIUM_DRIVER_ARGUMENTS': ['--headless=new'],
            'SELENIUM_DRIVER_LOGGER_LEVEL': 'INFO'
        }
        cls.spider_klass = cls.SimpleSpider
