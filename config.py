import os
import nltk

DEBUG = False

# Source
BASE_URL = "https://www.sciencemediacenter.de"

# Dataset
BASE_DIR = os.path.join("data", "SMC_dataset")
METADATA_PATH = os.path.join(BASE_DIR, "metadata.csv")
DB_PATH = os.path.join(BASE_DIR, "dataset.db")

# NLTK
NLTK_DATA_PATH = os.path.join("data", "nltk_data")
if not os.path.exists(NLTK_DATA_PATH):
    os.makedirs(NLTK_DATA_PATH)
    nltk.download("punkt", NLTK_DATA_PATH)
    nltk.data.path.append(NLTK_DATA_PATH)
