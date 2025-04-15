FROM python:3.11-slim

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Try and run pip command after setting the user with `USER user` to avoid permission issues with Python
RUN pip install --no-cache-dir --upgrade pip

# Copy the current directory contents into the container at $HOME/app setting the owner to the user
COPY --chown=user *.py $HOME/app
COPY --chown=user requirements.txt $HOME/app

# Install any other Python dependencies (e.g., from requirements.txt)
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Expose the port we run on (7860)
EXPOSE 7860

# Lancer le serveur FastAPI avec Uvicorn
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "7860"]
