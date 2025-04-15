FROM python:3.11-slim

# Crée l'utilisateur
RUN useradd -m -u 1000 user

USER user

ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copie tout le contenu du projet dans /home/user/app
COPY --chown=user . $HOME/app

# Installer les dépendances
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose le port de FastAPI
EXPOSE 7860

# Lancer FastAPI (avec --reload désactivé pour prod ; à garder pour dev uniquement)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860", "--reload"]
