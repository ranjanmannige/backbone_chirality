fresh_start = 0
downsample  = 2
step_size = 1

# GLOBAL IMPORTS:
import os, sys, copy 
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
sns.set_context("talk", font_scale=1.5, rc={"lines.linewidth": 4})
# -----------------------

if 1: # FIG 1c drawing left (L) and right (D) versions of the Alpha-helix
	N = 12
	omega = 180.0
	name_phi_psi = [('pdbs/alpha_d.pdb',-63, -43),('pdbs/alpha_l.pdb',63, 43)]
	#TO CREATE POLYPROLINE II HELICES, ADD THE FOLLOWING TUPLES TO <name_phi_psi: 
	# ('pdbs/ppII_d.pdb',75,-150),('pdbs/ppII_l.pdb',-75,150)
	
	for fn,phi,psi in name_phi_psi:
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
	# Fig 2b
	
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
			phipsi_range = np.arange(0,360.1,current_step_size)
			pdb_output_dir += "/cis"
			phi_to_chi_basefilename += "_cis"
			title = "$\omega=0^\circ (cis)$"
		else:# omega == 180.0:
			pdb_output_dir += "/trans"
			phi_to_chi_basefilename += "_trans"
		
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
			
			z = locallib.calculate_handedness1(st)
			
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
		# The pdbs in <pdb_output_dir> can be used to render the structure in the inset of Fig 2b
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
		plt.show()
		f = locallib.open_file(phi_to_chi_basefilename+".dat","w")
		for x,y in zip(X,Z):
			f.write("%f\t%f\n" %(x,y))
		f.close()
		sys.stdout.write("\n")
		sys.stdout.flush()
		plt.clf()
		
		if omega == 180.0:
			print "The file "+phi_to_chi_basefilename+".pdf is the graph in Fig 2b"
			print ""

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
	if fresh_start or not os.path.isfile(directory+"/chirality1_"+fnbasebase+".xyz"):
		do1 = 1
	do2 = 0
	if fresh_start or not os.path.isfile(directory+"/chirality2_"+fnbasebase+".xyz"):
		do2 = 1
	do3 = 0
	if fresh_start or not os.path.isfile(directory+"/chirality3_"+fnbasebase+".xyz"):
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
		
		anglerange = [(-180,180,2),(-180,180,5),(0,360,2),(-180,360*2,5)]
		#anglerange = [(0,360,5)]
		
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
				phi_bound = -180.+(phi+180.) % 360.
				for psi in np.arange(amin,amax+astep/2,astep):
					psi_bound = -180.+(psi+180.) % 360.
					chi = phi_psi_to_chi[(psi_bound,phi_bound)]
					newX.append(phi)
					newY.append(psi)
					newZ.append(chi)
			
			if amin == -180 and amax == 180:
				if "chirality1" in output_fnbase:
					print "Writing panel Fig 2a and Fig 3a as '"+output_fnbase+".*'"
				if "chirality2" in output_fnbase:
					print "Writing panel Fig 3b as '"+output_fnbase+".*'"
				if "chirality3" in output_fnbase:
					print "Writing panel Fig 3c as '"+output_fnbase+".*'"
			
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
			
			fns = [output_fnbase+".png",output_fnbase+".eps"]
			print "WRITING TO:",",".join(fns)
			locallib.make2Dfigure(newX,newY,newZ,fn=fns,
			                     xscaling=1, cmap=cmap,title=title,
			                     xtitle="$\phi$",ytitle="$\psi$",
			                     xticks=xticks, yticks=yticks,
			                     xlim=[amin,amax],ylim=[amin,amax],show=0,start_fresh=1, colorbar=1)#,zlim=[-1,1])

