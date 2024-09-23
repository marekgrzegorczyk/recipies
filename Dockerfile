FROM python:3.9-alpine3.13
# Use the official Python image from the Docker Hub
LABEL maintainer="grigori9311"
# Set environment variables for the image
ENV PYTHONUNBUFFERED 1
# Disable buffering for stdout and stderr
COPY ./requirements.txt /tmp/requirements.txt
# Copy the requirements file to the /tmp directory
COPY ./app /app
# Copy the app directory to the /app directory
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# Copy the dev requirements file to the /tmp directory
WORKDIR /app
# Set the working directory to /app
EXPOSE 8000
# Expose port 8000 to the outside world (this is the port that Django runs on)
ARG DEV=false
# Define an argument called DEV with a default value of false
RUN python -m venv /py && \
    # Create a virtual environment in the /py directory using the venv module
    /py/bin/pip install --upgrade pip && \
    # Upgrade pip in the virtual environment to the latest version
    /py/bin/pip install -r /tmp/requirements.txt && \
    # Install the dependencies from the requirements file in the virtual environment \
    if [ "$DEV" = "true" ]; then \
      /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    # If the DEV argument is set to true, install the dev dependencies from the dev requirements file
    rm -rf /tmp && \
    # Remove the /tmp directory and its contents
    adduser \
    # Add a new user to the image with the following options:
      --disabled-password \
      # Do not assign a password to the user
      --no-create-home \
      # Do not create a home directory for the user
      django-user
      # Set the username of the new user to django-user

ENV PATH="/py/bin:$PATH"
# Add the /py/bin directory to the PATH environment variable
# so that the virtual environment is used by default
USER django-user
# Switch to the django-user user for security reasons