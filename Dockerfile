# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install Tesseract OCR for label scanning
RUN apt-get update && apt-get install -y tesseract-ocr && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
