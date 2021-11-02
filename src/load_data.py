# -*- coding: utf-8 -*-
"""Module to retrieve Predd Briefings from the sciencemediacenter.de website. All urls to 
the pdfs are extracted through the pressbriefing sites from the overview website. The pdfs 
are downloaded and saved to a specified directory.

Todo:
    * Functions should be changed to single url level and not list of urls
    * URL parsing should be improved to be more robust and retrieve more urls
"""

import os
import random
import re
import time
from typing import Dict, List, Set

import requests
from bs4 import BeautifulSoup  # type: ignore

from config import DEBUG

BASE_URL = "https://www.sciencemediacenter.de"
PATTERN = re.compile(r"Transkript")  # search pattern for the <p> containing the url


def extrect_all_pressbriefing_links() -> List[str]:
    """Retrieve all links to pressbriefing sites from the SMC site.

    Returns:
        List[str]: List of unique links.
    """

    def _extrect_mac_pages() -> int:
        """Extract the maximum number of pressbriefing pages from html.

        Returns:
            int: Maximum number of pressbriefing pages
        """
        responds = requests.get("https://www.sciencemediacenter.de/alle-angebote/press-briefing/")
        bs = BeautifulSoup(responds.content, "html.parser")
        num_pages_str = bs.find(class_="last page-item").text
        num_pages = int(re.findall(r"\d+", num_pages_str)[0])
        return num_pages

    page = 1
    url = "https://www.sciencemediacenter.de/alle-angebote/press-briefing/?tx_news_pi1%5B%40widget_0%5D%5BcurrentPage%5D={}&cHash=1af09de0bd1dee82e5c45c74c125b7cd#tab_c235"
    links: list[str] = []

    responds = requests.get(url)
    while page <= _extrect_mac_pages():
        page += 1
        responds = requests.get(url.format(page))
        time.sleep(random.randint(1, 7))  # random sleep
        bs = BeautifulSoup(responds.content, "html.parser")
        for link in bs.find_all(class_="m-news-list__link"):
            pdf_url = BASE_URL + link["href"]
            links.append(pdf_url)
        if DEBUG:
            print(f"On page {str(page)} right now.")
            print(str(len(links)), "collected.")

    return list(set(links))


def extrect_introduction(bs: BeautifulSoup) -> str:
    """Extract the introduction text from the HTML site.

    Args:
        bs (BeautifulSoup): Beautifullsoup object.

    Returns:
        str: Introduction text for the pressbriefing.
    """
    introduction = str()
    p = bs.find_all("p")
    for paragraph in p:
        introduction += paragraph.text + "\n"
    return introduction


def extrect_pdf_url(bs: BeautifulSoup) -> str:
    """Extrect the URL for the transcribt pdf from the HTML site.

    Args:
        bs (BeautifulSoup): Beautifullsoup object.

    Returns:
        str: URL to transcript pdf.
    """
    p = bs.find_all("p")
    pdf_url = str()
    for i in p:
        candidate = PATTERN.search(i.text)
        if candidate:
            try:
                pdf_url = i.find("a")["href"]  # try to get an <a> from the <p>
            except:
                print("no a")
    return pdf_url


def extrect_all_pdf_urls(press_briefing_links: list[str]) -> list[str]:
    """DEPRECATED: Get the pdf URLs from the PressBriefing pages.

    Args:
        press_briefing_links (list[str]): List with PressBriefing pages.

    Returns:
        list[str]: List with pdf urls.
    """
    results: list[str] = []
    transkript = re.compile(r"Transkript")  # search pattern for the <p> containing the url
    base_url = "https://www.sciencemediacenter.de"

    for link in press_briefing_links:
        responds = requests.get(base_url + link)
        bs = BeautifulSoup(responds.content, "html.parser")
        print("opening link:")
        p = bs.find_all("p")
        time.sleep(random.randint(1, 7))  # random sleep
        for i in p:
            pdf_url = ""
            candidate = transkript.search(i.text)
            if candidate:
                try:
                    pdf_url = i.find("a")["href"]  # try to get an <a> from the <p>
                    results.append(pdf_url)
                except:
                    print("no a")
    return results


def load_pdf_from_url(pdf_url: str, save_dir: str) -> str:
    """Get a pdf file from a url and save it to a given directory. Since some urls start
    with the domane and others are just the relative path, this is checked as well.

    Args:
        pdf_url (str): URL to the pdf on the website.
        save_dir (str): directory to save the pdfs to.

    Returns:
        str: Path to saved file.
    """
    filename: str = pdf_url.split("/")[-1:][0]  # get the name from the url of the pdf file

    base_url = "https://www.sciencemediacenter.de"
    if not pdf_url.startswith("http"):
        pdf_url = base_url + pdf_url

    responds = requests.get(pdf_url)  # request th pdf

    with open(os.path.join(save_dir, filename), "wb") as f:
        f.write(responds.content)
        return os.path.join(save_dir, filename)
