FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files at build time
RUN DJANGO_SECRET_KEY=build-placeholder python manage.py collectstatic --noinput

# Cloud Run injects PORT env var (default 8080)
ENV PORT=8080
EXPOSE 8080

# Run migrations at startup then start gunicorn
CMD python manage.py migrate --noinput && exec gunicorn mizzou_cbc.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4
