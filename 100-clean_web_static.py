#!/usr/bin/python3
"""deploy archive!"""
from fabric.api import *
from fabric.operations import put, run, sudo
import os.path
import os
import time
env.hosts = ['18.234.145.228', '54.157.183.178']


def do_pack():
    """compress before sending"""
    time_string = time.strftime("%Y%m%d%H%M%S")
    try:
        local("mkdir -p versions")
        local("tar -cvzf /versions/web_static_{}.tgz /web_static".
              format(time_string))
        return ("/versions/web_static_{}.tgz".format(time_string))
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
        run("sudo mkdir -p {}".format(new_path))
        run("sudo tar -xzf /tmp/{} -C {}".format(archive_filename, new_path))
        run("sudo rm /tmp/{}".format(archive_filename))
        run("sudo mv {}/web_static/* {}/".format(new_path, new_path))
        run("sudo rm -rf {}/web_static".format(new_path))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {} /data/web_static/current".format(new_path))
        return True
    except:
        return False


def deploy():
    """full deployment: create and distribute archive to the web servers"""
    created_archive = do_pack()
    if created_archive is None:
        return False
    return (do_deploy(created_archive))


def do_clean(number=0):
    """delete out-of-date archives"""
    number = 1 if int(number) == 0 else int(number)

    files = sorted(os.listdir("versions"))
    [files.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(j) for j in files)]

    with cd("data/web_static/releases"):
        files = run("ls -tr").split()
        files = [j for j in files if "web_static_" in j]
        [files.pop() for i in range(number)]
        [run("sudo rm -rf ./{}".format(j)) for j in files]
