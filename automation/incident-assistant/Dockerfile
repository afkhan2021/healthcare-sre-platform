
FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn

RUN groupadd --gid 10001 appuser \
    && useradd --uid 10001 --gid 10001 --create-home appuser

COPY --chown=appuser:appuser automation/incident-assistant/main.py ./main.py
COPY --chown=appuser:appuser incidents/runbooks/ ./incidents/runbooks/

USER appuser

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]