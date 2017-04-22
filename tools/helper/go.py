#!/usr/bin/env python

import os
import sys
import commands
import subprocess

import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--config')
parser.add_argument('--basepath')
parser.add_argument('--action')
args = parser.parse_args()

import json
with open(args.config) as _file:
    config = json.load(_file)

basepath = args.basepath


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


def f_GetFullPath(subpath):
    return os.path.join(basepath.rstrip('/'), subpath).rstrip('/')


def f_Link(customCodeDir, _subItem, options, destCodeDir):
    customCodeBasename = f_Run("basename %s" % (customCodeDir), False)
    subItem = _subItem.rstrip('/')
    _list = f_Run("find %s %s" % (
        f_GetFullPath("%s/%s" % (customCodeDir.rstrip('/'), subItem.lstrip('/'))),
        options
        ) + ' -printf "%P\\n"').splitlines()
    for _item in _list:
        item = _item.lstrip('/')
        if subItem:
            relativePath = "%s/%s" % (subItem, item)
        else:
            relativePath = item
        level = relativePath.count('/') + 1
        prefix = '../' * level
        toPath = (prefix + os.path.join(customCodeBasename.rstrip('/'), relativePath.lstrip('/'))).strip('/')
        fromPath = f_GetFullPath("%s/%s" % (destCodeDir.rstrip('/'), relativePath.lstrip('/')))
        f_Run((''
            + " mkdir -p $(dirname %s);" % (fromPath)
            + " ln -fs %s %s" % (toPath, fromPath)
            ).strip(), False)


def f_LinkAll():
    f_Link(f_GetFullPath(config['code']['custom']), 'app/code', '-mindepth 3 -maxdepth 3 -type d', config['code']['dest'])
    f_Link(f_GetFullPath(config['code']['custom']), 'app/design', '-mindepth 1 -type f', config['code']['dest'])
    f_Link(f_GetFullPath(config['code']['custom']), 'app/etc', '-mindepth 1 -type f', config['code']['dest'])
    f_Link(f_GetFullPath(config['code']['custom']), 'app/locale', '-mindepth 1 -type f', config['code']['dest'])
    f_Link(f_GetFullPath(config['code']['custom']), 'errors', '-mindepth 1 -maxdepth 1', config['code']['dest'])
    f_Link(f_GetFullPath(config['code']['custom']), 'js', '-mindepth 1 -type f', config['code']['dest'])
    f_Link(f_GetFullPath(config['code']['custom']), 'lib', '-mindepth 1 -maxdepth 1', config['code']['dest'])
    f_Link(f_GetFullPath(config['code']['custom']), 'media', '-mindepth 1 -type f', config['code']['dest'])
    f_Link(f_GetFullPath(config['code']['custom']), 'shell', '-mindepth 1 -type f', config['code']['dest'])
    f_Link(f_GetFullPath(config['code']['custom']), 'skin', '-mindepth 1 -type f', config['code']['dest'])
    f_Link(f_GetFullPath(config['code']['custom']), 'var', '-mindepth 1 -maxdepth 1', config['code']['dest'])
    f_Link(
        f_GetFullPath(config['code']['custom']),
        '',
        '-mindepth 1 -maxdepth 1'
            + ' ! -name app ! -name errors ! -name js ! -name lib ! -name media ! -name shell ! -name skin ! -name var',
        config['code']['dest']
        )


if args.action == 'system':
    f_Run("sudo cp -r %s/. /usr/local/bin; sudo chmod -R 0777 /usr/local/bin" % (f_GetFullPath(config['bin']['path'])))
    f_Run("sudo cp -r %s/. /etc" % (f_GetFullPath(config['etc']['path'])))
    f_Run('mysql -u root -e "grant all privileges on *.* to \'root\'@\'%\' identified by \'\' with grant option"')
    f_Run('sudo service mysql restart')
    f_Run('sudo service mongod restart')
    f_Run('sudo service php7.0-fpm restart')
    f_Run('sudo service nginx restart')

elif args.action == 'composer':
    f_Run('('
        + " cd %s;" % (f_GetFullPath(''))
        + " rm -fr %s;" % (f_GetFullPath(config['code']['vendor']))
        + " rm -fr %s;" % (f_GetFullPath(config['code']['dest']))
        + ' %s/composer.phar install --verbose --prefer-dist --no-dev' % (f_GetFullPath(config['bin']['path']))
        + ' )'
        )

elif args.action == 'code':
    f_Run("mkdir -p %s" % (f_GetFullPath(config['code']['dest'])))
    f_Run("cp -r %s/. %s" % (
        f_GetFullPath(config['code']['magento']),
        f_GetFullPath(config['code']['dest'])
        ))
    f_Run("cp -r %s/. %s" % (
        f_GetFullPath(config['code']['plus']),
        f_GetFullPath(config['code']['dest'])
        ))

elif args.action == 'link':
    f_LinkAll()

elif args.action == 'patch':
    with open(config['composer']['file'].rstrip('/')) as _file:
        composerJson = json.load(_file)
    patches = composerJson['extra']['patches']
    for patchesGroup in patches:
        for patch in patches[patchesGroup]:
            f_Run("(cd %s; patch -p1 < ../patches/%s)" % (f_GetFullPath(config['code']['dest']), patches[patchesGroup][patch]))

elif args.action == 'sass':
    folders = f_Run("find -L %s -type d -name scss" % (f_GetFullPath(config['code']['dest']))
        + ' -printf "%P\\n"').splitlines()
    for item in folders:
        f_Run("(cd %s && compass compile)" % (
        "%s/%s" % (
            f_GetFullPath(config['code']['dest']).rstrip('/'), 
            item.lstrip('/')
            )
        ), True, False)

elif args.action == 'mongodb':
    f_Run("mongoimport --db %s --collection %s --type json --file %s" % (
        config['mongo']['dbname'],
        config['mongo']['collection'],
        f_GetFullPath(config['mongo']['file'])
        ))

elif args.action == 'mysqldb':
    f_Run('mysql -u root -e "drop database if exists zoro"')
    f_Run('mysql -u root -e "create database zoro character set utf8 collate utf8_general_ci"')
    f_Run("mysql -u root zoro < %s" % (f_GetFullPath(config['db']['file'])))
