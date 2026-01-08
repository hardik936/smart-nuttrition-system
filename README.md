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
    uvicorn app:app --reload
    ```

