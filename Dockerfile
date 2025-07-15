# Stage 1: Build
FROM python:3.9-slim as builder

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    pip install --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.9-alpine

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
ENV FLASK_APP=run.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]