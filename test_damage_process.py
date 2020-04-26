import json
import copy

import numpy as np

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from matplotlib.collections import PolyCollection
from importlib import reload

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

shots = 10000
points = [Panels.generate_point(radius=80) for x in range(shots)]
print("Taking shots")
hits = [plane.current_contains_point(*point) for point in points]
print("Done")
points = np.array(points)

not_hits = [not(hit) for hit in hits]

fig, ax = plt.subplots()
coll = PolyCollection(plane.current(), edgecolors='black', alpha=0.8)
ax.add_collection(coll)
ax.autoscale_view()
ax.set_aspect('equal', 'box')

ax.plot(points[not_hits,0], points[not_hits,1],'.', c='black', alpha=0.5)

damage = np.array([plane.calculate_damage_of_shot(hit[0], hit[1]) for hit in points[hits,:]])
ax.scatter(points[hits,0], points[hits,1],s=6, c=damage, cmap=cm.Reds)

plt.show()

plt.clf()
plt.close()


### Kill some planes

plane_test = copy.deepcopy(plane)


Nshots = 100
shots = [Panels.generate_point(radius=80) for x in range(shots)]
print("Taking shots")
for shot in shots:
    plane_test.take_hit(*shot)

plane_test.get_health()




