# Alternative deployment path (Cloud Run, Fly.io, etc.). Modal is the
# primary target (see modal_app.py). Keep this in sync with pyproject.toml.

FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    "fastapi>=0.115" \
    "uvicorn[standard]>=0.32" \
    "pydantic>=2.9" \
    "anthropic>=0.39" \
    "python-pptx>=1.0" \
    "structlog>=24.4"

COPY . /app

ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT}"]
