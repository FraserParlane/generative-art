import lxml.builder
import lxml.etree
import numpy as np
import os

# Generate the base elements.
elements = lxml.builder.ElementMaker()

# Set the random seed
np.random.seed(1)


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
    :param x: The x position of the centre
    :param y: The y position of the centre
    :param r: The radius
    :param start: The start position of the arc. Measured in polar coordinates
    where 1 is a complete rotation. The arc is drawn between the start and the
    stop position
    :param stop: The stop position of the arc. Measured in polar coordinates
    where 1 is a complete rotation. The arc is drawn between the start and the
    stop position
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


def make_random_circle_arc(
        x: float,
        y: float,
        r: float,
        d_buff: float,
) -> elements.path:
    """
    Make a circle arc of random length
    :param x: The x position of the centre
    :param y: The y position of the centre
    :param r: The radius
    :param d_buff: The buffer on the sweep. For example, if d_buff = 0.1, the
    length of the arc is randomly chosen between 0.05 and 0.95
    :return: The path element
    """

    # Generate random start and stop positions
    start = np.random.uniform()
    stop_min = start + d_buff
    stop_max = 1 + start - d_buff
    stop = np.random.uniform(stop_min, stop_max) % 1

    # Return the circle arc path
    return make_circle_arc(
        x=x,
        y=y,
        r=r,
        start=start,
        stop=stop,
    )


def run():

    # Constants that define the page
    height = 1000
    width = 1000
    doc = elements.doc
    svg = elements.svg

    # Constants that define circle generation
    rows = 3
    cols = 3
    min_r = 10
    max_r = 100
    n = 3
    min_d = 10
    max_d = 80
    page_pad = 350
    d_buff = 0.2
    lw = 5
    bg_color = '#1b1b1b'
    draw_color = '#ff9800'

    # Create SVG fields
    path = elements.path
    circle = elements.circle
    rect = elements.rect
    animate_transform = elements.animateTransform

    # Create document with white background
    doc = svg(
        xmlns="http://www.w3.org/2000/svg",
        height=str(height),
        width=str(width),
        style='background-color: white;'
    )
    doc.append(rect(
        x='0',
        y='0',
        width=str(width),
        height=str(height),
        fill=bg_color,
    ))

    # Calculate some spacing constants
    x_space = (width - 2 * page_pad) / (rows - 1)
    y_space = (height - 2 * page_pad) / (cols - 1)
    d_space = (max_d - min_d) / n

    # Alternate the rotation direction
    direction = 1

    # For each position, circle
    for i_row in range(rows):
        for i_col in range(cols):
            for i_n in range(n):

                # Create the positions
                x = page_pad + i_row * x_space
                y = page_pad + i_col * y_space
                r = min_d + i_n * d_space

                # Make circle arcs
                a = make_random_circle_arc(
                    x=x,
                    y=y,
                    r=r,
                    d_buff=d_buff,

                )

                # Format
                a.attrib['stroke'] = draw_color
                a.attrib['fill'] = 'none'
                a.attrib['stroke-width'] = str(lw)
                a.attrib['stroke-linecap'] = 'round'

                # Animate
                anim = animate_transform(
                    attributeName='transform',
                    type='rotate',
                    begin='0s',
                    dur='10s',
                    repeatCount='indefinite',
                )
                anim.attrib['from'] = f'0 {x} {y}'
                anim.attrib['to'] = f'{direction * 360} {x} {y}'
                a.append(anim)

                # Dash some
                if np.random.uniform() < 1 / 3:
                    a.attrib['stroke-dasharray'] = '7 15'

                # Add to document
                doc.append(a)

                # Generate a circle at a random angle
                theta = np.random.uniform()
                cx = x + r * np.cos(theta * 2 * np.pi)
                cy = y + r * np.sin(theta * 2 * np.pi)

                # Randomly, for 1/3
                if np.random.uniform() < 1/3:

                    # Add the circle
                    circ = circle(
                        cx=str(cx),
                        cy=str(cy),
                        r=str(d_space / 3),
                        stroke=draw_color,
                        fill=bg_color,
                    )
                    circ.attrib['stroke-width'] = str(lw)

                    # Animate
                    anim = animate_transform(
                        attributeName='transform',
                        type='rotate',
                        begin='0s',
                        dur='10s',
                        repeatCount='indefinite',
                    )
                    anim.attrib['from'] = f'0 {x} {y}'
                    anim.attrib['to'] = f'{direction * 360 * -1} {x} {y}'
                    circ.append(anim)
                    doc.append(circ)

                # Reverse direction for next object
                direction *= -1
    # Save
    base = os.path.basename(__file__).split('.')[0]
    with open(f'svg/{base}.svg', 'wb') as f:
        f.write(lxml.etree.tostring(doc, pretty_print=True))


if __name__ == "__main__":
    run()
