FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Collect static files and run migrations (build-time secret key for manage.py commands)
RUN DJANGO_SECRET_KEY=build-placeholder python manage.py collectstatic --noinput
RUN DJANGO_SECRET_KEY=build-placeholder python manage.py migrate --noinput

# Cloud Run injects PORT env var (default 8080)
ENV PORT=8080
EXPOSE 8080

# Run with gunicorn
CMD exec gunicorn mizzou_cbc.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4
