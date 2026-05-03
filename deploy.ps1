$PROJECT = "marketresearch-495214"
$REGION = "us-central1"
$REPO = "us-central1-docker.pkg.dev/$PROJECT/marketresearch"
$SQL_INSTANCE = "$PROJECT`:$REGION`:marketresearch-db"
$API_URL = "https://api-422485581146.us-central1.run.app"
$UI_URL  = "https://ui-422485581146.us-central1.run.app"

Write-Host "Building images..." -ForegroundColor Cyan
gcloud builds submit --config cloudbuild.yaml .
if ($LASTEXITCODE -ne 0) { Write-Host "Build failed" -ForegroundColor Red; exit 1 }

Write-Host "Deploying API..." -ForegroundColor Cyan
gcloud run deploy api `
    --image "$REPO/api:latest" `
    --port 8000 `
    --region $REGION `
    --add-cloudsql-instances $SQL_INSTANCE `
    --set-secrets "DATABASE_URL=DATABASE_URL:latest,FINNHUB_API_KEY=FINNHUB_API_KEY:latest,GOOGLE_CLIENT_ID=GOOGLE_CLIENT_ID:latest,GOOGLE_CLIENT_SECRET=GOOGLE_CLIENT_SECRET:latest,GOOGLE_REDIRECT_URI=GOOGLE_REDIRECT_URI:latest,FLET_BASE_URL=FLET_BASE_URL:latest,JWT_SECRET=JWT_SECRET:latest" `
    --allow-unauthenticated `
    --platform managed
if ($LASTEXITCODE -ne 0) { Write-Host "API deploy failed" -ForegroundColor Red; exit 1 }

Write-Host "Deploying UI..." -ForegroundColor Cyan
gcloud run deploy ui `
    --image "$REPO/ui:latest" `
    --port 8550 `
    --region $REGION `
    --set-secrets "FLET_BASE_URL=FLET_BASE_URL:latest,JWT_SECRET=JWT_SECRET:latest" `
    --set-env-vars "API_BASE_URL=$API_URL,GOOGLE_AUTH_URL=$API_URL/auth/google/authorize" `
    --allow-unauthenticated `
    --min-instances 1 `
    --max-instances 1 `
    --platform managed
if ($LASTEXITCODE -ne 0) { Write-Host "UI deploy failed" -ForegroundColor Red; exit 1 }

Write-Host "Deploy complete." -ForegroundColor Green
