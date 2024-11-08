import requests
import os
import sys
import time
import textwrap


def getArticle():
    validTitle = False
    while not validTitle:
        r = requests.get(
            "https://en.wikipedia.org/w/api.php?action=query&format=json&list=random&rnlimit=5"
        )
        data = r.json()["query"]["random"][0]["title"].lower().strip()
        if (
            data.startswith("user talk:")
            or data.startswith("talk:")
            or data.startswith("wikipedia:")
            or data.startswith("wikipedia talk:")
            or data.startswith("category:")
            or data.startswith("category talk:")
            or data.startswith("file:")
            or data.startswith("file talk:")
            or data.startswith("user:")
            or data.startswith("portal:")
            or data.startswith("template:")
            or data.startswith("template talk:")
        ):
            print("Finding suitable random page")
            time.sleep(1)
        else:
            id = r.json()["query"]["random"][0]["id"]
            validTitle = True

    pr = requests.get(
        f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&pageids={id}"
    )
    pageData = pr.json()
    return [
        data,
        pageData["query"]["pages"][str(id)]["extract"],
        f"<https://en.wikipedia.org/?curid={str(id)}>",
    ]
