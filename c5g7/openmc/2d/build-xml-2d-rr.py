import openmc
import sys
sys.path.append('../')
from materials_td import materials
from lattices_rr import lattices, universes, cells
from surfaces_rr import surfaces
from tally_td import tallies

###############################################################################
#                      Simulation Input File Parameters
###############################################################################

# OpenMC simulation parameters
batches = 10000
inactive = 3500
particles = 650

###############################################################################
#                       OpenMC materials.xml File
###############################################################################

# Instantiate a Materials collection, register all Materials, and export to XML
materials = openmc.Materials(materials.values())
materials.cross_sections = './mgxs.h5'

###############################################################################
#                       OpenMC geometry.xml File
###############################################################################

# Instantiate Core boundaries
cells['Core'].region = +surfaces['Core x-min'] & +surfaces['Core y-min'] & \
    -surfaces['Core x-max'] & -surfaces['Core y-max']

lattices['Core'] = openmc.RectLattice(lattice_id=2010, name='3x3 core lattice')
lattices['Core'].dimension = [3, 3]
lattices['Core'].lower_left = [-32.13, -32.13]
lattices['Core'].pitch = [21.42, 21.42]
w = universes['Reflector Unrodded Assembly']
u = universes['UO2 Unrodded Assembly']
m = universes['MOX Unrodded Assembly']
lattices['Core'].universes = [[u, m, w], [m, u, w], [w, w, w]]
cells['Core'].fill = lattices['Core']

# Instantiate a Geometry, register the root Universe, and export to XML
geometry = openmc.Geometry()
geometry.root_universe = universes['Root']


###############################################################################
#                         OpenMC settings.xml File
###############################################################################

# Instantiate a Settings, set all runtime parameters, and export to XML
settings = openmc.Settings()
settings.energy_mode = "multi-group"
settings.batches = batches
settings.inactive = inactive
settings.particles = particles
settings.output = {'tallies': False, 'summary': True}
lower_left = (-32.13, -32.13, -1)
upper_right = (32.13, 32.13, 1)
uniform_dist = openmc.stats.Box(lower_left, upper_right)
rr_source = openmc.IndependentSource(space=uniform_dist)

settings.random_ray['distance_active'] = 628.0
settings.random_ray['distance_inactive'] = 13.0
settings.random_ray['ray_source'] = rr_source
settings.random_ray['volume_normalized_flux_tallies'] = True
settings.random_ray['bd_order'] = 1
settings.random_ray['sample_method'] = 'halton'
settings.random_ray['time_method'] = 'ti'
settings.random_ray['precursor_method'] = 'bd'

settings.run_mode = "time dependent"
settings.time_dependent = {
    "dt": 0.01,
    "n_timesteps": 1000,
    "timestep_units": "s",
}


###############################################################################
#                         OpenMC plots.xml File
###############################################################################
import random
plots = openmc.Plots()

plot = openmc.Plot.from_geometry(geometry, basis='xy')
plot.color_by = 'cell'
cell_dict = {}
# UO2, red
r = 255
for i in range(1,41):
    g = random.randrange(0, 128, 1)
    b = g
    cell_dict[i] = (r, g, b)
# MOX 4.3, green
g = 224
for i in range(41, 81):
    r = random.randrange(0, 128, 1)
    b = r
    cell_dict[i] = (r, g, b)
# MOX 7.0, orange
r = 255
for i in range(81, 121):
    b = random.randrange(0, 64, 1)
    g = 128 + b
    cell_dict[i] = (r, g, b)
# MOX 8.7, yellow
r = 255
for i in range(121, 161):
    b = random.randrange(0, 64, 1)
    g = r - b
    cell_dict[i] = (r, g, b)
# Fission Chamber, purple
r = 255
for i in range(161, 201):
    g = random.randrange(0, 64, 1)
    b = r - g
    cell_dict[i] = (r, g, b)
# Guide Tube, cyan
g = 224
for i in range(201, 241):
    r = random.randrange(0, 128, 1)
    b = g - r
    cell_dict[i] = (r, g, b)
# Control Rod, grey
for i in range(241, 281):
    r = random.randrange(112, 144, 1)
    g = r
    b = r
    cell_dict[i] = (r, g, b)
# Moderator, blue
b = 255
for i in range(281, 305):
    r = random.randrange(0, 128, 1)
    g = r
    cell_dict[i] = (r, g, b)
    cell_dict[i + 1 * 24] = (r, g, b)
    cell_dict[i + 2 * 24] = (r, g, b)
    cell_dict[i + 3 * 24] = (r, g, b)
    cell_dict[i + 4 * 24] = (r, g, b)
    cell_dict[i + 5 * 24] = (r, g, b)
    cell_dict[i + 6 * 24] = (r, g, b)
# Moderator Infinite, blue
b = 255
for i in range(457, 462):
    r = random.randrange(0, 128, 1)
    g = r
    cell_dict[i] = (r, g, b)

plot.width = (7 * 1.26, 7 * 1.26)
plot.origin = ((21.42 - 1.26)/2, (-21.42 + 1.26)/2, 0)
plot.pixels = (2000, 2000)
plot.colors = cell_dict
plots.append(plot)

plot = openmc.Plot.from_geometry(geometry, basis='xy')
plot.pixels = (2000, 2000)
plot.color_by = 'material'
plot.colors = {1: (255, 0, 0), # UO2, red
               2: (0, 255, 0), # MOX 4.3, green
               3: (255, 128, 0), # MOX 7, orange
               4: (255, 255, 0), # MOX 8.7, yellow
               5: (255, 0, 255), # Fission Chamber, purple
               6: (0, 192, 192), # Guide Tube, cyan
               7: (0, 0 , 255), # Water, blue
               8: (0, 0, 128),  # Water Reflector, blue
               9: (128, 128, 128)  # Water Reflector, grey
               }
plots.append(plot)

###############################################################################
#                         OpenMC tallies.xml File
###############################################################################

# Instantiate a Tallies, register Tally/Mesh, and export to XML
tallies = openmc.Tallies(tallies.values())

###############################################################################
#                       Export to OpenMC model.xml File
###############################################################################

model = openmc.Model(geometry, materials, settings, tallies, plots)
model.export_to_model_xml()
