FROM python:3.12-slim-trixie

WORKDIR /app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN python -m pip install --no-cache-dir --upgrade "pip>=26.2.0" "setuptools>=84.1.0"

COPY automation/incident-assistant/requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir -r requirements.txt

RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --create-home appuser

COPY --chown=appuser:appuser automation/incident-assistant/main.py ./main.py
COPY --chown=appuser:appuser incidents/runbooks/ ./incidents/runbooks/

USER appuser

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
