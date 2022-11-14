import lxml.builder
import lxml.etree
import os


def run():
    """
    Generate the readme file.
    :return: None
    """

    # Generate the base file
    elements = lxml.builder.ElementMaker()
    doc = elements.doc

    # Fields tags to use
    h1 = elements.h1
    img = elements.img
    html = elements.html
    body = elements.body
    doc = html()
    body = body()
    doc.append(body)

    # Loop through the SVG files
    for fname in sorted(os.listdir('svg')):
        if fname.endswith('.svg'):
            name = fname.split('.')[0]
            name = name.replace('-', ' ').title()

            # Add title
            body.append(h1(name))
            body.append(img(
                src=f'./svg/{fname}'
            ))

    # Save the readme file
    with open('README.md', 'wb') as f:
        f.write(lxml.etree.tostring(doc, pretty_print=True))


if __name__ == '__main__':
    run()
