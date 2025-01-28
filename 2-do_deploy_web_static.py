#!/usr/bin/python3
"""deploy archive!"""
from fabric.api import env
from fabric.operations import put, run, sudo
import os.path
env.hosts = ['18.234.145.228', '54.157.183.178']


def do_deploy(archive_path):
    """distribute an archive to the webservers"""
    if (os.path.isfile(archive_path) is False):
        return False
    try:
        put(archive_path, "/tmp/")
        archive_filename = archive_path.split("/")[-1]
        new_path = ("/data/web_static/releases/" + archive_filename.
              split(".")[0])
        run("sudo tar -xzf /tmp/{} -C {}".format(archive_filename, new_path))
        run("sudo rm /tmp/{}".format(archive_filename))
        run("sudo mkdir -p {}".format(new_path))
        run("sudo mv {}/web_static/* {}/".format(new_path, new_path))
        run("sudo rm -rf {}/web_static".format(new_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_path))
        return True
    except:
        return False
