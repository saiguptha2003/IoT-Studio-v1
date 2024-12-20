# Step 1: Use a lightweight Python image as the base
FROM python:3.10-slim

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy the requirements file into the container
COPY requirements.txt .

# Step 4: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the application code into the container
COPY . .

# Step 6: Expose the port that your Flask app runs on
EXPOSE 5000

# Step 7: Command to run the Flask application
CMD ["python", "main.py"]
