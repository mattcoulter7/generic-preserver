# Use the official Python image from the Docker Hub
FROM python:3.9.0-slim

# Set environment variables for non-interactive builds
ARG GIT_USERNAME
ARG GIT_PAT

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1

# Install git
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

RUN git config --global url."https://$GIT_USERNAME:$GIT_PAT@github.com/".insteadOf "https://github.com/"

# Set the working directory inside the container
WORKDIR /app

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install Poetry using pip
RUN pip install --no-cache-dir poetry

# Copy the dependencies file
COPY pyproject.toml ./

# Install dependencies
RUN poetry install --with dev --no-root

# Copy the necessary files and directories
COPY ./ ./

# Install additional package meta, such as scripts etc.
#
# Note: it may seem odd to have to poetry install calls here, but it
#       enables us to cache the docker layer for installing dependencies.
#       otherwise, each time the application code is updated, it would
#       need to re install all of the dependencies...
RUN poetry install --with dev

# run pytest
CMD ["pytest"]
