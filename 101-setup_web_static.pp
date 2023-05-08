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

# Create the necessary directories
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create the test HTML file
file { '/data/web_static/releases/test/index.html':
  content => 'Holberton School',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create the symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
}

# Update the Nginx configuration
file { '/etc/nginx/sites-available/default':
  content => template('nginx/default.erb'),
  owner   => 'root',
  group   => 'root',
  mode    => '0644',
  notify  => Service['nginx'],
}
