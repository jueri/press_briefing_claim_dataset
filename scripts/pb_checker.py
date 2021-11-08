# -*- coding: utf-8 -*-
"""Check press briefing parses for database import. Since the press briefing pdfs are not consistent, the parser may fail.
This script helps to get a quick overview of the parse quality. A brief overview for each press briefing is presented at 
run and can be accepted (y) or denied (n). All filenames for denied parses are written to a file for further investigation
or exclusion.
"""

import os
import sys
from typing import Any, Optional

import pandas as pd

sys.path.append("..")
from src.create_dataset import parse_pdf


def prepare_data(pdf: pd.Series) -> dict[str, Any]:
    """Parse a pressbriefing pdf from a pressbriefing metadata table row into a dictionary.

    Args:
        pdf (pd.Series): Row from pressbriefing metadata table.

    Returns:
        dict[str, str]: Dictionary with pressbriefing information.
    """

    # add metadata
    pdf_path = pdf[1]["pdf_path"]
    pdf_url = pdf[1]["pdf_url"]
    introduction_text = pdf[1]["introduction"]

    # read pdf file
    head, body = parse_pdf.read_pdf("../" + pdf[1]["pdf_path"])  # parse pdf
    fulltext = " ".join(body)
    fulltext_clean = parse_pdf.sanetize(fulltext)

    # parse head
    head_metadata = parse_pdf.parse_head(head)  # type: ignore
    title = head_metadata.get("title")
    date = head_metadata.get("date")
    video_url = head_metadata.get("video_url")

    # parse body
    segments = parse_pdf.parse_body(body)
    persons = list(set([part.get("speaker") for part in segments]))

    return {
        "pdf_path": pdf_path,
        "pdf_url": pdf_url,
        "introduction_text": introduction_text,
        "fulltext": fulltext,
        "fulltext_clean": fulltext_clean,
        "title": title,
        "date": date,
        "video_url": video_url,
        "person": persons,
        "segments": segments,
    }


def print_pb(pb: dict[str, Optional[Any]]):
    """Pretty print pressbriefing information from a dictionary.

    Args:
        pb (dict[str, str]): Pressbriefing dictionarry.
    """
    segments = [s.get("text") for s in pb.get("segments")]  # type: ignore
    timecodes = str([t.get("timecode") for t in pb.get("segments")])  # type: ignore
    num_segments = str(len(segments))
    person = str(set([t.get("speaker") for t in pb.get("segments")]))  # type: ignore

    print(
        "############################################################################################################################################"
    )
    print("Title:               ", pb.get("title"))
    print(
        "--------------------------------------------------------------------------------------------------------------------------------------------"
    )
    print("pdf_path:            ", pb.get("pdf_path"))
    print("pdf_url:             ", pb.get("pdf_url"))
    print("introduction_text:   ", pb.get("introduction_text", "1234567890")[:100])  # type: ignore
    print("fulltext:            ", pb.get("fulltext", "1234567890")[:100])  # type: ignore
    print("fulltext_clean:      ", pb.get("fulltext_clean", "1234567890")[:100])  # type: ignore
    print("date:                ", pb.get("date"))
    print("video_url:           ", pb.get("video_url"))
    print(
        "--------------------------------------------------------------------------------------------------------------------------------------------"
    )
    print("num_segments:        ", num_segments)
    print("timecodes:           ", timecodes[:100])
    print("Speaker:             ", person)
    print(
        "############################################################################################################################################"
    )
    print("\n")


def done(no):
    with open("parse_errors.txt", "w") as outFile:
        for pdf in no:
            outFile.write(pdf)
            outFile.write("\n")

    print("### All Done ###")


if __name__ == "__main__":
    BASE_DIR = "../data/SMC_dataset"
    METADATA_PATH = os.path.join(BASE_DIR, "metadata.csv")
    DB_PATH = os.path.join(BASE_DIR, "dataset.db")

    metadata = pd.read_csv(METADATA_PATH)
    metadata = metadata.dropna().reset_index(drop=True)  # delete na rows

    no: list = []
    for pdf in metadata.iterrows():
        print("Num:             ", str(pdf[0]))
        data = prepare_data(pdf)
        print_pb(data)
        command = input()
        if command == "q":
            done(no)
            break
        elif command == "y":
            continue
        elif command == "n":
            no.append(pdf[1]["pdf_path"])
        os.system("clear")  # Linux - OSX

    done(no)
