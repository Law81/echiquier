# Image de base Python officielle et légère
FROM python:3.11-slim

# Évite que Python écrive des fichiers .pyc et bufferise les logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Définit le dossier de travail dans le conteneur
WORKDIR /app

# Crée un utilisateur non-privilégié pour la sécurité
RUN useradd -m appuser && chown -R appuser /app

# Copie d'abord les dépendances pour maximiser la mise en cache de Docker
COPY requirements.txt .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copie le reste du code source de l'application
COPY src/ ./src

# Bascule vers l'utilisateur non-privilégié
USER appuser

# Commande par défaut pour lancer l'application (exemple avec Uvicorn/FastAPI)
CMD ["python", "src/main.py"]