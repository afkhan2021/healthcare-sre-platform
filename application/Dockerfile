FROM python:3.12-slim-trixie


WORKDIR /app

# Apply Debian security and package updates
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools to secure versions
RUN python -m pip install --no-cache-dir --upgrade "pip>=26.2.0" "setuptools>=84.1.0"

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
