#!/usr/bin/env python3

def prn(*args):
    print(*args, end='')

body = False
with open('gs.html') as f:
    for line in f:
        if '<head>' in line:
            prn(line)
            print('<meta name="viewport" content="width=device-width"/>')
            continue
        if '<body>' in line:
            body = True
            prn(line)
            continue
        if line.startswith('<pre') or line.startswith('</pre'):
            # delete it
            continue
        if not body or '<' in line:
            prn(line)
            continue
        if '<' not in line:
            pos = line.rfind('  ')
            if pos != -1: pos += len('  ')
            indent = line[:pos]
            width = len(indent) / 2
            prn('<span style="width: {}ex; display: inline-block;">{}</span>'
                    .format(width, indent))
            prn(line[pos:])
            print('<br/>')


