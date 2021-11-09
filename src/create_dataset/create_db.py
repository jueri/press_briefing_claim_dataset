# -*- coding: utf-8 -*-
"""Create and interact with a sqlite database for the SMC Dataset."""

import sqlite3


def create_connection(path: str) -> sqlite3.Connection:
    """Create a connection and if not allready existing a database at a given path.

    Args:
        path (str): Path to sqlite database.

    Returns:
        sqlite3.Connection: Connection object to interact with the database.
    """
    return sqlite3.connect(path)


def db_execute(command: str, connection: sqlite3.Connection):
    """Wrapper to execute commands on a sqlite database.

    Args:
        command (str): Command to execute.
        connection (sqlite3.Connection): Database connection object.
    """
    cur = connection.cursor()
    cur.execute(command)
    connection.commit()


def create_tables(connection: sqlite3.Connection):
    """Create the tables for the SMC dataset."""

    # Person Table
    command = """CREATE TABLE Person
    (
        person_ID INTEGER PRIMARY KEY autoincrement,
        name text NOT NULL,
        resort text,
        afiliation text
    )
    """
    db_execute(command, connection)

    # Press_Briefing Table
    command = """CREATE TABLE Press_Briefing
    (
        pb_ID INTEGER PRIMARY KEY autoincrement,
        title text,
        date text,
        host int,
        pdf_path text,
        pdf_url text,
        video_url text,
        introduction_text text,
        fulltext text,
        fulltext_clean text,
        FOREIGN KEY (host) REFERENCES Person (person_ID)
    )
    """
    db_execute(command, connection)

    # is guest table
    command = """CREATE TABLE is_guest
    (
        pb_ID int,
        person_ID int,
        FOREIGN KEY (pb_ID) REFERENCES Press_Briefing (pb_ID)
        FOREIGN KEY (person_ID) REFERENCES Person (person_ID)
    )
    """
    db_execute(command, connection)

    # segment table
    command = """CREATE TABLE Segment
    (
        segment_ID INTEGER PRIMARY KEY autoincrement,
        pb_ID int NOT NULL,
        text text NOT NULL,
        speaker int,
        timecode text,

        FOREIGN KEY (speaker) REFERENCES Person (person_ID)
        FOREIGN KEY (pb_ID) REFERENCES Press_Briefing (pb_ID)
    )
    """
    db_execute(command, connection)

    # sentences table
    command = """CREATE TABLE Sentence
    (
        sentence_ID INTEGER PRIMARY KEY autoincrement,
        pb_ID int,
        segment_ID int,
        sentence text NOT NULL,

        FOREIGN KEY (pb_ID) REFERENCES Press_Briefing (pb_ID)
        FOREIGN KEY (segment_ID) REFERENCES Segment (segment_ID)
    )
    """
    db_execute(command, connection)

    # Sentence wikification table
    command = """CREATE TABLE Sentence_Wikification
    (
        sentence_wikification_ID INTEGER PRIMARY KEY autoincrement,
        sentence_ID int,
        term text NOT NULL,
        wiki_num int NOT NULL,
        confidence real NOT NULL,
        url text,

        FOREIGN KEY (sentence_ID) REFERENCES Sentence (sentence_ID)
    )
    """
    db_execute(command, connection)

    # Sentence wikification table
    command = """CREATE TABLE pb_Wikification_title
    (
        pb_wiki_title_ID INTEGER PRIMARY KEY autoincrement,
        pb_ID int,
        term text NOT NULL,
        wiki_num int NOT NULL,
        confidence real NOT NULL,
        url text,

        FOREIGN KEY (pb_ID) REFERENCES Press_Briefing (pb_ID)
    )
    """
    db_execute(command, connection)

    # Sentence wikification table
    command = """CREATE TABLE pb_Wikification_intro
    (
        pb_wiki_intro_ID INTEGER PRIMARY KEY autoincrement,
        pb_ID int,
        term text,
        wiki_num int NOT NULL,
        confidence real NOT NULL,
        url text,

        FOREIGN KEY (pb_ID) REFERENCES Press_Briefing (pb_ID)
    )
    """
    db_execute(command, connection)
