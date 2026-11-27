FROM python:3.12-slim-trixie

WORKDIR /app

# Apply Debian security and package updates
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and setuptools
RUN python -m pip install --no-cache-dir --upgrade "pip>=26.2.0" "setuptools>=84.1.0"

# Install application dependencies
COPY application/requirements.txt ./requirements.txt

RUN python -m pip install --no-cache-dir -r requirements.txt

# Create a dedicated non-root user
RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --create-home appuser

# Copy application files with correct ownership
COPY --chown=appuser:appuser application/app/ ./app/

# Run as non-root user
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
