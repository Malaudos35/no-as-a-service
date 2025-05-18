# Utilise une image de base Python
FROM python:3.9-slim

# Définit le répertoire de travail dans le conteneur
WORKDIR /app

# Copie les fichiers de dépendances
COPY requirements.txt .

# Installe les dépendances
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update
RUN apt-get dist-upgrade -y

# Copie le reste des fichiers de l'application
COPY ./code/ .

# Expose le port sur lequel l'application Flask écoute
EXPOSE 5000

# Commande pour exécuter l'application Flask
#CMD ["python", "app.py"]

# Commande pour exécuter l'application avec Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
