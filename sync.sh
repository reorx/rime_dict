#!/bin/bash

rsync -avr --exclude='*.bin' ~/Library/Rime/* ~/Dropbox/Backup/Rime/$(date +%Y-%m-%d-%H%M%S)
