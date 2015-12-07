#!/usr/bin/env python
# coding: utf-8

HEAD = """
---
name: easy_en
version: "0.2"
sort: by_weight
use_preset_vocabulary: false
...
"""

if __name__ == '__main__':
    new_lines = []

    count = 0
    with open('easy_en.dict.yaml.bak', 'r') as f:
        WORD_START = False
        for line in f.readlines():
            if line.startswith('...'):
                WORD_START = True
                continue
            if WORD_START:
                if line.strip():
                    word = line.split('	')[0]
                    if len(word) > 4:
                        new_line = '	'.join([word, word, '1']) + '\n'
                        new_lines.append(new_line)

                        #print new_lines
                        #count += 1
                        #if count == 30:
                        #    break

    with open('easy_en.dict.yaml', 'w') as f:
        new_lines.insert(0, HEAD)
        f.writelines(new_lines)
