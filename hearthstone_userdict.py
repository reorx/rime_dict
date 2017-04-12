#!/usr/bin/env python
# coding: utf-8

import re
import sys
import json
import itertools

import parser


OUTPUT_FILEPATH = 'Rime/custom_dict/luna_pinyin.hs.dict.yaml'


if __name__ == '__main__':
    CMDS = ['test', 'write']
    cmd = sys.argv[1]
    if cmd not in CMDS:
        print 'Invalid command, available commands: {}'.format(CMDS)
        sys.exit(1)

    with open('cards.json', 'r') as f:
        text = f.read()

    cards = json.loads(text)
    cardset = set()

    number_regex = re.compile(r'[0-9]')
    abc_regex = re.compile(r'[a-zA-Z]')

    for card in cards:
        _name = card.get('name')
        if not _name:
            continue
        if len(_name) > 9:
            continue

        # Remove puncturator
        name = parser.remove_punc(_name)

        # Remove number
        name = re.sub(number_regex, '', name)
        if not name:
            continue

        # Remove first-character-is-English word
        if abc_regex.match(name[0]):
            continue

        cardset.add(name)

    print 'collected {} card names'.format(len(cardset))

    if cmd == 'test':
        for i in cardset:
            print i.encode('utf8')
    else:
        print 'write to {}'.format(OUTPUT_FILEPATH)

        with open(OUTPUT_FILEPATH, 'w') as f:
            f.writelines(
                itertools.chain(
                    parser.generate_head_lines('luna_pinyin.hs', '1.1'),
                    parser.iter_lines(cardset, priority=1)
                )
            )
