#!/bin/bash
# if no argument is given, report usage
if [ $# -eq 0 ]; then
    echo "Usage: $0 <file>"
    exit 1
fi

python3 ~/git/webrepl/webrepl_cli.py  -p `cut -d\' -f2 webrepl_cfg.py` $1 192.168.0.113:
