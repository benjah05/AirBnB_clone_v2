#!/usr/bin/python3
"""import all from fabric.api and create an archive file"""
from fabric.api import local
import time


def do_pack():
    """compress before sending"""
    time_string = time.strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -cvzf versions/web_static_{}.tgz web_static".
              format(time_string))
        return ("versions/web_static_{}.tgz".format(time_string))
    except:
        return None
