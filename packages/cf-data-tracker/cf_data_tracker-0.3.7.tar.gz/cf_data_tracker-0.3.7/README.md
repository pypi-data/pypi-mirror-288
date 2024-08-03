# CF Data Tracker
## Purpose
This packages ensembles all the functions required to manage the raw and clean files loaded in the raw and clean pipelines at CF.

## Set up
To run the package, please ensure to have the following env variables in your environment. Either you can load them using dotenv by stuffing them .env or you can set directly from terminal.

```
AWS_DEST_BUCKET_RAW=s3 bucket to save the raw data json tracker
AWS_REGION_NAME= AWS Region to connect s3
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```