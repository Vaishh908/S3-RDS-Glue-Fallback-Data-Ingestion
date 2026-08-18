# Data Ingestion from S3 to RDS with Fallback to AWS Glue using Dockerized Python Application

# Project Overview

Data Ingestion from S3 to RDS with Fallback to AWS Glue using Dockerized Python Application is a cloud-based data ingestion pipeline that automatically reads CSV data from Amazon S3 and loads it into an Amazon RDS MySQL database using a Dockerized Python application.

The application uses Python, Pandas, Boto3, SQLAlchemy, and PyMySQL to process and transfer the data. Under normal conditions, the CSV records are successfully inserted into RDS. If the RDS database is unavailable or the data insertion fails, the application automatically uses AWS Glue Data Catalog as a fallback and registers the S3 dataset as an external table.

This project demonstrates practical implementation of AWS cloud services, Python data processing, Docker containerization, database integration, error handling, and fallback architecture.

---

# Technology Stack

| Technology                | Purpose                               |
| ------------------------- | ------------------------------------- |
| **Python 3.12**           | Data ingestion and processing         |
| **Pandas**                | Reading and processing CSV data       |
| **Boto3**                 | Interacting with AWS S3 and Glue      |
| **SQLAlchemy**            | RDS database connectivity             |
| **PyMySQL**               | MySQL database driver                 |
| **Docker**                | Containerizing the Python application |
| **Amazon S3**             | Source storage for CSV files          |
| **Amazon RDS MySQL**      | Primary database for storing records  |
| **AWS Glue Data Catalog** | Fallback external table catalog       |
| **AWS IAM**               | Access control and permissions        |
| **GitHub**                | Source code and project repository    |
| **Linux/Ubuntu**          | Application execution environment     |

---

# Architechtural Diagram


<img width="1536" height="1024" alt="ChatGPT Image Aug 18, 2026, 03_08_45 PM" src="https://github.com/user-attachments/assets/c5bcc1a9-120d-4191-bd4e-fca5c3183f5d" />


----

# Prerequisites

Before implementing the project, ensure the following are available:

Software
 - Python 3.12 or later
 -  Docker
 -  Git
 -  MySQL Client
 -  Linux/Ubuntu environment or an EC2 instance
 - AWS CLI (recommended)

Verify installations:

- python3 --version
- docker --version
- git --version
- aws --version
- mysql --version

---

# Installation Steps

Follow these steps to prepare the environment for the Data Ingestion from S3 to RDS with Fallback to AWS Glue using Dockerized Python Application project.

## 1. Clone the GitHub Repository

Clone the project repository to your Linux/Ubuntu system or EC2 instance.

    git clone <YOUR-GITHUB-REPOSITORY-URL>

Navigate to the project directory:

      cd Data-Ingestion-S3-RDS-Glue

Verify the project files:

       ls

You should see:

 - app.py
 - Dockerfile
 - requirements.txt
 - README.md
 -.gitignore
 - screenshots

---

## 2. Update the System

Update the Ubuntu package repository:

      sudo apt update
      sudo apt upgrade -y

---

## 3. Install Python

Install Python and required development tools:

       sudo apt install python3 python3-pip python3-venv -y

Verify:

        python3 --version
        pip3 --version

The Python version should be 3.12 or later.

---

## 4. Create a Python Virtual Environment

Inside the project directory:
 
        python3 -m venv venv
  
Activate the virtual environment:

       source venv/bin/activate

You should see:

     (venv)

at the beginning of your terminal prompt.

---

## 5. Install Python Dependencies

The project uses Pandas, Boto3, SQLAlchemy, and PyMySQL.

Install them using:

       pip install -r requirements.txt

Verify:

       pip list

The required packages should be displayed.

---

## 6. Install Docker

Install Docker if it is not already available:

     sudo apt update
     sudo apt install docker.io -y

Start Docker:

     sudo systemctl start docker

Enable Docker at system startup:

     sudo systemctl enable docker

Check Docker:

    docker --version

If your user gets a permission error when running Docker, add the user to the Docker group:

    sudo usermod -aG docker $USER

Log out and log back in for the change to take effect.

---

## 7. Install Git

If Git is not installed:

   sudo apt install git -y

Verify:

    git --version

---

## 8. Install MySQL Client

The MySQL client is useful for testing the RDS connection and verifying inserted records.

   sudo apt install mysql-client -y

Verify:

    mysql --version

---

## 9. Install and Configure AWS CLI

Install AWS CLI:

  sudo apt install awscli -y

Verify:

  aws --version

If you are using AWS access keys:

  aws configure

Enter the required information:

AWS Access Key ID:
AWS Secret Access Key:
Default region name:
Default output format:
 
If the application runs on an EC2 instance, an IAM role attached to the EC2 instance is preferred over storing long-term access keys.

---

# Project Structure

The project is organized into application code, Docker configuration, dependencies, documentation, and screenshots.

```text
S3-RDS-Glue-Fallback-Data-Ingestion/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── customers.csv
├── .gitignore
├── README.md
├── Summary Report.md
├── LICENSE
│
└── screenshots/
    ├── 01-s3-csv-upload.png
    ├── 02-docker-image-build.png
    ├── 03-docker-container-running.png
    ├── 04-container-logs-rds-success.png
    ├── 05-rds-records.png
    └── 06-glue-table-fallback.png
```
---

# Implementation Steps

## 1. Launch EC2 Instance

Launch an Ubuntu EC2 instance in us-east-1.
Attach the IAM role project5-ec2-role.
Allow SSH access through port 22.
Connect to the instance using your .pem key.

<img width="1916" height="1012" alt="image" src="https://github.com/user-attachments/assets/e3359977-61e9-4b04-a663-d3ec6f34d4fe" />

---

## 2. Install Required Tools

Install and verify:

    sudo apt update
    sudo apt install -y awscli python3-pip mysql-client

Verify:

    aws --version
    python3 --version
    pip3 --version
    docker --version

<img width="1369" height="793" alt="image" src="https://github.com/user-attachments/assets/04ab4191-f2f9-4564-a7e6-3f0d90f64143" />

---

## 3. Verify IAM Role

      aws sts get-caller-identity

Confirm that the output shows:

      assumed-role/project5-ec2-role

<img width="1916" height="1021" alt="image" src="https://github.com/user-attachments/assets/0f68b052-6217-4a98-a80c-0eb55841f7fb" />

---

## 4. Create S3 Bucket

Create the bucket:

     project5-data-ingestion-2026-vaishnavi

Use:

Region: us-east-1
Bucket type: General purpose
Object Ownership: Bucket owner enforced
Block Public Access: Enabled
Versioning: Enabled
Encryption: SSE-S3

<img width="1920" height="1080" alt="Screenshot 2026-08-17 163038" src="https://github.com/user-attachments/assets/5c864bd4-50eb-41fe-8ec7-856c42acfa8f" />


---

## 5. Create CSV File

Create:

           customers.csv

Example:

        id,name,email,city
        1,Vaishnavi,vaishnavi@example.com,Pune
        2,Rahul,rahul@example.com,Mumbai
        3,Priya,priya@example.com,Nashik
        4,Amit,amit@example.com,Nagpur
        5,Neha,neha@example.com,Aurangabad

Use 10–20 records.

---

## 6. Upload CSV to S3

Create the folder:

        data/

Upload:

      customers.csv

<img width="1920" height="1080" alt="Screenshot 2026-08-17 164028" src="https://github.com/user-attachments/assets/c6a5ebac-148c-42fc-bc53-f8e5916fc332" />


Final location:

   s3://project5-data-ingestion-2026-vaishnavi/data/customers.csv

Verify:

   aws s3 ls s3://project5-data-ingestion-2026-vaishnavi/data/

<img width="976" height="121" alt="image" src="https://github.com/user-attachments/assets/01629c45-530b-4d25-bd7d-de2f002acc2b" />

---

## 7. Test S3 Access from EC2

        mkdir -p ~/project5/test

Download:

         aws s3 cp \
        s3://project5-data-ingestion-2026-vaishnavi/data/customers.csv \
        ~/project5/test/customers.csv

Verify:

        cat ~/project5/test/customers.csv

<img width="1348" height="592" alt="image" src="https://github.com/user-attachments/assets/4ae50971-527e-40ec-a885-67cedad01a12" />

---

## 8. Create RDS MySQL

Create an RDS MySQL database with:

Engine: MySQL
Creation method: Full configuration
Template: Free tier
DB identifier: project5-rds
Username: admin
Database: projectdb
Port: 3306

Use a strong password.

Keep:

Public access: No

<img width="1918" height="1018" alt="image" src="https://github.com/user-attachments/assets/fe92f6c8-5c9f-417e-96f2-67b3880c6af5" />

---

## 9. Configure RDS Security Group

Create:

project5-rds-sg

Inbound:

Type: MySQL/Aurora
Port: 3306
Source: EC2 Security Group

Avoid opening:

0.0.0.0/0

<img width="1916" height="1021" alt="image" src="https://github.com/user-attachments/assets/d0992322-f30f-4de6-8320-30ef468c57d4" />

---

## 10. Test RDS Connectivity

From EC2:
 
     nc -zv project5-rds.cmvikomsaif1.us-east-1.rds.amazonaws.com 3306

Then connect:

     mysql \
     -h project5-rds.cmvikomsaif1.us-east-1.rds.amazonaws.com \
     -P 3306 \
     -u admin \
     -p

<img width="1452" height="216" alt="image" src="https://github.com/user-attachments/assets/2c8b68bd-9e86-43c7-bc34-c09448c11690" />

---

## 11. Verify RDS Database
       
       SHOW DATABASES;

Select:

       USE projectdb;

Create the table if required:

      CREATE TABLE customers (
      id INT,
      name VARCHAR(100),
      email VARCHAR(150),
      city VARCHAR(100)
      );

<img width="1050" height="805" alt="image" src="https://github.com/user-attachments/assets/0a237f40-cdd4-4efb-8e05-8b85ca99e1fa" />

---

## 12. Create Project Directory

     mkdir -p ~/project5
     cd ~/project5

Create:

   touch app.py Dockerfile requirements.txt .gitignore README.md

---

## 13. Create requirements.txt

Add:

boto3
pandas
sqlalchemy
pymysql

<img width="1395" height="339" alt="image" src="https://github.com/user-attachments/assets/e1014a55-1e54-4b29-b16f-f94ad3f20c36" />

---

## 14. Create Dockerfile

Use
FROM python:3.12-slim


WORKDIR /app


COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt


COPY app.py .


CMD ["python", "app.py"]

<img width="1583" height="556" alt="image" src="https://github.com/user-attachments/assets/71967725-5c43-45fe-8611-19d738518b45" />

---

## 15. Build Docker Image

   docker build -t project5-data-ingestion:latest .

Verify:

  docker images

<img width="1157" height="287" alt="image" src="https://github.com/user-attachments/assets/db47e6af-bedc-4e59-a125-14404dda3f51" />

---

## 16. Run Docker Application

Run the container with the required environment variables:

docker run --rm \
-e AWS_REGION=us-east-1 \
-e S3_BUCKET=project5-data-ingestion-2026-vaishnavi \
-e S3_KEY=data/customers.csv \
-e RDS_HOST=project5-rds.cmvikomsaif1.us-east-1.rds.amazonaws.com \
-e RDS_USER=admin \
-e RDS_PASSWORD='YOUR_PASSWORD' \
-e RDS_DATABASE=projectdb \
-e RDS_TABLE=customers \
-e GLUE_DATABASE=project5_glue_db \
-e GLUE_TABLE=customers \
-e GLUE_S3_LOCATION=s3://project5-data-ingestion-2026-vaishnavi/data/ \
project5-data-ingestion:latest

<img width="1297" height="850" alt="image" src="https://github.com/user-attachments/assets/178ddf4b-bc62-4db6-a089-d9f0c367b9f6" />

---

## 17. Verify RDS Upload

Connect to RDS:

  mysql -h project5-rds.cmvikomsaif1.us-east-1.rds.amazonaws.com \
  -P 3306 -u admin -p

Run:

USE projectdb;

Then:

SELECT * FROM customers;

Verify:

SELECT COUNT(*) FROM customers;

Expected:

15

<img width="1593" height="900" alt="image" src="https://github.com/user-attachments/assets/b8675f16-40b1-4f4f-9339-1643c5f09d14" />

---

## 18. Create AWS Glue Database

Create:

               project5_glue_db

Verify:
 
               aws glue get-databases

<img width="1140" height="527" alt="image" src="https://github.com/user-attachments/assets/1a57d617-14fa-4c14-9065-f326880ada58" />

---

## 19. Test Glue Fallback

Temporarily use an invalid RDS endpoint:

            RDS_HOST=invalid-rds-endpoint

Run the Docker container again.

The application should:

Attempt RDS
   ↓
RDS connection fails
   ↓
Catch exception
   ↓
Activate Glue fallback
   ↓
Create Glue table
   ↓
Register S3 location

---

## 20. Verify Glue Table

aws glue get-table \
--database-name project5_glue_db \
--name customers \
--query 'Table.[Name,TableType,StorageDescriptor.Location]' \
--output table

Verify:

customers
EXTERNAL_TABLE
s3://project5-data-ingestion-2026-vaishnavi/data/

<img width="971" height="255" alt="image" src="https://github.com/user-attachments/assets/b6f45e95-d8d8-4fbc-841c-ccf1aac39eaa" />

---

# Result

The Data Ingestion from S3 to RDS with Fallback to AWS Glue using Dockerized Python Application was successfully implemented.

The customers.csv file containing 15 customer records was successfully uploaded to Amazon S3.
The Dockerized Python application successfully downloaded and processed the CSV file using Pandas and Boto3.
The application successfully connected to the RDS MySQL database and inserted all 15 records into the customers table.
The RDS result was verified using SELECT COUNT(*), which returned 15 records.
A Docker image named project5-data-ingestion:latest was successfully built and executed.
AWS Glue was configured as the fallback mechanism.
The Glue database project5_glue_db and external table customers were successfully created.
The Glue table was successfully registered with the S3 location:
s3://project5-data-ingestion-2026-vaishnavi/data/
The complete workflow was verified as:

S3 CSV
   ↓
Dockerized Python Application
   ↓
RDS MySQL
   ↓
15 Records Successfully Inserted


RDS Failure
   ↓
AWS Glue Data Catalog
   ↓
External Table → S3 Dataset

Therefore, the project successfully demonstrates S3 data ingestion, RDS database loading, Docker containerization, and AWS Glue fallback for reliable data processing.

----

# Conclusion

The Data Ingestion from S3 to RDS with Fallback to AWS Glue using Dockerized Python Application was successfully implemented as a reliable cloud-based data ingestion pipeline.

The project demonstrates how a Python application running inside a Docker container can retrieve CSV data from Amazon S3, process the data using Pandas, and load it into an Amazon RDS MySQL database. The successful insertion and verification of 15 customer records confirm that the primary data ingestion workflow is working correctly.

A fallback mechanism using AWS Glue Data Catalog was also implemented. When the RDS operation is unavailable or fails, the application can register the S3 dataset as an external Glue table. This ensures that the data remains accessible through the S3-based data catalog even when the primary relational database cannot be used.

Docker provides portability and consistency by packaging the Python application and its dependencies into a single container image. The use of Boto3, SQLAlchemy, PyMySQL, and Pandas demonstrates practical integration between Python and AWS services.

The project also demonstrates important AWS security practices, including the use of an IAM role for EC2, private S3 storage, restricted RDS network access, and avoiding hard-coded AWS credentials in the application.

Overall, the project successfully demonstrates cloud data ingestion, database integration, containerization, AWS service integration, fault tolerance, and secure AWS authentication. It provides a practical foundation for building larger and more reliable data-processing pipelines in real-world cloud environments.


