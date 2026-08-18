# Data Ingestion from S3 to RDS with Fallback to AWS Glue using Dockerized Python Application

# Project Overview

Data Ingestion from S3 to RDS with Fallback to AWS Glue using Dockerized Python Application is a cloud-based data ingestion pipeline that automatically reads CSV data from Amazon S3 and loads it into an Amazon RDS MySQL database using a Dockerized Python application.

The application uses Python, Pandas, Boto3, SQLAlchemy, and PyMySQL to process and transfer the data. Under normal conditions, the CSV records are successfully inserted into RDS. If the RDS database is unavailable or the data insertion fails, the application automatically uses AWS Glue Data Catalog as a fallback and registers the S3 dataset as an external table.

This project demonstrates practical implementation of AWS cloud services, Python data processing, Docker containerization, database integration, error handling, and fallback architecture.

#
