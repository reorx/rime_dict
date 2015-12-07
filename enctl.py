#!/usr/bin/env python
# coding: utf-8

import click
import parser

EN_FILEPATH = 'Rime/custom_dict/luna_pinyin.cn_en.dict.yaml'


@click.group()
def cli():
    pass


@cli.command('list')
def cmd_list():
    head, body = parser.parse_userdict(EN_FILEPATH)
    count = 0

    print 'All en words:'
    for line in body:
        word, input, priority = parser.parse_userdict_line(line)
        if word:
            print '{}	{}'.format(word, input)
            count += 1
    print '\nTotal: {}'.format(count)


@cli.command('add')
@click.argument('word')
@click.argument('input')
@click.argument('priority', default=1)
def cmd_add(word, input, priority):
    """Add a word into userdict:

    \b
    WORD   the word that pointed by input
    INPUT  input character sequence
    PRIORITY sorting priority
    """
    print word, input, priority

    head, body = parser.parse_userdict(EN_FILEPATH)

    ud = parser.UserDict(body)
    item = ud.get(input)
    confirmed = False
    if item:
        if click.confirm('Item already exists: {} {} {}, do you want to overwrite it?'.format(*item)):
            confirmed = True
    else:
        confirmed = True

    if confirmed:
        ud.add(word, input, priority)

    # Write back


if __name__ == '__main__':
    cli()
