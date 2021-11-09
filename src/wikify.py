# -*- coding: utf-8 -*-
"""Detect the main concept of a text through wikification."""

import time
from typing import Any, Optional

import requests


def wifify(text: str, service: str, token: str, language: str = "de") -> Optional[Any]:
    """Detect Wikipedia entities mentioned in a text. Choose one of two APIs implemented at the moment.

    Args:
        text (str): Text to retrieve entities of off.
        service (str): Name of the API. Either dandaleon or tagme.
        token (str): Token for the API.
        language (str, optional): Language of the input text. Defaults to "de".

    Returns:
        Optional[Any]: Result dictionary with detected nain_concepts if available or "Error" if not enough credits are left.
    """
    if len(text.split(" ")) < 4:
        return None

    if service == "dandaleon":
        api = f"https://api.dandelion.eu/datatxt/nex/v1/?lang={language}&text={text}&token={token}"
        time.sleep(0.02)  # obey rate limit of 50 calls per second
    elif service == "tagme":
        api = f"https://tagme.d4science.org/tagme/tag?lang={language}&gcube-token={token}&tweet=false&text={text}"
        time.sleep(0.02)

    r = requests.get(api)
    if r.status_code == 403:
        print("ERROR: not enough credits left.")
        return "Error"

    if r.status_code == 200 and r.json().get("annotations"):
        return r.json().get("annotations")
    else:
        return None


def detect_main_concept(
    text: str, token: str, num_entetys: int = 1, language: str = "de"
) -> Optional[Any]:
    """Detect the main concept as a Wikipedia article from a given text. By using the `top_entities` parameter of the dandaleon api,
    the extracted entities are ranked accordingly to the relevance for the input text.

    Args:
        text (str): Text to retrieve entities of off.
        token (str): Token for the API.
        num_entetys (int, optional): Number of main entities for the text to return. Defaults to 1.
        language (str, optional): Language of the input text. Defaults to "de".

    Returns:
        Optional[Any]: Result dictionary with detected nain_concepts if available or "Error" if not enough credits are left.
    """
    if len(text.split(" ")) < 4:
        return None

    if len(text) > 4000:
        print("Error: Text is longer than 4000 chars.")
        return None

    num_entetys_str: str = str(num_entetys)
    api = f"https://api.dandelion.eu/datatxt/nex/v1/?lang={language}&text={text}&token={token}&top_entities={num_entetys_str}"
    time.sleep(0.02)  # obey rate limit of 50 calls per second

    r = requests.get(api)
    if r.status_code == 403:
        print("ERROR: not enough credits left.")
        return "Error"
    if r.status_code == 200 and r.json().get("annotations"):
        return r.json().get("annotations")
    else:
        return None
