# -*- coding: utf-8 -*-
import sys
import os
import os.path as op
import shutil
import tempfile
import warnings
from io import StringIO


class _TempDir(str):
    """Class for creating and auto-destroying temp dir

    This is designed to be used with testing modules. Instances should be
    defined inside test functions. Instances defined at module level can not
    guarantee proper destruction of the temporary directory.

    When used at module level, the current use of the __del__() method for
    cleanup can fail because the rmtree function may be cleaned up before this
    object (an alternative could be using the atexit module instead).
    """
    def __new__(self):
        new = str.__new__(self, tempfile.mkdtemp())
        return new

    def __init__(self):
        self._path = self.__str__()

    def __del__(self):
        shutil.rmtree(self._path, ignore_errors=True)


tempdir = _TempDir()

shutil.copy(op.join(op.dirname(__file__), '..', '..', 'bin', 'om_viz'),
            op.join(tempdir, 'om_viz.py'))
sys.path.append(tempdir)


class ArgvSetter(object):
    """Temporarily set sys.argv"""
    def __init__(self, args=(), disable_stdout=True, disable_stderr=True):
        self.argv = list(('python',) + args)
        self.stdout = StringIO() if disable_stdout else sys.stdout
        self.stderr = StringIO() if disable_stderr else sys.stderr

    def __enter__(self):
        self.orig_argv = sys.argv
        sys.argv = self.argv
        self.orig_stdout = sys.stdout
        sys.stdout = self.stdout
        self.orig_stderr = sys.stderr
        sys.stderr = self.stderr
        return self

    def __exit__(self, *args):
        sys.argv = self.orig_argv
        sys.stdout = self.orig_stdout
        sys.stderr = self.orig_stderr


base_dir = op.join(op.dirname(__file__), 'data')
geom_fname = op.join(base_dir, "sample.geom")

warnings.simplefilter('always')


def check_usage(module, force_help=False):
    """Helper to ensure we print usage"""
    args = ('--help',) if force_help else ()
    with ArgvSetter(args) as out:
        try:
            module.run()
        except SystemExit:
            pass
        assert 'Usage:' in out.stdout.getvalue()


def test_om_viz():
    """Test om_viz"""
    import om_viz
    import pyvista as pv

    os.environ['OM_VIZ_OFFSCREEN'] = 'True'
    check_usage(om_viz)
    with ArgvSetter((geom_fname,)):
        om_viz.run()
        pv.close_all()
