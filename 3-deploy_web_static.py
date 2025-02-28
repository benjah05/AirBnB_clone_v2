#!/usr/bin/python3
"""deploy archive!"""
from fabric.api import *
from fabric.operations import put, run, sudo
import os.path
import time
env.hosts = ['18.234.145.228', '54.157.183.178']


def do_pack():
    """compress before sending"""
    time_string = time.strftime("%Y%m%d%H%M%S")
    try:
        if os.path.isdir("versions") is False:
            if local("mkdir -p versions").failed is True:
                return None
        if local("tar -cvzf /versions/web_static_{}.tgz web_static".
                 format(time_string)).failed is True:
            return None
        return ("versions/web_static_{}.tgz".format(time_string))
    except:
        return None


def do_deploy(archive_path):
    """distribute an archive to the webservers"""
    if not os.path.isfile(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        archive_filename = archive_path.split("/")[-1]
        new_path = ("/data/web_static/releases/" + archive_filename.
                    split(".")[0])
        if run("sudo mkdir -p {}".format(new_path)).failed is True:
            return False
        if run("sudo tar -xzf /tmp/{} -C {}".
                format(archive_filename, new_path)).failed is True:
            return False
        if run("sudo rm /tmp/{}".format(archive_filename)).failed is True:
            return False
        if run("sudo mv {}/web_static/* {}/".
                format(new_path, new_path)).failed is True:
            return False
        if run("sudo rm -rf {}/web_static".format(new_path)).failed is True:
            return False
        if run("sudo rm -rf /data/web_static/current").failed is True:
            return False
        if run("sudo ln -s {} /data/web_static/current".
                format(new_path)).failed is True:
            return False
        return True
    except:
        return False


def deploy():
    """full deployment: create and distribute archive to the web servers"""
    created_archive = do_pack()
    if created_archive is None:
        return False
    return (do_deploy(created_archive))
