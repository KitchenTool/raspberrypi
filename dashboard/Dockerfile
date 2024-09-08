# Use the official Python base image
FROM python:3.9-slim

# Set environment variables to avoid issues with encoding
ENV PYTHONUNBUFFERED=1
ENV LANG C.UTF-8
ENV TZ=UTC
ENV NEXTCLOUD_KEY=YOUR_NEXTCLOUD_KEY

# Install cron and any required dependencies
RUN apt-get update && \
    apt-get install -y python3-pip unzip cron && \
    apt-get clean

# Install any needed packages specified in requirements.txt
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r /usr/src/app/requirements.txt
RUN playwright install firefox && playwright install-deps

# Copy the Python script into the Docker image
COPY download_images.py /usr/src/app/download_images.py

# Copy the crontab file into the Docker image
COPY crontab.txt /etc/cron.d/download_cron

# Copy the HTML files into the Docker image
COPY index.html /usr/src/app/public/

# Set permissions on the crontab file
RUN chmod 0644 /etc/cron.d/download_cron

# Apply the crontab
RUN crontab /etc/cron.d/download_cron

# Create a directory for the HTML files
RUN mkdir -p /usr/src/app/public

# Make a directory for serving files
WORKDIR /usr/src/app/public/

# Expose port 8000 for the HTTP server
EXPOSE 8000

# Command to run the cron service and HTTP server in the background
CMD pwd && ls && cron && python3 -m http.server 8000 --bind 0.0.0.0
# CMD cron && python3 /usr/src/app/download_images.py && python3 -m http.server 8000 --bind 0.0.0.0
