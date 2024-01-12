#!/usr/bin/python3
""" Fabric script based on the file 1-pack_web_static.py that distributes an
    archive to the web servers
"""
from fabric.api import task, local, env, put, run
from datetime import datetime
import os

env.hosts = ['54.146.10.116', '54.209.206.165']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/id_rsa'

@task
def do_pack():
    """ Generates a .tgz archive from the contents of the web_static folder.
    """
    formatted_dt = datetime.now().strftime('%Y%m%d%H%M%S')
    mkdir = "mkdir -p versions"
    path = "versions/web_static_{}.tgz".format(formatted_dt)
    print("Packing web_static to {}".format(path))
    if local("{} && tar -cvzf {} web_static".format(mkdir, path)).succeeded:
        return path
    return None

@task
def do_deploy(archive_path):
    """ Deploy package to remote server.

        Arguments:
            archive_path: Path to archive to deploy.
    """
    try:
        if not os.path.exists(archive_path):
            return False
        fn_with_ext = os.path.basename(archive_path)
        fn_no_ext, ext = os.path.splitext(fn_with_ext)
        dpath = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("sudo rm -rf {}{}/".format(dpath, fn_no_ext))
        run("sudo mkdir -p {}{}/".format(dpath, fn_no_ext))
        run("sudo tar -xzf /tmp/{} -C {}{}/".format(fn_with_ext, dpath, fn_no_ext))
        run("sudo rm /tmp/{}".format(fn_with_ext))
        run("sudo mv {0}{1}/web_static/* {0}{1}/".format(dpath, fn_no_ext))
        run("sudo rm -rf {}{}/web_static".format(dpath, fn_no_ext))
        run("sudo rm -rf /data/web_static/current")
        run("sudo ln -s {}{}/ /data/web_static/current".format(dpath, fn_no_ext))
        print("New version deployed!")
        return True
    except Exception:
        return False

@task
def deploy():
    """ The deploy method.
    """
    path = do_pack()
    if path is None:
        print("Error: Unable to create archive.")
        return False

    if do_deploy(path):
        print("Deployment successful!")
        return True
    else:
        print("Error: Deployment failed.")
        return False

