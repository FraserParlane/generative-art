import lxml.builder
import lxml.etree
import numpy as np
import os

# Generate the base elements.
elements = lxml.builder.ElementMaker()

# Set the random seed
np.random.seed(5)


def run():

    # Constants that define the page
    height = 1000
    width = 1000
    svg = elements.svg

    # Drawing constants
    bg_color = '#1b1b1b'
    draw_color = '#f82672'

    # Elements
    rect = elements.rect
    animate_transform = elements.animateTransform

    # Document with background
    doc = svg(
        xmlns="http://www.w3.org/2000/svg",
        height=str(height),
        width=str(width),
    )
    doc.append(rect(
        x='0',
        y='0',
        width=str(width),
        height=str(height),
        fill=bg_color,
    ))

    # Design constants
    n = 20
    r_width = 500
    r_height = 500
    lw = 3
    scale_delta = 1.1

    # Iteratively create the squares
    for i in range(n):

        # Create both the dark outline and the color
        for ilw, icolor in zip([lw * 4, lw], [bg_color, draw_color]):

            r = rect(
                x=str((height - r_height) / 2),
                y=str((width - r_width) / 2),
                width=str(r_width),
                height=str(r_height),
                fill=bg_color,
                stroke=icolor,
            )
            r.attrib['stroke-width'] = str(ilw)

            # Generate animation
            anim = animate_transform(
                attributeName='transform',
                type='rotate',
                begin='0s',
                dur=f'60s',
                repeatCount='indefinite',
            )
            anim.attrib['from'] = f'0 {width / 2} {height / 2}'
            anim.attrib['to'] = f'{(i+1) * 360} {width / 2} {height / 2}'
            r.append(anim)
            doc.append(r)

        # Update attributes
        r_width /= scale_delta
        r_height /= scale_delta

    # Save
    base = os.path.basename(__file__).split('.')[0]
    with open(f'../svg/{base}.svg', 'wb') as f:
        f.write(lxml.etree.tostring(doc, pretty_print=True))


if __name__ == "__main__":
    run()
