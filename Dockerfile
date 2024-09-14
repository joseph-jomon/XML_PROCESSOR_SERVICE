# Dockerfile

FROM python:3.9

# Set working directory
WORKDIR ./

# Copy application files
COPY ./app /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r ./app/requirements.txt

# Install debugpy for debugging
EXPOSE 21
EXPOSE 30000-30009
EXPOSE 5678

# Default command (can be overridden in docker-compose)
CMD ["sh", "-c", "python -m debugpy --wait-for-client --listen 0.0.0.0:5678 ftp_handler.py"]
