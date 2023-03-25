import bs4
import requests

from time import sleep
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from util.environment_util import get_platform, Platform
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from ..download_url_resolver import DownloadUrlResolver


class UnableToResolveException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class ZuluDownloadUrlResolver(DownloadUrlResolver):
    def __init__(self):
        self.download_url_root = 'https://cdn.azul.com/zulu/bin/'
        self.scraper = AzulZuluVersionScraper()

    def get_url(self, version: str, platform: Platform) -> str:
        # Example package version: 17.0.6+10  --> 17.0.6
        return f'{self.download_url_root}/{self.get_file_to_download(version, platform)}'

    def get_resolved_version(self, version: str):
        return self.scraper.resolve_version_title(version)[1]

    def get_file_to_download(self, version: str, platform: Platform) -> str:
        package_title = self.scraper.resolve_version_title(version)[0].split('+')[0]
        return f'zulu{version.strip()}-ca-jdk{package_title.strip()}-{platform.value}.zip'


class AzulZuluVersionScraper:
    def __init__(self):
        self.root_url = 'https://www.azul.com/downloads/#zulu'
        self.soup = self._get_soup()

    def resolve_version_title(self, package_version: str) -> (str, str):
        package_version_divs = self.soup.findAll("div", class_='c-dlt__package-version')

        # Try resolve by searching for exact verison
        container_element = None
        for div in package_version_divs:
            if f'Azul Zulu: {package_version}' == div.text.strip():
                container_element = div.parent
        if container_element:
            return container_element.find('div', class_='c-dlt__package-title').text, package_version

        # Fallback strategy: Find the latest version that matches e.g. 17.40 --> 17.40.19
        found_package_versions = list(map(lambda x: x.text.strip(), package_version_divs))
        versions = list(filter(lambda x: f'Azul Zulu: {package_version}' in x, found_package_versions))
        sorted_versions = list(sorted(versions))
        if len(sorted_versions) > 0:
            fallback_version = sorted_versions[0].split("Azul Zulu:")[1].strip()
            print(f'Could not find exact match for {package_version}, falling back to {fallback_version}')
            for div in package_version_divs:
                if f'Azul Zulu: {fallback_version}' == div.text.strip():
                    container_element = div.parent
            if container_element:
                return container_element.find('div', class_='c-dlt__package-title').text, fallback_version

        raise UnableToResolveException(f'Could not resolve version title for package version: {package_version}')

    def _get_soup(self) -> bs4.BeautifulSoup:
        browser = self._get_selenium_driver()
        browser.implicitly_wait(10)
        browser.get(self.root_url)
        browser.find_element(By.CLASS_NAME, "c-dlt__package-version")
        page = browser.page_source
        return bs4.BeautifulSoup(page, 'lxml')

    def _get_selenium_driver(self):
        driver_binary = ChromeDriverManager().install()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(service=ChromeService(driver_binary), options=chrome_options)
        return driver
