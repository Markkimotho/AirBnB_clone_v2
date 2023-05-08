# puppet file that sets up my web servers for the deployment of web_static
# Install Nginx if it's not already installed
package { 'nginx':
  ensure => installed,
}

# Start the Nginx service
service { 'nginx':
  ensure => running,
  enable => true,
}

exec { 'server setup':
  command  => 'sudo mkdir -p /data/web_static/shared/ && sudo mkdir -p /data/web_static/releases/test/ && echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html > /dev/null && sudo ln -sf /data/web_static/releases/test/ /data/web_static/current && sudo chown -R ubuntu:ubuntu /data/ && sudo sed -i \'44i \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\' /etc/nginx/sites-available/default && sudo service nginx restart',
  provider => shell,
}
