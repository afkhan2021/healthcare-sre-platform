
FROM python:3.12-slim

WORKDIR /app

# Install application dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Create a dedicated non-root user
RUN useradd --create-home appuser

# Copy application files with correct ownership
COPY --chown=appuser:appuser app/ ./app/

# Run as non-root user
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
