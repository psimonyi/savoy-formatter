#!/usr/bin/env python3

from xml.dom import minidom
from xml.dom.minidom import Node
import html5lib

def main():
    dom = source_dom()
    newdom = blank_template()
    format(dom, newdom)
    write_dom(newdom)

def source_dom():
    source = 'gutenberg-source.html'
    with open(source, 'rb') as f:
        dom = html5lib.parse(f, treebuilder='dom')
    dom.normalize()
    return dom

def format(old, new):
    # H2s are used for both opera names and act numbers.  There's also an H2 in
    # the page heading, but we can ignore that.
    h2s = old.getElementsByTagName('h2')[1:]
    article = new.getElementsByTagName('article')[0]
    section = None
    for h2 in h2s:
        part = format_part(h2, new)
        if part.firstChild.tagName == 'h1':
            if section: article.appendChild(section)
            section = new.createElement('section')
        transplantChildren(part, section)
    article.appendChild(section)

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

def transplantChildren(source, dest):
    while source.hasChildNodes():
        dest.appendChild(source.firstChild)

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

    index = blank_template()
    idx_main = index.getElementsByTagName('article')[0]
    idx_list = idx_main.appendChild(index.createElement('ul'))
    def idx_add(label, filename):
        a = index.createElement('a')
        a.setAttribute('href', filename)
        a.appendChild(index.createTextNode(label))
        li = index.createElement('li')
        li.appendChild(a)
        idx_list.appendChild(li)

    # Copy each play's section into its own file.
    for section in newdom.getElementsByTagName('section'):
        h1 = section.firstChild
        title = h1.firstChild.data.strip().title()
        filename = 'gs-{}.html'.format(title.replace(' ', '-'))
        idx_add(title, filename)

        single = blank_template()
        article = single.getElementsByTagName('article')[0]
        article.appendChild(single.importNode(section, True))

        with open(filename, 'w') as f:
            single.writexml(f)

    idx_add("All libretti", 'gs14.html')

    with open('index.html', 'w') as f:
        index.writexml(f)

if __name__ == '__main__':
    main()
