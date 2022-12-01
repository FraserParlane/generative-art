from typing import List
import lxml.builder
import lxml.etree
import numpy as np
import os

# Generate the base elements.
elements = lxml.builder.ElementMaker()

# Set the random seed
np.random.seed(5)


def color_interpolator(
        start: str,
        stop: str,
        steps: int,
) -> List[str]:
    """
    Given two colors, generate a list of n colors linearly spaced between them
    :param start: HEX code for start color
    :param stop: HEX code for stop color
    :param steps: Number of steps, including start and stop
    :return: List of HEX codes
    """
    pass


def run():

    # Constants that define the page
    height = 1000
    width = 1000
    doc = elements.doc
    svg = elements.svg
    bg_color = '#1b1b1b'

    # Create SVG fields
    path = elements.path
    circle = elements.circle
    rect = elements.rect

    # Create document with white background
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

    # Save
    base = os.path.basename(__file__).split('.')[0]
    with open(f'../svg/{base}.svg', 'wb') as f:
        f.write(lxml.etree.tostring(doc, pretty_print=True))


if __name__ == "__main__":
    run()
