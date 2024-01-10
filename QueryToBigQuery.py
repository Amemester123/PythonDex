from google.cloud import bigquery
from google.oauth2 import service_account
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\final\AppData\Roaming\gcloud\application_default_credentials.json"

from google.cloud import bigquery

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
table_id = "pokemon-database-408302.movelist.moves"
file_path = r"C:\Users\final\OneDrive\Documents\df copied.csv"

job_config = bigquery.LoadJobConfig(
    source_format=bigquery.SourceFormat.CSV, skip_leading_rows=1, autodetect=True,
    write_disposition=bigquery.WriteDisposition.WRITE_APPEND  # added to have truncate and insert load
)

with open(file_path, "rb") as source_file:
    job = client.load_table_from_file(source_file, table_id, job_config=job_config)

job.result()  # Waits for the job to complete.

table = client.get_table(table_id)  # Make an API request.
print(
    "Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), table_id
    )
)