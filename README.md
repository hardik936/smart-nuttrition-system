# Smart Nutrition System - AI-Enhanced, Free & Open Source

This project aims to provide a Zero-Budget Smart Nutrition System using Open Source tools and Open Data (OpenFoodFacts, USDA).

## Architecture
- **Backend**: FastAPI
- **Frontend**: React / Streamlit
- **ML**: PyTorch / Scikit-Learn
- **Database**: PostgreSQL

## Setup

1.  **Backend Environment**:
    ```bash
    cd backend
    python -m venv venv
    # Windows:
    .\venv\Scripts\Activate
    # Mac/Linux:
    # source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    - Copy `backend/.env.example` to `backend/.env`
    - Update values if necessary.

3.  **Run Backend**:
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```



## Deployment (Recommended)

For a free-friendly Render alternative, deploy on Railway using the step-by-step guide:

- [Railway Deployment Guide](docs/deploy_railway.md)



4.  **Run Frontend (optional local dev)**:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

