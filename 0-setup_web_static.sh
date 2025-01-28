#!/usr/bin/env bash
#preparing the web servers

#installing nginx
sudo apt-get update
sudo apt-get install -y nginx

#create all necessary directories
mkdir -p /data/web_static/releases/test
mkdir -p /data/web_static/shared

#create index.html file
echo "<!DOCTYPE html>
<html>
  <head>
  </head>
  <body>
    ALX
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

#remove already existing symbolic link and create a new symbolic link
ln -sf /data/web_static/releases/test /data/web_static/current

# Set ownership to the 'ubuntu' user and group recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration
config='\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;}'
sed -i "38i $config" /etc/nginx/sites-available/default

# Restart Nginx to apply changes and Exit
service nginx restart
exit 0
