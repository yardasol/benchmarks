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
        cells[f'{pt} Inner A Azimuthal {i}'] = openmc.Cell(
            name=f'{pt} Inner A Azimuthal {i}'
        )
        cells[f'{pt} Inner B Azimuthal {i}'] = openmc.Cell(
            name=f'{pt} Inner B Azimuthal {i}'
        )
        cells[f'{pt} Inner C Azimuthal {i}'] = openmc.Cell(
            name=f'{pt} Inner C Azimuthal {i}'
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
        cells[f'{pt} Inner A Azimuthal {i}'].region = (
            -surfaces['Pin Cell Inner Ring A'] &
            +surfaces[f'Azimuthal Plane {i}'] &
            -surfaces[f'Azimuthal Plane {(i+1) % 8}']
        )
        cells[f'{pt} Inner B Azimuthal {i}'].region = (
            +surfaces['Pin Cell Inner Ring A'] &
            -surfaces['Pin Cell Inner Ring B'] &
            +surfaces[f'Azimuthal Plane {i}'] &
            -surfaces[f'Azimuthal Plane {(i+1) % 8}']
        )
        cells[f'{pt} Inner C Azimuthal {i}'].region = (
            +surfaces['Pin Cell Inner Ring B'] &
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
        cells[f'{pt} Inner A Azimuthal {i}'].fill = materials[pt]
        cells[f'{pt} Inner B Azimuthal {i}'].fill = materials[pt] 
        cells[f'{pt} Inner C Azimuthal {i}'].fill = materials[pt]

for pt in pincell_type:
    for i in range(8):
        cells[f'{pt} Moderator Inner A Azimuthal {i}'].fill = materials['Water'] 
        cells[f'{pt} Moderator Outer B Azimuthal {i}'].fill = materials['Water'] 
        cells[f'{pt} Moderator Outer C Azimuthal {i}'].fill = materials['Water'] 

# Material Cell
reflector_infinite = openmc.Cell(fill=materials['Water'],
                                 name='Reflector Infinite')
ru = openmc.Universe()
ru.add_cells([reflector_infinite])

pitch = 1.26
lattice = openmc.RectLattice()
lattice.lower_left = [-pitch/2.0, -pitch/2.0]
lattice.pitch = [pitch/10.0, pitch/10.0]
lattice.universes = np.full((10, 10), ru)

cells['Reflector'].fill = lattice
