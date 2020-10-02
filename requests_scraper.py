import requests
import requests.cookies
import os
from bs4 import BeautifulSoup


class RequestScraper:
    base_url = 'https://extranet.jiscd.sk'

    def __init__(self):
        url = 'https://extranet.jiscd.sk/portal/tool/2082f5b6-0ce9-418f-81e2-a3d301b14270/ShowPage?errorMessage' \
              '=&clearAttr=&newTopLevel=false&recheck=&itemId=6725&id=&addTool=-1&title=&source=&studentItemId=0' \
              '&backPath=push&sendingPage=6474&path=next&postedComment=false&returnView= '
        url2 = 'https://extranet.jiscd.sk/portal/tool/2082f5b6-0ce9-418f-81e2-a3d301b14270/ShowPage?errorMessage' \
               '=&clearAttr=&newTopLevel=false&recheck=&itemId=6725&id=&addTool=-1&title=&source=&studentItemId=0' \
               '&backPath=push&sendingPage=6474&path=next&postedComment=false&returnView= '
        cookies = 'BIGipServerprod_frontappext.jiscd-weblogic-usc=1696559114.23323.0000; ' \
                  '_ga=GA1.2.1793773393.1594991455; ' \
                  'BIGipServerprod_frontappext.jiscd-weblogic-e=1696559114.23323.0000; LastMRH_Session=cf4cd7b2; ' \
                  'F5_ST=1z1z1z1601456304z43200; MRHSession=3c3b270321a58402620fd3accf4cd7b2; ' \
                  'SAKAI_JSESSIONID=OWve9-F3Ichu0qSdtiji3pKYtyTv6fMV6n8JF6xjJqKjV-ddSPek!-996783959; ' \
                  '_WL_AUTHCOOKIE_SAKAI_JSESSIONID=dhk1PsUQ1bl0tdhm79PN; serverTime=1601468746399; ' \
                  'sessionExpiry=1601475646399; JSESSIONID=2ce82890-bd2e-4a9e-a361-0f0b41e9c367.sakaiext1a.jiscd '

        jar = requests.cookies.RequestsCookieJar()
        # jar.set('BIGipServerprod_frontappext.jiscd-weblogic-usc', '1696559114.23323.0000')
        # jar.set('_ga', 'GA1.2.1793773393.1594991455')
        jar.set('LastMRH_Session', 'df7863e2')
        # jar.set('F5_ST', '1z1z1z1601456304z43200')
        jar.set('MRHSession', '10e1bbf567e9467a66e7e9c4df7863e2')
        # jar.set('SAKAI_JSESSIONID', 'OWve9-F3Ichu0qSdtiji3pKYtyTv6fMV6n8JF6xjJqKjV-ddSPek!-996783959')
        jar.set('_WL_AUTHCOOKIE_SAKAI_JSESSIONID', 'Imis6AAIj1iY4cb4edt.')
        # jar.set('serverTime', '1601468746399')
        # jar.set('sessionExpiry', '1601475646399')
        jar.set('JSESSIONID', 'f91b3713-5119-468b-b3ee-af4f48bdf754.sakaiext1a.jiscd')
        jar.set('F5_ST', '1z1z1z1601531092z43200')

        print(jar)

        session = requests.Session()
        session.cookies = jar

        r = session.get(url=url)
        print(r)
        print(r.cookies)
        print(r.url)
        print(r.headers)
        print(r.text)
        # self.extract_images(session, r.text)
        self.extract_scripts(session, r.text)

        # str_as_bytes = str.encode(r.text)
        # f = open('jiscd.html', 'wb')
        # f.write(str_as_bytes)
        # f.close()

        # print(r.text)

    def extract_images(self, session, text):
        soup = BeautifulSoup(text, "html.parser")
        for link in soup.findAll('img'):
            image_url = link.get('src')
            print(image_url)
            response = session.get(image_url, stream=True)
            if response.status_code == 200:
                with open("/home/rastislav/PycharmProjects/drive_school_scraper/assets/" + image_url.split('/')[-1],
                          'wb') as file:
                    print(file)
                    file.write(response.content)

        pass

    def extract_scripts(self, session, text):
        soup = BeautifulSoup(text, "html.parser")

        for script in soup.findAll('script'):
            script_type = script.get('type')

            if script_type is not None and script_type == 'text/javascript' and script.get('src') is not None:
                script_url = script.get('src')

                print(script_url)

                if 'http' not in script_url:
                    script_url = self.base_url + script_url

                response = session.get(script_url)
                if response.status_code == 200:
                    with open("/home/rastislav/PycharmProjects/drive_school_scraper/assets/script/" +
                              script_url.split('/')[-1],
                              'wb') as file:
                        print(file)
                        file.write(response.content)

        for link in soup.findAll('link'):
            link_type = link.get('type')

            if link_type == 'text/css':
                link_url = link.get('href')

                print(link_url)

                if 'http' not in link_url:
                    link_url = self.base_url + link_url

                response = session.get(link_url)
                if response.status_code == 200:
                    with open("/home/rastislav/PycharmProjects/drive_school_scraper/assets/css/" + link_url.split('/')[
                        -1],
                              'wb') as file:
                        print(file)
                        file.write(response.content)

        pass
