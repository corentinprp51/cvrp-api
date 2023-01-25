# Indicate the Gurobi reference image
FROM gurobi/python:9.5.2

# Set the application directory
WORKDIR /app

# Install the application dependencies
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the application code 
COPY . .

# Command used to start the application
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0"]