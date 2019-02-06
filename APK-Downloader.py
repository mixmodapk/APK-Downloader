import requests
import os
try:
    from bs4 import BeautifulSoup
except ModuleNotFoundError:
    os.system('pip3 install bs4')

def main():
    GooglePlayLink = input('Insert a Google Play link or Package name (com.spotify.music or https://play.google.com/store/apps/details?id=)\n\033[32m> \033[m')

    def PackageName(GooglePlayLink): # For find Package Name from GooglePlay link - like "com.spotify.music"
        j = 0
        if GooglePlayLink[0:46] == "https://play.google.com/store/apps/details?id=": # If "GooglePlayLink" is a Link
            for i in GooglePlayLink:
                j += 1
                if i == '=':
                    if GooglePlayLink[-3] == '=':
                        return (GooglePlayLink[j:-6])
                    elif GooglePlayLink[-9] == '&':
                        return (GooglePlayLink[j:-9])
                    else:
                        return (GooglePlayLink[j:])
        elif ('.' in GooglePlayLink) == True: # If "GooglePlayLink" is a Package name
            return GooglePlayLink
        else:
            print('Your input not true.')
            return main()

    PackageName = PackageName(GooglePlayLink)

    def command_function():
        command = input('\n\n\nYou wants download this App/Game or show download link(D:download, S:show link, B:both): ')

        if command is 'd':
            os.system('wget -P APK %s' % downloadUrl['href'])
            print('\n\nYour App/Game has been downloaded and saved in \'APK\' folder.')
        elif command is 'D':
            os.system('wget -P APK %s' % downloadUrl['href'])
            print('\n\nYour App/Game has been downloaded and saved in \'APK\' folder.')

        elif command is 's':
            print('\n\n\nThat\'s your Link %s' % downloadUrl['href'])
        elif command is 'S':
            print('\n\n\nThat\'s your Link %s' % downloadUrl['href'])
            
        elif command is 'b':
            print('\n\n\nThat\'s your Link %s' % downloadUrl['href'])
            os.system('wget -P APK %s' % downloadUrl['href'])
            print('\n\n\nYour App/Game has been downloaded and saved in \'APK\' folder.')
        elif command is 'B':
            print('\n\n\nThat\'s your Link %s' % downloadUrl['href'])
            os.system('wget -P APK %s' % downloadUrl['href'])
            print('\n\n\nYour App/Game has been downloaded and saved in \'APK\' folder.')

        else:
            print('Wrong command.')
            return command_function()

    if PackageName is not None: # If "PackageName" function do not be return "None" value
        apkdl = 'https://apkdl.in/app/details?id=%s' % PackageName
        try:
            r = requests.get(apkdl)
            soup = BeautifulSoup(r.text, 'html.parser')

            downloadUrl = soup.find("a", itemprop='downloadUrl')

            # For find App/Game info
            print('info:\n\tName: '+soup.find('b').string)
            print('\tVersion: '+soup.find('span', itemprop='softwareVersion').string)
            print('\tUpdated on: '+soup.find('span', itemprop='dateModified').string)
            print('\tDownload size: '+soup.find('span', itemprop='fileSize').string)

            # For find App/Game Download Link
            downloadUrl = ('https://apkdl.in'+downloadUrl['href'])
            r = requests.get(downloadUrl)
            soup = BeautifulSoup(r.text, 'html.parser')
            downloadUrl = soup.find("a", rel='nofollow')
            command_function()


        except requests.exceptions.ConnectionError:
            print('No internet.\nCheck your network connection.')

        except TypeError:
            print('App/Game not found.')

if __name__ == "__main__":
    main()