#!/usr/bin/python3
"""Module that generates an archive of
web static
"""
from datetime import datetime
from fabric.api import local


def do_pack():
    """Function that compresses web_static
    to generate an archive
    """
    # location for the archive
    local("mkdir -p versions/")

    current_time = datetime.now()
    archive = "versions/web_static_{}.tgz".format(
        current_time.strftime("%Y%m%d%H%M%S"))

    # archiving process
    result = local("tar -cvzf {} {}".format(archive, "web_static"))

    # check for success
    if result.succeeded:
        return archive
