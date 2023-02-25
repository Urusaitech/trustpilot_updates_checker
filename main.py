import datetime
import re
import time
import logging
from pathlib import Path
# from typing import Callable
import requests
import random
from bs4 import BeautifulSoup as bs
from tg_notifyer import main as tg_notice
from configs import *

logging.basicConfig(
    level=logging.DEBUG,
    filename="trust_log.log",
    filemode="a",
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def update_reviews_list() -> list:
    """
    create list of the recent reviews on the first page
    :return: list of reviews
    """
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    all_links = soup.findAll(href=re.compile("reviews"))
    reviews = []

    for i in all_links:
        href = i.get("href")
        if str(href).startswith("/reviews"):
            reviews.append(href)
    logging.debug("update_reviews_list")
    return reviews


def get_review_text(tr_response: requests.Response) -> list:
    """
    finds text of a given review
    :param tr_response: http response
    :return: list
    """
    new_soup = bs(tr_response.text, "html.parser")
    review = new_soup.findAll("p")
    pointer_text = 'data-service-review-text-typography="true">'
    pointer_index = str(review).find(pointer_text)
    review_text = str(review)[pointer_index + len(pointer_text):]
    print(review_text.split("<br/>"))
    logging.debug("get_reviews_text")
    return review_text.split("<br/>")


def collect_reviews(reviews: list) -> None:
    """
    collects all recent reviews on the first page
    :return:
    """
    for i in reviews:
        tr_response = requests.get("https://www.trustpilot.com" + i)
        print(tr_response.url)
        get_review_text(tr_response)
    logging.debug("collect_reviews")


def save_reviews_to_file(reviews: list) -> None:
    """
    save reviews to file
    :param reviews:
    :return:
    """
    with open("trust_reviews.txt", "w") as file:
        file.write("\n".join(reviews))
    print("saved")
    logging.debug("save_reviews_to_file")


def cycle() -> bool or None:
    """
    Runs checks and updates
    :return: False if interrupted, else keeps on working
    """
    while True:
        try:
            new_reviews = update_reviews_list()
            reviews_list = []
            with open("trust_reviews.txt", "r") as f:
                logging.debug("reading from local file")
                # collect reviews from file
                for line in f.readlines():
                    if "\n" in line:
                        reviews_list.append(line[:-1])
                    else:
                        reviews_list.append(line)

                if new_reviews == reviews_list:
                    print("no new reviews")
                    logging.debug("no new reviews")
                else:
                    print("an updated detected")
                    logging.debug("an update detected")

                    if tg_notify:
                        tg_notice()

                    save_reviews_to_file(new_reviews)
            # random retry time to reduce chance of being ip-blocked
            rand = random.randint(60, timeout)
            now = time.strftime("%m-%d %H:%M:%S", time.gmtime())
            print(f"{now}: sleeping for {('{:.2f}'.format(round(rand/60, 2)))} minutes")
            logging.info(f"sleeping for {('{:.2f}'.format(round(rand/60, 2)))} minutes")
            time.sleep(rand)
        # BaseException seem to cause the script stuck in some cases, gotta test
        except BaseException as e:
            print(f"interrupted: {e}")
            logging.debug(f"interrupted {e}")
            return False


if __name__ == "__main__":
    logging.debug("starting")
    reviews_path = Path("trust_reviews.txt")

    try:
        # check if the reviews list exists
        my_abs_path = reviews_path.resolve(strict=True)
        logging.debug("File exists, skipping update")
        print("File exists, skipping update")
    except FileNotFoundError:
        print('Reviews file not found in current directory')
        if update_reviews_txt:
            save_reviews_to_file(update_reviews_list())
    cycle()
