import json
import copy
import os
import numpy as np

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from matplotlib.collections import PolyCollection
from importlib import reload

import pprint as pp

import multiprocessing as mp

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

# Make the plane face upwards
turn_rad = np.radians(90)
plane.update_rotation( turn_rad )

# Write out the plane polygons in this position

plane_polys = plane.current()

plane_polys = [x.tolist() for x in plane_polys]

savepath = 'plane_plots'
savename = 'plane_AA_shapes.json'
savefullname = Path(savepath, savename)
with open(savefullname, 'w') as f:
    f.write(json.dumps(plane_polys, indent=2))

# ------------------------------------------
#   Kill some planes
# ------------------------------------------


def simulate_plane_damage(seed):
    # Use the plane number as seed, otherwise parallel runs won't work properly
    np.random.seed(seed)
    plane_test = copy.deepcopy(plane)
    Nshots = 500
    hits = []
    ishot = 1
    while not plane_test.is_destroyed() and ishot <= Nshots:
        shot = Panels.generate_point(radius=80)
        dmg = plane_test.take_hit(*shot)
        if dmg > 0:
            hits.append(shot)
        ishot = ishot + 1

    health = plane_test.get_health()
    destroyed = plane_test.is_destroyed()
    numhits = len(hits)

    plane_outcome = {
        #'health' : health,
        'destroyed' : destroyed,
        'hits' : hits,
        'numhits': numhits}

    return plane_outcome


# You have to declare the pool after declaring the function you want exported
N = 100
print('Starting parallel workers')
pool = mp.Pool(4)
results = pool.map(simulate_plane_damage, [i for i in range(N)])
pool.close()

# Check that they are all unique
# If we aren't careful with the seeds, we will not get N unique damage patterns
# https://stackoverflow.com/a/9433953/2001958
# Dumb check: Do a sum of all the hit x,y coordinates.
checksum = np.array([np.array(res['hits']).sum() for res in results])
assert len(set(checksum)) == N # If this fails, your normal seeds are wrong

def plane_poly_collection(destroyed):
    """
    Function to return a polycollection for a generic plane
    """
    facec = 'red' if destroyed else 'blue'
    res = PolyCollection(plane.current(),
                   edgecolors='black',
                   facecolors=facec,
                   alpha=0.6)
    return res


Path("plane_plots").mkdir(parents=True, exist_ok=True)
def plot_plane(key, plane_outcome):
    destroyed = plane_outcome['destroyed']
    hits = np.array(plane_outcome['hits'])

    fig, ax = plt.subplots()
    ax.add_collection(plane_poly_collection(destroyed))
    ax.autoscale_view()
    ax.set_aspect('equal', 'box')
    ax.scatter(hits[:,0], hits[:,1],s=6, c='black')

    savepath = 'plane_plots'

    plt.title('Destroyed: {}'.format(destroyed))
    savename = '{name}.png'.format(name=key)
    savefullname = Path(savepath, savename)
    plt.savefig(savefullname)
    plt.close()
    plt.clf()

    savename = '{name}.json'.format(name=key)
    savefullname = Path(savepath, savename)
    with open(savefullname, 'w') as f:
        f.write(json.dumps(plane_outcome))

    return None

print('plotting planes in parallel')
pool = mp.Pool(4)
plane_names = ['plane_{}'.format(i) for i in range(N)]
parallel_args = zip(plane_names, results)
pool.starmap(plot_plane, parallel_args)
pool.close()
print('done')





