import json

from bokeh.plotting import figure, output_file, show
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import matplotlib as mpl
import copy

import json
from pprint import pprint as pp

with open('Parser/data_shapes.json') as json_data:
    d = json.load(json_data)
    json_data.close()


list_of_polys = []
for key, value in d.items():
    list_of_polys.append(value)


import Panels
reload(Panels)


A = Panels.panel(list_of_polys[0])


plane = Panels.plane(list_of_polys=list_of_polys)

plane.fix_ref_location(-100, -100)
plane.fix_ref_rotation(np.pi/2)


if False:
    fig, ax = plt.subplots()

    coll = PolyCollection(plane.current(), edgecolors='black')
    ax.add_collection(coll)


    for i in range(1,10):

        plane.move_forward( 140 )
        if i % 2 ==0:
            rr = -45 + np.random.random_sample()*90
            turn_deg = np.radians(rr)
            plane.update_rotation( turn_deg )

        coll = PolyCollection(plane.current(), edgecolors='black')
        ax.add_collection(coll)


    ax.autoscale_view()
    ax.set_aspect('equal', 'box')
    plt.show()


output_file("patch.html")

p = figure(match_aspect=True)

# add a patch renderer with an alpha an line width

for poly in plane.current():
    p.patch(poly[:,0],poly[:,1], alpha=0.5, line_width=2)

for i in range(1,10):

    plane.move_forward( 140 )
    if i % 2 ==0:
        rr = -45 + np.random.random_sample()*90
        turn_deg = np.radians(rr)
        plane.update_rotation( turn_deg )

    for poly in plane.current():
        p.patch(poly[:,0],poly[:,1], alpha=0.5, line_width=2)

show(p)






