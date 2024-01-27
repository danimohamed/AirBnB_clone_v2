#!/bin/bash
read -p "Enter the file to add and commit: " file
if [ -e "$file" ]; then
    git add "$file"
    read -p "Enter the commit message: " message
    git commit -m "$message"
    git push origin master
else
    echo "File not found. Please enter a valid file."
fi

