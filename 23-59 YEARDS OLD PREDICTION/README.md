Create new Project
activate cloud run API and cloud builds API

gcloud builds submit --tag gcr.io/wasting-demo-test/predicts

gcloud run deploy --image gcr.io/wasting-demo-test/predicts --platform managed
