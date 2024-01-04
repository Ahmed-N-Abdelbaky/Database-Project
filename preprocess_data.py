import pandas as pd
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.stem import PorterStemmer

### Tokenize Dataset ###
def tokenize_col(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """
    Preprocess a Dataframe to tokenize selected column.

    Args:
        df (pd.DataFrame): Dataframe to be changed.
        col (str): Name of col to tokenize.

    Returns:
        pd.Dataframe : A Dataframe with tokenized column as a string of tokens.
    """

    punctuation = [*"!\"#$%′&'⩽−-()*+,./:;<=>?@[\]^_`{|}~“”’"]

    stemmer = PorterStemmer()
    for index, row in df.iterrows():
        desc = row[col]

        # Error handling
        if type(desc) is pd.Series:
            desc = desc.to_string()

        if type(desc) is not str:
            desc = ['']
            continue

        # Lowercase the column
        desc = desc.lower()

        # Remove newlines
        desc = desc.replace('\n', ' ').replace('\r', '')

        # Remove stopwords
        for word in nltk.corpus.stopwords.words('english'):
            temp = desc.split()
            while word in temp:
                temp.remove(word)
            desc = ' '.join(temp)

        # Remove digits
        for digit in [0,1,2,3,4,5,6,7,8,9]:
            desc = desc.replace(str(digit), '')

        # Remove punctuation
        for p in punctuation:
            desc = desc.replace(p, '')

        # Tokenize
        tokens = nltk.tokenize.word_tokenize(desc)

        # Stem words
        for i in range(len(tokens)):
            tokens[i] = stemmer.stem(tokens[i])

        desc = ' '.join(tokens)

        df.at[index, col] = desc

    return df

### Companies.CSV ###
#####################

df = pd.read_csv('data/company_details/companies.csv')

# removing unwanted Columns
df = df[['company_id', 'name', 'description', 'zip_code']]

# removing rows with empty company_id
df = df[df['company_id'].notna()]

# removing rows with empty description
df = df[df['description'].notna()]

# renaming columns to be as The ER diagram
df.rename(columns={'company_id':'CID','name': 'Name', 'description': 'Description', 'zip_code': 'Zipcode'}, inplace=True)

# Tokenize description
tokenize_col(df, 'Description')

#exporting 
df.to_csv('data_cleaned/company_details/companies.csv', index= False)

### company_industries.CSV ###
##############################

df = pd.read_csv("data/company_details/company_industries.csv")
# removing rows with empty company_id or empty industry
df =df[df['company_id'].notna()]
df =df[df['industry'].notna()]

# renaming columns to be as The ER diagram
df.rename(columns={'company_id':'CID'}, inplace=True)

#exporting after finishing
df.to_csv('data_cleaned/company_details/company_industries.csv', index= False)

### company_specialities.CSV ###
################################

df = pd.read_csv("data/company_details/company_specialities.csv")
# removing rows with empty company_id or industry
df =df[df['company_id'].notna()]
df =df[df['speciality'].notna()]

# renaming columns to be as The ER diagram
df.rename(columns={'company_id':'CID'}, inplace=True)

#exporting after finishing
df.to_csv('data_cleaned/company_details/company_specialities.csv', index= False)

### employee_counts.CSV ###
###########################

df = pd.read_csv("data/company_details/employee_counts.csv")
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
df.to_csv('data_cleaned/company_details/employee_counts.csv', index= False)


#####################  Job Table  #####################

### job_posting.CSV ###
df = pd.read_csv('data/job_details/job_postings.csv')

# removing unwanted Columns
df = df[['job_id', 'company_id', 'description', 'title', 'skills_desc', 'work_type']]

## removing rows with empty job_id
df =df[df['job_id'].notna()]

# removing rows with empty company_id
df =df[df['company_id'].notna()]

# renaming columns to be as The ER diagram
df.rename(columns={'job_id': 'JID', 'company_id':'CID', 'description': 'Description', 'title':'Title'}, inplace=True)

df['CID'] = df['CID'].astype(int)

# Tokenize description
tokenize_col(df, 'Description')
tokenize_col(df, 'skills_desc')

#exporting after finishing
df.to_csv('data_cleaned/job_details/job_postings.csv', index= False)


#####################  Salary Table  #####################

df = pd.read_csv("data/job_details/salaries.csv")

# removing rows without salary_id 
df =df[df['salary_id'].notna()]

# removing unwanted Columns
df = df[['job_id','salary_id', 'max_salary', 'med_salary', 'min_salary', 'pay_period', 'currency']]

# renaming columns to be as The ER diagram
df.rename(columns={'job_id':'JID','salary_id':'SID', 'max_salary': 'Max', 'med_salary': 'Med', 'min_salary': 'Min', 'pay_period': 'Pay_Period', 'currency': 'Currency'},inplace=True)

#exporting 
df.to_csv('data_cleaned/job_details/salaries.csv', index= False)