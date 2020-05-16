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


plane = Panels.plane(list_of_polys=list_of_polys)

# Set the reference location and heading
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
plane.fix_ref_location(-100, -100)
plane.fix_ref_rotation(np.pi/2)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

turn_rad = np.radians(90)
plane.update_rotation( turn_rad )

x = 0.0
y = 0.0

shots = 1000
points = [Panels.generate_point(radius=80) for x in range(shots)]
print("Taking {} shots".format(shots))
hits = [plane.current_contains_point(*point) for point in points]
print("Done")
points = np.array(points)

not_hits = [not(hit) for hit in hits]

fig, ax = plt.subplots()
coll = PolyCollection(plane.current(), edgecolors='black', alpha=0.8)
ax.add_collection(coll)
ax.autoscale_view()
ax.set_aspect('equal', 'box')

ax.plot(points[hits,0], points[hits,1],'.', c='red', alpha=0.5)
ax.plot(points[not_hits,0], points[not_hits,1],'.', c='black', alpha=0.5)

# I will place two weak points here
ax.scatter([-15,15], [40, 40], s=100, c='green')

plt.show()


plt.clf()
plt.close()
fig, ax = plt.subplots()
ax.set_aspect('equal', 'box')

tt = ax.hexbin(points[hits,0], points[hits,1], gridsize=30)

x,y = tt.get_offsets().transpose()

ax.scatter(x,y,s = 5, c='white')

plt.show()
