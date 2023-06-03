#!/usr/bin/env bash
# Bash script that sets up my web servers for the deployment of web_static

# Installing Nginx
sudo apt-get -y update
sudo apt-get -y install nginx

# Creating files
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

# html file for testing Nginx config
echo "
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# File permissions
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx config 
sudo sed -i '/server {/a \
    location /hbnb_static/ {\
        alias /data/web_static/current/;\
    }' /etc/nginx/sites-available/default

# Restart Nginx to update changes
sudo service nginx restart
