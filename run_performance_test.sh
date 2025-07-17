#!/bin/bash

# Load environment variables
source config.env

# Run Locust with specified parameters
locust -f locustfiles/locust_test.py \
  --host="$TARGET_HOST" \
  --users="$USERS" \
  --spawn-rate="$SPAWN_RATE" \
  --run-time="$RUN_TIME" \
  --headless \
  --html reports/html/performance_report.html \
  --csv=reports/html/performance_results \
  --logfile=logs/perfguard.log
