#!/usr/bin/env python
# coding: utf-8

import sys
import time
import pypinyin
import unicodedata
from StringIO import StringIO


TAB = '	'
TEMPLATE_WITH_PRIORITY = '{}	{}	{}'


def parse_dict(filepath):
    head_lines = []
    body_lines = []
    with open(filepath, 'r') as f:
        is_head = True

        for line in f.readlines():
            if is_head:
                head_lines.append(line)
            else:
                body_lines.append(line)

            if line.strip() == '...':
                is_head = False

    return head_lines, body_lines


def parse_dict_line(line):
    """Format:
    A Word	a word	1
    """
    line = line.strip()
    if not line:
        return None, None, None
    word, input, priority = tuple(line.split(TAB))
    return word, input, priority


class DictSet(object):
    """A Set like container for dict items"""

    def __init__(self, lines):
        self.dictset = {}
        for i in lines:
            word, input, priority = parse_dict_line(i)
            if word:
                self.dictset[input] = (word, input, priority)

    def get(self, input):
        return self.dictset.get(input)

    def add(self, word, input, priority):
        self.dictset[input] = (word, input, priority)

    def delete(self, input):
        del self.dictset[input]

    def iter_lines(self, sort=True):
        iterator = self.dictset.itervalues()
        if sort:
            iterator = sorted(iterator, key=lambda x: x[0].decode('utf8'))
        for cols in iterator:
            yield TEMPLATE_WITH_PRIORITY.format(*cols) + '\n'


punc_table = {i: None for i in xrange(sys.maxunicode)
              if unicodedata.category(unichr(i)).startswith('P')}


def remove_punc(u):
    return u.translate(punc_table)


def iter_lines(s, with_pinyin=True, priority=1):
    for name in s:
        if with_pinyin:
            cols = [name]
            pinyin = ' '.join(pypinyin.lazy_pinyin(name))
            cols.append(pinyin)

            if priority is not None:
                cols.append(str(priority))

            result_str = TAB.join(cols).encode('utf8')
        else:
            result_str = name.encode('utf8')
        yield result_str + '\n'


HEAD_TEMPLATE = """---
name: {name}
version: "{version}"
sort: by_weight
use_preset_vocabulary: {use_preset_vocabulary}
...
"""


def generate_head_lines(name, version, use_preset_vocabulary=True):
    version = '{}.{}'.format(version, int(time.time()))
    use_preset_vocabulary = 'true' if use_preset_vocabulary else 'false'

    head_str = HEAD_TEMPLATE.format(**{
        'name': name,
        'version': version,
        'use_preset_vocabulary': use_preset_vocabulary
    })
    return StringIO(head_str).readlines()
