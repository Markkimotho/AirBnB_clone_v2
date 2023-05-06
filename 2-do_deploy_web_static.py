#!/usr/bin/python3
"""Module that distributes an
archive to my web servers"""
from os import path
from fabric.api import local, run, env, put
from datetime import datetime


env.hosts = ['54.197.21.216', '100.25.138.59']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_path):
    """Function that deploys the compressed
    archive on local to remote servers
    """ 
    # Check if file exists
    if not path.exists(archive_path):
        return False

    try:

        # Upload archive to server
        put(archive_path, '/tmp/')

        # Uncompress the archive to the folder on the web server
        archive_file = archive_path.split('/')[-1]
        folder_name = archive_file.split('.')[0]
        run('sudo mkdir -p /data/web_static/releases/{}/'.format(folder_name))
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(\
            archive_file, folder_name))
        run('sudo rm /tmp/{}'.format(archive_file))
