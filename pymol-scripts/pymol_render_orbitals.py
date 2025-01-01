import pymol
import __main__
__main__.pymol_argv = ['pymol', '-qc']
pymol.finish_launching()

# constants
cube_name = 'febpycn4s_monoCA'
pdb_filename = f"{cube_name}.pdb"
cubeiso = 'cubeiso'
isosurfaces = ['0.01', '0.02', '0.03', '0.04', '0.05', '0.06', '0.008']
orbital_first, orbital_last = 69, 71
output_width, output_height, output_dpi = 800, 500, 300

# visualization settings
pymol.cmd.set('auto_zoom', 'off')
pymol.cmd.set('auto_show_lines', 'off')
pymol.cmd.bg_color('white')
pymol.cmd.set('orthoscopic', 'on')
pymol.cmd.viewport(output_width, output_height)
pymol.cmd.set('fog_start', '0.5')
pymol.cmd.set('ray_trace_fog', '0')
pymol.cmd.set('antialias', '2')
pymol.cmd.set('reflect', '0.8')
pymol.cmd.set('reflect_power', '1.5')
pymol.cmd.set('ray_shadows', 'off')
pymol.cmd.set('ray_trace_mode', '0')
pymol.cmd.show('sticks', 'all')
pymol.cmd.set_bond('stick_radius', '0.10', 'all')
pymol.cmd.set_color('poscolor', [0.0, 0.0, 225.0])
pymol.cmd.set_color('negcolor', [225.0, 225.0, 225.0])

# load molecule
pymol.cmd.load(pdb_filename)
pymol.cmd.hide('all')
pymol.cmd.enable(cube_name)
pymol.cmd.select(cube_name)

# atom coloring
color_map = {
    'H*': 'white',
    'C*': 'gray40',
    'N*': 'deepblue',
    'O*': 'red',
    'P*': 'brightorange',
    'S': 'yellow',
    'Fe*': 'lightblue'
}
for atom, color in color_map.items():
    pymol.cmd.color(color, f'name {atom}')


# viewing perspective
pymol.cmd.set_view('''
     1.000000000,    0.000000000,    0.000000000,
     0.000000000,    1.000000000,    0.000000000,
     0.000000000,    0.000000000,    1.000000000,
     0.000000000,    0.000000000,  -39.426231384,
    -0.003028393,    0.381257057,   -0.005542755,
    32.775791168,   46.076675415,  -20.000000000''')

# generate cube files and render images
for orbital_num in range(orbital_first, orbital_last + 1):
    cube_basename = f"{cube_name}_mo{orbital_num}"
    cube_filename = f"{cube_basename}.cube"

    for isosurface in isosurfaces:
        pymol.cmd.load(cube_filename, cubeiso)
        pymol.cmd.isosurface('pos', cubeiso, isosurface)
        pymol.cmd.color('poscolor', 'pos')
        pymol.cmd.isosurface('neg', cubeiso, f"-{isosurface}")
        pymol.cmd.color('negcolor', 'neg')

        output_png = f"{cube_basename}_iso{isosurface}.png"
        pymol.cmd.ray()
        pymol.cmd.png(output_png, width=output_width,
                      height=output_height, dpi=output_dpi)

        pymol.cmd.delete(cubeiso)

pymol.cmd.quit()
