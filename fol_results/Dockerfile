# Use Ubuntu 18.04 as the base image
FROM ubuntu:18.04

# Set environment variable to avoid prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Update and install basic packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    wget \
    git \
    vim \
    ca-certificates \
    zsh \
    flex \
    bison \
    libssl-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget https://github.com/Kitware/CMake/releases/download/v3.31.3/cmake-3.31.3-linux-x86_64.sh
RUN chmod +x cmake-3.31.3-linux-x86_64.sh
RUN yes | ./cmake-3.31.3-linux-x86_64.sh --prefix=/opt/cmake --skip

RUN apt update
RUN yes | apt install software-properties-common
RUN add-apt-repository ppa:swi-prolog/stable
RUN apt update
RUN yes | apt install swi-prolog

# Install pyenv
RUN curl https://pyenv.run | bash

# Set up pyenv in zsh
ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PATH"

# Initialize pyenv for RUN commands
RUN eval "$(pyenv init --path)" && \
    eval "$(pyenv init -)" && \
    pyenv install 3.9 && \
    pyenv global 3.9

RUN echo 'export PATH="/opt/cmake/cmake-3.31.3-linux-x86_64/bin:$PATH"' >> /root/.bashrc && \
    echo 'export PYENV_ROOT="/root/.pyenv"' >> /root/.bashrc && \
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> /root/.bashrc && \
    echo 'eval "$(pyenv init --path)"' >> /root/.bashrc && \
    echo 'eval "$(pyenv init -)"' >> /root/.bashrc

RUN git clone https://github.com/DiPalmaGiuseppe/AIF-Project.git /root/AIF-Project

# Set a working directory
WORKDIR /root/AIF-Project/

ENV PATH="/opt/cmake/cmake-3.31.3-linux-x86_64/bin:$PATH"

RUN eval "$(pyenv init --path)" && \
    eval "$(pyenv init -)" && \
    pip install gym==0.23.0 matplotlib==3.9.2 pyswip==0.3.2 minihack==0.1.6

# Default command
CMD ["/bin/bash"]
