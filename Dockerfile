# Use the official Python base image
FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Start the application
CMD ["python", "flask_app.py"]
