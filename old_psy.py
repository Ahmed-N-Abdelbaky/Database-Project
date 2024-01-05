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
CREATE TABLE  Company (
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
CREATE TABLE IF NOT EXISTS Job (
    JID INT PRIMARY KEY,
    CID INT REFERENCES Company(CID),
    Description TEXT,
    Title VARCHAR(255),
    Skill_Desc TEXT,
    Work_Type VARCHAR(255)
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS Salary (
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
        if -2147483648 <= result <= 2147483647:
            return result
        else:
            return default
    except (ValueError, TypeError):
        return default
## companies CSV for the -- Company Table--            

with open(r'D:\Database Final Project\archive(16)\company_details\companies.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    company_data = []  
    for row in reader:
        company_data.append((
            int(row['company_id']),  
            row['name'],             
            row['description'],      
            row['zip_code']          #
        ))
# job_posting CSV for the --Job Table--
with open(r'D:\Database Final Project\archive(16)\job_postings.csv', 'r',encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    job_data = []  
    for row in reader:
        job_data.append((
            safe_int(row['job_id']),
            safe_int(row['company_id']),
            row['description'],
            row['skills_desc'],
            row['work_type']
        ))
# salries CSV for the --salaries Table --
with open(r'D:\Database Final Project\archive(16)\job_details\salaries.csv', 'r',encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    salary_data = []
    for row in reader:
        company_data.append((
        safe_int(row['salary_id']),
        safe_int(row['max_salary']),
        safe_int(row['med_salary']),
        safe_int(row['min_salary']),
        row['pay_period'],
        row['currency']
        ))
    # Insert data into company table using batch operation for efficiency
    execute_values(cursor, """
    INSERT INTO Company (CID, Name, Description, zipcode) VALUES %s
    ON CONFLICT (CID) DO NOTHING;
    """, company_data)

    # Insert data into job table using batch operation for efficiency
    execute_values(cursor, """
    INSERT INTO Job (JID, CID, Title, Description, work_type) VALUES %s
    ON CONFLICT (JID) DO NOTHING;
    """, job_data)

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