#!/bin/bash

# Install and setup Conda virtual environment
echo "Setting up the conda environment..."
conda create -n openagents python=3.10 -y
conda activate openagents
pip install -r backend/requirements.txt

# Check if it's a macOS or Linux environment
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS

    # MongoDB setup for macOS
    echo "Setting up MongoDB for macOS..."
    brew tap mongodb/brew
    brew update
    brew install mongodb-community@6.0
    brew services start mongodb-community@6.0

    # MongoDB collection creation
    echo "Creating MongoDB collections..."
    mongosh --eval 'db = db.getSiblingDB("xlang"); db.createCollection("user"); db.createCollection("message"); db.createCollection("conversation"); db.createCollection("folder"); db.getCollectionNames();'

    # Redis setup for macOS
    echo "Setting up Redis for macOS..."
    brew install redis
    brew services start redis
else
    # Linux

    # MongoDB setup for Linux
    wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.4.list
    sudo apt-get update
    sudo apt-get install -y mongodb-org
    sudo systemctl start mongod

    # MongoDB collection creation
    echo "Creating MongoDB collections..."
    mongosh --eval 'db = db.getSiblingDB("xlang"); db.createCollection("user"); db.createCollection("message"); db.createCollection("conversation"); db.createCollection("folder"); db.getCollectionNames();'

    # Redis setup for Linux
    echo "Setting up Redis for Linux..."
    curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list > /dev/null
    sudo apt-get update
    sudo apt-get install redis -y
    sudo systemctl start redis-server &
fi

# Setting up environment variables
echo "Setting up environment variables..."
export VARIABLE_REGISTER_BACKEND=redis
export MESSAGE_MEMORY_MANAGER_BACKEND=database
export JUPYTER_KERNEL_MEMORY_MANAGER_BACKEND=database
export MONGO_SERVER=127.0.0.1

echo "Deployment complete\!"
