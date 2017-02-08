'''
Companion scripts for: 
Mannige RV (2017) On the other hand: chirality and the peptide backbone. Manuscript prepared.
The location of each figure's panel is stored in "output.txt"
'''

output_file = open("output.txt","w")

# GLOBAL IMPORTS:
import os, sys, copy, random
import matplotlib.pyplot as plt                       # For utilizing colormap interpolation 
import numpy as np
import Bio.PDB # Biopython's PDB module
# LOCAL IMPORTS
sys.path.insert(0, "./local_imports/") # for the local imports
import Geometry, PeptideBuilder, locallib
# -----------------------
# GLOBAL GRAPHING IMPORTS
import seaborn as sns
np.random.seed(sum(map(ord, "aesthetics")))
sns.set_style('ticks') # *
sns.set_context("paper", font_scale=1.5, rc={"lines.linewidth": 4})
# -----------------------

#sns.palplot(sns.color_palette("husl", 3)); plt.show()

def cos(a):
	return np.cos(np.radians(a))
def sin(a):
	return np.sin(np.radians(a))

# ===================================================================================
# SETTING UP A CUSTOM COLORMAP
# 
COLORSWITCH = 0.5; bc = [1,1,1] # background (white)
import seaborn as sns
import colorsys
r  = [colorsys.rgb_to_hsv(1,0,0)[0],0.75,0.5]
y  = [colorsys.rgb_to_hsv(1,1,0)[0],0.5,0.75]
c3 = colorsys.hsv_to_rgb(*r) # the '*' converts [a,b,c] into a,b,c
c4 = colorsys.hsv_to_rgb(*y)
# Now the color map dictionary
cdict = {
	'red':   ((0.00,  c3[0], c3[0]), (COLORSWITCH,  bc[0], bc[0]), (1.0, c4[0], c4[0])), 
	'green': ((0.00,  c3[1], c3[1]), (COLORSWITCH,  bc[1], bc[1]), (1.0, c4[1], c4[1])),
	'blue':  ((0.00,  c3[2], c3[2]), (COLORSWITCH,  bc[2], bc[2]), (1.0, c4[2], c4[2])) 
}
from matplotlib.colors import LinearSegmentedColormap # For making your own colormaps
cmap = LinearSegmentedColormap('chirality_r', cdict)
plt.register_cmap(cmap=cmap)

# ----------------------------------------------------------------------------

if 1:
	# Fig 4c
	
	output_file.write("\n")
	
	# Slices through a trans Ramachandran plot (from the bottom left to the 
	# top right). At each 1 degree step, a structure is generated and saved in 
	# "pdbs/trans(or cis)/aligned*.pdb", its handedness is calculated. The relationship between 
	# phi or psi and handedness (chi_b) is saved as a file in: "graphs/slice_trans(or cis).*"
	
	# In order to read the slice of structures as a trajectory run the following command:
	# "vmd -e study_handedness.vmd -args handedness(_cis)
	# "study_handedness.vmd" streams "study_handedness.tcl", which aligns the backbone.
	
	# Above, "(_cis)" indicates that omega was set to 0, and so the names were changed accordingly.
	
	for omega in [180.0,0.0]:
		N = 7
		current_step_size = 1
		
		phipsi_range = np.arange(-180,180.1,current_step_size)
		pdb_output_dir = "pdbs"
		phi_to_chi_basefilename = "graphs/slice"
		
		
		
		title = "$\omega=180^\circ (trans)$"
		if omega == 0.0:
			#
			phipsi_range = np.arange(0,360.1,current_step_size)
			pdb_output_dir += "/cis"
			phi_to_chi_basefilename += "_cis"
			title = "$\omega=0^\circ (cis)$"
		else:# omega == 180.0:
			pdb_output_dir += "/trans"
			phi_to_chi_basefilename += "_trans"
			
			output_file.write("Structures for Fig 4c:\t"+pdb_output_dir+"/*.pdb\n")
		
		if not os.path.isdir(os.path.dirname(phi_to_chi_basefilename)):
			os.makedirs(os.path.dirname(phi_to_chi_basefilename))
		if not os.path.isdir(pdb_output_dir):
			os.makedirs(pdb_output_dir)
		
		counter = 0
		X=[]
		Y=[]
		Z=[]
		for phi in phipsi_range:
			psi = phi
			if omega == 0.0:
				psi = -1.0 * phi
			
			counter += 1
			if counter % 10 == 0.0:
				#sys.stdout.write("\r-----------------\n")
				sys.stdout.write("\r\t%d " % int(100.0*float(counter)/360.))
				sys.stdout.write(r"%")
				sys.stdout.flush()
			angles = []
			for n in range(N):
				angles.append((phi,psi,omega))
			
			st = locallib.build_structure(angles)
			
			#z = locallib.calculate_handedness1(st)
			chi, theta, d = locallib.calculate_handedness_from_theory(phi,psi,omega)
			z = chi
			
			if counter > 1:
				rmsd, st = locallib.calculate_rmsd(stOld,st)
			
			stOld = copy.deepcopy(st)
			
			out = Bio.PDB.PDBIO()
			out.set_structure(st[0])
			pdbfn = pdb_output_dir+"/aligned_p%03d.pdb" %(int(np.abs(phi)))
			if phi < 0:
				pdbfn = pdb_output_dir+"/aligned_m%03d.pdb" %(int(np.abs(phi)))
			
			
			#print 'writing to:',pdbfn
			out.save(pdbfn)
			X.append(phi)
			Y.append(psi)
			Z.append(z)
		
		add_cis = ""
		if omega == 0.0:
			add_cis = "_cis"
		# The pdbs in <pdb_output_dir> can be used to render the structure in the inset of Fig 4b
		# All structures can be viewed using the following VMD command:
		#os.system("vmd -e local_imports/study_handedness"+add_cis+".vmd -args "+pdb_output_dir)
		
		print
		# ---------------------
		# SOME GRAPH FORMATTING
		plt.clf()
		sns.set_style('whitegrid')
		cmap = plt.get_cmap("chirality_r")
		plt.plot(X, Z, c='k', ls="solid", lw=1.5)
		plt.xticks(range(int(phipsi_range[0]),int(phipsi_range[-1])+1,180))
		plt.yticks([-1,-0.5,0,0.5,1])
		plt.xlabel(r"$\phi,\psi$")
		plt.ylabel(r"$\chi_b^1$")
		plt.title(title)
		x1,x2,y1,y2 = plt.axis()
		
		padding = float(phipsi_range[-1]-phipsi_range[0])*0.05
		plt.axis((phipsi_range[0]-padding,phipsi_range[-1]+padding,y1,y2))
		# ---------------------
		plt.savefig(phi_to_chi_basefilename+".pdf",dpi=170,bbox_inches="tight")
		plt.savefig(phi_to_chi_basefilename+".png",dpi=170,bbox_inches="tight")
		
		f = locallib.open_file(phi_to_chi_basefilename+".dat","w")
		for x,y in zip(X,Z):
			f.write("%f\t%f\n" %(x,y))
		f.close()
		sys.stdout.write("\n")
		sys.stdout.flush()
		plt.clf()


if 0:
	# Creating Fig 4b in many color combinations to see which one prints OK 
	# in black and white
	sns.set_style('whitegrid')
	
	# getting the data
	omega = 180.0 # trans backbones only
	#plt.clf()
	X = []
	Y = []
	Z = []
	for phi in range(-180,181,5):
		for psi in range(-180,181,5):
			
			chi, theta, d = locallib.calculate_handedness_from_theory(phi,psi,omega)
			
			X.append(phi)
			Y.append(psi)
			Z.append(chi)
	imagex,imagey,imagez = locallib.xyz_to_image(X,Y,Z)
	xset = sorted(set(imagex.flatten()))
	yset = sorted(set(imagey.flatten()))
	extent = [xset[0], xset[-1], yset[0], yset[-1]]
	# ---------------------------------------------------------------
	
	saturation_and_value_iterations = 4
	
	from mpl_toolkits.axes_grid1 import AxesGrid
	fig = plt.figure()
	grid = AxesGrid(fig, 111,
			nrows_ncols=(4, 6),
			axes_pad=0.0,
			aspect = 1.0,
			share_all=False,
			label_mode="L",
			)
	
	cmap = plt.get_cmap("chirality_r")
	
	red_choices    = [(.5,.5),(.5,.75),(1,.5),(.75,1),(1,1),(.75,.5)]
	yellow_choices = [(.5,.75),(.75,.75),(.75,.5),(1,.75)]
	
	xcount = 0
	ycount = 1
	#for i in range(saturation_and_value_iterations*saturation_and_value_iterations):
	#help(grid)
	rcounter = 0
	ycounter = 0
	for ax in grid:
		#S1 = random.choice([0.5,0.75,1.0])
		#V1 = random.choice([0.5,0.75,1.0])
		#S2 = random.choice([0.5,0.75,1.0])
		#V2 = random.choice([0.5,0.75,1.0])
		
		r  = red_choices[rcounter]
		y  = yellow_choices[ycounter]
		S1 = r[0]
		V1 = r[1]
		S2 = y[0]
		V2 = y[1]
		
		rcounter += 1
		if rcounter % 6 == 0:
			ycounter += 1
			rcounter  = 0
		
		#
		'''
		S1 = random.choice(np.arange(0.4,1.01,0.1))
		V1 = random.choice(np.arange(0.4,1.01,0.1))
		S2 = random.choice(np.arange(0.4,1.01,0.1))
		V2 = random.choice(np.arange(0.4,1.01,0.1))
		choice = random.choice([0,1])
		S1 = random.choice(np.arange(0.5  ,0.751,0.1))
		S2 = random.choice(np.arange(0.751,1.01,0.1))
		V1 = random.choice(np.arange(0.751,1.01,0.1))
		V2 = random.choice(np.arange(0.5  ,0.751,0.1))
		if choice == 0:
			S1 = random.choice(np.arange(0.751,1.01,0.1))
			S2 = random.choice(np.arange(0.5  ,0.751,0.1))
			V1 = random.choice(np.arange(0.5  ,0.751,0.1))
			V2 = random.choice(np.arange(0.751,1.01,0.1))
		'''
		# ===================================================================================
		# SETTING UP SOME COLORMAP
		# 
		COLORSWITCH = 0.5; bc = [1,1,1] # background (white)
		import seaborn as sns
		import colorsys
		red_hue    = colorsys.rgb_to_hsv(1,0,0)[0]
		blue_hue   = colorsys.rgb_to_hsv(0,0,1)[0]
		yellow_hue = colorsys.rgb_to_hsv(1,1,0)[0]
		blue_hue = yellow_hue #!!!!!!!!!!!!
		c3 = colorsys.hsv_to_rgb(red_hue , S1, V1)
		c4 = colorsys.hsv_to_rgb(blue_hue, S2, V2)
		# Now the color map dictionary
		cdict = {
			'red':   ((0.00,  c3[0], c3[0]), (COLORSWITCH,  bc[0], bc[0]), (1.0, c4[0], c4[0])), 
			'green': ((0.00,  c3[1], c3[1]), (COLORSWITCH,  bc[1], bc[1]), (1.0, c4[1], c4[1])),
			'blue':  ((0.00,  c3[2], c3[2]), (COLORSWITCH,  bc[2], bc[2]), (1.0, c4[2], c4[2])) 
		}
		from matplotlib.colors import LinearSegmentedColormap # For making your own colormaps
		cmap = LinearSegmentedColormap('chirality_r', cdict)
		#plt.register_cmap(cmap=cmap_chirality_r)
		
		ax.pcolor(imagex,imagey,imagez, cmap=cmap, vmin=np.nanmin(Z),vmax=np.nanmax(Z))
		#help(ax)
		ax.axes.set_xlim(-180,180)
		ax.axes.set_ylim(-180,180)
		ax.axes.set_yticks([])
		ax.axes.set_xticks([])
		ax.axes.text(1.0, 1.0, "("+str(round(S1,2))+","+str(round(V1,2))+")\n"
	                              +"("+str(round(S2,2))+","+str(round(V2,2))+")",
		            size=7,horizontalalignment='center',verticalalignment='center',)
		#plt.yticks([])
		#plt.axis(extent)
		
		plt.savefig("deme.png",dpi=280,bbox_inches="tight")
		

		
	plt.show()
	exit()
	
if 1:
	# Fig 4a
	# Fig 4b
	# Fig 5a-(i)
	# Fig 5b-(i)
	# Fig 6a
	# Fig 6b
	# Fig 6c
	# Fig 6d
	
	output_file.write('\n')
	sns.set_style('ticks') # *
	
	for omega in [180.0,0.0]:
		plt.clf()
		
		X = []
		Y = []
		Z_chi   = []
		Z_theta = []
		Z_d     = []
		phi_psi_to_chi   = {}
		phi_psi_to_theta = {}
		phi_psi_to_d = {}
		for phi in range(-180,181,1):
			for psi in range(-180,181,1):
				
				chi, theta, d = locallib.calculate_handedness_from_theory(phi,psi,omega)
				
				X.append(phi)
				Y.append(psi)
				Z_chi.append(chi)
				Z_theta.append(theta)
				Z_d.append(d)
				
				phi_psi_to_chi[(phi,psi)]   = chi
				phi_psi_to_theta[(phi,psi)] = theta
				phi_psi_to_d[(phi,psi)]     = d
		
		# ---------------------------------------------------------------
		cis_or_trans = 'trans'
		if omega == 0.0:
			cis_or_trans = 'cis'
		
		fn_base = './graphs/chirality_from_theory_'+cis_or_trans
		
		
		anglerange = [(-180,180,2),(-180,180,5),(0,360,2)]
		
		for amin,amax,astep in anglerange:
			
			newX = []
			newY = []
			newZd = []
			newZtheta = []
			newZchi = []
			
			output_fn = fn_base
			
			if amin == -180 and amax == 180:
				pass
			else:
				output_fn += "_range"+str(amin)+"-"+str(amax)
			
			output_fn += "_step"+str(astep)
			
			for phi in np.arange(amin,amax+astep/2,astep):
				phi_bound = phi
				if -180 <= phi and phi <= 180:
					pass
				else:
					phi_bound = (phi+180.0) % 360.0 - 180.0
				
				for psi in np.arange(amin,amax+astep/2,astep):
					psi_bound = psi
				
					if -180 <= psi and psi <= 180:
						pass
					else:
						psi_bound = (psi+180.0) % 360.0 -180.0
					
					chi   = phi_psi_to_chi[(phi_bound,psi_bound)]
					theta = phi_psi_to_theta[(phi_bound,psi_bound)]
					d     = phi_psi_to_d[(phi_bound,psi_bound)]
					
					chi, theta, d = locallib.calculate_handedness_from_theory(phi,psi,omega)
					
					newX.append(phi)
					newY.append(psi)
					newZchi.append(chi)
					newZtheta.append(theta)
					newZd.append(d)
			
			xticks = range(int(amin),int(amax)+1,180)
			yticks = range(int(amin),int(amax)+1,180)
			
			plt.clf()
			for x in xticks:
				if x != amin and x != amax:
					ls = 'solid'
					if x % 360 == 0.0:
						ls = 'dashed' #or 'dotted'
					plt.plot([x, x], [amin, amax], c='k', ls=ls, lw=1)
			for y in yticks:
				if y != amin and y != amax:
					ls = 'solid'
					if y % 360 == 0.0:
						ls = 'dashed' #or 'dotted'
					plt.plot([amin, amax], [y, y], c='k', ls=ls, lw=1)
			
			
			xticks = range(int(amin),int(amax)+1,180)
			yticks = range(int(amin),int(amax)+1,180)
			
			if amin == -180 and amax == 180:
				if astep == 2:
					if omega == 180.0:

						output_file.write("Fig 4b:        \t"+output_fn+"_chi.*\n")
						output_file.write("Fig 5a(i):     \t"+output_fn+"_chi.*\n")
						output_file.write("Fig 6a:        \t"+output_fn+"_chi.*\n")
					if omega == 0.0:
						output_file.write("Fig 5b(i):     \t"+output_fn+"_chi.*\n")
						output_file.write("Fig 6c:        \t"+output_fn+"_chi.*\n")
					
				if astep == 5:
					
					if omega == 180.0:
						output_file.write("Fig 4a (left): \t"+output_fn+"_theta.*\n")
					if omega == 180.0:
						output_file.write("Fig 4a (right):\t"+output_fn+"_d.*\n")
					
					locallib.draw_ramachandran_lines(amin=amin,amax=amax)
					sns.set_style('ticks')
					cmap = plt.get_cmap("chirality_r")
					locallib.make2Dfigure(newX,newY,np.array(newZtheta)-180,
							fn=[output_fn+'_theta.eps',output_fn+'_theta.png'],
							xscaling=1, cmap=cmap,title=r'$\theta-180^\circ$',
							xtitle="$\phi$",ytitle="$\psi$", 
							xticks=xticks, yticks=yticks,
							xlim=[amin,amax],ylim=[amin,amax],show=0,start_fresh=1, colorbar=1)#,zlim=[-1,1])
					
					locallib.draw_ramachandran_lines(amin=amin,amax=amax)
					sns.set_style('ticks')
					cmap = plt.get_cmap("chirality_r")
					locallib.make2Dfigure(newX,newY,newZd,fn=[output_fn+'_d.eps',output_fn+'_d.png'],
							xscaling=1, cmap=cmap,title='$d$',
							xtitle="$\phi$",ytitle="$\psi$", 
							xticks=xticks, yticks=yticks,
							xlim=[amin,amax],ylim=[amin,amax],show=0,start_fresh=1, colorbar=1)#,zlim=[-1,1])
			
			
			locallib.draw_ramachandran_lines(amin=amin,amax=amax)
			sns.set_style('ticks')
			cmap = plt.get_cmap("chirality_r")
			locallib.make2Dfigure(newX,newY,newZchi,fn=[output_fn+'_chi.eps',output_fn+'_chi.png'],
					xscaling=1, cmap=cmap,title=r'$(d [\theta - 180^\circ]/(180^\circ|d|)$',
					xtitle="$\phi$",ytitle="$\psi$", 
					xticks=xticks, yticks=yticks,
					xlim=[amin,amax],ylim=[amin,amax],show=0,start_fresh=1, colorbar=1,
					zlim=[np.nanmin(newZchi),np.nanmax(newZchi)])

if 1: # Fig 1c drawing left (L) and right (D) versions of the Alpha-helix
	N = 12
	omega = 180.0
	
	name_phi_psi = [('pdbs/alpha_d.pdb',-63, -43),('pdbs/alpha_l.pdb',63, 43)]
	#TO CREATE POLYPROLINE II HELICES, ADD THE FOLLOWING TUPLES TO <name_phi_psi: 
	# ('pdbs/ppII_d.pdb',75,-150),('pdbs/ppII_l.pdb',-75,150)
	
	for fn,phi,psi in name_phi_psi:
		if "alpha_l" in fn:
			output_file.write("Fig 1c (left): \t"+output_fn+"_chi.*\n")
		if "alpha_d" in fn:
			output_file.write("Fig 1c (right):\t"+output_fn+"_chi.*\n")
		
		angles = []
		for n in range(N):
			angles.append((phi,psi,omega))
		
		st = locallib.build_structure(angles)
		
		basedir = os.path.dirname(fn)
		if not os.path.isdir(basedir):
			os.makedirs(basedir)
		
		import Bio.PDB # import Biopython's PDB module .
		out = Bio.PDB.PDBIO()
		out.set_structure(st[0])
		pdbfn = fn
		print 'writing to:',pdbfn
		out.save(pdbfn)
		# Fig 1c contains this pdbfn (and its mirror symmetric version)
		# Rendering this VMD scene gets you Fig 1c
		#os.system("vmd -e local_imports/draw_structure.vmd -args "+pdbfn)

if 1:
	# Fig 5a-(ii)
	# Fig 5a-(iii)
	# Fig 5b-(ii)
	# Fig 5b-(iii)
	step_size = 1
	output_file.write("\n")
	for omega in [180,0]:
		sns.set_style('ticks') # *
		N=5 #Since all residues are identical in dihedral angle arrangements, we can get away with N=4
		
		phipsi_range = np.arange(-180,180.1,step_size)
		
		directory = "graphs"
		if not os.path.isdir(directory):
			os.makedirs(directory)
		
		fnbasebase = "step"+str(step_size)
		
		if omega == 0:
			fnbasebase += "_cis"
		else:
			fnbasebase += "_trans"
		do1 = 0
		if not os.path.isfile(directory+"/chirality1_"+fnbasebase+".xyz"):
			do1 = 1
		do2 = 0
		if not os.path.isfile(directory+"/chirality2_"+fnbasebase+".xyz"):
			do2 = 1
		do3 = 0
		if not os.path.isfile(directory+"/chirality3_"+fnbasebase+".xyz"):
			do3 = 1
		
		X = []
		Y = []
		Z1 = []
		Z2 = []
		Z3 = []
		counter = 0
		
		if do1+do2+do3 > 0:
			for phi in phipsi_range:
				for psi in phipsi_range:
					counter += 1
					if counter % 100 == 0.0:
						str_phi = "{0: >4}".format(int(phi))
						str_psi = "{0: >4}".format(int(psi))
						#print [str_phi,str_psi]
						#raw_input()
						sys.stdout.write("\rOmega:%d\t(%s,%s)" %(omega,str_phi,str_psi))
						sys.stdout.flush()
					
					angles = []
					for n in range(N):
						angles.append((phi,psi,omega))
					
					st1 = []
					st1 = locallib.build_structure(angles)
					
					X.append(phi)
					Y.append(psi)
					if do1:
						Z1.append(locallib.calculate_handedness1(st1))
					if do2:
						Z2.append(locallib.calculate_handedness2(st1))
					if do3:
						Z3.append(locallib.calculate_handedness3(st1))
			sys.stdout.write("\n")
		
		if do1:
			fnbase = directory+"/chirality1_"+fnbasebase
			f = locallib.open_file(fnbase+".xyz","w")
			for x,y,z in zip(X,Y,Z1):
				f.write("%f\t%f\t%f\n" %(x,y,z))
			f.close()
		if do2:
			fnbase = directory+"/chirality2_"+fnbasebase
			f = locallib.open_file(fnbase+".xyz","w")
			for x,y,z in zip(X,Y,Z2):
				f.write("%f\t%f\t%f\n" %(x,y,z))
			f.close()
		if do3:
			fnbase = directory+"/chirality3_"+fnbasebase
			f = locallib.open_file(fnbase+".xyz","w")
			for x,y,z in zip(X,Y,Z3):
				f.write("%f\t%f\t%f\n" %(x,y,z))
			f.close()
		
		for fnbase in [directory+"/chirality1_"+fnbasebase,directory+"/chirality2_"+fnbasebase,directory+"/chirality3_"+fnbasebase]:
			
			X = []
			Y = []
			Z = []
			phi_psi_to_chi = {}
			print "READING:",fnbase+".xyz"
			f = open(fnbase+".xyz","r")
			for l in f.read().split("\n"):
				if len(l):
					l = l.split("\t")
					x = float(l[0])
					y = float(l[1])
					z = float(l[2])
					X.append(x)
					Y.append(y)
					Z.append(z)
					phi_psi_to_chi[(x,y)] = z
			f.close()
			
			cmap = plt.get_cmap("chirality_r")
			
			if 0: # draw histogram
				plt.clf()
				locallib.draw_histogram(Z,bins=40)
				plt.clf()
			
			title = r"$\chi_b^"+os.path.basename(fnbase).split("_")[0][-1]+"$"
			if omega == 0:
				title+= " (cis)"
			else:
				title+= " (trans)"
			
			anglerange = [(-180,180,5)]
			
			for amin,amax,astep in anglerange:
				
				output_fnbase = os.path.dirname(fnbase)+"/"+os.path.basename(fnbase).split("_")[0]+"_"+os.path.basename(fnbase).split("_")[-1]
				
				print "\trange:\t",(amin,amax)
				newX = []
				newY = []
				newZ = []
				
				if amin == -180 and amax == 180:
					pass
				else:
					output_fnbase += "_range"+str(amin)+"-"+str(amax)
				output_fnbase += "_step"+str(astep)
					
				
				for phi in np.arange(amin,amax+astep/2,astep):
					if -180.0 <= phi and phi <= 180.0:
						phi_bound = phi
					else:
						phi_bound = -180.+(phi+180.) % 360.
					#
					for psi in np.arange(amin,amax+astep/2,astep):
						if -180.0 <= psi and psi <= 180.0:
							psi_bound = psi
						else:
							psi_bound = -180.+(psi+180.) % 360.
						#
						chi = phi_psi_to_chi[(phi_bound,psi_bound)]
						newX.append(phi)
						newY.append(psi)
						newZ.append(chi)
				
				if amin == -180 and amax == 180:
					if "chirality1" in output_fnbase:
						if omega == 180.0:
							output_file.write("Fig 5a-(ii):   \t"+output_fn+"_chi.*\n")
						if omega == 0.0:
							output_file.write("Fig 5b-(ii):   \t"+output_fn+"_chi.*\n")
					if "chirality2" in output_fnbase:
						if omega == 180.0:
							output_file.write("Fig 5a-(iii):  \t"+output_fn+"_chi.*\n")
						if omega == 0.0:
							output_file.write("Fig 5b-(iii):  \t"+output_fn+"_chi.*\n")
				
				xticks = range(int(amin),int(amax)+1,180)
				yticks = range(int(amin),int(amax)+1,180)
				
				plt.clf()
				for x in xticks:
					if x != amin and x != amax:
						ls = 'solid'
						if x % 360 == 0.0:
							ls = 'dashed' #or 'dotted'
						plt.plot([x, x], [amin, amax], c='k', ls=ls, lw=1)
				for y in yticks:
					if y != amin and y != amax:
						ls = 'solid'
						if y % 360 == 0.0:
							ls = 'dashed' #or 'dotted'
						plt.plot([amin, amax], [y, y], c='k', ls=ls, lw=1)
				
				fns = [output_fnbase+".eps"] #output_fnbase+".png",
				print "WRITING TO:",",".join(fns)
				locallib.make2Dfigure(newX,newY,newZ,fn=fns,
						xscaling=1, cmap=cmap,title=title,
						xtitle="$\phi$",ytitle="$\psi$",
						xticks=xticks, yticks=yticks,
						xlim=[amin,amax],ylim=[amin,amax],show=0,start_fresh=1, colorbar=1)#,zlim=[-1,1])


if 1:
	# Inline plots shown after Item 2 of Conclusions.
	#
	sns.set_style('ticks')
	#
	output_file.write('\n')
	output_file.write('The inline figure in Conclusion #2 appears in:\t./graphs/other_omegas/*.eps\n')
	#
	
	counter = 0
	step = 10
	for omega in [-180,-180+45,-90,-90+45,0]: #range(-180,181,5):#[180.0,0.0]:
		plt.clf()
		
		X = []
		Y = []
		Z_chi   = []
		Z_theta = []
		Z_d     = []
		phi_psi_to_chi   = {}
		phi_psi_to_theta = {}
		phi_psi_to_d = {}
		for phi in range(-180,181,step):
			for psi in range(-180,181,step):
				
				chi, theta, d = locallib.calculate_handedness_from_theory(phi,psi,omega)
				
				X.append(phi)
				Y.append(psi)
				Z_chi.append(chi)
				Z_theta.append(theta)
				Z_d.append(d)
				
				phi_psi_to_chi[(phi,psi)]   = chi
				phi_psi_to_theta[(phi,psi)] = theta
				phi_psi_to_d[(phi,psi)]     = d
		
		# ---------------------------------------------------------------
		cis_or_trans = 'trans'
		if omega == 0.0:
			cis_or_trans = 'cis'
		cis_or_trans = ''
		
		counter+=1
		fn_base = './graphs/other_omegas/icon_'+str(omega)
		
		if not os.path.isdir(os.path.dirname(fn_base)):
			os.makedirs(os.path.dirname(fn_base))
		
		anglerange = [(-180,180,step)]
		for amin,amax,astep in anglerange:
			
			print "\trange:\t",(amin,amax)
			newX = []
			newY = []
			newZd = []
			newZtheta = []
			newZchi = []
			
			output_fn = fn_base
			
			for phi in np.arange(amin,amax+astep/2,astep):
				if -180.0 <= phi and phi <= 180.0:
					phi_bound = phi
				else:
					phi_bound = (phi+180.0) % 360.0 - 180.0
				for psi in np.arange(amin,amax+astep/2,astep):
					if -180.0 <= psi and psi <= 180.0:
						psi_bound = psi
					else:
						psi_bound = (psi+180.0) % 360.0 -180.0
					chi   = phi_psi_to_chi[(phi_bound,psi_bound)]
					theta = phi_psi_to_theta[(phi_bound,psi_bound)]
					d     = phi_psi_to_d[(phi_bound,psi_bound)]
					
					newX.append(phi)
					newY.append(psi)
					newZchi.append(chi)
					newZtheta.append(theta)
					newZd.append(d)
			
			
			xticks = range(int(amin),int(amax)+1,180)
			yticks = range(int(amin),int(amax)+1,180)
			
			plt.clf()
			for x in xticks:
				if x != amin and x != amax:
					ls = 'solid'
					if x % 360 == 0.0:
						ls = 'dashed' #or 'dotted'
					plt.plot([x, x], [amin, amax], c='k', ls=ls, lw=1)
			for y in yticks:
				if y != amin and y != amax:
					ls = 'solid'
					if y % 360 == 0.0:
						ls = 'dashed' #or 'dotted'
					plt.plot([amin, amax], [y, y], c='k', ls=ls, lw=1)
			
			xticks = range(int(amin),int(amax)+1,180)
			yticks = range(int(amin),int(amax)+1,180)
			
			locallib.draw_ramachandran_lines(amin=amin,amax=amax)
			
			sns.set_style('ticks')
			cmap = plt.get_cmap("chirality_r")
			locallib.make2Dfigure(newX,newY,newZchi,fn=[output_fn+'.eps'], #, output_fn+'_chi.eps'],
					xscaling=1, cmap=cmap,title=r'$\omega$='+str(omega),
					xtitle="$\phi$",ytitle="$\psi$", 
					xticks=xticks, yticks=yticks,
					xlim=[amin,amax],ylim=[amin,amax],show=0,start_fresh=1, colorbar=0,
					zlim=[np.nanmin(newZchi),np.nanmax(newZchi)])

if 0:
	# Shows how the Ramachandran plot morphs as omega is tuned (some snapshots)
	# Currently not used in a manuscript, but it will be useful when making an animation
	# for a presentation
	sns.set_style('ticks') # *
	
	counter = 0
	step = 10
	for omega in range(-180,181,5):#[180.0,0.0]:
		plt.clf()
		
		X = []
		Y = []
		Z_chi   = []
		Z_theta = []
		Z_d     = []
		phi_psi_to_chi   = {}
		phi_psi_to_theta = {}
		phi_psi_to_d = {}
		for phi in range(-180,181,step):
			for psi in range(-180,181,step):
				
				chi, theta, d = locallib.calculate_handedness_from_theory(phi,psi,omega)
				
				'''
				# If we have an all-trans, then we can estimate theta and d more sussinctly:
				theta =2. * np.arccos(-0.817 * np.sin(float(psi + phi)/ 2.) - 0.045 * np.sin(float(psi - phi)/2.))
				d = float(2.967 * np.cos(float(psi + phi)/ 2.) - 0.664 * np.cos(float(psi - phi)/2.))/np.sin(theta/2.)
				'''
				
				X.append(phi)
				Y.append(psi)
				Z_chi.append(chi)
				Z_theta.append(theta)
				Z_d.append(d)
				
				phi_psi_to_chi[(phi,psi)]   = chi
				phi_psi_to_theta[(phi,psi)] = theta
				phi_psi_to_d[(phi,psi)]     = d
		
		# ---------------------------------------------------------------
		cis_or_trans = 'trans'
		if omega == 0.0:
			cis_or_trans = 'cis'
		cis_or_trans = ''
		
		counter+=1
		fn_base  = './graphs/anim/anim_omega'
		fn_base += '{0:0>6}'.format(counter)
		
		if not os.path.isdir(os.path.dirname(fn_base)):
			os.makedirs(os.path.dirname(fn_base))
		
		anglerange = [(-180,180,step)]
		for amin,amax,astep in anglerange:
			
			print "\trange:\t",(amin,amax)
			newX = []
			newY = []
			newZd = []
			newZtheta = []
			newZchi = []
			
			output_fn = fn_base
			if amin == -180 and amax == 180:
				pass
			else:
				output_fn += "_range"+str(amin)+"-"+str(amax)
			output_fn += "_step"+str(astep)
			
			for phi in np.arange(amin,amax+astep/2,astep):
				if -180.0 <= phi and phi <= 180.0:
					phi_bound = phi
				else:
					phi_bound = (phi+180.0) % 360.0 - 180.0
				for psi in np.arange(amin,amax+astep/2,astep):
					if -180.0 <= psi and psi <= 180.0:
						psi_bound = psi
					else:
						psi_bound = (psi+180.0) % 360.0 -180.0
					chi   = phi_psi_to_chi[(phi_bound,psi_bound)]
					theta = phi_psi_to_theta[(phi_bound,psi_bound)]
					d     = phi_psi_to_d[(phi_bound,psi_bound)]
					
					#chi, theta, d = locallib.calculate_handedness_from_theory(phi,psi,omega)
					newX.append(phi)
					newY.append(psi)
					newZchi.append(chi)
					newZtheta.append(theta)
					newZd.append(d)
			
			
			xticks = range(int(amin),int(amax)+1,180)
			yticks = range(int(amin),int(amax)+1,180)
			
			plt.clf()
			for x in xticks:
				if x != amin and x != amax:
					ls = 'solid'
					if x % 360 == 0.0:
						ls = 'dashed' #or 'dotted'
					plt.plot([x, x], [amin, amax], c='k', ls=ls, lw=1)
			for y in yticks:
				if y != amin and y != amax:
					ls = 'solid'
					if y % 360 == 0.0:
						ls = 'dashed' #or 'dotted'
					plt.plot([amin, amax], [y, y], c='k', ls=ls, lw=1)
			
			xticks = range(int(amin),int(amax)+1,180)
			yticks = range(int(amin),int(amax)+1,180)
			
			locallib.draw_ramachandran_lines(amin=amin,amax=amax)
			
			sns.set_style('ticks')
			cmap = plt.get_cmap("chirality_r")
			print output_fn
			locallib.make2Dfigure(newX,newY,newZchi,fn=[output_fn+'_chi.png'], #, output_fn+'_chi.eps'],
					xscaling=1, cmap=cmap,title=r'$\omega$='+str(omega),
					xtitle="$\phi$",ytitle="$\psi$", 
					xticks=xticks, yticks=yticks,
					xlim=[amin,amax],ylim=[amin,amax],show=0,start_fresh=1, colorbar=0,
					zlim=[np.nanmin(newZchi),np.nanmax(newZchi)])
