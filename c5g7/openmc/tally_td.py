import openmc
import numpy as np
from materials_td import egroups, n_dg


###############################################################################
#                   Exporting to OpenMC tallies.xml File
###############################################################################

tallies = {}

# Instantiate a tally mesh
mesh = openmc.RegularMesh(mesh_id=1)
mesh.dimension = [51, 51, 1]
mesh.lower_left = [-32.13, -32.13, -1.e50]
mesh.upper_right = [32.13, 32.13, 1.e50]

# Instantiate some tally Filters
mesh_filter = openmc.MeshFilter(mesh)
energy_filter = openmc.EnergyFilter(egroups)
delay_filter = openmc.DelayedGroupFilter(np.arange(1, n_dg+1, 1))

# Instantiate the Tally
tallies['Mesh Rates'] = openmc.Tally(tally_id=1, name='tally 1')
tallies['Mesh Rates'].filters = [mesh_filter, energy_filter]
tallies['Mesh Rates'].scores = ['flux', 'fission', 'nu-fission']

tallies['Global Rates'] = openmc.Tally(tally_id=2, name='tally 2')
tallies['Global Rates'].filters = [energy_filter]
tallies['Global Rates'].scores = ['flux', 'fission', 'nu-fission']

tallies['Mesh Delayed'] = openmc.Tally(tally_id=3, name='tally 3')
tallies['Mesh Delayed'].filters = [mesh_filter, delay_group_filter]
tallies['Mesh Delayed'].scores = ['precursors']

tallies['Global Delayed'] = openmc.Tally(tally_id=4, name='tally 4')
tallies['Global Delayed'].filters = [delay_group_filter]
tallies['Global Rates'].scores = ['precursors']


