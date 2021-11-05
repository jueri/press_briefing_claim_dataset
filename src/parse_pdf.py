# -*- coding: utf-8 -*-
"""Process the pdf transcripts into structured objects.

Examples:
    head, body = parse_pdf.read_pdf("path/to/pdf")
    
    metadata = parse_pdf.parse_head(head)
    passages = parse_pdf.parse_body(body)

Exceptional documents:
    The following documents do not provide a timecode at the same line as the speaker and therefor cannot be parsed 
    by the body parser:
    - Transkript_Atomenergie-und-Klimawandel_SMC-PressBriefing_2020-02-26.pdf
    - Transkript_CO2-Emissionen-im-Corona-Jahr_SMC-Press-Briefing_2020-12-10.pdf
    - Transkript_Die-_neue-GAP_SMC-Press-Briefing_20210316.pdf
    - Transkript_gesundeStaedte_vPressBriefing_30112020.pdf

    - Transkript_SMC_Press_Briefing_Machine_Learning_Medizin_180518.pdf

    The following documents have a divergent metadata page and therefor cannot or only partyally be parsed by the 
    head parser:
    - Transkript_Nationaler-Wasserdialog_vPB_2020-08-27.pdf
    - Transkript_SMC_Press_Briefing_Machine_Learning_Medizin_180518.pdf
    
    - Transkript_Befuerchteter_Personalmangel-auf-den-Intensivstationen_SMC-Press-Briefing_2020-10-30.pdf
    - Transkript_Heinsberg-Studie_Ergebnisse_SMC-Press-Briefing_2020-05-04.pdf
    - Transkript_Tests_Quarantaene_Press_Briefing_09042020.pdf
    - Transkript_Welche_Langzeitstrategie-ist-im-Umgang-mit-SARS-CoV-2-die-zielfuehrende_SMC-Press-Briefing-2021-02-01.pdf
"""

import io
import re
from typing import Any, Union

from pdfminer.converter import TextConverter  # type: ignore
from pdfminer.layout import LAParams  # type: ignore
from pdfminer.pdfdocument import PDFDocument  # type: ignore
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager  # type: ignore
from pdfminer.pdfpage import PDFPage  # type: ignore
from pdfminer.pdfparser import PDFParser  # type: ignore


def read_pdf(path: str) -> tuple[list[str], list[str]]:
    """Open a PDF file from a given path and return seperate lists of strings for the first page and the remaining pages.

    Args:
        path (str): Path to the PDF file to read.

    Returns:
        list[str]: List of all lines from the first page as string.
        list[str]: List of all lines from the remaining pages as string.
    """
    head_string = io.StringIO()  # output strings
    body_string = io.StringIO()

    with open(path, "rb") as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()

        device_head = TextConverter(rsrcmgr, head_string, laparams=LAParams())
        interpreter_head = PDFPageInterpreter(rsrcmgr, device_head)

        device_body = TextConverter(rsrcmgr, body_string, laparams=LAParams())
        interpreter_body = PDFPageInterpreter(rsrcmgr, device_body)

        firstpage = True
        for page in PDFPage.create_pages(doc):
            if firstpage:
                interpreter_head.process_page(page)
                firstpage = False
            else:
                interpreter_body.process_page(page)

    head = head_string.getvalue().split("\n")
    body = body_string.getvalue().split("\n")
    return (head, body)


def parse_head(lines: str) -> dict[str, Any]:
    metadata: dict[str, Any] = {"person": []}
    person: dict[str, str] = {}
    url = False
    date_pattern = re.compile(r"\d\d\.\d\d\.\d{4}")

    for line in lines:
        if url:
            metadata["video_url"] = metadata.get("video_url") + line.strip()  # type: ignore
        elif line.strip():
            # date
            if date_pattern.search(line):
                metadata["date"] = re.findall(date_pattern, line)[0]
            # title
            elif line.strip().startswith("„"):
                metadata["title"] = line.lstrip()
            elif line.strip().endswith("“"):
                metadata["title"] += line.rstrip()

            # url (rarely set at all)
            elif line.lstrip().startswith("http"):
                url = True
                metadata["video_url"] = line.strip()

            # person
            else:
                if person.get("name"):
                    if person["name"].startswith("Moderato"):
                        line_splits = line.split(",")
                        person["name"] = line_splits[0]
                        person["description"] = person.get("description", "") + ",".join(
                            line_splits[1:]
                        )
                    else:
                        person["description"] = person.get("description", "") + " " + line.strip()
                else:
                    person["name"] = line.strip()
        else:
            if person.get("description"):
                metadata["person"].append(person)
            person = {}
            url = False
    return metadata


def parse_body(lines: list[str]) -> list[dict[str, str]]:
    """Parse the transcript body into segments with a speaker, starting timecode and text.capitalize

    Args:
        lines (list[str]): List of transcript lines.

    Returns:
        list[dict[str, str]]: List of segments.
    """
    timecode_pattern = re.compile(
        r"\[\d\d:\d\d\]|\(\d\d:\d\d\)|\[\d\d:\d\d:\d\d\]"
    )  # Re pattern for timecode: [00:00] [00:00:00] (00:00)

    def _get_timecode(line: str):
        """Extract the timecode of a line."""
        result = timecode_pattern.search(line)  # check if match exists
        if result:
            timecode = re.findall(timecode_pattern, line)
            return timecode[0]

    def _get_name(line: str):
        """Extract the speaker name of a line."""
        result = timecode_pattern.search(line)  # check if match exists
        if result:
            line_split = timecode_pattern.split(line)  # split at match
            name = line_split[0].strip().replace(":", "")
            return name

    passages: list[dict[str, str]] = []
    current_passage: dict[str, str] = {}

    for line in lines:
        if "in der Redaktion" in line:  # stop at imprint page
            break
        if name := _get_name(line):
            if current_passage:  # Save recent passage
                passages.append(current_passage)
                current_passage = {}

            current_passage["speaker"] = name
            current_passage["timecode"] = _get_timecode(line)

        else:
            if current_passage.get("text"):
                current_passage["text"] += line.strip()
            else:
                current_passage["text"] = line.strip()

    passages.append(current_passage)  # save last passage
    return passages
