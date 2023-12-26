 -----------COMPANY TABLE Queries------------------- 

--CREATING TEMP TABLES
CREATE TEMP TABLE temp_companies (
CID BIGINT,
"Name" TEXT,
"Description" TEXT,
Zipcode TEXT
);

CREATE TEMP TABLE temp_follower_count (
CID BIGINT,
employee_count INT,
follower_count INT
);

CREATE TEMP TABLE temp_speciality (
CID BIGINT,
speciality TEXT
);

CREATE TEMP TABLE temp_industry (
CID BIGINT,
Industry TEXT
);

-- DATA Ingestion for Temp Tables
COPY temp_companies
FROM 'D:\Database Final Project\companies_cleaned.csv'
DELIMITER ',' CSV HEADER;

COPY temp_follower_count
FROM 'D:\Database Final Project\follower_count_cleaned.csv'
DELIMITER ',' CSV HEADER;

COPY temp_speciality
FROM 'D:\Database Final Project\speciality_cleaned.csv'
DELIMITER ',' CSV HEADER;

COPY temp_industry
FROM 'D:\Database Final Project\Industries_cleaned.csv'
DELIMITER ',' CSV HEADER;


-- MOVING The data from TEMP to Main Table
-- USING Joins
INSERT INTO Company (CID, "Name", "Description", Zipcode, Industry, Specialty, Employee_Count, Follower_Count)
SELECT DISTINCT ON (CID)
    CID, "Name", "Description", Zipcode, Industry, Specialty, Employee_Count, Follower_Count
FROM (
    SELECT 
        co.CID, 
        co."Name",
        co."Description", 
        co.Zipcode, 
        ind.Industry, 
        sp.speciality AS Specialty, 
        fc.employee_count,
        fc.follower_count
    FROM temp_companies co
    LEFT JOIN temp_follower_count fc ON co.CID = fc.CID
    LEFT JOIN temp_speciality sp ON co.CID = sp.CID
    LEFT JOIN temp_industry ind ON co.CID = ind.CID

    UNION ALL

    SELECT 
        fc.CID, 
        co."Name",
        co."Description", 
        co.Zipcode, 
        ind.Industry, 
        sp.speciality AS Specialty, 
        fc.employee_count,
        fc.follower_count
    FROM temp_follower_count fc
    LEFT JOIN temp_companies co ON fc.CID = co.CID
    LEFT JOIN temp_speciality sp ON fc.CID = sp.CID
    LEFT JOIN temp_industry ind ON fc.CID = ind.CID

    UNION ALL

    SELECT 
        sp.CID, 
        co."Name",
        co."Description", 
        co.Zipcode, 
        ind.Industry, 
        sp.speciality AS Specialty, 
        fc.employee_count,
        fc.follower_count
    FROM temp_speciality sp
    LEFT JOIN temp_companies co ON sp.CID = co.CID
    LEFT JOIN temp_follower_count fc ON sp.CID = fc.CID
    LEFT JOIN temp_industry ind ON sp.CID = ind.CID

    UNION ALL

    SELECT 
        ind.CID, 
        co."Name",
        co."Description", 
        co.Zipcode, 
        ind.Industry, 
        sp.speciality AS Specialty, 
        fc.employee_count,
        fc.follower_count
    FROM temp_industry ind
    LEFT JOIN temp_companies co ON ind.CID = co.CID
    LEFT JOIN temp_follower_count fc ON ind.CID = fc.CID
    LEFT JOIN temp_speciality sp ON ind.CID = sp.CID
) AS combined
ORDER BY CID;

--Dropping TEMP Tables

DROP TABLE temp_companies;
DROP TABLE temp_follower_count;
DROP TABLE temp_speciality;
DROP TABLE temp_industry;


 -----------JOB TABLE Queries------------------- 

 --CREATING TEMP TABLES
CREATE TEMP TABLE temp_job (
	JID BIGINT,
    CID BIGINT,
    Description TEXT,
    Title TEXT,
    Skill_Desc TEXT,
    Work_Type TEXT
);

COPY temp_job
FROM 'D:\Database Final Project\job_posting_cleaned.csv'
DELIMITER ',' CSV HEADER;

--INSERTING TO Job Table

INSERT INTO Job (JID, CID, Description, Title, Skill_Desc, Work_Type)
SELECT JID, CID, Description, Title, Skill_Desc, Work_Type
FROM temp_job
WHERE CID IN (SELECT CID FROM Company);

--DELETING THE TEMP table
DROP TABLE temp_job;

---------------SALARY TABLE Queries------------------
--TEMP Table
CREATE TEMP TABLE temp_salary (
    SID BIGINT ,
    JID BIGINT,
    "max" NUMERIC(15, 2),
    med NUMERIC(15, 2),
    "min" NUMERIC(15, 2),
    currency VARCHAR(50),
    pay_period VARCHAR(255)
);
COPY temp_salary
FROM 'D:\Database Final Project\Salaries_cleaned.csv'
DELIMITER ',' CSV HEADER;

--INSERTING into Salary Table
INSERT INTO salary (sid, jid, "max", med, "min", currency, pay_period)
SELECT SID, JID, "max", med, "min", currency, pay_period
FROM temp_salary 
WHERE JID IN (SELECT JID FROM job);

--DROPING the TEMP table
DROP TABLE temp_salary;
