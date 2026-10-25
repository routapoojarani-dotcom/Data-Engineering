FROM bitnami/spark:3.1.2

USER root

WORKDIR /app

COPY etl_job.py /app/
COPY redshift-jdbc42-2.1.0.1.jar /app/

# Install boto3 using the system Python
RUN apt-get update && apt-get install -y python3-pip && pip3 install boto3

ENV PYSPARK_PYTHON=python3

USER 1001

CMD ["spark-submit", "--jars", "redshift-jdbc42-2.1.0.1.jar", "etl_job.py"]