FROM python:3.13-slim

WORKDIR /app

COPY Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt

COPY . .

EXPOSE 8000

# Render injecte $PORT automatiquement
CMD gunicorn --bind 0.0.0.0:${PORT:-8000} --workers 2 run:app
