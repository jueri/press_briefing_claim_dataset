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
        Optional[Any]: Result dictionary with detected wikipedia entetys if available or "Error" if not enough credids are left.
    """
    if len(text.split(" ")) > 4:
        return None

    if service == "dandaleon":
        api = f"https://api.dandelion.eu/datatxt/nex/v1/?lang={language}&text={text}&token={token}"
        time.sleep(0.02)  # obey rate limit of 50 calls per second
    elif service == "tagme":
        api = f"https://tagme.d4science.org/tagme/tag?lang={language}&gcube-token={token}&tweet=false&text={text}"

    r = requests.get(api)
    if r.status_code == 403:
        print("ERROR: not enough credits left.")
        return "Error"

    if r.status_code == 200 and r.json().get("annotations"):
        return r.json().get("annotations")
    else:
        return None
