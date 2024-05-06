# Use an official Python runtime as a base image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR my_app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc curl gnupg2 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="${PATH}:/root/.local/bin"

# Copy the pyproject.toml (and optionally poetry.lock) file into the container
COPY pyproject.toml poetry.lock* ./

# Configure Poetry: Do not create a virtual environment as the container itself provides isolation
RUN poetry config virtualenvs.create false

# Install dependencies using Poetry
RUN poetry install --no-dev

COPY ./ /my_app

CMD ["python", "main.py"]