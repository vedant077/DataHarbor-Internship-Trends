# DataHarbor-Internship-Trends

## Overview

This project aims to automate the end-to-end process of collecting, categorizing, and analyzing internship records. The workflow involves scraping raw data using a custom job scraper, cleaning the data with Python and AWS Glue jobs, storing partially transformed records in CSV format on AWS S3, and completing the transformation with an AWS Glue Job. The finalized data is then loaded into an AWS RDS instance (MS SQL Server). The ultimate goal is to connect the RDS instance to Tableau, enabling the creation of interactive dashboards for insightful analysis of internship and job data across different sectors.

Data Ingestion Flow and Process

Our comprehensive data pipeline seamlessly extracts job listings, transforms the data, and loads it into an AWS RDS instance, ensuring a streamlined and automated process. The journey begins with a custom-built job scraper that gathers data and deposits CSV files into an S3 bucket. AWS S3 events trigger the initiation of an AWS Glue Crawler through AWS Lambda 1, which dynamically catalogs the data into the AWS Glue Data Catalog. CloudWatch monitors the crawler's progress, and upon successful completion, an AWS EventBridge rule is triggered. This EventBridge rule orchestrates the flow by invoking a Lambda function (AWS Lambda 2), which, in turn, triggers an AWS Glue Job responsible for the Extract, Transform, Load (ETL) process.

AWS S3 Bucket

Our data pipeline commences with a custom Python job scraper depositing job listings into an AWS S3 bucket. This snippet illustrates the CSV file uploads, showcasing the seamless data transfer process.

AWS Crawler Stages

AWS Glue Crawler plays a pivotal role in dynamically cataloging scraped data into the AWS Glue Data Catalog. This snippet provides insights into the running and completed states of the Crawler job, ensuring comprehensive data cataloging.

AWS Data Catalog

The AWS Data Catalog snippet contains metadata for all crawled data. It serves as a centralized repository, offering a structured overview of the cataloged information, and facilitating efficient data management and retrieval.

AWS Glue Job

The ETL process is executed through an AWS Glue Job triggered by an AWS EventBridge rule. This snippet provides a glimpse into the PySpark code driving the data transformation, along with monitoring details, showcasing the status of each job run for effective management.

AWS RDS

The AWS RDS snippet showcases the database instance where the curated job data seamlessly lands after the ETL process. This provides a clear view of the scalable and efficient solution for managing job listings within the AWS RDS environment.

RDS Database

IAM Role

The IAM console snippet reveals the roles and permissions crucial to our data pipeline. This concise overview showcases our commitment to security by implementing fine-grained access controls, adhering to the principle of least privilege for a robust AWS environment.

IAM Roles

IAM Permissions Policies

Tableau Analysis

We developed a comprehensive analysis dashboard focusing on extracted job data to discern key insights into internship positions. The dashboard provides a detailed breakdown of job distribution by category, shedding light on diverse opportunities. Geographical distribution analysis offers a visual representation of internship openings across regions, aiding in the identification of high-demand areas. Furthermore, the project identifies companies with the most internship openings, providing valuable insights for job seekers and recruiters. The user-friendly dashboard serves as a centralized platform, ultimately contributing to a deeper understanding of factors influencing internship availability. We have attached the dashboard file for the reference of this analysis.

Challenges

Navigating Job Board Scraping Policies:
Understanding and adhering to scraping policies of multiple job boards posed a significant hurdle in the data acquisition phase.
Data Scraping from Websites:
Overcoming the intricacies of website structures, handling dynamic content, and respecting scraping permissions were key challenges.
Data Cleaning for Sector Categorization:
Cleaning scraped data to categorize internship records into different sectors proved to be a substantial challenge, requiring thorough data cleansing strategies.
AWS Flow and Permissions Issues:
Implementing the end-to-end data flow in AWS posed challenges, particularly with AWS Glue Crawlers triggering Lambda functions, requiring meticulous configuration for a seamless and secure data pipeline.
