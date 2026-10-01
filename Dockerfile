FROM python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY scripts/aws_cost_audit.py ./scripts/aws_cost_audit.py

RUN mkdir -p /app/reports

CMD ["python", "scripts/aws_cost_audit.py"]
