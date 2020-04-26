import json

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import matplotlib as mpl
import copy
from importlib import reload

import json
from pprint import pprint as pp

plotter = False

with open('Parser/data_shapes.json') as json_data:
    d = json.load(json_data)
    json_data.close()


list_of_polys = []
for key, value in d.items():
    list_of_polys.append(value)


import physics.Panels as Panels
reload(Panels)


A = Panels.panel(list_of_polys[0])


plane = Panels.plane(list_of_polys=list_of_polys)

# Set the reference location and heading
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
plane.fix_ref_location(-100, -100)
plane.fix_ref_rotation(np.pi/2)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# For a random walk flight path

fig, ax = plt.subplots()

coll = PolyCollection(plane.current(), edgecolors='black')
ax.add_collection(coll)

n_steps = 10

for i in range(1,n_steps+1):

    plane.move_forward( 140 )
    if i % 2 ==0:
        # random turn angle
        turn_span = 60
        rr = -(turn_span/2) + np.random.random_sample()*turn_span
        turn_rad = np.radians(rr)
        plane.update_rotation( turn_rad )

    coll = PolyCollection(plane.current(), edgecolors='black')
    ax.add_collection(coll)


ax.autoscale_view()
ax.set_aspect('equal', 'box')
plt.show()
