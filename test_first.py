import json

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection
import matplotlib as mpl

import json
from pprint import pprint as pp

with open('Parser/data_shapes.json') as json_data:
    d = json.load(json_data)
    json_data.close()


list_of_polys = []
for key, value in d.items():
    list_of_polys.append(value)



colorvec = np.linspace(0.2, 0.3, len(list_of_polys))



#--------------------------------------------------
#  Test the plot
#--------------------------------------------------



fig, ax = plt.subplots()
# Make the collection and add it to the plot.
coll = PolyCollection(list_of_polys,
                      array=colorvec,
                      cmap=mpl.cm.jet,
                      edgecolors='black')
ax.add_collection(coll)
ax.autoscale_view()

# Add a colorbar for the PolyCollection
fig.colorbar(coll, ax=ax)
plt.show()


#--------------------------------------------------

tt = np.array( [[-100, -100]] )

theta = np.pi/2
tt = np.array( [[np.cos(theta)   , np.sin(theta)],
                [ -np.sin(theta)  , np.cos(theta)]] )




def rotate(poly, theta=np.pi/2):
    tt = np.array( [[ np.cos(theta)  , np.sin(theta)],
                    [ -np.sin(theta) , np.cos(theta)]] )
    return np.matmul(poly, tt)



Mat_translation = np.array(
    [[  1 , 0  ,  -100 ],
     [  0 , 1  ,  -100 ],
     [  0 , 0  , 1     ]]
    )

new_list_of_polys = map(lambda x: x , list_of_polys)

np.concatenate([x, np.ones((x.shape[0],1))] ,axis=1)


fig, ax = plt.subplots()
# Make the collection and add it to the plot.
coll = PolyCollection(new_list_of_polys, array=colorvec, cmap=mpl.cm.jet, edgecolors='black')
ax.add_collection(coll)
ax.autoscale_view()
ax.set_aspect('equal', 'box')
fig.colorbar(coll, ax=ax)
plt.show()



angles = np.linspace(0, np.pi*2, 8 )
angles = np.linspace(0, np.pi, 20)

list_of_transformed_polylists = [ map(lambda x: rotate(x, a), new_list_of_polys) for a in  angles]



fig, ax = plt.subplots()
# Make the collection and add it to the plot.


coll = PolyCollection(new_list_of_polys, array=colorvec, cmap=mpl.cm.jet, edgecolors='black')
ax.add_collection(coll)

for transformed in list_of_transformed_polylists:
    coll = PolyCollection(transformed, array=colorvec,
                          cmap=mpl.cm.jet,
                          edgecolors='black')
    ax.add_collection(coll)

ax.autoscale_view()

ax.set_aspect('equal', 'box')

# Add a colorbar for the PolyCollection
fig.colorbar(coll, ax=ax)
plt.show()



# In the future, use
# https://en.wikipedia.org/wiki/Transformation_matrix#Affine_transformations
# and
# https://en.wikipedia.org/wiki/Translation_(geometry)

