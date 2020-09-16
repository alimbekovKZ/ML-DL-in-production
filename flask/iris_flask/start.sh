#!/bin/bash

run_rq() {
  rq worker rest_api -u 'redis://app-redis:6379' 2>&1 | tee -a &
}

run_gunicorn() {
  gunicorn rest_api:app -b 0.0.0.0:5000 --workers=2 2>&1 | tee -a 
}

run_rq
run_gunicorn
