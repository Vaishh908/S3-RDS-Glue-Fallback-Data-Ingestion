
### 1. Data Flow: S3 → RDS → Glue Fallback

The project implements a reliable data ingestion pipeline in which CSV data is first stored in **Amazon S3** and then processed by a Dockerized Python application.

```text
CSV File
   │
   ▼
Amazon S3
   │
   ▼
Dockerized Python Application
   │
   ▼
Pandas + Boto3
   │
   ▼
Amazon RDS MySQL
   │
   ├── Success ──► Data inserted into RDS
   │
   └── Failure
          │
          ▼
     AWS Glue Data Catalog
          │
          ▼
     External Table
          │
          ▼
       S3 Dataset
```

The process starts when a CSV file containing customer records is uploaded to an S3 bucket. The Python application running inside a Docker container uses **Boto3** to retrieve the CSV file from S3. **Pandas** reads and processes the CSV data.

Under normal conditions, the application connects to **Amazon RDS MySQL** using **SQLAlchemy and PyMySQL** and inserts the processed records into the `customers` table.

If the RDS connection or data insertion fails, the application catches the error and activates the **AWS Glue fallback**. The application creates or accesses a Glue database and registers the S3 dataset as an external table.

This approach improves reliability because the original dataset remains safely stored in S3 and can still be cataloged through AWS Glue when RDS is unavailable.

---

### 2. AWS Services Used

| AWS Service | Purpose |
|---|---|
| **Amazon S3** | Stores the source CSV file containing customer data. |
| **Amazon RDS MySQL** | Primary database used to store the processed records. |
| **AWS Glue Data Catalog** | Fallback mechanism that registers the S3 dataset as an external table. |
| **Amazon EC2** | Provides the Linux environment where Docker and the application run. |
| **AWS IAM** | Provides secure permissions for the application to access AWS services. |
| **Amazon VPC** | Provides the networking environment for EC2 and RDS. |
| **Security Groups** | Controls network access between EC2 and RDS. |

An IAM role was attached to the EC2 instance so the application could access S3 and Glue without storing long-term AWS access keys.

The RDS security group was configured to allow MySQL traffic on port **3306 only from the EC2 security group**. This avoids exposing the database directly to the public internet.

---

### 3. Docker Setup

Docker was used to containerize the Python application and its dependencies. This provides a consistent and portable execution environment.

The project structure is:

```text
S3-RDS-Glue-Fallback-Data-Ingestion/
│
├── app.py
├── Dockerfile
├── requirements.txt
├── README.md
└── LICENSE
```

The required Python dependencies are:

```text
boto3
pandas
sqlalchemy
pymysql
```

The Dockerfile uses Python 3.12:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

The Docker image was built using:

```bash
docker build -t project5-data-ingestion:latest .
```

The container was executed using environment variables for the AWS region, S3 bucket, S3 key, RDS endpoint, database credentials, and Glue configuration.

Sensitive information such as the RDS password was passed through environment variables rather than being hard-coded in the application.

---

### 4. Challenges Faced and How They Were Solved

#### Challenge 1: RDS Connectivity

The Dockerized application needed to communicate with the private RDS MySQL database. Incorrect security-group configuration could prevent the application from connecting.

**Solution:**  
The RDS security group was configured to allow inbound traffic on port **3306** from the EC2 security group only.

Connectivity was tested using:

```bash
nc -zv <RDS-ENDPOINT> 3306
```

The MySQL client was also used to verify the database connection.

---

#### Challenge 2: AWS IAM Permissions

The application required permissions to read objects from S3 and create or access AWS Glue resources.

**Solution:**  
An IAM role was attached to the EC2 instance with the required permissions. The active identity was verified using:

```bash
aws sts get-caller-identity
```

This avoided storing permanent AWS access keys inside the Docker container.

---

#### Challenge 3: RDS Failure Handling

The main challenge was ensuring that the application would not completely stop if RDS became unavailable.

**Solution:**  
Exception handling was implemented in the Python application.

```text
RDS Connection
      │
      ├── Success ──► Insert Data ──► Complete
      │
      └── Failure ──► Catch Exception
                           │
                           ▼
                    AWS Glue Fallback
                           │
                           ▼
                    Create External Table
```

The application automatically activates the Glue fallback when the RDS operation fails.

---

#### Challenge 4: Creating the Glue External Table

The Glue table required the correct database name, table schema, S3 location, CSV format, and serialization configuration.

**Solution:**  
The application uses **Boto3 and AWS Glue APIs** to create the Glue database and external table. The table references the S3 location directly, so the original data does not need to be copied.

---

### 5. Overall Result

The project successfully demonstrates a fault-tolerant AWS data ingestion workflow:

```text
                 Amazon S3
              CSV Customer Data
                     │
                     ▼
          Dockerized Python App
                     │
              ┌──────┴──────┐
              ▼             ▼
          RDS Success    RDS Failure
              │             │
              ▼             ▼
        Amazon RDS      AWS Glue
          MySQL        Data Catalog
              │             │
              ▼             ▼
        Stored Data     External Table
                            │
                            ▼
                       S3 Dataset
```

The project demonstrates practical use of AWS cloud services, Python data processing, Docker containerization, database connectivity, IAM security, error handling, and fallback architecture. The design ensures that S3 remains the reliable source of the dataset while RDS serves as the primary database and AWS Glue provides an alternative cataloging mechanism during RDS failures.
