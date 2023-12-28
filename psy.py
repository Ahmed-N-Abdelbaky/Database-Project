import psycopg2
from psycopg2.extras import execute_values
import csv


conn_params = {
    'dbname': 'FinalProject',
    'user': 'postgres',
    'password': '123',
    'host': 'localhost'
}

conn = psycopg2.connect(**conn_params)
cursor = conn.cursor()

# Create tables based on the ER diagram
# This should be done only once, so you may comment out or remove this section after the first run
cursor.execute("""
DROP TABLE IF EXISTS Company CASCADE;
CREATE TABLE Company (
    CID INT PRIMARY KEY,
    Name VARCHAR(255),
    Description TEXT,
    Zipcode VARCHAR(255),
    Industry VARCHAR(255),
    Specialty VARCHAR(255),
    Employee_Count INT,
    Follower_Count INT
);
""")
cursor.execute("""
DROP TABLE IF EXISTS Job CASCADE;
CREATE TABLE Job (
    JID INT PRIMARY KEY,
    CID INT REFERENCES Company(CID),
    Description TEXT,
    Title TEXT,
    Skill_Desc TEXT,
    Work_Type VARCHAR(255)
);
""")
cursor.execute("""
DROP TABLE IF EXISTS Salary CASCADE;
CREATE TABLE Salary (
    SID SERIAL PRIMARY KEY,
    JID BIGINT REFERENCES Job(JID),
    Max NUMERIC(10, 2),
    Med NUMERIC(10, 2),
    Min NUMERIC(10, 2),
    Currency VARCHAR(255),
    Pay_Period VARCHAR(255)
);
""")
conn.commit()  # Commit to save the initial table structure



# Preprocess and insert data from the CSV
def safe_int(value, default=0):
    """Convert value to integer, using default if conversion fails or out of range."""
    try:
        result = int(value)
        if -2147483647 <= result <= 2147483646:
            return result
        else:
            return default
    except (ValueError, TypeError):
        return default
## companies CSV for the -- Company Table--            

with open('data_cleaned/company_details/companies.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    company_data = []  
    for row in reader:
        company_data.append((
            safe_int(row['CID']),
            row['Name'],
            row['Description'],
            row['Zipcode']
        ))

    # Insert data into company table using batch operation for efficiency
    execute_values(cursor, """
    INSERT INTO Company (CID, Name, Description, zipcode) VALUES %s
    ON CONFLICT (CID) DO NOTHING;
    """, company_data)

# job_posting CSV for the --Job Table--
with open('data_cleaned/job_details/job_postings.csv', 'r',encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    job_data = []  
    for row in reader:
        job_data.append((
            safe_int(row['JID']),
            safe_int(row['CID']),
            row['Description'],
            row['skills_desc'],
            row['work_type']
        ))

    # Insert data into job table using batch operation for efficiency
    execute_values(cursor, """
    INSERT INTO Job (JID, CID, Title, Description, work_type) VALUES %s
    ON CONFLICT (JID) DO NOTHING;
    """, job_data)

# salries CSV for the --salaries Table --
with open('data_cleaned/job_details/salaries.csv', 'r',encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    salary_data = []
    for row in reader:
        company_data.append((
        safe_int(row['SID']),
        safe_int(row['Max']),
        safe_int(row['Med']),
        safe_int(row['Min']),
        row['Pay_Period'],
        row['Currency']
        ))

    # Insert data into salary table using batch operation for efficiency
    execute_values(cursor, """
    INSERT INTO Salary (JID, Max, Med, Min, Currency, Pay_Period) VALUES %s
    ON CONFLICT (JID) DO NOTHING;
    """, salary_data)

# Commit the changes to the database
conn.commit()

# Close the cursor and the connection
cursor.close()
conn.close()