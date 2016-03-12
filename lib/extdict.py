# Copyright © 2016 Jakub Wilk <jwilk@jwilk.net>
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

'''
external (codespell, Lintian) misspelling dictionary

Supported dictionary formats:
+ Lintian <https://anonscm.debian.org/cgit/lintian/lintian.git/tree/data/spelling/corrections>
+ codespell <https://github.com/lucasdemarchi/codespell/blob/master/data/dictionary.txt>
+ plain word list
'''

def normalize_case(s):
    return s.lower().replace('-', '').replace(' ', '')

separators = {
    '||',  # Lintian
    '->',  # codespell
}

def parse_line(line):
    left = line
    for sep in separators:
        try:
            [left, right] = line.split(sep, 1)
        except ValueError:
            pass
        else:
            break
    else:
        sep = ''
    yield left
    if not left.islower():
        return
    if sep == '||' and normalize_case(left) == normalize_case(right):
        # Lintian's “correction-case” format
        return
    yield left.title()
    yield left.upper()

class Dictionary(object):

    def __init__(self, *paths):
        self._dict = set()
        for path in paths:
            self._read(path)

    def __contains__(self, word):
        return word in self._dict

    def _add(self, word):
        self._dict.add(word)

    def _read(self, path):
        with open(path, 'rt', encoding='UTF-8') as file:
            self._read_fp(file)

    def _read_fp(self, file):
        add = self._add
        for line in file:
            if line[:1] == '#':
                continue
            line = line.strip()
            if not line:
                continue
            for word in parse_line(line):
                add(word)

__all__ = ['Dictionary']

# vim:ts=4 sts=4 sw=4 et