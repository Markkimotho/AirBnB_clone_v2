#!/usr/bin/python3
"""Module that generates and distributes an archive
to web servers
"""
from datetime import datetime
from fabric.api import local, run, env, put
from os import path


env.hosts = ['54.197.21.216', '100.25.138.59']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """Function that compresses web_static directory
    to return an archive file path and false if otherwise
    """
    try:
        # Creates a new directory to store the archives
        if not path.exists("versions/"):
            local("mkdir -p versions/")

        current_time = datetime.now()
        archive = "versions/web_static_{}.tgz".format(
            current_time.strftime("%Y%m%d%H%M%S"))

        # archiving process
        result = local("tar -cvzf {} {}".format(archive, "web_static"))

        # check for success
        if result.succeeded:
            return archive
    except Exception as e:
        print(e)
        return False


def do_deploy(archive_path):
    """Function that deploys archive to remote
    Return True on success and False on failure
    """
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


def deploy():
    """Function that creates, compresses
    and distributes the archive to my web server
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)
