from typing import List
import lxml.builder
import lxml.etree
import numpy as np
import os

# Generate the base elements.
elements = lxml.builder.ElementMaker()

# Set the random seed
np.random.seed(5)


def hex_to_dec(
        hex_str: str,
) -> np.array:
    """
    Convert a HEX string to an array of values 0 to 255
    :param hex_str: String to convert. With or without # suffix
    :return: RGB values from 0 to 255
    """

    # Remove #.
    if hex_str[0] == '#':
        hex_str = hex_str[1:]

    # Convert
    rgb = np.array([int(hex_str[i:i+2], base=16) for i in range(0, 6, 2)])

    # Return
    return rgb


def dec_to_hex(
        dec: np.array,
) -> str:
    """
    Convert an array of 3 RGB decimal values to a single string.
    :param dec: aray to convert
    :return: String of hex.
    """

    # Convert, return
    hex_str = '#' + ''.join([hex(int(i))[2:].zfill(2) for i in dec])
    return hex_str


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

    # Convert to decimal
    start_dec = hex_to_dec(start)
    stop_dec = hex_to_dec(stop)

    # Interpolate
    interp_dec = np.linspace(start_dec, stop_dec, steps)

    # Convert back to hex
    hex_interp = [dec_to_hex(i) for i in interp_dec]

    # Return
    return hex_interp


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

    result = color_interpolator(
        start='#8ac839',
        stop='#0BFCC7',
        steps=10,
    )
    print(result)
