import lxml.builder
import lxml.etree
import numpy as np
import os

# Generate the base elements.
elements = lxml.builder.ElementMaker()

# Set the random seed
np.random.seed(1)


def grid_to_d(grid, offset):
    c = grid.reshape(4, 2)

    # Shrink
    c[0:2, 0] = c[0:2, 0] + offset
    c[1, 1] = c[1, 1] - offset
    c[3, 1] = c[3, 1] - offset

    # Generate path string
    d = f'M {c[0, 0]} {c[0, 1]}'
    for k in [0, 2, 1]:
        d += f' L {c[k + 1, 0]} {c[k + 1, 1]}'
    d += ' Z'

    return d


def run():

    # Constants that define the page
    height = 1000
    width = 1000
    svg = elements.svg

    # Drawing constants
    bg_color = '#1b1b1b'
    draw_color = '#a6e22e'

    # Elements
    rect = elements.rect
    path = elements.path
    animate_transform = elements.animateTransform
    animate = elements.animate

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

    # Constants that define the drawing
    n = 10
    n_rand = 10
    page_buff = 300
    shrink = 0.2
    random = 0.01

    # Calculate constants
    stride = (width - 2 * page_buff) / (n - 1)
    offset = stride * shrink

    # Make grid, random offsetS
    grid = np.zeros((n, n, 2))
    rand_offsets = [np.random.uniform(1-random, 1+random, (n, n, 2)) for i in range(n_rand)]

    # Fill with values, apply random offset
    for i, i_val in enumerate(np.linspace(page_buff, height - page_buff, n)):
        for j, j_val in enumerate(np.linspace(page_buff, width - page_buff, n)):
            grid[i, j] = (i_val, j_val)
    grids = [grid * rand for rand in rand_offsets]

    # For each square
    for j in range(n-1):
        for i in range(n-1):

            # Create d paths
            ds = [grid_to_d(g[i:i+2, j:j+2], offset=offset) for g in grids]

            # Plot square
            p = path(
                d=ds[0],
                fill='none',
                stroke=draw_color,
            )
            p.attrib['stroke-width'] = str(3)

            # Anim values
            values = '; '.join(ds + ds[:1])
            key_splines = '0.3 0 0.7 1; ' * n_rand

            anim = animate(
                attributeName='d',
                values=values,
                dur='5s',
                repeatCount='indefinite',
                keySplines=key_splines[:-1],
                calcMode='spline',
            )
            p.append(anim)
            doc.append(p)

    # Save
    base = os.path.basename(__file__).split('.')[0]
    with open(f'../svg/{base}.svg', 'wb') as f:
        f.write(lxml.etree.tostring(doc, pretty_print=True))


if __name__ == "__main__":
    run()
