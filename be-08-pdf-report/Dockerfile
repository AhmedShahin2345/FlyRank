FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for PostgreSQL and ReportLab
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY be-08-pdf-report/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY be-08-pdf-report/app ./app
COPY be-08-pdf-report/worker ./worker

# Create output directory
RUN mkdir -p /app/output/reports

# Expose port
EXPOSE 8008

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8008"]