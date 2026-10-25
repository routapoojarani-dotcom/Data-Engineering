-- Public-safe S3 -> Redshift load templates.
-- Replace placeholders with environment-specific values.
-- Never commit account IDs, credentials or private bucket names.

COPY atm_data.dim_location
FROM 's3://<bucket>/dim_location/'
IAM_ROLE '<redshift-role-arn>'
DELIMITER ','
REGION '<aws-region>'
CSV;

COPY atm_data.dim_atm
FROM 's3://<bucket>/dim_atm/'
IAM_ROLE '<redshift-role-arn>'
DELIMITER ','
REGION '<aws-region>'
CSV;

COPY atm_data.dim_date
FROM 's3://<bucket>/dim_date/'
IAM_ROLE '<redshift-role-arn>'
DELIMITER ','
REGION '<aws-region>'
CSV
TIMEFORMAT 'auto';

COPY atm_data.dim_card_type
FROM 's3://<bucket>/dim_card_type/'
IAM_ROLE '<redshift-role-arn>'
DELIMITER ','
REGION '<aws-region>'
CSV;

COPY atm_data.fact_atm_trans
FROM 's3://<bucket>/fact_atm_trans/'
IAM_ROLE '<redshift-role-arn>'
DELIMITER ','
REGION '<aws-region>'
CSV;
