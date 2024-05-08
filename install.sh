#!/bin/bash

# Copy the tool to /usr/local/bin
sudo cp trulier trulier.py /usr/local/bin/

# Give execute permission to the tool
sudo chmod +x /usr/local/bin/trulier
sudo chmod +x /usr/local/bin/trulier.py

# Remove the original directory
sudo rm -R "$(pwd)"

# Show successful message
echo "Your tool has been successfully installed!"
