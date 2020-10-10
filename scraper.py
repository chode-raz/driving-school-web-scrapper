import requests
import os
from bs4 import BeautifulSoup
import requests.cookies
import re
import fileinput


class ScrapIt:
    base_url = 'https://extranet.jiscd.sk'

    pages_path = '/home/rastislav/PycharmProjects/drive_school_scraper/test/'

    forbidden_urls = ['',
                      'https://public.test2.jiscd/portal/tool/8ffcfe76-ea9f-49c7-937e-e2bcca6ea426/ShowPage?errorMessage=&clearAttr=&newTopLevel=false&recheck=&itemId=2144&id=&addTool=-1&title=&source=&studentItemId=0&backPath=&sendingPage=2143&path=&postedComment=false&returnView='
                      ]

    def __init__(self):
        jar = requests.cookies.RequestsCookieJar()
        jar.set('LastMRH_Session', '3c253e69')
        jar.set('MRHSession', 'de9d929e38cc248b9383cc663c253e69')
        jar.set('_WL_AUTHCOOKIE_SAKAI_JSESSIONID', 'a0mV5E1BPmLoxLGcWGOl.')
        jar.set('JSESSIONID', '824fc494-553a-4da2-b946-6e972e72edeb.sakaiext1a.jiscd')
        jar.set('F5_ST', '1z1z1z1602240306z43200')

        self.session = requests.Session()
        self.session.cookies = jar

        self.get_urls()
        pass

    def get_urls(self):
        # url = 'https://extranet.jiscd.sk/portal/tool/6acfc7f9-406e-4728-bab5-5d518bf7e914'
        # r = self.session.get(url=url)
        # print(r.text)

        with open('/home/rastislav/PycharmProjects/drive_school_scraper/menu.html') as file:
            data = file.read()
        file.close()

        soup = BeautifulSoup(data, "html.parser")
        containers = soup.select('.textType')
        for container in containers:
            texts = container.select('.textbox span')
            title = ''
            for text in texts:
                if "Lekcia" in text.get_text():
                    title = text.get_text()

            if title is not None and title is not "":
                urls = []
                elements = container.select('.textbox li p a')
                i = 1
                for element in elements:
                    url = element.get('href')
                    header = element.get_text()
                    urls.append((header, url))
                    dir_path = self.pages_path + title + '/' + str(i) + '. ' + header.replace('/', ' ')
                    file_path = dir_path + '/' + header.replace('/', ' ') + '.html'
                    if not os.path.exists(file_path):
                        if url is not None and url not in self.forbidden_urls:
                            i += 1
                            self.create_dir(dir_path)
                            self.get_page(url, file_path)
        pass

    def create_dir(self, dir_name):
        access_rights = 0o755
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        pass

    def get_page(self, url, file_path):
        response = self.session.get(url=url)
        str_as_bytes = str.encode(response.text)
        f = open(file_path, 'wb')
        f.write(str_as_bytes)
        f.close()

    pass


def create_assets_folder(self, path):
    self.create_dir(path + '/assets/')
    pass


def get_page_assets(self, page_path, storage_path):
    with open(page_path) as file:
        page = file.read()
    file.close()

    file_input = fileinput.input(page_path, inplace=True)

    soup = BeautifulSoup(page, "html.parser")

    for link in soup.findAll('img'):
        image_url = link.get('src')
        response = self.session.get(image_url, stream=True)
        if response.status_code == 200:
            with open(storage_path + image_url.split('/')[-1], 'wb') as file:
                file.write(response.content)

    for script in soup.findAll('script'):
        script_type = script.get('type')

        if script_type is not None and script_type == 'text/javascript' and script.get('src') is not None:
            script_url = script.get('src')

            if 'http' not in script_url:
                script_url = self.base_url + script_url

            response = self.session.get(script_url)
            if response.status_code == 200:
                with open(storage_path + script_url.split('/')[-1], 'wb') as file:
                    file.write(response.content)

    for link in soup.findAll('link'):
        link_type = link.get('type')

        if link_type == 'text/css':
            link_url = link.get('href')

            if 'http' not in link_url:
                link_url = self.base_url + link_url

            response = self.session.get(link_url)
            if response.status_code == 200:
                with open(storage_path + link_url.split('/')[-1], 'wb') as file:
                    file.write(response.content)

    pass


def replace_url(self, old_element: BeautifulSoup):
    new_path = './assets/'

    new_element = BeautifulSoup('', 'xml')
    pass
