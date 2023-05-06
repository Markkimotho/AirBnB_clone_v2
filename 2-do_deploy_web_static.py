#!/usr/bin/python3
"""Module that distributes an
archive to my web servers"""
from os import path
from fabric.api import run, env, put
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

        # Upload archive to remote server
        put(archive_path, '/tmp/')

        # Create folder to uncompress archive
        archive_file = archive_path.split('/')[-1]
        folder_name = archive_file.split('.')[0]
        run('sudo mkdir -p /data/web_static/releases/{}/'.format(folder_name))

        # Uncompress the archive to the folder on the web server
        run('sudo tar -xzf /tmp/{} -C /data/web_static/releases/{}/'
            .format(archive_file, folder_name))

        # Delete the archive from the web server
        run('sudo rm /tmp/{}'.format(archive_file))

        # move the content of uncompressed folder to parent folder
        run('sudo mv /data/web_static/releases/{}/web_static/* '
            '/data/web_static/releases/{}/'.format(folder_name, folder_name))

        # delete uncompressed folder
        run('sudo rm -rf /data/web_static/releases/{}/web_static'
            .format(folder_name))

        # Delete the symbolic link & Create a new symbolic link
        run('sudo rm -rf /data/web_static/current')
        run('sudo ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(folder_name))

    # Deployment succesful
        print("New version deployed!")
        return True

    # Catch exceptions if any
    except Exception as e:
        print(e)
        return False
