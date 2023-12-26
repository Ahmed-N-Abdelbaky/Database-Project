#####################  Company Table  #####################


import Pandas as pd

### Companies.CSV ###
#####################

df = pd.read_csv(r'D:\Database Final Project\archive(16)\company_details\companies.csv')

# removing unwanted Columns
df = df[['company_id', 'name', 'description', 'zip_code']]

# removing rows with empty company_id
df =df[df['company_id'].notna()]

# renaming columns to be as The ER diagram
df.rename(columns={'company_id':'CID','name': 'Name', 'description': 'Description', 'zip_code': 'Zipcode'}, inplace=True)

#exporting 
df.to_csv(r'D:\Database Final Project\companies_cleaned.csv', index= False)

### company_industries.CSV ###
##############################

df = pd.read_csv(r"D:\Database Final Project\archive(16)\company_details\company_industries.csv")
# removing rows with empty company_id or empty industry
df =df[df['company_id'].notna()]
df =df[df['industry'].notna()]

# renaming columns to be as The ER diagram
df.rename(columns={'company_id':'CID'}, inplace=True)

#exporting after finishing
df.to_csv(r'D:\Database Final Project\Industries_cleaned.csv', index= False)

### company_specialities.CSV ###
################################

df = pd.read_csv(r"D:\Database Final Project\archive(16)\company_details\company_industries.csv")
# removing rows with empty company_id or industry
df =df[df['company_id'].notna()]
df =df[df['speciality'].notna()]

# renaming columns to be as The ER diagram
df.rename(columns={'company_id':'CID'}, inplace=True)

#exporting after finishing
df.to_csv(r'D:\Database Final Project\Speciality_cleaned.csv', index= False)

### employee_counts.CSV ###
###########################

df = pd.read_csv(r"D:\Database Final Project\archive(16)\company_details\employee_counts.csv")
# removing rows without company_id 
df =df[df['company_id'].notna()]

# removing unwanted Columns
df = df[['company_id', 'employee_count', 'follower_count']]

# Ensuring that Counts are INT
df['employee_count'] = df['employee_count'].astype(int)
df['follower_count'] = df['follower_count'].astype(int)

# renaming columns to be as The ER diagram
df.rename(columns={'company_id':'CID'},inplace=True)

#exporting
df.to_csv(r'D:\Database Final Project\employee_count_cleaned1.csv', index= False)


#####################  Job Table  #####################

### job_posting.CSV ###
df = pd.read_csv(r'D:\Database Final Project\archive(16)\job_postings.csv')

# removing unwanted Columns
df = df[['job_id', 'company_id', 'description', 'title', 'skills_desc', 'work_type']]

## removing rows with empty job_id
df =df[df['job_id'].notna()]

# removing rows with empty company_id
df =df[df['company_id'].notna()]

# renaming columns to be as The ER diagram
df.rename(columns={'job_id': 'JID', 'company_id':'CID', 'description': 'Description', 'title':'Title'}, inplace=True)

#exporting after finishing
df.to_csv(r'D:\Database Final Project\job_posting_cleaned2.csv', index= False)


#####################  Salary Table  #####################

df = pd.read_csv(r"D:\Database Final Project\archive(16)\job_details\salaries.csv")

# removing rows without salary_id 
df =df[df['salary_id'].notna()]

# removing unwanted Columns
df = df[['job_id','salary_id', 'max_salary', 'med_salary', 'min_salary', 'pay_period', 'currency']]

# renaming columns to be as The ER diagram
df.rename(columns={'job_id':'JID','salary_id':'SID', 'max_salary': 'Max', 'med_salary': 'Med', 'min_salary': 'Min', 'pay_period': 'Pay_Period', 'currency': 'Currency'},inplace=True)

#exporting 
df.to_csv(r'D:\Database Final Project\Salaries_cleaned.csv', index= False)