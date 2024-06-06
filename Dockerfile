# Use the latest Python runtime as a parent image
FROM python:3.12.3

# Set the working directory in the container
WORKDIR /app


# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies specified in the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Command to run your application
CMD ["python", "test2.py"]