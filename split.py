#!/usr/bin/env python3

from xml.dom import minidom
from xml.dom.minidom import Node
import html5lib

def main():
    dom = source_dom()
    newdom = blank_template()
    article = newdom.getElementsByTagName('article')[0]
    # H2s are used for both opera names and act numbers.  There's also an H2 in
    # the page heading, but we can ignore that.
    h2s = dom.getElementsByTagName('h2')
    for h2 in h2s:
        article.appendChild(format_part(h2, newdom))
    write_dom(newdom)

def source_dom():
    source = 'gutenberg-source.html'
    with open(source, 'rb') as f:
        dom = html5lib.parse(f, treebuilder='dom')
    dom.normalize()
    return dom

def format_part(h2, doc):
    # The <h2> is followed by one or more <pre>, and we stop at the <p>.

    section = doc.createElement('section')
    if 'ACT' in h2.firstChild.data:
        elem = section.appendChild(doc.createElement('h2'))
    else:
        elem = section.appendChild(doc.createElement('h1'))
    elem.appendChild(doc.createTextNode(h2.firstChild.data))
    section.appendChild(elem)

    node = nextElementSibling(h2)
    while node.tagName == 'pre':
        section.appendChild(format_pre(node, doc))
        node = nextElementSibling(node)

    return section

def nextElementSibling(node):
    node = node.nextSibling
    while node and node.nodeType != Node.ELEMENT_NODE:
        node = node.nextSibling
    return node

def format_pre(pre, doc):
    div = doc.createElement('div')
    text = pre.firstChild.data
    for line in text.splitlines():
        p = doc.createElement('p')
        if not len(line):
            p.setAttribute('class', 'blank')
        else:
            if '   ' in line:
                pos = line.rfind('   ') + len('   ')
                indent = line[:pos]
                if indent.isupper():
                    indent = indent.title()
                width = len(indent) * 0.6
                span = doc.createElement('span')
                style = 'width: {}ex; display: inline-block;'.format(width)
                span.setAttribute('style', style)
                span.appendChild(doc.createTextNode(indent))
                p.appendChild(span)
                line = line[pos:]
            if any(line.strip().startswith(t) for t in SONG_TYPES):
                # TODO: This is a little too greedy; it ought to skip lines
                # containing all-lowercase words other than 'and' and 'with'.
                p.setAttribute('class', 'songstart')
            p.appendChild(doc.createTextNode(line))
        div.appendChild(p)

    return div

SONG_TYPES = [
    'ARIA',
    'BALLAD',
    'BARCAROLLE',
    'CHANT',
    'CHORUS',
    'DUET',
    'ENSEMBLE',
    'EXEUNT FOR',
    'FINALE',
    'GLEE',
    'INVOCATION',
    'LEGEND',
    'MADRIGAL',
    'OCTETTE',
    'OPENING CHORUS',
    'QUARTET',
    'QUINTET',
    'RECIT',
    'RECIT.',
    'RECITATIVE',
    'SCENA',
    'SCENE',
    'SOLO',
    'SONG',
    'TRIO',
]

def blank_template():
    return minidom.parseString('''
    <html>
    <head>
    <meta name='viewport' content='initial-scale=1'/>
    <meta charset='utf-8'/>
    <title>Reformatted Libretti</title>
    <style type='text/css'>
        p {
            margin: 0;
        }
        p.blank {
            height: 0.6em;
        }
        p.songstart{
            font-weight: bold;
        }
    </style>
    </head>
    <body>
    <article/>
    </body>
    </html>''')

def write_dom(newdom):
    with open('gs14.html', 'w') as f:
        newdom.writexml(f)

if __name__ == '__main__':
    main()
