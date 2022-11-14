import lxml.builder
import lxml.etree
import numpy as np

# Generate the base elements.
elements = lxml.builder.ElementMaker()


def make_circle_arc(
        x: float,
        y: float,
        r: float,
        start: float,
        stop: float,
) -> elements.path:
    """
    Generate a path element for an arc on a circle. The arc will be drawn
    counterclockwise from start to stop
    :param x: The x position of the centre.
    :param y: The y position of the centre.
    :param r: The radius
    :param start: The start position of the arc. Measured in polar coordinates
    where 1 is a complete rotation. The arc is drawn between the start and the
    stop position.
    :param stop: The stop position of the arc. Measured in polar coordinates
    where 1 is a complete rotation. The arc is drawn between the start and the
    stop position.
    :return: The path element.
    """

    # Check locations
    for loc in [start, stop]:
        if loc < 0 or loc > 1:
            raise ValueError(f'{loc} not in [0, 1]')

    # Get the x, y position of the start and stop locations.
    start_x = x + r * np.cos((1 - start) * 2 * np.pi)
    start_y = y + r * np.sin((1 - start) * 2 * np.pi)
    stop_x = x + r * np.cos((1 - stop) * 2 * np.pi)
    stop_y = y + r * np.sin((1 - stop) * 2 * np.pi)

    # If the distance from start to stop is _, flip
    dist = stop - start
    dist += 1 if dist < 0 else 0
    large = 1 if dist > 0.5 else 0

    # Generate the path d attribute
    d = f'M {start_x} {start_y} A {r} {r} 0 {large} 0 {stop_x} {stop_y}'

    # Make and return the path
    path = elements.path
    p = path(d=d)
    return p


def run():


    height = '1000'
    width = '1000'
    doc = elements.doc
    svg = elements.svg

    # Create SVG fields
    path = elements.path
    circle = elements.circle
    rect = elements.rect

    # Create document with white background
    doc = svg(
        xmlns="http://www.w3.org/2000/svg",
        height=height,
        width=width,
        style='background-color: white;'
    )
    doc.append(rect(
        x='0',
        y='0',
        width=width,
        height=height,
        fill='white',
    ))

    p = make_circle_arc(
        x=500,
        y=500,
        r=100,
        start=0.95,
        stop=0.55,
    )
    p.attrib['stroke'] = 'crimson'
    p.attrib['stroke-width'] = '5'
    p.attrib['fill'] = 'none'
    doc.append(p)

    # Outline circle
    doc.append(circle(
        cx='500',
        cy='500',
        r='100',
        stroke='silver',
        fill='None',
    ))

    # # Circle
    # c = circle(
    #     cx='500',
    #     cy='500',
    #     r='5',
    #     stroke='red',
    #     fill='None',
    # )
    # print(c.attrib['stroke'])
    # doc.append(c)

    # Save
    with open('xml-approach.svg', 'wb') as f:
        f.write(lxml.etree.tostring(doc, pretty_print=True))


if __name__ == "__main__":
    run()