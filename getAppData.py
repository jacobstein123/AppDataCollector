import splinter
import time
import zipfile
import binascii
import BeautifulSoup
import urllib2
import os

def download_apk(package_name, location): #C:\SSD-Folders\Google Drive (SSD)\Projects\AppDataGrabber\Testing\APKs
    """
    downloads the apk file to the specified folder
    """
    error_text = ['''Ops, we are not able to download. (invalid package/non-free/not compatible).''',
                  '''Ops, we are out of quota, please try others apps or try again in another hour''',
                  '''Please make sure package name or URL is valid''']
    pref = {"browser.helperApps.neverAsk.saveToDisk": "application/vnd.android.package-archive",
                "browser.download.folderList": 2,
                "browser.download.dir": location}
    br = splinter.Browser('firefox', profile_preferences=pref)
    br.visit("http://apps.evozi.com/apk-downloader/")
    br.find_by_id('packagename').first.fill(package_name)
    br.find_by_id('download_apk').first.click()
    down_button = br.find_by_id('download_apk_link').first
    for i in range(60):
        if down_button.visible:
            down_button.click()
            break
        else:
            for item in br.find_by_tag('p'):
                if item.visible and any(k in item.text for k in error_text):
                    print item.text
                    return False
        time.sleep(1)
    time.sleep(2)
    for i in range(60):    # timeout 2 min
        if not "{0}.apk.part".format(package_name) in os.listdir(location):
            break
        time.sleep(2)
    else:
        print 'TIMEOUT: Download took more than 2 minutes'
        return False
    return True

def get_signature(package_name, location):
    """
    returns the signature as a string
    """
    filename = "{0}\\{1}.apk".format(location,package_name)
    with open(filename,"rb") as f:
        z = zipfile.ZipFile(f)
        for n in z.namelist():
            if n.startswith('META-INF/') and ( n.endswith('.RSA') or n.endswith('.DSA') ):
                bytes = z.read(n).encode('hex').upper()
                signature = binascii.hexlify(z.read(n)).decode('utf-8').upper()
                return signature

def get_google_play_info(package_name):
    """
    returns a dictionary of the score, email, and downloads of the app
    """
    response_text = urllib2.urlopen("https://play.google.com/store/apps/details?id="+package_name).read()
    tree = BeautifulSoup.BeautifulSoup(response_text)
    score = float(tree.findAll(attrs={'class':'score'})[0].contents[0])
    email_results = tree.findAll(attrs={'class':'dev-link'})
    a=str(email_results[-1])
    email = a[a.find("mailto:")+7:a.find("rel")-2]
    downloads = str(tree.findAll(attrs={'itemprop':'numDownloads'})[0].contents[0])
    return {'score':score, 'email':email, 'downloads':downloads}

def main():
    LOCATION = str("C:\\SSD-Folders\\Google Drive (SSD)\\Projects\\AppDataGrabber\\Testing\\APKs")
    PACKAGE_NAME = raw_input('Enter package name: ')

    success = download_apk(PACKAGE_NAME, LOCATION)
    if success:
        print get_signature(PACKAGE_NAME, LOCATION)
        print get_google_play_info(PACKAGE_NAME)

if __name__ == "__main__":
    main()
