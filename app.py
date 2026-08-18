import os
import io
import boto3
import pandas as pd
from sqlalchemy import create_engine


# --------------------------------------------------
# Environment Variables
# --------------------------------------------------

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

S3_BUCKET = os.getenv("S3_BUCKET")
S3_KEY = os.getenv("S3_KEY")

RDS_HOST = os.getenv("RDS_HOST")
RDS_USER = os.getenv("RDS_USER")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_DATABASE = os.getenv("RDS_DATABASE")
RDS_TABLE = os.getenv("RDS_TABLE", "customers")

GLUE_DATABASE = os.getenv("GLUE_DATABASE", "project5_glue_db")
GLUE_TABLE = os.getenv("GLUE_TABLE", "customers")
GLUE_S3_LOCATION = os.getenv("GLUE_S3_LOCATION")


# --------------------------------------------------
# AWS Clients
# --------------------------------------------------

s3_client = boto3.client("s3", region_name=AWS_REGION)
glue_client = boto3.client("glue", region_name=AWS_REGION)


# --------------------------------------------------
# Read CSV from S3
# --------------------------------------------------

def read_csv_from_s3():

    print("Reading CSV file from S3...")

    response = s3_client.get_object(
        Bucket=S3_BUCKET,
        Key=S3_KEY
    )

    data = response["Body"].read()

    df = pd.read_csv(io.BytesIO(data))

    print(f"Successfully read {len(df)} records from S3.")

    return df


# --------------------------------------------------
# Load Data into RDS
# --------------------------------------------------

def load_to_rds(df):

    print("Connecting to RDS MySQL...")

    connection_string = (
        f"mysql+pymysql://{RDS_USER}:{RDS_PASSWORD}"
        f"@{RDS_HOST}:3306/{RDS_DATABASE}"
    )

    engine = create_engine(connection_string)

    df.to_sql(
        RDS_TABLE,
        con=engine,
        if_exists="append",
        index=False
    )

    print(
        f"Successfully inserted {len(df)} records "
        f"into RDS table '{RDS_TABLE}'."
    )


# --------------------------------------------------
# AWS Glue Fallback
# --------------------------------------------------

def glue_fallback():

    print("RDS ingestion failed.")
    print("Activating AWS Glue fallback...")

    # Create Glue database if it does not exist
    try:

        glue_client.get_database(
            Name=GLUE_DATABASE
        )

        print(
            f"Glue database '{GLUE_DATABASE}' already exists."
        )

    except glue_client.exceptions.EntityNotFoundException:

        glue_client.create_database(
            DatabaseInput={
                "Name": GLUE_DATABASE,
                "Description": "Fallback database for S3 data ingestion"
            }
        )

        print(
            f"Created Glue database '{GLUE_DATABASE}'."
        )

    # Create external Glue table

    table_input = {
        "Name": GLUE_TABLE,

        "TableType": "EXTERNAL_TABLE",

        "Parameters": {
            "classification": "csv",
            "typeOfData": "file"
        },

        "StorageDescriptor": {
            "Columns": [
                {
                    "Name": "id",
                    "Type": "int"
                },
                {
                    "Name": "name",
                    "Type": "string"
                },
                {
                    "Name": "email",
                    "Type": "string"
                },
                {
                    "Name": "city",
                    "Type": "string"
                }
            ],

            "Location": GLUE_S3_LOCATION,

            "InputFormat": (
                "org.apache.hadoop.mapred.TextInputFormat"
            ),

            "OutputFormat": (
                "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"
            ),

            "SerdeInfo": {
                "SerializationLibrary": (
                    "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe"
                ),

                "Parameters": {
                    "field.delim": ",",
                    "skip.header.line.count": "1"
                }
            }
        }
    }

    try:

        glue_client.create_table(
            DatabaseName=GLUE_DATABASE,
            TableInput=table_input
        )

        print(
            f"Glue external table '{GLUE_TABLE}' created successfully."
        )

    except glue_client.exceptions.AlreadyExistsException:

        print(
            f"Glue table '{GLUE_TABLE}' already exists."
        )


# --------------------------------------------------
# Main Application
# --------------------------------------------------

def main():

    print("=" * 60)
    print("S3 → RDS Data Ingestion Application")
    print("=" * 60)

    try:

        # Step 1: Read CSV from S3
        df = read_csv_from_s3()

        # Step 2: Load into RDS
        load_to_rds(df)

        print("=" * 60)
        print("DATA INGESTION SUCCESSFUL")
        print("=" * 60)

    except Exception as error:

        print(f"RDS ingestion error: {error}")

        try:

            glue_fallback()

            print("=" * 60)
            print("GLUE FALLBACK COMPLETED")
            print("=" * 60)

        except Exception as glue_error:

            print(
                f"Glue fallback also failed: {glue_error}"
            )

            raise


if __name__ == "__main__":
    main()
