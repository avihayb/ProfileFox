#!python
#!/usr/bin/env python
# -*- coding: utf-8; mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vim: fileencoding=utf-8 tabstop=4 expandtab shiftwidth=4

# (C) COPYRIGHT © Preston Landers 2010
# Released under the same license as Python 2.6.5

# coding: utf-8
import sys
import ctypes
import subprocess
def unicode(param):
    # don't know what this function is supposed to be for sure
    return param

def run_as_admin(argv=None, debug=False):
    shell32 = ctypes.windll.shell32
    if argv is None and shell32.IsUserAnAdmin():
        return True

    if argv is None:
        argv = sys.argv
    # if hasattr(sys, '_MEIPASS'):
    #     # Support pyinstaller wrapped program.
    #     arguments = list(map(unicode, argv[1:]))
    # else:
    #     arguments = list(map(unicode, argv))
    # bad argument_line = u' '.join(arguments)
    arguments = argv
    argument_line = subprocess.list2cmdline(arguments[1:])
    #executable = unicode(sys.executable)
    executable = unicode(arguments[0])
    if debug:
        print ('Command line: ', executable, argument_line)
    ret = shell32.ShellExecuteW(None, u"runas", executable, argument_line, None, 1)
    if int(ret) <= 32:
        return False
    return None


if __name__ == '__main__':
    ret = run_as_admin()
    if ret is True:
        print ('I have admin privilege.')
        input('Press ENTER to exit.')
    elif ret is None:
        print ('I am elevating to admin privilege.')
        input('Press ENTER to exit.')
    else:
        print ('Error(ret=%d): cannot elevate privilege.' % (ret, ))
