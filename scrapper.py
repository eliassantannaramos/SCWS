from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# DataSet
# import pandas as pd


# configure driver
def configure_driver():
    """
    This will configure the driver to connect with the selected page.
    :return:
    """
    # Add additional Options to the webdriver
    chrome_options = Options()
    # add the argument and make the browser Headless.
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=os.path.join(BASE_PATH, "chromedriver.exe"), options=chrome_options)
    return driver


def scroll_page(driver):
    """
    This will scroll down the page in order to activated the lazy list.
    :param driver: Driver to create the page that will be scrapped
    :return:
    """
    previous_height = driver.execute_script('return document.body.scrollHeight')
    while True:
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        new_height = driver.execute_script('return document.body.scrollHeight')
        if new_height == previous_height:
            break
        else:
            previous_height = new_height


def get_user_followers(user) -> dict:
    """
    Get all followers of the user
    :param user: Name of the user
    :return: List of all followers of the user.
    """
    # start the driver
    driver = configure_driver()
    # Step 1: Go to user profile

    driver.get(f"https://soundcloud.com/{user}/followers")
    time.sleep(1)

    scroll_page(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Step 3: Iterate the tables
    db_user_followers = {}
    for course_page in soup.select("div.badgeList"):
        for course in course_page.select("div.userBadgeListItem"):
            follower_div = "div.userBadgeListItem__title"
            follower_user = course.select_one(follower_div).text.strip()
            links = course.select_one(follower_div).find_all('a')
            follower_user_link = [x['href'] for x in links]
            db_user_followers["".join(follower_user_link)] = follower_user
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
    time.sleep(1)

    scroll_page(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Step 3: Iterate the tables
    db_track_likes = {}
    for course_page in soup.select("div.badgeList"):
        for course in course_page.select("div.userBadgeListItem"):
            likes_div = "div.userBadgeListItem__title"
            likes_user = course.select_one(likes_div).text.strip()
            links = course.select_one(likes_div).find_all('a')
            likes_user_link = [x['href'] for x in links]
            db_track_likes["".join(likes_user_link)] = likes_user
    driver.close()
    return db_track_likes


def get_user_track_list(user) -> dict:
    """
    Get a list of tracks produced by the user
    :param user: Name of the user
    :return: List of all tracks produced by the user
    """
    driver = configure_driver()
    # Step 1: Go to user profile
    driver.get(f"https://soundcloud.com/{user}/tracks")
    time.sleep(1)

    scroll_page(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Step 3: Iterate the tables
    db_user_tracks = {}
    for course_page in soup.select("div.soundList"):
        for course in course_page.select("div.sound"):
            # Get Track URL
            follower_div = "div.soundTitle__usernameTitleContainer"
            track_links = course.select_one(follower_div).find_all('a')
            follower_user_link = [x['href'] for x in track_links]
            # Get Track Name
            track_name = course.select_one(follower_div).text.strip().split("\n")
            # Send to Dict
            db_user_tracks[follower_user_link[1]] = track_name[5]
        driver.close()
    return db_user_tracks


def get_track_comments(track) -> dict:
    """
    This function will return a list of user that commented the track
    :param track: Link of the track
    :return: List of users that commented the selected track
    """
    driver = configure_driver()
    # Step 1: Go to user profile
    driver.get(f"https://soundcloud.com{track}")
    time.sleep(1)

    scroll_page(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Step 3: Iterate the tables
    db_comment_tracks = {}
    for course_page in soup.select("div.commentsList"):
        for course in course_page.select("div.commentItem"):
            # Get user comment name
            follower_div = "div.commentItem__content a"
            user_name = course.select_one(follower_div).text.strip()
            # Link do user do comment
            follower_div = "div.commentItem__content"
            track_links = course.select_one(follower_div).find_all('a')
            follower_user_link = [x['href'] for x in track_links]
            # Send to Dict
            if follower_user_link[0] in db_comment_tracks:
                str_split = db_comment_tracks[follower_user_link[0]].find(",")
                db_comment_tracks[follower_user_link[0]] = str(
                    user_name + "," + str(int(db_comment_tracks[follower_user_link[0]][str_split + 1:]) + 1))
            else:
                db_comment_tracks[follower_user_link[0]] = str(user_name + "," + "1")
        driver.close()
        return db_comment_tracks


def get_track_repost(track) -> dict:
    """
    This function will return a list of user that reposted the track
    :param track: Link of the track
    :return: List of users that reposted the selected track
    """
    driver = configure_driver()
    # Step 1: Go to user profile
    driver.get(f"https://soundcloud.com{track}/reposts")
    time.sleep(1)

    scroll_page(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Step 3: Iterate the tables
    db_user_followers = {}
    for course_page in soup.select("div.badgeList"):
        for course in course_page.select("div.userBadgeListItem"):
            follower_div = "div.userBadgeListItem__title"
            follower_user = course.select_one(follower_div).text.strip()
            links = course.select_one(follower_div).find_all('a')
            follower_user_link = [x['href'] for x in links]
            db_user_followers["".join(follower_user_link)] = follower_user

    driver.close()
    return db_user_followers


def get_track_tags(track) -> dict:
    """
    Get all tags of an specific track
    :param track: Link of the track
    :return: List of Tags of the track
    """
    driver = configure_driver()
    # Step 1: Go to user profile
    driver.get(f"https://soundcloud.com{track}")
    time.sleep(1)

    # ScrollPage(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")

    # Step 3: Iterate the tables
    db_info = {}
    for course in soup.select("div.soundTags"):
        # Get user comment name
        div = "div.sc-tag-group"
        try:
            info = course.select_one(div).text.strip().replace("\n", ",")
            db_info[track] = info
        except:
            db_info[track] = []
    driver.close()
    return db_info


def get_user_track_reposted(user) -> dict:
    """
    Get all track reposted by an specific user
    :param user: link of the user
    :return: List of tracks reposted by the user
    """
    driver = configure_driver()
    # Step 1: Go to user profile
    driver.get(f"https://soundcloud.com/{user}/reposts")
    time.sleep(1)

    scroll_page(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")
    # Step 3: Iterate the tables
    db_user_tracks = {}
    for course_page in soup.select("div.userReposts"):
        for course in course_page.select("div.userStreamItem"):
            # Get Time
            follower_time = "time.relativeTime"
            follower_c_time = course.select_one(follower_time)["datetime"]
            # Get Track URL
            follower_div = "div.soundTitle__usernameTitleContainer"
            track_links = course.select_one(follower_div).find_all('a')
            follower_user_link = [x['href'] for x in track_links]
            db_user_tracks[follower_user_link[2]] = follower_c_time
    driver.close()
    return db_user_tracks


def get_user_last_comments(user) -> dict:
    """
    Get the previously tracks commented and the quantity of comments for a specific user
    :param user: Link of the user
    :return: List of tracks commented
    """
    driver = configure_driver()
    # Step 1: Go to user profile
    driver.get(f"https://soundcloud.com/{user}/comments")
    time.sleep(1)

    scroll_page(driver)

    # Step 2: Create a parse tree of page sources after searching
    soup = BeautifulSoup(driver.page_source, "lxml")
    # Step 3: Iterate the tables
    db_user_tracks = {}
    for course_page in soup.select("div.userNetwork"):
        for course in course_page.select("div.commentBadge"):
            # Get Time
            follower_time = "time.relativeTime"
            follower_c_time = course.select_one(follower_time)["datetime"]
            # Get Track Name
            follower_div = "div.commentBadge__title"
            # Get Track link
            links = course.select_one(follower_div).find_all('a')
            follower_user_link = [x['href'] for x in links][0]
            if not follower_user_link in db_user_tracks:
                db_user_tracks[follower_user_link] = [1, follower_c_time]
            else:
                db_user_tracks[follower_user_link][0] = db_user_tracks[follower_user_link][0] + 1
                db_user_tracks[follower_user_link].append(follower_c_time)
    driver.close()

    return db_user_tracks
