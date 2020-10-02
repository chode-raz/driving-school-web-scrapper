import requests
import os
from bs4 import BeautifulSoup
import requests.cookies


class ScrapIt:
    base_url = 'https://extranet.jiscd.sk'

    def __init__(self):
        jar = requests.cookies.RequestsCookieJar()
        jar.set('LastMRH_Session', 'df7863e2')
        jar.set('MRHSession', '10e1bbf567e9467a66e7e9c4df7863e2')
        jar.set('_WL_AUTHCOOKIE_SAKAI_JSESSIONID', 'Tz9YZ3NSoGpKYoyfDMv7.')
        jar.set('JSESSIONID', '22ab0f84-c375-49ff-8018-8425eec3805f.sakaiext1a.jiscd')
        jar.set('F5_ST', '1z1z1z1601531092z43200')

        self.session = requests.Session()
        self.session.cookies = jar

        self.get_urls()
        pass

    def get_urls(self):
        url = 'https://extranet.jiscd.sk/portal/tool/6acfc7f9-406e-4728-bab5-5d518bf7e914'
        r = self.session.get(url=url)
        print(r.text)
        soup = BeautifulSoup(r.text, "html.parser")
        textbox = soup.select('.textbox span span')
        pass

    def create_dir(self):
        pass

    def get_page(self):
        pass

    def create_assets_folder(self):
        pass

    def get_page_assets(self):
        pass
