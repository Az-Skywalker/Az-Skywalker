FROM ubuntu:latest

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Update and install required packages
RUN apt update && apt upgrade -y \
    && apt install -y git build-essential python3.12 python3.12-venv python3-pip python3-dev libffi-dev \
    && pip install --upgrade pip setuptools wheel \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /root

# Clone the repository
RUN git clone https://github.com/Az-Skywalker/Az-Skywalker-Dev.git

# Change to the python source directory
WORKDIR /root/Az-Skywalker-Dev/src/python

# Create and activate virtual environment
RUN python3 -m venv sky \
    && /bin/bash -c "source sky/bin/activate && pip install -r requirements.txt"

# Start a bash shell when the container runs
CMD ["/bin/bash"]