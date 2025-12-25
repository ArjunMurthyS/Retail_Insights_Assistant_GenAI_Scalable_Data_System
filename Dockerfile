FROM python:3.9-slim

WORKDIR /app

# Install system dependencies if any needed (e.g. for some python packages)
# RUN apt-get update && apt-get install -y ...

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ src/
# Note: We copy data assuming it's small enough for the Docker build context or use volume
# Ideally for 100GB+ we wouldn't COPY, but mount it. For this assignment, we'll assume mount.

ENV PYTHONPATH=/app/src
ENV PYTHONUNBUFFERED=1

CMD ["python", "src/sales_data_analysis/main.py"]
