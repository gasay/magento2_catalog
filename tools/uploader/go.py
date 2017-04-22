#!/usr/bin/env python

import os
import sys
import commands
import subprocess

import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--config')
parser.add_argument('--basepath')
parser.add_argument('--env')
args = parser.parse_args()

import json
with open(args.config) as _file:
    config = json.load(_file)

basepath = args.basepath
env = args.env

userHost = "%s@%s" % (
    config['env'][env]['remote_user'],
    config['env'][env]['remote_host']
    )
remoteReleasePath = "%s/version_%s" % (
    config['env'][env]['remote_release_subpath'].rstrip('/'),
    os.popen('date \'+%y%m%d_%H%M%S\'').read().rstrip("\n")
    )


def f_Run(_command, printCommand=True, exitOnError=True):
    command = _command.rstrip("\n").strip()
    if printCommand:
        print(command)
    sys.stdout.flush()
    (status, _output) = commands.getstatusoutput(command)
    output = _output.strip().rstrip("\n")
    if output:
        print(output)
    if exitOnError and status != 0:
        sys.exit(status)
    else:
        return output


def f_WrapWithSsh(command):
    sshCommand = "ssh %s %s" % (userHost, command)
    return sshCommand


def f_WrapWithPass(command):
    passCommand = ("%s %s" % (config['env'][env]['sshpass'], command)).lstrip(' ')
    return passCommand


def f_LinkShared(subPath):
    return "ln -fs %s-current %s" % (
        os.path.join(config['env'][env]['remote_shared_path'], subPath).rstrip('/'),
        os.path.join(remoteReleasePath, subPath).rstrip('/')
        )


def f_LinkConfig():
    return "ln -fs %s %s" % (
        os.path.join(config['env'][env]['remote_config_path'], 'local-current.xml').rstrip('/'),
        os.path.join(remoteReleasePath, 'app/etc/local.xml').rstrip('/')
        )


def f_RemoveTarget():
    return "rm -fr %s" % (config['env'][env]['remote_target_path'].rstrip('/'))


def f_LinkTarget():
    return "ln -fs %s %s" % (
        remoteReleasePath.rstrip('/'),
        config['env'][env]['remote_target_path'].rstrip('/')
        )


releases = f_Run(f_WrapWithPass(f_WrapWithSsh(
    "find %s -mindepth 1 -maxdepth 1 -type d | sort" % (
        config['env'][env]['remote_release_subpath'].rstrip('/')
        )))).split("\n")
releasesCount = len(releases)
countToLeave = 2
if releasesCount > countToLeave:
    countToRemove = releasesCount - countToLeave
    index = 0
    while (index < countToRemove):
        pointer = index
        index += 1
        f_Run(f_WrapWithPass(f_WrapWithSsh("rm -fr %s" % releases[pointer])))
        
archiveFilePath = os.path.join(basepath, config['general']['archive_file']).rstrip('/')

f_Run("cp -rL %s %s" % (
    os.path.join(basepath, config['general']['src_path']).rstrip('/'),
    os.path.join(basepath, config['general']['dst_path']).rstrip('/')
    ))
f_Run("rm -fr %s; rm -fr %s; rm -fr %s" % (
    os.path.join(basepath, config['general']['dst_path'], 'app/etc/local.xml').rstrip('/'),
    os.path.join(basepath, config['general']['dst_path'], 'media').rstrip('/'),
    os.path.join(basepath, config['general']['dst_path'], 'var').rstrip('/')
    ))
f_Run("tar -czf %s -C %s ." % (
    archiveFilePath.rstrip('/'),
    os.path.join(basepath, config['general']['dst_path']).rstrip('/')
    ))
f_Run(f_WrapWithPass(f_WrapWithSsh("mkdir -p %s" % (
    remoteReleasePath.rstrip('/')
    ))))
f_Run(f_WrapWithPass("scp %s %s:%s" % (
    archiveFilePath.rstrip('/'),
    userHost,
    remoteReleasePath.rstrip('/')
    )))
f_Run(f_WrapWithPass(f_WrapWithSsh("tar -xzf %s -C %s" % (
    os.path.join(remoteReleasePath, config['general']['archive_file']).rstrip('/'),
    remoteReleasePath.rstrip('/')
    ))))
f_Run(f_WrapWithPass(f_WrapWithSsh("rm %s" % (
    os.path.join(remoteReleasePath, config['general']['archive_file']).rstrip('/')
    ))))
f_Run("rm %s; rm -fr %s" % (
    archiveFilePath.rstrip('/'),
    os.path.join(basepath, config['general']['dst_path']).rstrip('/')
    ))

f_Run(f_WrapWithPass(f_WrapWithSsh(f_LinkConfig())))
f_Run(f_WrapWithPass(f_WrapWithSsh(f_LinkShared('media'))))
f_Run(f_WrapWithPass(f_WrapWithSsh(f_LinkShared('var'))))
f_Run(f_WrapWithPass(f_WrapWithSsh(f_LinkShared('sitemaps'))))

f_Run(f_WrapWithPass(f_WrapWithSsh(f_RemoveTarget())))
f_Run(f_WrapWithPass(f_WrapWithSsh(f_LinkTarget())))

f_Run(f_WrapWithPass(f_WrapWithSsh("php %s --root-dir=%s cache:flush" % (
    os.path.join(remoteReleasePath, 'n98-magerun.phar').rstrip('/'),
    config['env'][env]['remote_target_path'].rstrip('/')
    ))))
