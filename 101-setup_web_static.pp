# puppet file that sets up my web servers for the deployment of web_static

# Ensure Nginx is installed and the service is running
package { 'nginx':
  ensure => 'installed',
}

service { 'nginx':
  ensure => 'running',
}

# Create necessary directories
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Create the fake HTML file
file { '/data/web_static/releases/test/index.html':
  ensure  => 'file',
  content => 'Hello World',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

# Create the symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  force  => true,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

# Update Nginx configuration
file_line { 'hbnb_static':
  path    => '/etc/nginx/sites-available/default',
  line    => 'location /hbnb_static { alias /data/web_static/current/; }',
  match   => '^[\s]*location \/ {',
  ensure  => present,
  require => File['/data/web_static/current'],
}

# Restart Nginx
service { 'nginx':
  ensure => 'running',
  require => File_line['hbnb_static'],
}
