 -----------SCHEMA------------------- 

    CREATE TABLE  Company (
    CID BIGINT PRIMARY KEY,
    "Name" TEXT,
    "Description" TEXT,
    Zipcode TEXT,
    Industry TEXT,
    Specialty TEXT,
    Employee_Count INT,
    Follower_Count INT
);

CREATE TABLE Job (
    JID BIGINT PRIMARY KEY,
    CID BIGINT,
    Description TEXT,
    Title TEXT,
    Skill_Desc TEXT,
    Work_Type TEXT,
    FOREIGN KEY (CID) REFERENCES Company(CID)
);

CREATE TABLE Salary (
    SID BIGINT PRIMARY KEY,
    JID BIGINT,
    Max NUMERIC(15, 2),
    Med NUMERIC(15, 2),
    Min NUMERIC(15, 2),
    Currency VARCHAR(50),
    Pay_Period VARCHAR(255),
    FOREIGN KEY (JID) REFERENCES Job(JID)
);
