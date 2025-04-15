# Base image with Python
FROM python:3.11-slim
# Set working directory inside container
WORKDIR /app

# Copy your project files into the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Default command
CMD ["python", "src/main.py"]
