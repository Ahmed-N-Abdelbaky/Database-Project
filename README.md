# Database Project
The goal of this project is to produce a database that can be queried to find relevant keywords to put in a resume.

## Reproducibility in Python
- Create a venv
> python -m venv .venv
- Activate venv
> .venv/scripts/activate
- Install requirements
> pip install -r requirements.txt
- Add the file **job_postings.csv** from the dataset to the **data/job_details/** directory as it exceeds GitHub's file size limitation.
- Run **preprocess_data.py** to generate the cleaned data.
> python preprocess_data.py

## Reproducability in pgAdmin4
- Create a new database called **FinalProject**.
- Change the login requirements at the top of **psy.py**.
> Password can be changed under **Login/Group Roles(15)** -> **postgres** -> **preferences** -> **definition** -> **password**