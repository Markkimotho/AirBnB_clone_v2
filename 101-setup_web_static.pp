# puppet file that sets up my web servers for the deployment of web_static
package { 'nginx':
  ensure => installed,
}

file { '/data':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/shared':
  ensure => directory,
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/data/web_static/releases/test/index.html':
  content => 'Holberton School',
  owner   => 'ubuntu',
  group   => 'ubuntu',
}

file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test/',
  owner  => 'ubuntu',
  group  => 'ubuntu',
}

file { '/etc/nginx/sites-available/default':
  ensure => present,
  source => 'puppet:///modules/mymodule/default',
}

file { '/etc/nginx/sites-enabled/default':
  ensure => 'link',
  target => '/etc/nginx/sites-available/default',
}

file { '/etc/nginx/sites-available/default':
  content => template('mymodule/nginx.conf.erb'),
}

service { 'nginx':
  ensure  => running,
  enable  => true,
  require => [
    File['/data/web_static/current'],
    File['/etc/nginx/sites-enabled/default'],
  ],
  subscribe => [
    File['/etc/nginx/sites-available/default'],
    File['/data/web_static/current'],
  ],
}
