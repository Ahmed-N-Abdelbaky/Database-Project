-- Company Table
CREATE TEMP TABLE IF NOT EXISTS Company (
    company_id BIGINT PRIMARY KEY,
    "name" VARCHAR(255),
    "description" TEXT,
    company_size BIGINT,
    "state" VARCHAR(255),
    country VARCHAR(255),
    city VARCHAR(255),
    zip_code VARCHAR(255),
    "address" TEXT,
    "url" TEXT
);

-- Job Postings Table
CREATE TEMP TABLE IF NOT EXISTS Job_Postings (
    job_id BIGINT PRIMARY KEY,
    company_id BIGINT REFERENCES Company(company_id),
    title VARCHAR(255),
    description TEXT,
    max_salary NUMERIC(15, 2),
    med_salary NUMERIC(15, 2),
    min_salary NUMERIC(15, 2),
    pay_period VARCHAR(255),
    formatted_work_type VARCHAR(255),
    "location" VARCHAR(255),
    applies INT,
    original_listed_time VARCHAR(200),
    remote_allowed INT,
    "views" INT,
    job_posting_url VARCHAR(255),
    application_url VARCHAR(255),
    application_type VARCHAR(255),
    expiry VARCHAR(200),
    closed_time BIGINT,
    formatted_experience_level VARCHAR(255),
    skills_desc TEXT,
    listed_time VARCHAR(200),
    posting_domain VARCHAR(255),
    sponsored BOOLEAN,
    work_type VARCHAR(255),
    currency VARCHAR(3),
    compensation_type VARCHAR(255),
    scraped VARCHAR(200),
);

-- Company Industries Table
CREATE TEMP TABLE IF NOT EXISTS Company_Industries (
    company_id INT REFERENCES Company(company_id),
    industry VARCHAR(255),
    PRIMARY KEY (company_id, industry)
);

-- Company Specialities Table
CREATE TEMP TABLE IF NOT EXISTS Company_Specialities (
    company_id BIGINT REFERENCES Company(company_id),
    speciality VARCHAR(255),
    PRIMARY KEY (company_id, speciality)
);

-- Employee Counts Table
CREATE TEMP TABLE IF NOT EXISTS Employee_Counts (
    company_id BIGINT REFERENCES Company(company_id),
    employee_count BIGINT,
    follower_count BIGINT,
    time_recorded VARCHAR(255),
    PRIMARY KEY (company_id, time_recorded)
);

-- Benefits Table
CREATE TEMP TABLE IF NOT EXISTS Benefits (
    job_id BIGINT REFERENCES Job_Postings(job_id),
    inferred BOOLEAN,
    "type" VARCHAR(255),
    PRIMARY KEY (job_id, type)
);

-- Job Industries Table
CREATE TEMP TABLE IF NOT EXISTS Job_Industries (
    job_id BIGINT REFERENCES Job_Postings(job_id),
    industry_id BIGINT,
    PRIMARY KEY (job_id, industry_id)
);

-- Job Skills Table
CREATE TEMP TABLE IF NOT EXISTS Job_Skills (
    job_id BIGINT REFERENCES Job_Postings(job_id),
    skill_abr VARCHAR(255),
    PRIMARY KEY (job_id, skill_abr)
);

-- Salaries Table
CREATE TEMP TABLE IF NOT EXISTS Salaries (
    salary_id BIGINT PRIMARY KEY,
    job_id BIGINT REFERENCES Job_Postings(job_id),
    max_salary NUMERIC(15, 2),
    med_salary NUMERIC(15, 2),
    min_salary NUMERIC(15, 2),
    pay_period VARCHAR(255),
    currency VARCHAR(50),
    compensation_type VARCHAR(255)
);

COPY Company FROM 'D:/Database Final Project/archive(16)/company_details/companies.csv' WITH CSV HEADER;

-- Copy data into Job_Postings table
COPY Job_Postings FROM 'D:/Database Final Project/archive(16)/job_postings.csv' WITH CSV HEADER;

-- Copy data into Company_Industries table
COPY Company_Industries FROM 'D:/Database Final Project/archive(16)/company_details/company_industries.csv' WITH CSV HEADER;

-- Copy data into Company_Specialities table
COPY Company_Specialities FROM 'D:/Database Final Project/archive(16)/company_details/company_specialities.csv' WITH CSV HEADER;

-- Copy data into Employee_Counts table
COPY Employee_Counts FROM 'D:/Database Final Project/archive(16)/company_details/employee_counts.csv' WITH CSV HEADER;

-- Copy data into Benefits table
COPY Benefits FROM 'D:/Database Final Project/archive(16)/benefits.csv' WITH CSV HEADER;

-- Copy data into Job_Industries table
COPY Job_Industries FROM 'D:/Database Final Project/archive(16)/job_details/job_industries.csv' WITH CSV HEADER;

-- Copy data into Job_Skills table
COPY Job_Skills FROM 'D:/Database Final Project/archive(16)/job_details/job_skills.csv' WITH CSV HEADER;

-- Copy data into Salaries table
COPY Salaries FROM 'D:/Database Final Project/archive(16)/job_details/salaries.csv' WITH CSV HEADER;
