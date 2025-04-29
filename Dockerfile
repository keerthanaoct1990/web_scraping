# Use official Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the scraper code
COPY movie_scraper.py .

# Set default command
CMD ["python", "movie_scraper.py"]
