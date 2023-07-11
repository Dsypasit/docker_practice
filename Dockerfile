# Use a base image
FROM ubuntu:latest

# Update package lists and install Vim
RUN apt-get update && apt-get install -y vim

# Set the default command to run when the container starts
CMD ["/bin/bash"]
