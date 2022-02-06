# The press briefing claim dataset
![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/jueri/claim_model_comparison)

### 💡 Info:
This repository holds the code to create the press briefing claim dataset. The main modules can be found in the [src](https://github.com/jueri/SMC_claim_dataset/src) directory. Three notebooks in the root directory interface these modules and guide through the dataset creation process.

This repository is part of my bachelore theses with the title **Automated statement extractionfrom press briefings**. For more indepth information see the [Statement Extractor](https://github.com/jueri/statement_extractor) repository.

### ⚙️ Setup:
This repository uses Pipenv to manage a virtual environment with all python packages. Information about how to install Pipenv can be found [here](https://pipenv.pypa.io/en/latest/).
To create a virtual environment and install all packages needed, call `pipenv install` from the root directory.

Default directorys and parameter can be defined in [config.py](https://github.com/jueri/SMC_claim_dataset/tree/master/config.py).

The wikification module relies on two wikification services, [Dandelion](https://dandelion.eu/) and [TagMe](https://sobigdata.d4science.org/web/tagme). API keys for these services can be created for free. The wikify module expects the environment variables `DANDELION_TOKEN` and `TAGME_TOKEN`.

### 📋 Content:
Data:
- [data/SMC_dataset](https://github.com/jueri/SMC_claim_dataset/tree/master/data/SMC_dataset) holds the full dataset as SQLite database and csv tables.
- [data/SMC_dataset/pre_labeled](https://github.com/jueri/SMC_claim_dataset/tree/master/data/SMC_dataset/pre_labeled) holds pre labeled dataset slices that are ready for labeling.
- [data/SMC_dataset/labeled](https://github.com/jueri/SMC_claim_dataset/tree/master/data/SMC_dataset/labeled) holds labeled dataset slices.

Code:
- [src](https://github.com/jueri/SMC_claim_dataset/tree/master/src) conatins main modules to scrape, parse and import the data.

Notebooks:
- [create_dataset.ipynb](https://github.com/jueri/SMC_claim_dataset/tree/master/create_dataset.ipynb) guieds through the database creation process.
- [create_tables.ipynb](https://github.com/jueri/SMC_claim_dataset/tree/master/create_tables.ipynb) guides through the table creation process.
- [dataset_analysis.ipynb](https://github.com/jueri/SMC_claim_dataset/tree/master/dataset_analysis.ipynb) holds the analysis of the dataset. 

### 💾 Dataset:
Besides the dataset from the SMC press briefings, a translated version of the *IBM Debater® - Claim Sentences Search* (`IBM_Debater_(R)_claim_sentences_search`) dataset, from the [claim model comparision](https://github.com/jueri/claim_model_comparison) is used to balance the dataset. To create the training data, the `Claim Sentences Search` dataset needs to be preprocessed like in the [claim model comparision](https://github.com/jueri/claim_model_comparison) repo and translated into german.

The SQLite database `dataset.db` has the following structure:
![database](doc/static/db.png)
