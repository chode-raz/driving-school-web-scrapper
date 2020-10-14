import requests
import os
from bs4 import BeautifulSoup
import requests.cookies
import re
import fileinput


class ScrapIt:
    base_url = 'https://extranet.jiscd.sk'

    assets_path = '/assets/'
    pages_path = '/download/'

    forbidden_urls = ['',
                      'https://public.test2.jiscd/portal/tool/8ffcfe76-ea9f-49c7-937e-e2bcca6ea426/ShowPage?errorMessage=&clearAttr=&newTopLevel=false&recheck=&itemId=2144&id=&addTool=-1&title=&source=&studentItemId=0&backPath=&sendingPage=2143&path=&postedComment=false&returnView='
                      ]

    def __init__(self):
        jar = requests.cookies.RequestsCookieJar()
        jar.set('LastMRH_Session', '93a79448')
        jar.set('MRHSession', 'd42d8987e6e895c6629ca39b93a79448')
        jar.set('_WL_AUTHCOOKIE_SAKAI_JSESSIONID', 'Ws9Oy94KIc.U9Tg6Tv4j')
        jar.set('JSESSIONID', 'fdce9aae-4a90-4052-ad07-b41496bc2616.sakaiext1a.jiscd')
        jar.set('F5_ST', '1z1z1z1602604338z43200')

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
            title = ""
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
                    if url is not None and url not in self.forbidden_urls:
                        if not os.path.exists(file_path):
                            i += 1
                            self.create_dir(dir_path)
                            self.get_page(url, file_path)
                        self.get_page_assets(file_path, dir_path)

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
        self.create_dir(path + self.assets_path)
        pass

    def get_page_assets(self, page_path, dir_path):
        self.create_assets_folder(dir_path)

        with open(page_path, 'r+') as page_file:
            page = page_file.read()
        page_file.close()

        soup = BeautifulSoup(page, "html.parser")

        for link in soup.findAll('img'):
            image_url = link.get('src')
            image_name = image_url.split('/')[-1]
            new_path = dir_path + self.assets_path + image_name
            relative_path = '.' + self.assets_path + image_name
            link['src'] = relative_path

            if 'http' not in image_url:
                image_url = self.base_url + image_url

            response = self.session.get(image_url, stream=True)
            if response.status_code == 200:
                with open(new_path, 'wb') as file:
                    file.write(response.content)
                file.close()

        for script in soup.findAll('script'):
            script_type = script.get('type')

            if script_type is not None and script_type == 'text/javascript' and script.get('src') is not None:
                script_url = script.get('src')
                script_name = script_url.split('/')[-1]
                new_path = dir_path + self.assets_path + script_name
                relative_path = '.' + self.assets_path + script_name
                script['src'] = relative_path

                if 'http' not in script_url:
                    script_url = self.base_url + script_url

                response = self.session.get(script_url)
                if response.status_code == 200:
                    with open(new_path, 'wb') as file:
                        file.write(response.content)
                    file.close()

        for link in soup.findAll('link'):
            link_type = link.get('type')

            if link_type == 'text/css':
                link_url = link.get('href')

                if 'http' not in link_url:
                    link_url = self.base_url + link_url

                link_name = link_url.split('/')[-1]
                new_path = dir_path + self.assets_path + link_name
                relative_path = '.' + self.assets_path + link_name
                link['href'] = relative_path

                response = self.session.get(link_url)
                if response.status_code == 200:
                    with open(new_path, 'wb') as file:
                        file.write(response.content)
                    file.close()

        with open(page_path, 'w') as page_file:
            page_file.write(str(soup))
        page_file.close()

        pass
