# Dockerfile

FROM python:3.9

# Set working directory
WORKDIR /app

# Copy application files
COPY ./app /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for FastAPI
EXPOSE 8000

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
