#!/bin/bash

# Determine which pip command to use
if command -v pip &>/dev/null; then
    PIP_CMD="pip"
elif command -v pip3 &>/dev/null; then
    PIP_CMD="pip3"
else
    echo "Error: Neither pip nor pip3 was found. Please install Python and pip."
    exit 1
fi

# Install dependencies using the appropriate pip command
$PIP_CMD install -r requirements.txt

# Build the executable
pyinstaller main.py

# Create destination directory if it doesn't exist
mkdir -p ../../main

# Move the executable to destination
cp -r dist/main ../../main/ || mv dist/main ../../main/

echo "To use this service, you'll need a Gemini API key"
echo "You can find your API key at https://ai.google.dev/gemini-api/docs/api-key"
echo

# Prompt user for API key
read -p "Please enter your API key: " API_KEY

# Create or overwrite .env file
touch ../../main/.env
echo "API_KEY=$API_KEY" > ../../main/.env
echo "API key added"
