import openmc
## TODO: ADD OPTION FOR CONDITIONAL IMPORT FOR TD OR SS SIMULATIONS
import numpy as np
from materials_td import materials
from surfaces_rr import surfaces

###############################################################################
#                     Create a dictionary of all shared cells
###############################################################################

# Instantiate Cells
pincell_type = ['UO2', 'MOX 4.3%', 'MOX 7.0%', 'MOX 8.7%', 'Fission Chamber', 'Guide Tube', 'Control Rod']

cells = {}

# Normal cells
for pt in pincell_type:
    for i in range(8):
        cells[f'{pt} Inner 1 Azimuthal {i}'] = openmc.Cell(
            name=f'{pt} Inner 1 Azimuthal {i}'
        )
        cells[f'{pt} Inner 2 Azimuthal {i}'] = openmc.Cell(
            name=f'{pt} Inner 3 Azimuthal {i}'
        )
        cells[f'{pt} Inner 3 Azimuthal {i}'] = openmc.Cell(
            name=f'{pt} Inner 3 Azimuthal {i}'
        )
        cells[f'{pt} Inner 4 Azimuthal {i}'] = openmc.Cell(
            name=f'{pt} Inner 4 Azimuthal {i}'
        )
        cells[f'{pt} Inner 5 Azimuthal {i}'] = openmc.Cell(
            name=f'{pt} Inner 5 Azimuthal {i}'
        )

for pt in pincell_type:
    for i in range(8):
        cells[f'{pt} Moderator Inner A Azimuthal {i}'] = openmc.Cell(
            name=f'{pt} Moderator Inner A Azimuthal {i}'
        )
        cells[f'{pt} Moderator Outer B Azimuthal {i}'] = openmc.Cell(
            name=f'{pt} Moderator Outer B Azimuthal {i}'
        )
        cells[f'{pt} Moderator Outer C Azimuthal {i}'] = openmc.Cell(
            name=f'{pt} Moderator Outer C Azimuthal {i}'
        )

## Material cell
cells['Reflector']                   = openmc.Cell(name='Reflector')

## Lattice cells
cells['UO2 Unrodded Assembly']       = openmc.Cell(name='UO2 Unrodded Assembly')
cells['UO2 Rodded Assembly']         = openmc.Cell(name='UO2 Rodded Assembly')
cells['MOX Unrodded Assembly']       = openmc.Cell(name='MOX Unrodded Assembly')
cells['MOX Rodded Assembly']         = openmc.Cell(name='MOX Rodded Assembly')
cells['Reflector Unrodded Assembly'] = openmc.Cell(name='Water Unrodded Assembly')
cells['Reflector Rodded Assembly']   = openmc.Cell(name='Water Rodded Assembly')
cells['Core']                        = openmc.Cell(name='Core')

# Use surface half-spaces to define regions
for pt in pincell_type:
    for i in range(8):
        cells[f'{pt} Inner 1 Azimuthal {i}'].region = (
            -surfaces['Pin Cell Inner Ring 1'] &
            +surfaces[f'Azimuthal Plane {i}'] &
            -surfaces[f'Azimuthal Plane {(i+1) % 8}']
        )
        cells[f'{pt} Inner 2 Azimuthal {i}'].region = (
            +surfaces['Pin Cell Inner Ring 1'] &
            -surfaces['Pin Cell Inner Ring 2'] &
            +surfaces[f'Azimuthal Plane {i}'] &
            -surfaces[f'Azimuthal Plane {(i+1) % 8}']
        )
        cells[f'{pt} Inner 3 Azimuthal {i}'].region = (
            +surfaces['Pin Cell Inner Ring 2'] &
            -surfaces['Pin Cell Inner Ring 3'] &
            +surfaces[f'Azimuthal Plane {i}'] &
            -surfaces[f'Azimuthal Plane {(i+1) % 8}']
        )
        cells[f'{pt} Inner 4 Azimuthal {i}'].region = (
            +surfaces['Pin Cell Inner Ring 3'] &
            -surfaces['Pin Cell Inner Ring 4'] &
            +surfaces[f'Azimuthal Plane {i}'] &
            -surfaces[f'Azimuthal Plane {(i+1) % 8}']
        )
        cells[f'{pt} Inner 5 Azimuthal {i}'].region = (
            +surfaces['Pin Cell Inner Ring 4'] &
            -surfaces['Pin Cell ZCylinder'] &
            +surfaces[f'Azimuthal Plane {i}'] &
            -surfaces[f'Azimuthal Plane {(i+1) % 8}']
        )

for pt in pincell_type:
    for i in range(8):
        cells[f'{pt} Moderator Inner A Azimuthal {i}'].region = (
            +surfaces['Pin Cell ZCylinder'] &
            -surfaces['Pin Cell Outer Ring A'] &
            +surfaces[f'Azimuthal Plane {i}'] &
            -surfaces[f'Azimuthal Plane {(i+1) % 8}']
        )
        cells[f'{pt} Moderator Outer B Azimuthal {i}'].region = (
            +surfaces['Pin Cell Outer Ring A'] &
            -surfaces['Pin Cell Outer Ring B'] &
            +surfaces[f'Azimuthal Plane {i}'] &
            -surfaces[f'Azimuthal Plane {(i+1) % 8}']
        )
        cells[f'{pt} Moderator Outer C Azimuthal {i}'].region = (
            +surfaces['Pin Cell Outer Ring B'] &
            +surfaces[f'Azimuthal Plane {i}'] &
            -surfaces[f'Azimuthal Plane {(i+1) % 8}']
        )

## TODO: Delete this and make a bounding box for the universe in pin/build-xml-pin-rr.py
#cells['UO2 Pin'].region                   = +surfaces['Pin Cell ZCylinder'] & \
#                                            +surfaces['Pin x-min'] & \
#                                            -surfaces['Pin x-max'] & \
#                                            +surfaces['Pin y-min'] & \
#                                            -surfaces['Pin y-max']

# Register Materials with Cells
for pt in pincell_type:
    for i in range(8):
        cells[f'{pt} Inner 1 Azimuthal {i}'].fill = materials[pt]
        cells[f'{pt} Inner 2 Azimuthal {i}'].fill = materials[pt]
        cells[f'{pt} Inner 3 Azimuthal {i}'].fill = materials[pt]
        cells[f'{pt} Inner 4 Azimuthal {i}'].fill = materials[pt]
        cells[f'{pt} Inner 5 Azimuthal {i}'].fill = materials[pt]


for pt in pincell_type:
    for i in range(8):
        cells[f'{pt} Moderator Inner A Azimuthal {i}'].fill = materials['Water']
        cells[f'{pt} Moderator Outer B Azimuthal {i}'].fill = materials['Water']
        cells[f'{pt} Moderator Outer C Azimuthal {i}'].fill = materials['Water']

# Material Cell
reflector_infinite = {}
for i in range(10):
    reflector_infinite[f'Reflector Infinite {i}'] = openmc.Cell(fill=materials['Water'],
                                                                name=f'Reflector Infinite {i}')

ru0 = openmc.Universe(universe_id=15, cells=[reflector_infinite['Reflector Infinite 0']])
ru1 = openmc.Universe(universe_id=16, cells=[reflector_infinite['Reflector Infinite 1']])
ru2 = openmc.Universe(universe_id=17, cells=[reflector_infinite['Reflector Infinite 2']])
ru3 = openmc.Universe(universe_id=18, cells=[reflector_infinite['Reflector Infinite 3']])
ru4 = openmc.Universe(universe_id=19, cells=[reflector_infinite['Reflector Infinite 4']])

pitch = 1.26
lattice = openmc.RectLattice(lattice_id=100)
lattice.lower_left = [-pitch/2.0, -pitch/2.0]
lattice.pitch = [pitch/5.0, pitch/5.0]
arr = np.array([ru1, ru2, ru3, ru4, ru0])
univs = arr
for i in range(1,5):
    univs = np.vstack((univs, np.roll(arr, i)))
np.random.shuffle(univs)
lattice.universes = univs
cells['Reflector'].fill = lattice
