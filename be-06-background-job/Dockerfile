FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY be-06-background-job/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY be-06-background-job/app ./app
COPY be-06-background-job/worker ./worker

# Copy BE-07 LLM pipeline (read-only)
COPY be-07-llm/src ./be-07-llm/src
COPY be-07-llm/prompts ./be-07-llm/prompts

# Create logs directory
RUN mkdir -p /app/logs

# Expose port
EXPOSE 8000

# Default command (can be overridden in docker-compose)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]