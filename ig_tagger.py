from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from configparser import ConfigParser
from datetime import datetime

import signal
import time
import random
import platform
import os.path


LOGIN_XPATH = '//*[@id="loginForm"]/div/div[3]/button'
USERNAME_XPATH = '//*[@id="loginForm"]/div/div[1]/div/label/input'
PASS_XPATH = '//*[@id="loginForm"]/div/div[2]/div/label/input'
COMMENT_XPATH = '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[3]/div/form/textarea'
POST_XPATH = '//*[@id="react-root"]/section/main/div/div[1]/article/div[3]/section[3]/div/form/button'


def choose_names_to_tag(ig_names, required_tags):
    tags = []

    while len(tags) < int(required_tags):
        name = random.choice(ig_names)

        if name not in tags:
            tags.append(name)

    return tags

def signal_handler(*args):
    print("\n\nTotal tags made:\t {}".format(number_of_tags))
    exit(0)


if __name__ == "__main__":

    number_of_tags = 0
    signal.signal(signal.SIGINT, signal_handler)

    parser = ConfigParser()
    parser.read('config.ini', encoding='utf8')

    contest_url = parser.get('Instagram', 'Contest')
    ig_names = parser.get('Instagram', 'Names').replace('\n', '').split(',')
    required_tags = parser.get('Instagram', 'Tags')
    username = parser.get('Instagram', 'Username')
    password = parser.get('Instagram', 'Password')

    if platform.system() == 'Linux':
        chromedriver_path = parser.get('Selenium', 'Linux_Driver_Path')
    elif platform.system() == 'Windows':
        chromedriver_path = parser.get('Selenium', 'Win_Driver_Path')
    else:
        print("OS not supported. Please run this script in Linux or Windows system.")

    chrome = webdriver.Chrome(executable_path=chromedriver_path)
    chrome.get("https://www.instagram.com")

    WebDriverWait(chrome, 15).until(EC.presence_of_element_located((By.XPATH, USERNAME_XPATH)))

    username_input = chrome.find_element_by_xpath(USERNAME_XPATH)
    password_input = chrome.find_element_by_xpath(PASS_XPATH)
    login_button = chrome.find_element_by_xpath(LOGIN_XPATH)

    username_input.send_keys(username)
    password_input.send_keys(password)

    time.sleep(1)

    login_button.click()

    time.sleep(3)

    chrome.get(contest_url)

    while True:
        names = choose_names_to_tag(ig_names, required_tags)

        comment_input = chrome.find_element_by_xpath(COMMENT_XPATH)
        comment_input.click()
        comment_input = chrome.find_element_by_xpath(COMMENT_XPATH)
        
        comment = ""
        for name in names:
            comment += "{} ".format(name)

        comment_input.send_keys(comment)
        post_button = chrome.find_element_by_xpath(POST_XPATH)
        post_button.click()

        time.sleep(2)

        waiting_to_unblock = True

        while waiting_to_unblock:
            try:
                # if element is present then IG blocked comments
                chrome.find_element_by_class_name("HGN2m")

                print("blocked")

                # wait 1 min before commenting again
                time.sleep(60)
                post_button = chrome.find_element_by_xpath(POST_XPATH).click()
                time.sleep(2)
            except:
                waiting_to_unblock = False
                number_of_tags += 1

                # set a random waiting time to mess with IG algorithm
                seconds_to_wait = random.randint(1,60)
                print("Waiting for {} seconds".format(seconds_to_wait))
                time.sleep(seconds_to_wait)
