#!/bin/bash
gcloud builds submit --tag gcr.io/gestion-documental-smadsot/sistema-smadsot && \
gcloud run deploy sistema-smadsot \
  --image gcr.io/gestion-documental-smadsot/sistema-smadsot \
  --region=us-central1 \
  --platform=managed \
  --add-cloudsql-instances=gestion-documental-smadsot:us-central1:gestion-db-smadsot
