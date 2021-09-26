
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# DataSet
# import pandas as pd


# configure driver
def configure_driver():

    # Add additional Options to the webdriver
    chrome_options = Options()
    # add the argument and make the browser Headless.
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)
    return driver


# Scroll page to overcome lazylist
def scroll_page(driver):
    previous_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == previous_height:
            break
        else:
            previous_height = new_height


# This Function will get all users followers
def get_user_followers(user):
    # start the driver
    driver = configure_driver()
    # Step 1: Go to user profile

    driver.get(f"https://soundcloud.com/{user}/followers")
    time.sleep(3)

    scroll_page(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Step 3: Iteracao das tabelas
    db_user_followers = {}
    for course_page in soup.select("div.badgeList"):
        for course in course_page.select("div.userBadgeListItem"):
            folower_div = "div.userBadgeListItem__title"
            folower_user = course.select_one(folower_div).text.strip()
            links = course.select_one(folower_div).find_all('a')
            folower_user_link = [x['href'] for x in links]
            db_user_followers["".join(folower_user_link)] = folower_user
    driver.close()
    return db_user_followers


def get_user_track_likes(track) -> dict:
    """
    This Function will get all users that liked specific track
    :param track: Track selected by the user
    :return: Followers that likes the track
    """
    driver = configure_driver()
    # Step 1: Go to user profile
    driver.get(f"https://soundcloud.com{track}/likes")
    time.sleep(3)

    scroll_page(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Step 3: Iteracao das tabelas
    db_track_likes = {}
    for course_page in soup.select("div.badgeList"):
        for course in course_page.select("div.userBadgeListItem"):
            likes_div = "div.userBadgeListItem__title"
            likes_user = course.select_one(likes_div).text.strip()
            links = course.select_one(likes_user).find_all('a')
            likes_user_link = [x['href'] for x in links]
            db_track_likes["".join(likes_user_link)] = likes_user
    driver.close()
    return db_track_likes


# Get track list of a specific user
def get_user_track_list(user):
    driver = configure_driver()
    # Step 1: Go to user profile
    driver.get(f"https://soundcloud.com/{user}/tracks")
    time.sleep(3)

    scroll_page(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Step 3: Iteracao das tabelas
    db_user_tracks = {}
    for course_page in soup.select("div.soundList"):
        for course in course_page.select("div.sound"):
            # Get Track URL
            folower_div = "div.soundTitle__usernameTitleContainer"
            track_links = course.select_one(folower_div).find_all('a')
            folower_user_link = [x['href'] for x in track_links]
            # Get Track Name
            track_name = course.select_one(folower_div).text.strip().split("\n")
            # Send to Dict
            db_user_tracks[folower_user_link[1]] = track_name[5]
        driver.close()
        return db_user_tracks


# Get all user that commented in a specific track
def get_track_comments(track):
    driver = configure_driver()
    # Step 1: Go to user profile
    driver.get(f"https://soundcloud.com{track}")
    time.sleep(3)

    scroll_page(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Step 3: Iteracao das tabelas
    db_comment_tracks = {}
    for course_page in soup.select("div.commentsList"):
        for course in course_page.select("div.commentItem"):
            # Get user comment name
            folower_div = "div.commentItem__content a"
            user_name = course.select_one(folower_div).text.strip()
            # Link do user do comment
            folower_div = "div.commentItem__content"
            track_links = course.select_one(folower_div).find_all('a')
            folower_user_link = [x['href'] for x in track_links]
            # Send to Dict
            if folower_user_link[0] in db_comment_tracks:
                strsplit = db_comment_tracks[folower_user_link[0]].find(",")
                db_comment_tracks[folower_user_link[0]] = str(
                    user_name + "," + str(int(db_comment_tracks[folower_user_link[0]][strsplit + 1:]) + 1))
            else:
                db_comment_tracks[folower_user_link[0]] = str(user_name + "," + "1")
        driver.close()
        return db_comment_tracks


# Get all users that reposted a specific track
def get_track_repost(track):
    driver = configure_driver()
    # Step 1: Go to user profile
    driver.get(f"https://soundcloud.com{track}/reposts")
    time.sleep(3)

    scroll_page(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Step 3: Iteracao das tabelas
    db_user_followers = {}
    for course_page in soup.select("div.badgeList"):
        for course in course_page.select("div.userBadgeListItem"):
            follower_div = "div.userBadgeListItem__title"
            follower_user = course.select_one(follower_div).text.strip()
            links = course.select_one(follower_div).find_all('a')
            folower_user_link = [x['href'] for x in links]
            db_user_followers["".join(folower_user_link)] = follower_user

    driver.close()
    return db_user_followers


#Get all tags of a specific track
def get_track_tags(track):
    driver = configure_driver()
    # Step 1: Go to user profile
    driver.get(f"https://soundcloud.com{track}")
    time.sleep(3)

    # ScrollPage(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Step 3: Iteracao das tabelas
    DB_info = {}
    for course in soup.select("div.soundTags"):
        # Get user comment name
        div = "div.sc-tag-group"
        try:
            Info = course.select_one(div).text.strip().replace("\n", ",")
            DB_info[track] = Info
        except:
            DB_info[track] = []
    driver.close()
    return DB_info


# Get the prevouly track reposted for a specific user
def get_user_track_reposted(user):
    driver = configure_driver()
    # Step 1: Go to user profile
    driver.get(f"https://soundcloud.com/{user}/reposts")
    time.sleep(3)

    scroll_page(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")
    # Step 3: Iteracao das tabelas
    DB_User_tracks = {}
    for course_page in soup.select("div.userReposts"):
        for course in course_page.select("div.userStreamItem"):
            # Get Time
            Folower_time = "time.relativeTime"
            Folower_CTime = course.select_one(Folower_time)["datetime"]
            # Get Track URL
            Folower_div = "div.soundTitle__usernameTitleContainer"
            track_links = course.select_one(Folower_div).find_all('a')
            Folower_User_link = [x['href'] for x in track_links]
            DB_User_tracks[Folower_User_link[2]] = Folower_CTime
    driver.close()
    return DB_User_tracks


# Get the prevouly track commented and the quantity of comments for a specific user
def get_user_last_comments(user):
    driver = configure_driver()
    # Step 1: Go to user profile
    driver.get(f"https://soundcloud.com/{user}/comments")
    time.sleep(3)

    scroll_page(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")
    # Step 3: Iteracao das tabelas
    DB_User_tracks = {}
    for course_page in soup.select("div.userNetwork"):
        for course in soup.select("div.commentBadge"):
            # Get Time
            Folower_time = "time.relativeTime"
            Folower_CTime = course.select_one(Folower_time)["datetime"]
            # Get Track Name
            Folower_div = "div.commentBadge__title"
            Folower_User = course.select_one(Folower_div).text.replace("on", "\n").strip()
            # Get Track link
            links = course.select_one(Folower_div).find_all('a')
            Folower_User_link = [x['href'] for x in links][0]
            if not Folower_User_link in DB_User_tracks:
                DB_User_tracks[Folower_User_link] = [1, Folower_CTime]
            else:
                DB_User_tracks[Folower_User_link][0] = DB_User_tracks[Folower_User_link][0] + 1
                DB_User_tracks[Folower_User_link].append(Folower_CTime)
    driver.close()
    return DB_User_tracks