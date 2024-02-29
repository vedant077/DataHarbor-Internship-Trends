import requests
from bs4 import BeautifulSoup
import pandas as pd
import boto3

# aws credentials
aws_access_key_id = ["AWS_KEY_ID"]
aws_secret_access_key = ["AWS_ACESS_KEY"]
s3_bucket_name = ["S3_BUCKET_NAME"]
s3_key = ["S3_KEY"]
 
# Function to extract the information from the page rendered
def extract(page):
    url = f'https://www.linkedin.com/jobs/search/?currentJobId=3719124343&geoId=101949407&keywords=internship&location=Illinois%2C%20United%20States&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&start={page}' # LinkedIn URL for job data you are trying to extract
    user = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'}
    r = requests.get(url, user)
    search = BeautifulSoup(r.text, "html.parser")
    return search

# Transform function finds the important details from the parsed data and keeps data like job title,company details, location and some other details

def transform(search):
    divs = search.find_all('div', class_ = 'base-search-card__info')
    for items in divs:
        title = items.find('h3').text.strip()
        company = items.find('a').text.strip()
        location = items.find('span').text.strip()
        reference = items.find('a', class_ = 'hidden-nested-link')
        try:
            PostingDate = items.find('time').text.strip()
            Link = reference['href']
            # Active= items.find('span', class_ = 'result-benefits__text')
            # ActivelyPosting = Active.string
        except:
            PostingDate = ''
            Link = ''
            # ActivelyPosting = 'N/A'

        job = {
            'Title': title,
            'Company': company,
            'Location': location,
            'Posting_date': PostingDate,
            'Job_Link': Link,
            'tag': 1
        }

        job_list.append(job)
        #print('Title:',title,'\n','Company:',company,'\n','Location:',location,'\n', 'Posting Date:',PostingDate, '\n','Link:',Link,'\n')
    return

job_list = []

for i in range(0,2001,25):
    print(f'Scraping job till {i+1}')
    c = extract(i)
    transform(c)

# putting everything in a dataframe
df = pd.DataFrame(job_list)
# use -> print(df.head(n)) to get the top n rows of the dataframe

# dropping duplicates
df.drop_duplicates(inplace=True)

# adding extracted date column
df['Extracted_date'] = pd.to_datetime('today').normalize()

# splitting location column
df[['State', 'Country']] = df['Location'].str.split(',', expand=True)

# creating category to segregate title related to the respected fields
category_keywords = {
    'Technical': ['product','data scientist', 'data engineer', 'software engineer', 'analyst', 'analysis', 'full stack', 'frontend', 'backend', 'cyber', 'ai', 'machine learning', 'big data'],
    'HR': ['hr','human resource'],
    'Marketing': ['marketing','social media', 'public relations', 'media'],
    'Finance': ['finance', 'wealth management'],
    'Sports': ['athlete', 'baseball', 'player development', 'football', 'basketball'],
    'Medicine': ['medical'],
    'Management': ['project management', 'operations', 'strategy', 'e-commerce', 'ecommerce', 'planning', 'product', 'production', 'partnership']
}

# Function to categorize positions based on keywords
def categorize_position(position):
    for category, keywords in category_keywords.items():
        if any(keyword in position for keyword in keywords):
            return category
    return 'Other'

# Create a new 'Category' column based on keywords in 'Position'
df['Category'] = df['Title'].str.lower().apply(categorize_position)

# df.to_csv('D:\SOFTWARE\PYCHARM\PROJECTS\LinkedInJobs.csv')


job_csv = df.to_csv(index = False)
s3_connection = boto3.client('s3', aws_access_key_id = aws_access_key_id, aws_secret_access_key= aws_secret_access_key)
s3_connection.put_object(Body = job_csv , Bucket = s3_bucket_name, Key = s3_key)

print("Data pushed to S3 Bucket")

