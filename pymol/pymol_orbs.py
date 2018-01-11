import __main__
__main__.pymol_argv = ['pymol','-qc']
import sys,time,os
import pymol
pymol.finish_launching()
cname='febpycn4s_monoCA'
pymol.cmd.set('auto_zoom','off')
pymol.cmd.set('auto_show_lines','off')
pymol.cmd.load(cname+'.pdb')
pymol.cmd.hide('all')
pymol.cmd.enable(cname)
pymol.cmd.select(cname)
pymol.cmd.bg_color('white')
pymol.cmd.color('white','name H*')
pymol.cmd.color('gray40','name C*')
pymol.cmd.color('deepblue','name N*')
pymol.cmd.color('red','name O*')
pymol.cmd.color('brightorange','name P*')
pymol.cmd.color('yellow','name S')
pymol.cmd.color('lightblue','name Fe*')
pymol.cmd.show('sticks','all')
pymol.cmd.set_bond('stick_radius','0.10','all')
pymol.cmd.set_color('poscolor',[0.0,0.0,225.0])
pymol.cmd.set_color('negcolor',[225.0,225.0,225.0])
pymol.cmd.set('orthoscopic','on')
pymol.cmd.viewport(800,500)
pymol.cmd.set('fog_start','0.5')
pymol.cmd.set('ray_trace_fog','0')
pymol.cmd.set('antialias','2')
pymol.cmd.set('reflect','0.8')
pymol.cmd.set('reflect_power','1.5')
pymol.cmd.set('ray_shadows','off')
pymol.cmd.set('ray_trace_mode','0')
pymol.cmd.set_view('\
     1.000000000,    0.000000000,    0.000000000,\
     0.000000000,    1.000000000,    0.000000000,\
     0.000000000,    0.000000000,    1.000000000,\
     0.000000000,    0.000000000,  -39.426231384,\
    -0.003028393,    0.381257057,   -0.005542755,\
    32.775791168,   46.076675415,  -20.000000000')
bn=69
en=71
fprefix=cname+'_mo'
cubeiso='cubeiso'
isolst=['0.01','0.02','0.03','0.04','0.05','0.06','0.008']
for i in range(en-bn+1):
    for j in isolst: 
	    cubestr=fprefix+str(i+bn)
	    cubename=cubestr+'.cube'
	    pymol.cmd.load(cubename,cubeiso)
	    pymol.cmd.isosurface('pos',cubeiso,j)
	    pymol.cmd.color('poscolor','pos')
	    pymol.cmd.isosurface('neg',cubeiso,'-'+j)
	    pymol.cmd.color('negcolor','neg')
	    pymol.cmd.ray()
	    pymol.cmd.png(cubestr+'_iso'+j+'.png',width='800',height='500',dpi=300.0)
	    pymol.cmd.delete(cubeiso)
pymol.cmd.quit

