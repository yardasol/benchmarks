import openmc
import sys
sys.path.append('../')
from materials_td import materials
from lattices_rr import lattices, universes, cells
from surfaces_rr import surfaces
from tally import tallies

###############################################################################
#                      Simulation Input File Parameters
###############################################################################

# OpenMC simulation parameters
batches = 20000
inactive = 3500 
particles = 650

###############################################################################
#                 Exporting to OpenMC materials.xml File
###############################################################################

# Instantiate a Materials collection, register all Materials, and export to XML
materials_file = openmc.Materials(materials.values())
materials_file.cross_sections = './mgxs.h5'
materials_file.export_to_xml()


###############################################################################
#                 Exporting to OpenMC geometry.xml File
###############################################################################

# Instantiate Core boundaries
cells['Core'].region = +surfaces['Core x-min'] & +surfaces['Core y-min'] & \
    -surfaces['Core x-max'] & -surfaces['Core y-max']

lattices['Core'] = openmc.RectLattice(lattice_id=201, name='3x3 core lattice')
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
geometry.export_to_xml()


###############################################################################
#                   Exporting to OpenMC settings.xml File
###############################################################################

# Instantiate a Settings, set all runtime parameters, and export to XML
settings_file = openmc.Settings()
settings_file.energy_mode = "multi-group"
settings_file.batches = batches
settings_file.inactive = inactive
settings_file.particles = particles
settings_file.output = {'tallies': True, 'summary': True}
lower_left = (-32.13, -32.13, -1)
upper_right = (32.13, 32.13, 1)
uniform_dist = openmc.stats.Box(lower_left, upper_right)
rr_source = openmc.IndependentSource(space=uniform_dist)

settings_file.random_ray['distance_active'] = 628.0
settings_file.random_ray['distance_inactive'] = 13.0
settings_file.random_ray['ray_source'] = rr_source
settings_file.random_ray['volume_normalized_flux_tallies'] = True
settings_file.random_ray['bd_order'] = 4
settings_file.random_ray['sample_method'] = 'halton'
settings_file.random_ray['time_mode'] = 'ti'
settings_file.random_ray['precursor_mode'] = 'bd'

settings_file.run_mode = "time dependent"
settings_file.time_dependent = {
    "dt": 1,
    "n_timesteps": 1000,
    "timestep_units": "ms",
}
settings_file.export_to_xml()


###############################################################################
#                   Exporting to OpenMC plots.xml File
###############################################################################

plot_1 = openmc.Plot(plot_id=1)
plot_1.filename = 'plot_1'
plot_1.origin = [0.0, 0.0, 0.0]
plot_1.width = [64.26, 64.26]
plot_1.pixels = [500, 500]
plot_1.color_by = 'material'
plot_1.basis = 'xy'

# Instantiate a Plots collection and export to XML
plot_file = openmc.Plots([plot_1])
plot_file.export_to_xml()

###############################################################################
#                   Exporting to OpenMC tallies.xml File
###############################################################################

# Instantiate a Tallies, register Tally/Mesh, and export to XML
tallies_file = openmc.Tallies(tallies.values())
tallies_file.export_to_xml()
