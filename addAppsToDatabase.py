from getGooglePlayData import *
import urllib2
import BeautifulSoup
import time
import pickle

def cycleThroughApps():
    """
    Gathers apps from Google Play via breadth-first searching.
    Gets info of each app and saves it to the database.
    Uses pickle to store the current tree level so the program will pick up from its last place.
    """
    current_level = pickle.load(open("current_level.p", "rb"))
    all_apps = current_level[:]
    start = time.time()

    while True:
        new_packages = []
        saved_level = current_level[:]
        for package_name in current_level:
            print '||||||||'+package_name
            response_text = urllib2.urlopen("https://play.google.com/store/apps/details?id="+package_name).read()
            tree = BeautifulSoup.BeautifulSoup(response_text)
            targets = tree.findAll(attrs={'class':"card-content id-track-click id-track-impression"})
            for target in targets:
                card_click_target = str(target.contents[1])
                package_name = card_click_target[card_click_target.find('href')+29:card_click_target.find('" aria')]
                if package_name not in all_apps:
                    new_packages.append(package_name)
                    all_apps.append(package_name)
                    info = get_google_play_info(package_name)
                    add_to_database(db, info, offer_update=False)
                    print package_name
            saved_level = saved_level[1:]
            pickle.dump(saved_level, open("current_level.p", "wb"))
        current_level = new_packages[:]
        pickle.dump(current_level, open("current_level.p", "wb"))
        print current_level

if __name__ == "__main__":
    cycleThroughApps()