import openmc

###############################################################################
#                     Create a dictionary of all shared cells
###############################################################################

# Create a dictionary to store the surfaces
surfaces = {}
o_r = 0.54
ir_a = 0.33
ir_b = 0.45
or_a = 0.60
or_b = 0.69
fuel_or = openmc.ZCylinder(r=o_r, name='Fuel OR')

# Instantiate Pin Cell ZCylinder surface
surfaces['Pin Cell ZCylinder'] = openmc.ZCylinder(x0=0, y0=0, r=0.54, name='Pin Cell ZCylinder')
surfaces['Pin Cell Inner Ring A'] inner_ring_a = openmc.ZCylinder(r=ir_a, name='Pin Cell Inner Ring A')
surfaces['Pin Cell Inner Ring B'] inner_ring_b = openmc.ZCylinder(r=ir_b, name='Pin Cell Inner Ring B')
surfaces['Pin Cell Outer Ring A'] outer_ring_a = openmc.ZCylinder(r=or_a, name='Pin Cell Outer Ring A')
surfaces['Pin Cell Outer Ring B'] outer_ring_b = openmc.ZCylinder(r=or_b, name='Pin Cell Outer Ring B')

surfaces['Pin Cell Outer Ring B'] outer_ring_b = openmc.ZCylinder(r=or_b, name='Pin Cell Outer Ring B')

for i in range(8):
    angle = 2 * i * openmc.pi / 8
    normal_vector = (-openmc.sin(angle), openmc.cos(angle), 0)
    surfaces[f'Azimuthal Plane {i}'] = openmc.Plane(a=normal_vector[0],
                                                    b=normal_vector[1],
                                                    c=normal_vector[2], d=0)

surfaces['Core x-min']         = openmc.XPlane(x0=-32.13, name='Core x-min')
surfaces['Core x-max']         = openmc.XPlane(x0= 32.13, name='Core x-max')
surfaces['Core y-min']         = openmc.YPlane(y0=-32.13, name='Core y-min')
surfaces['Core y-max']         = openmc.YPlane(y0= 32.13, name='Core y-max')
surfaces['Small Core z-min']   = openmc.ZPlane(z0=-32.13, name='Small Core z-min')
surfaces['Small Core z-max']   = openmc.ZPlane(z0= 32.13, name='Small Core z-max')
surfaces['Big Core z-min']     = openmc.ZPlane(z0=-107.1, name='Big Core z-min')
surfaces['Big Core z-max']     = openmc.ZPlane(z0= 107.1, name='Big Core z-max')
surfaces['Pin x-min']          = openmc.XPlane(x0=-0.63, name='Pin x-min')
surfaces['Pin x-max']          = openmc.XPlane(x0=+0.63, name='Pin x-max')
surfaces['Pin y-min']          = openmc.YPlane(y0=-0.63, name='Pin y-min')
surfaces['Pin y-max']          = openmc.YPlane(y0=+0.63, name='Pin y-max')

surfaces['Core x-max'].boundary_type       = 'vacuum'
surfaces['Core y-min'].boundary_type       = 'vacuum'
surfaces['Core y-max'].boundary_type       = 'reflective'
surfaces['Small Core z-min'].boundary_type = 'reflective'
surfaces['Small Core z-max'].boundary_type = 'vacuum'
surfaces['Big Core z-min'].boundary_type   = 'reflective'
surfaces['Big Core z-max'].boundary_type   = 'vacuum'
surfaces['Pin x-min'].boundary_type        = 'reflective'
surfaces['Pin x-max'].boundary_type        = 'reflective'
surfaces['Pin y-min'].boundary_type        = 'reflective'
surfaces['Pin y-max'].boundary_type        = 'reflective'
surfaces['Core x-min'].boundary_type       = 'reflective'
