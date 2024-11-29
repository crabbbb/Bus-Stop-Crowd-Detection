# base image 
FROM jupyter/base-notebook:x86_64-ubuntu-22.04

# Switch to root user to install packages
USER root

# Update package lists and install Git and SSH client ( 1 ) 
RUN apt-get update && \ 
    apt-get install -y git openssh-client && \
    apt-get install -y libgl1-mesa-dev && \
    apt-get install -y libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Configure SSH to skip host verification for GitHub
RUN mkdir -p /root/.ssh && \ 
    touch /root/.ssh/config && \
    echo "Host github.com\n\tStrictHostKeyChecking no\n" >> /root/.ssh/config

# Set the working directory inside the container
WORKDIR /home/jovyan

COPY requirements.txt .

RUN pip install -r requirements.txt

# Switch back to default user for running the application
USER jovyan

# set environment variable - only if use this then can set direct startup with jupyther lab
ENV JUPYTER_ENABLE_LAB=yes

# port to use 
EXPOSE 8888

# start with jupyter lab
CMD ["start.sh", "jupyter", "lab"]