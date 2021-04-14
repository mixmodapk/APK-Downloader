# Coded by: Hamidreza Moradi
# www.github.com/hamidrezamoradi 

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

################# colors #################
BLUE = '\033[1;34m'
GREEN = '\033[1;32m'
YELLOW = '\033[1;33m'
RED = '\033[1;31m'

RED_BG = '\033[1;77m\033[41m'

CLOSE_COLOR = '\033[m'
##########################################

print(f'''{GREEN}
     ___    ____  __ __ ____                      __                __         
    /   |  / __ \/ //_// __ \____ _      ______  / /___  ____ _____/ /__  _____
   / /| | / /_/ / ,<  / / / / __ \ | /| / / __ \/ / __ \/ __ `/ __  / _ \/ ___/
  / ___ |/ ____/ /| |/ /_/ / /_/ / |/ |/ / / / / / /_/ / /_/ / /_/ /  __/ /    
 /_/  |_/_/   /_/ |_/_____/\____/|__/|__/_/ /_/_/\____/\__,_/\__,_/\___/_/     

 {RED_BG}      Google Play  Downloader  v2.0,  Author:  @HamidrezaMoradi  (Github)     {CLOSE_COLOR}\n
''')

try:
    def details(GP_input):
        if 'https://' in GP_input or 'http://' in GP_input:
            pakage_id = BeautifulSoup(requests.get(GP_input).text, 'html.parser').find("meta", attrs={'name': 'appstore:bundle_id'})['content']
            return pakage_id 
        elif '.' in GP_input:
            return GP_input
        else:
            print(f'\n{RED} [!] Your input not true.{CLOSE_COLOR}')
            return None    

    def downloader(downloadURL, name):
        try:
            r_downloadURL = requests.get(downloadURL, stream=True)

            with open('File/' + name + '.apk', "wb") as handle:
                for data in tqdm(r_downloadURL.iter_content()):
                    handle.write(data)
            return True
        except Exception:
            return False
        
    def continue_statement():
        statement = input(f'{GREEN} [*] Have you any other requests?([Y]es or [N]):\n {YELLOW}> {CLOSE_COLOR}')
        if statement.lower() == 'yes' or statement.lower() == 'y':
            return True
        elif statement.lower() == 'no' or statement.lower() == 'n':
            return False
        else:
            return continue_statement()

    class Services:
        @staticmethod
        def apkdl_in(pakage_id):
            apkdl = 'https://apkdl.in/app/details?id=%s' % pakage_id
            r = requests.get(apkdl)
            App_Page = BeautifulSoup(r.text, 'html.parser')
            downloadUrl = App_Page.find("a", itemprop='downloadUrl')

            downloadUrl = 'https://apkdl.in'+downloadUrl['href']
            r = requests.get(downloadUrl)
            DownloadPage = BeautifulSoup(r.text, 'html.parser')
            downloadUrl = DownloadPage.find("a", rel='nofollow')
            return downloadUrl

        @staticmethod
        def apkplz_net(pakage_id):
            url = 'https://apkplz.net/app/%s' % pakage_id
            r = requests.get(url)
            App_Page = BeautifulSoup(r.text, 'html.parser')
            downloadUrl = App_Page.find("div", attrs={'class':'col-sm-12 col-md-12 text-center'})

            downloadUrl = downloadUrl.find("a", rel='nofollow')['href']
            r = requests.get(downloadUrl)
            DownloadPage = BeautifulSoup(r.text, 'html.parser')
            downloadUrl = DownloadPage.find("a", string='click here')
            return downloadUrl['href']

        @staticmethod
        def apktada_com(pakage_id):
            url = 'https://apktada.com/download-apk/%s' % pakage_id
            r = requests.get(url)
            App_Page = BeautifulSoup(r.text, 'html.parser')
            downloadUrl = App_Page.find("a", string='click here')
            return downloadUrl['href']

        @staticmethod
        def m_apkpure_com(pakage_id):
            url = 'https://m.apkpure.com/android/%s/download?from=details' % pakage_id
            r = requests.get(url)
            App_Page = BeautifulSoup(r.text, 'html.parser')
            downloadUrl = App_Page.find("a", string='click here')
            return downloadUrl['href']

    if __name__ == "__main__":
        while True:
            GP_input = input(f'{GREEN} [*] Enter a \"Google Play URL\" or \"APP Code\":\n {YELLOW}> {CLOSE_COLOR}')
            pakage_id = details(GP_input)
            service_number = input(f'\n{GREEN} [*] Select one among the following sites:\n 1. apkdl.in\n 2. apkplz.net\n 3. apktada.com\n 4. m.apkpure.com\n {YELLOW}> {CLOSE_COLOR}')
            if service_number == '1':
                download_URL = Services.apkdl_in(pakage_id)
            elif service_number == '2':
                download_URL = Services.apkplz_net(pakage_id)
            elif service_number == '3':
                download_URL = Services.apktada_com(pakage_id)
            elif service_number == '4':
                download_URL = Services.m_apkpure_com(pakage_id)
            else:
                print(f'\n{RED} [!] The entry is not correct.\n Please choose between one of the top websites!{CLOSE_COLOR}')
                statement = continue_statement()
                if statement: continue
                else: break

            if downloader(download_URL, pakage_id):
                print(f'\n{GREEN} [*] The download successfully performed and stored in the "file" folder. Enjoy :){CLOSE_COLOR}')
                statement = continue_statement()
                if statement: continue
                else: break
            else:
                print(f'\n{GREEN} [!] There is a problem for download.{CLOSE_COLOR}')
                statement = continue_statement()
                if statement: continue
                else: break

except requests.exceptions.ConnectionError:
    print(f'\n{RED} [!] No Connection.{CLOSE_COLOR}')
except TypeError:
    print(f'\n{RED} [!] App/Game not found.\n [!] Try again later.{CLOSE_COLOR}')
except:
    print(f'\n{RED} [!] There\'s a problem.\n [!] Try another website.{CLOSE_COLOR}')
