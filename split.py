#!/usr/bin/env python3

from xml.dom import minidom
from xml.dom.minidom import Node

def main():
    source = 'gutenberg-source.html'
    dom = minidom.parse(source)
    dom.normalize()
    h2s = dom.getElementsByTagName('h2')
    newdom = new()
    article = newdom.getElementsByTagName('article')[0]
    # H2s are used for both opera names and act numbers.  There's also an H2 in
    # the page heading, but we can ignore that.
    for h2 in h2s:
        article.appendChild(formatPart(h2, newdom))
    print(newdom.toxml())

def formatPart(h2, doc):
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
        section.appendChild(formatPre(node, doc))
        node = nextElementSibling(node)

    return section

def nextElementSibling(node):
    node = node.nextSibling
    while node.nodeType != Node.ELEMENT_NODE:
        node = node.nextSibling
    return node

def formatPre(pre, doc):
    div = doc.createElement('div')
    text = pre.firstChild.data
    for line in text.splitlines():
        p = doc.createElement('p')
        if '  ' in line:
            pos = line.rfind('  ') + len('  ')
            indent = line[:pos]
            main = line[pos:]
            width = len(indent) * 0.6
            span = doc.createElement('span')
            style = 'width: {}ex; display: inline-block;'.format(width)
            span.setAttribute('style', style)
            span.appendChild(doc.createTextNode(indent))
            p.appendChild(span)
            p.appendChild(doc.createTextNode(main))
        else:
            p.appendChild(doc.createTextNode(line))
        div.appendChild(p)

    return div

def new():
    return minidom.parseString('''
    <html>
    <head>
    <meta name='viewport' content='initial-scale=1'/>
    <title>Reformatted Libretti</title>
    <style type='text/css'>
        p {
            margin: 0;
        }
    </style>
    </head>
    <body>
    <article/>
    </body>
    </html>''')

if __name__ == '__main__':
    main()
