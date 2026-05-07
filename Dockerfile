FROM python:3.13-slim

WORKDIR /app

# Installer les dépendances
COPY Requirements.txt .
RUN pip install --no-cache-dir -r Requirements.txt

# Copier le code source
COPY . .

# Initialiser la base de données
RUN python init_db.py

EXPOSE 8000

CMD ["python", "run.py"]
