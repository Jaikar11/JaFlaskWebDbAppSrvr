#!/bin/bash
# This is a pre-run script to build /tag docmer image and push the image to GCR container
set -x

sudo cat acg_gcp_serviceaccount.json | tr -s '\n' ' ' > gcp_key.json
sudo chmod 444 gcp_key.json
PROJECT_ID=$(sudo cat gcp_key.json | grep -o '"project_id": "[^"]*' | grep -o '[^"]*$')
echo "Project_ID --> " $PROJECT_ID
REPO_ID="ja-repo-$PROJECT_ID"
echo "Repo Id --> " $REPO_IDi

#Authenticate Gcloud Service Account
gcloud auth activate-service-account cli-service-account-1@$PROJECT_ID.iam.gserviceaccount.com --key-file=gcp_key.json --project=$PROJECT_ID

gcloud auth configure-docker us-central1-docker.pkg.dev -q # -q given to be quiet to avoid prompt

#Tag Flask App Docker Image in GCP Artifact/GCR format
docker tag flask-app us-central1-docker.pkg.dev/$PROJECT_ID/$REPO_ID/flask-app:staging

#Push Docker Image to GCR Artifact Repository 
docker push us-central1-docker.pkg.dev/$PROJECT_ID/$REPO_ID/flask-app:staging

