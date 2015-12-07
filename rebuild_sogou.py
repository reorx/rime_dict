#!/usr/bin/env python
# coding: utf-8

INPUT_FILENAME = 'sogou_userdict.txt'
OUTPUT_FILENAME = 'sogou_userdict.1.txt'


if __name__ == '__main__':
    new_lines = []

    count = 0
    with open(INPUT_FILENAME, 'r') as f:
        for line in f.readlines():
            line_strip = line.strip()
            splited = line_strip.split('	')
            word = splited[0].decode('utf8')
            if len(word) % 2 == 0:
                half_len = len(word) / 2
                half = word[:half_len]
                if half == word[half_len:]:
                    continue

            new_lines.append(line)

    with open(OUTPUT_FILENAME, 'w') as f:
        f.writelines(new_lines)
