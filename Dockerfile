FROM --platform=linux/amd64 python:3.11.4

WORKDIR /app

# Set pip configurations for better reliability
ENV PIP_DEFAULT_TIMEOUT=300 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Copy the distribution package
COPY dist/ds_service-1.0.tar.gz .

# Install base dependencies first
RUN pip install --upgrade pip setuptools wheel

# Install requests explicitly first (since it's a core dependency)
RUN pip install "requests>=2.31.0,<3.0.0"

# Install critical dependencies one by one to avoid version conflicts
RUN pip install \
    "numpy>=1.26.4,<2.0.0" \
    "pydantic>=2.10.6,<3.0.0" \
    "langchain-core>=0.1.45,<0.2.0" \
    "aiohttp>=3.9.5,<4.0.0" \
    "groq>=0.15.0" \
    "langchain-groq>=0.1.1"

# Install the distribution package
RUN pip install --no-cache-dir ds_service-1.0.tar.gz

# Set the environment variable for the Flask app
ENV FLASK_APP=src/app/__init__.py

# Expose the port
EXPOSE 8010

# Start the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=8010"]