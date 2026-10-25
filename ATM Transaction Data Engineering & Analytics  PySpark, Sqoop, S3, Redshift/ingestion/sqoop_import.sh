#!/usr/bin/env bash
set -euo pipefail

: "${RDS_JDBC_URL:?Set RDS_JDBC_URL}"
: "${RDS_USER:?Set RDS_USER}"
: "${RDS_PASSWORD:?Set RDS_PASSWORD}"

sqoop import \
  --connect "${RDS_JDBC_URL}" \
  --table SRC_ATM_TRANS \
  --username "${RDS_USER}" \
  --password "${RDS_PASSWORD}" \
  --target-dir /user/root/SRC_ATM_TRANS \
  -m 1
