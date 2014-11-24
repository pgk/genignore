#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os.path import join, realpath, abspath
import logging
import time
from datetime import datetime
from subprocess import Popen, PIPE


FORMAT = '[%(asctime)s][%(levelname)s] - %(message)s'
log = logging.getLogger('genignore.testing.log')
logging.basicConfig(format=FORMAT)
log.setLevel(logging.DEBUG)


realify = lambda *items: abspath(join(*items))


def check_exists(path, as_dir=False):
    if as_dir:
        log.debug('** checking if {0} dir exists'.format(path))
        return os.path.isdir(path)
    else:
        log.debug('** checking if {0} exists'.format(path))
        return os.path.exists(path)


def ensure_exists(path, as_dir=False):
    existent = check_exists(path, as_dir)

    if not existent:
        log.debug('** checking if {0} exists'.format(path))
        os.makedirs(path)


def touch(file_path):
    parts = file_path.split(os.sep)
    log.debug(parts)
    fpath, fname = os.sep.join(parts[:-1]), parts[-1]
    log.debug(fpath)
    log.debug(fname)
    ensure_exists(fpath, as_dir=True)
    return shell('touch %s' % file_path)


def shell(cmd, chdir=None, preserve_output=False):
    if isinstance(cmd, basestring):
        cmd = cmd.split(' ')

    if chdir:
        log.debug('changing dir into {0}'.format(chdir))
        os.chdir(chdir)

    log.debug('executing {0}'.format(" ".join(cmd)))
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)

    out, err = [], []

    while p.poll() is None:
        try:
            _o = p.stdout.read()
            _e = p.stderr.read()

            log.debug(_o)
            if _e:
                log.error(_e)

            if preserve_output:
                out.append(_o.strip())
                err.append(_e.strip())
        except Exception, e:
            log.exception(e)
        time.sleep(0.125)

    if err:
        log.error(err)
    log.debug(out)
    if p.returncode != 0:
        log.debug('error executing {0}'.format(" ".join(cmd)))
    return p, "".join(out), "".join(err)


def ln(from_path, to_path, *args):
    return shell("ln -s {0} {1}".format(from_path, to_path))


