# Copyright © 2014-2015 Jakub Wilk <jwilk@jwilk.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import sys
import io
import glob

import lib.cli as M

from nose.tools import (
    assert_multi_line_equal,
)

assert_multi_line_equal.__self__.maxDiff = None

def _get_output(path, language):
    binstdout = io.BytesIO()
    [old_stdout, old_argv] = [sys.stdout, sys.argv]
    try:
        sys.argv = ['mwic', '--language', language, path]
        textstdout = sys.stdout = io.TextIOWrapper(binstdout, encoding='utf-8')
        try:
            M.main()
            sys.stdout.flush()
            return binstdout.getvalue().decode('utf-8')
        finally:
            textstdout.close()
    finally:
        [sys.stdout, sys.argv] = [old_stdout, old_argv]

def _test_text(ipath, xpath):
    assert xpath.endswith('.exp')
    if '@' in xpath:
        language = xpath[:-4].rsplit('@')[1]
    else:
        language = 'en-US'
    text = _get_output(ipath, language)
    with open(xpath, 'rt', encoding='utf-8') as file:
        expected = file.read()
    assert_multi_line_equal(text, expected)

def test_text():
    here = os.path.dirname(__file__)
    here = os.path.relpath(here)
    ipaths = glob.glob(os.path.join(here, '*.txt'))
    for ipath in ipaths:
        pathbase, pathsuffix = os.path.splitext(ipath)
        for xpath in glob.glob(pathbase + '*.exp'):
            yield _test_text, ipath, xpath

# vim:ts=4 sts=4 sw=4 et
