# Coded by: Hamidreza Moradi
# www.github.com/hamidrezamoradi
import sys
import requests
from bs4 import BeautifulSoup
import shutil

################# colors #################
BLUE = "\033[1;34m"
GREEN = "\033[1;32m"
YELLOW = "\033[1;33m"
RED = "\033[1;31m"
CLOSE_COLOR = "\033[m"

##########################################


def verify_package_id(pakage_id):
    if "https://" in pakage_id or "http://" in pakage_id:
        return BeautifulSoup(requests.get(pakage_id).text, "html.parser").find(
            "meta", attrs={"name": "appstore:bundle_id"}
        )["content"]
    elif "." in pakage_id:
        return pakage_id
    else:
        print(f"\n{RED} [!] Your input not true.{CLOSE_COLOR}")
        return None


def download_file(url, output):
    with requests.get(url, stream=True) as r:
        with open(output, "wb") as f:
            shutil.copyfileobj(r.raw, f)


def apkdl_in(pakage_id):
    apkdl = "https://apkdl.in/app/details?id=%s" % pakage_id
    r = requests.get(apkdl)
    App_Page = BeautifulSoup(r.text, "html.parser")
    downloadUrl = App_Page.find("a", itemprop="downloadUrl")

    downloadUrl = "https://apkdl.in" + downloadUrl["href"]
    r = requests.get(downloadUrl)
    DownloadPage = BeautifulSoup(r.text, "html.parser")
    downloadUrl = DownloadPage.find("a", rel="nofollow")
    return downloadUrl


def apkplz_net(pakage_id):
    url = "https://apkplz.net/app/%s" % pakage_id
    r = requests.get(url)
    App_Page = BeautifulSoup(r.text, "html.parser")
    downloadUrl = App_Page.find("div", attrs={"class": "col-sm-12 col-md-12 text-center"})

    downloadUrl = downloadUrl.find("a", rel="nofollow")["href"]
    r = requests.get(downloadUrl)
    DownloadPage = BeautifulSoup(r.text, "html.parser")
    downloadUrl = DownloadPage.find("a", string="click here")
    return downloadUrl["href"]


def apktada_com(pakage_id):
    url = "https://apktada.com/download-apk/%s" % pakage_id
    r = requests.get(url)
    App_Page = BeautifulSoup(r.text, "html.parser")
    downloadUrl = App_Page.find("a", string="click here")
    return downloadUrl["href"]


def m_apkpure_com(pakage_id):
    url = "https://m.apkpure.com/android/%s/download?from=details" % pakage_id
    r = requests.get(url)
    App_Page = BeautifulSoup(r.text, "html.parser")
    downloadUrl = App_Page.find("a", string="click here")
    return downloadUrl["href"]


SERVICES = {
    "apkdl": apkdl_in,
    "apkplz": apkplz_net,
    "apktada": apktada_com,
    "apkpurl": m_apkpure_com,
}


def main():
    if len(sys.argv) != 2:
        print("USAGE APK-Downloader.py {com.bla.bla | https://play.google.com/...}")
        return
    pakage_id = sys.argv[1]
    for service_name, service_func in SERVICES.items():
        print(f"{GREEN} [*] trying with {service_name}{CLOSE_COLOR}")
        try:
            download_url = service_func(pakage_id)
            print(f"{GREEN} [*] got url: {download_url}{CLOSE_COLOR}")
            download_file(download_url, pakage_id + ".apk")
            print(f"\n{GREEN} [*] {pakage_id} was downloaded successfully. Enjoy :){CLOSE_COLOR}")
            break

        except requests.exceptions.ConnectionError:
            print(f"\n{RED} [!] No Connection.{CLOSE_COLOR}")
        except TypeError:
            print(f"\n{RED} [!] App/Game not found.\n [!] Try again later.{CLOSE_COLOR}")
        except Exception:
            print(f"\n{RED} [!] There's a problem.\n [!] Try another website.{CLOSE_COLOR}")


if __name__ == "__main__":
    main()
