# Use Python 3.10 as the base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    GRADIO_SERVER_NAME="0.0.0.0" \
    HOME=/home/user

# Create a non-root user
RUN useradd -m -u 1000 user
WORKDIR $HOME/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY --chown=user . .

# Expose the port Gradio runs on
EXPOSE 7860

# Start the application
CMD ["python", "app.py"]
