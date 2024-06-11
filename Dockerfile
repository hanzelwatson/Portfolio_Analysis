

FROM ubuntu:24.04

# Set the non-interactive mode to avoid user interaction during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update the package list and install required packages
RUN apt-get update && \
    apt-get install -y \
    curl \
    openssl \
    python3 \
    python3-pip \
    jupyter-notebook && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

#Verify Python SSL
RUN python3 -c "import ssl; print(ssl.OPENSSL_VERSION)" 

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .


# Install the required Python packages using apt-get (pip gives SSL error)
RUN apt-get update && apt-get install -y python3-pandas
RUN apt-get update && apt-get install -y python3-flask
RUN apt-get update && apt-get install -y python3-matplotlib
RUN apt-get update && apt-get install -y python3-notebook


COPY . .

# Expose the port the notebook server and app.py run on
EXPOSE 8888 5000

CMD [ "python3", "stats.py" ]