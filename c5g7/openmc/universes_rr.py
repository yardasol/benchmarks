import openmc
from cells_rr import cells, pincell_type

###############################################################################
#                     Create a dictionary of all shared universes
###############################################################################

# Instantiate Universes
universes = {}
universes['Root']                        = openmc.Universe(universe_id=0,  name='Root')
universes['UO2']                         = openmc.Universe(universe_id=1,  name='UO2')
universes['MOX 4.3%']                    = openmc.Universe(universe_id=2,  name='MOX 4.3%')
universes['MOX 7.0%']                    = openmc.Universe(universe_id=3,  name='MOX 7.0%')
universes['MOX 8.7%']                    = openmc.Universe(universe_id=4,  name='MOX 8.7%')
universes['Fission Chamber']             = openmc.Universe(universe_id=5,  name='Fission Chamber')
universes['Guide Tube']                  = openmc.Universe(universe_id=6,  name='Guide Tube')
universes['Control Rod']                 = openmc.Universe(universe_id=7,  name='Control Rod')
universes['Reflector']                   = openmc.Universe(universe_id=8,  name='Reflector')
universes['UO2 Unrodded Assembly']       = openmc.Universe(universe_id=9,  name='UO2 Unrodded Assembly')
universes['UO2 Rodded Assembly']         = openmc.Universe(universe_id=10, name='UO2 Rodded Assembly')
universes['MOX Unrodded Assembly']       = openmc.Universe(universe_id=11, name='MOX Unrodded Assembly')
universes['MOX Rodded Assembly']         = openmc.Universe(universe_id=12, name='MOX Rodded Assembly')
universes['Reflector Unrodded Assembly'] = openmc.Universe(universe_id=13, name='Reflector Unrodded Assembly')
universes['Reflector Rodded Assembly']   = openmc.Universe(universe_id=14, name='Reflector Rodded Assembly')

# Register Cells with Universes
universes['Root']                       .add_cell(cells['Core'])

for pt in pincell_type:
    for i in range(8):
        universes[f'{pt}'].add_cells(
                [
                    cells[f'{pt} Inner A Azimuthal {i}'],
                    cells[f'{pt} Inner B Azimuthal {i}'],
                    cells[f'{pt} Inner C Azimuthal {i}'],
                    cells[f'{pt} Moderator Inner A Azimuthal {i}'],
                    cells[f'{pt} Moderator Outer B Azimuthal {i}'],
                    cells[f'{pt} Moderator Outer C Azimuthal {i}']
                ]
        )

universes['Reflector']                  .add_cell(cells['Reflector'])
universes['UO2 Unrodded Assembly']      .add_cell(cells['UO2 Unrodded Assembly'])
universes['UO2 Rodded Assembly']        .add_cell(cells['UO2 Rodded Assembly'])
universes['MOX Unrodded Assembly']      .add_cell(cells['MOX Unrodded Assembly'])
universes['MOX Rodded Assembly']        .add_cell(cells['MOX Rodded Assembly'])
universes['Reflector Unrodded Assembly'].add_cell(cells['Reflector Unrodded Assembly'])
universes['Reflector Rodded Assembly']  .add_cell(cells['Reflector Rodded Assembly'])
