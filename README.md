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

app.py
Dockerfile
requirements.txt
README.md
.gitignore
screenshots

## 2. Update the System

Update the Ubuntu package repository:

sudo apt update
sudo apt upgrade -y

## 3. Install Python

Install Python and required development tools:

sudo apt install python3 python3-pip python3-venv -y

Verify:

python3 --version
pip3 --version

The Python version should be 3.12 or later.

## 4. Create a Python Virtual Environment

Inside the project directory:

python3 -m venv venv

Activate the virtual environment:

source venv/bin/activate

You should see:

(venv)

at the beginning of your terminal prompt.

## 5. Install Python Dependencies

The project uses Pandas, Boto3, SQLAlchemy, and PyMySQL.

Install them using:

pip install -r requirements.txt

Verify:

pip list

The required packages should be displayed.

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

## 7. Install Git

If Git is not installed:

sudo apt install git -y

Verify:

git --version

## 8. Install MySQL Client

The MySQL client is useful for testing the RDS connection and verifying inserted records.

sudo apt install mysql-client -y

Verify:

mysql --version

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

Data-Ingestion-S3-RDS-Glue/
│
├── app.py
│
├── Dockerfile
│
├── requirements.txt
│
├── .gitignore
│
├── README.md
│
└── screenshots/
    │
    ├── 01-s3-csv-upload.png
    ├── 02-docker-image-build.png
    ├── 03-docker-container-running.png
    ├── 04-container-logs-rds-success.png
    ├── 05-rds-records.png
    └── 06-glue-table-fallback.png

---




