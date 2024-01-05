# Use an Ubuntu base image

FROM ubuntu:latest



# Update package lists and install Python3

RUN apt-get update && apt-get install -y python3 python3-distutils



# Set the working directory

WORKDIR /PyDE



# Define the command to run when the container starts

CMD ["/bin/bash"]