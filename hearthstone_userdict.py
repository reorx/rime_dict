#!/usr/bin/env python
# coding: utf-8

import re
import json
import itertools

import parser


OUTPUT_FILEPATH = 'Rime/custom_dict/luna_pinyin.hs.dict.yaml'


if __name__ == '__main__':
    with open('AllSets.zhCN.json', 'r') as f:
        text = f.read()

    d = json.loads(text)
    cardset = set()

    number_regex = re.compile(r'[0-9]')
    abc_regex = re.compile(r'[a-zA-Z]')

    for sname, cards in d.iteritems():
        #print sname
        for card in cards:
            _name = card['name']

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

    with open(OUTPUT_FILEPATH, 'w') as f:
        f.writelines(
            itertools.chain(
                parser.generate_head_lines('luna_pinyin.hs', '1.0'),
                parser.iter_lines(cardset, priority=10)
            )
        )
