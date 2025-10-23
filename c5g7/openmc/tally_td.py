import openmc

###############################################################################
#                   Exporting to OpenMC tallies.xml File
###############################################################################

tallies = {}

# Instantiate a tally mesh
material_filter = openmc.MaterialFilter([1,2])

energy_filter = openmc.EnergyFilter(e_bins)

delay_filter = openmc.DelayedGroupFilter(np.arange(1, n_dg+1, 1))

tallies = openmc.Tallies()

tally = openmc.Tally(name='flux tally')
tally.scores = ['flux']
tally.filters = [material_filter, energy_filter]
tallies.append(tally)

tally = openmc.Tally(name='precursor tally')
tally.scores = ['precursors']
tally.filters = [material_filter, delay_filter]
tallies.append(tally)

tally = openmc.Tally(name='fission rate tally')
tally.scores = ['fission']
tally.filters = [material_filter]
tallies.append(tally)

# Instantiate some tally Filters
mesh_filter = openmc.MeshFilter(mesh)

# Instantiate the Tally
tallies['Mesh Rates'] = openmc.Tally(tally_id=1, name='tally 1')
tallies['Mesh Rates'].filters = [mesh_filter]
tallies['Mesh Rates'].scores = ['flux', 'fission', 'nu-fission']

tallies['Global Rates'] = openmc.Tally(tally_id=2, name='tally 2')
tallies['Global Rates'].scores = ['flux', 'fission', 'nu-fission']
