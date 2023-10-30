# Use an official Python runtime as a parent image
FROM python:3.8-slim


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY app.py /app

# Copy the requirements file into the container at /app
COPY requirements.txt /app

# Upgrade pip
RUN pip install --upgrade pip


# Download the NLTK stopwords resource
#RUN python -m nltk.downloader stopwords

# Install any needed packages specified in requirements.txt
#RUN pip install -r requirements.txt


# Copy the requirements file into the Docker image
COPY requirements.txt /tmp/

# Install the required Python packages
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Download the NLTK stopwords resource
RUN python -m nltk.downloader stopwords


# Make port 7860 available to the world outside this container
EXPOSE 7860

# Run app.py when the container launches
CMD ["python", "app.py"]
