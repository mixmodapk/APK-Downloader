# Coded by: Hamidreza Moradi
# www.github.com/hamidrezamoradi
import sys
import re
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
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"

EVOZI_HEADERS = {
    "User-Agent": USER_AGENT,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://apps.evozi.com",
    "Connection": "keep-alive",
    "Referer": "https://apps.evozi.com/apk-downloader/",
}


def verify_package_id(package_id):
    if "https://" in package_id or "http://" in package_id:
        return BeautifulSoup(
            requests.get(package_id, headers={"User-Agent": USER_AGENT}).text,
            "html.parser",
        ).find("meta", attrs={"name": "appstore:bundle_id"})["content"]
    elif "." in package_id:
        return package_id
    else:
        print(f"\n{RED} [!] Your input not true.{CLOSE_COLOR}")
        return None


def download_file(url, output):
    with requests.get(url, headers={"User-Agent": USER_AGENT}, stream=True) as r:
        with open(output, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    return True


def apkdl_in(package_id):
    apkdl = "https://apkdl.in/app/details?id=%s" % package_id
    r = requests.get(apkdl)
    App_Page = BeautifulSoup(r.text, "html.parser")
    downloadUrl = App_Page.find("a", itemprop="downloadUrl")

    downloadUrl = "https://apkdl.in" + downloadUrl["href"]
    r = requests.get(downloadUrl, headers={"User-Agent": USER_AGENT})
    DownloadPage = BeautifulSoup(r.text, "html.parser")
    downloadUrl = DownloadPage.find("a", rel="nofollow")
    return downloadUrl["href"]


def apkplz_net(package_id):
    url = "https://apkplz.net/app/%s" % package_id
    r = requests.get(url)
    App_Page = BeautifulSoup(r.text, "html.parser")
    downloadUrl = App_Page.find(
        "div", attrs={"class": "col-sm-12 col-md-12 text-center"}
    )

    downloadUrl = downloadUrl.find("a", rel="nofollow")["href"]
    r = requests.get(downloadUrl, headers={"User-Agent": USER_AGENT})
    DownloadPage = BeautifulSoup(r.text, "html.parser")
    downloadUrl = DownloadPage.find("a", string="click here")
    return downloadUrl["href"]


def apktada_com(package_id):
    url = "https://apktada.com/download-apk/%s" % package_id
    r = requests.get(url, headers={"User-Agent": USER_AGENT})
    App_Page = BeautifulSoup(r.text, "html.parser")
    downloadUrl = App_Page.find("a", string="click here")
    return downloadUrl["href"]


def m_apkpure_com(package_id):
    url = "https://m.apkpure.com/android/%s/download?from=details" % package_id
    r = requests.get(url, headers={"User-Agent": USER_AGENT})
    App_Page = BeautifulSoup(r.text, "html.parser")
    downloadUrl = App_Page.find("a", string="click here")
    return downloadUrl["href"]


def apkcombo_com(package_id):
    url = "https://apkcombo.com/apk-downloader/?format=apk&package=%s" % package_id
    r = requests.get(url, headers={"User-Agent": USER_AGENT})
    App_Page = BeautifulSoup(r.text, "html.parser")
    downloadUrl = App_Page.select_one(r"a[href*=apkcombo\.com\.apk]")
    return downloadUrl["href"]


def apkdl_com(package_id):
    url = "https://apk-dl.com/search?q=%s" % package_id
    r = requests.get(url, headers={"User-Agent": USER_AGENT})
    downloadUrl = re.search('"downloadUrl" : "(.*?)"', r.text).groups()[0]
    return downloadUrl + "&dl=2"


# from https://github.com/jayluxferro/APK-Downloader
def evozi_com(package_id):
    web_data = requests.get("https://apps.evozi.com/apk-downloader")
    if web_data.status_code == 200:
        res = web_data.text.splitlines()
        token1 = res[195].strip().split(":")[1].strip().split(",")[0]
        token2 = (
            res[164].strip().split("=")[-1].strip().replace("'", "").replace(";", "")
        )
        token3 = (
            res[195]
            .strip()
            .split("=")[-1]
            .strip()
            .replace(" ", "")
            .strip("{")
            .split(",")[:-1]
        )

        payload = {}
        payload[token3[0].split(":")[0]] = token1
        payload[token3[1].split(":")[0]] = package_id
        payload[token3[2].split(":")[0]] = token2
        payload["fetch"] = False

        res = requests.post(
            "https://api-apk.evozi.com/download", data=payload, headers=EVOZI_HEADERS
        )
        res = res.json()
        return "https:{}".format(res["url"])


SERVICES = (
    ("apkdl-com", apkdl_com),
    ("apkcombo", apkcombo_com),
    ("evozi", evozi_com),
    ("apkdl-in", apkdl_in),
    ("apktada", apktada_com),
    ("apkplz", apkplz_net),
    ("apkpurl", m_apkpure_com),
)


def main():
    if len(sys.argv) != 2:
        print("USAGE APK-Downloader.py {com.bla.bla | https://play.google.com/...}")
        return
    package_id = sys.argv[1]
    for service_name, service_func in SERVICES:
        print(f"{GREEN} [*] trying with {service_name}{CLOSE_COLOR}")
        try:
            download_url = service_func(package_id)
            print(f"{GREEN} [*] got url: {download_url}{CLOSE_COLOR}")
            download_file(download_url, package_id + ".apk")
            print(
                f"\n{GREEN} [*] {package_id} was downloaded successfully. Enjoy :){CLOSE_COLOR}"
            )
            break

        except requests.exceptions.ConnectionError:
            print(f"\n{RED} [!] No Connection.{CLOSE_COLOR}")
        except TypeError:
            print(
                f"\n{RED} [!] App/Game not found.\n [!] Try again later.{CLOSE_COLOR}"
            )
        except Exception:
            print(
                f"\n{RED} [!] There's a problem.\n [!] Try another website.{CLOSE_COLOR}"
            )


if __name__ == "__main__":
    main()
