FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies if requirements.txt exists
RUN pip install --no-cache-dir -r requirements.txt || true

# Expose Django default port
EXPOSE 8000

# Default command to run the Django development server on all interfaces
CMD ["python", "main.py", "runserver", "0.0.0.0:8000"]