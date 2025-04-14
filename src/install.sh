#!/bin/bash

pip install -r requirements.txt

pyinstaller main.py

mv dist/main ../../main

echo "To use this service, you'll need a gemini api key"
echo "You can find your API key at https://ai.google.dev/gemini-api/docs/api-key"
echo

# Prompt user for API key
read -p "Please enter your API key: " API_KEY

touch ../../main/.env
echo "API_KEY=$API_KEY" > ../../main/.env

echo "api key added"
