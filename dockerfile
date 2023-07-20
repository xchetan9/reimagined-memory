# Use an official Python runtime as the base image
FROM python:3

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any required dependencies for your bot
# If you have a requirements.txt file, uncomment the following line
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Define the command to run your Python script
CMD ["python3", "-m", "bot"]
