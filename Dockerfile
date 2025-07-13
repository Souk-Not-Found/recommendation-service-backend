FROM python:3.9-slim

WORKDIR /app

# Install system dependencies and clean up in one layer
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

# Use the Python module approach to run gunicorn (more reliable)
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "run:app"]
