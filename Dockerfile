
# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the notebooks and scripts into the container
COPY notebooks/ ./notebooks/
COPY scripts/ ./scripts/

# Expose the port Jupyter will run on
EXPOSE 8888

# Run Jupyter Lab when the container starts
CMD ["jupyter", "lab", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
