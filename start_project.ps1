$currentDir = Get-Location

# Start Backend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$currentDir\backend'; .\venv\Scripts\Activate; uvicorn main:app --reload"

# Start Frontend
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$currentDir\frontend'; npm run dev"

Write-Host "Started Backend and Frontend in new windows."
