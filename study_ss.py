#!/usr/bin/env python
'''
COMPANION SCRIPT #2, TESTED ONLY ON PYTHON 2.7, FOR: 
Mannige RV (2017) An exhaustive survey of regular peptide conformations 
using a new metric for backbone handedness (h). PeerJ.

This script generates:
1. data associated with secondary structure distributions in
both (phi,psi)-space (Fig 1b, Fig 9a) and in (theta,d)-space (Fig 9b,c)
2. regions dominantly occupied by proteins (dashed lines in Fig 1b and Fig 9)
3. possible regions for all cis and trans peptides (Fig 4, Fig9b,c)

The location of each figure's panel is stored in "output2.txt" generated by this script
'''

target_omega =  180.0 # only analyze backbones close to this value +/- 50 degrees
target_omega =  0.0

output_file = open("output2.txt","w")

# GLOBAL IMPORTS:
import os, sys, copy, random, glob, time, re
import matplotlib.pyplot as plt                       # For utilizing colormap interpolation 
import scipy.ndimage
import scipy.stats as st
from scipy import interpolate
from matplotlib.colors import LogNorm
import numpy as np
import Bio.PDB # Biopython's PDB module
from Bio import PDB
import pandas as pd
# LOCAL IMPORTS
sys.path.insert(0, "./local_imports/") # for the local imports
import Geometry, PeptideBuilder, locallib



if 1:
	#plt.ion() # turn on interactive mode
	'''testing'''
	A = 120.0
	B = 90.0
	
	omega = 180.0
	
	'''
	import sympy as sp
	d,theta,phi,psi = sp.symbols("d,theta,phi,psi")
	theta = sp.pi
	expression = 2*sp.acos( -0.8235*sp.sin((phi+psi)/2) + 0.0222*sp.sin((phi-psi)/2) )  - theta
	#expression  =  ( (  2.9986*sp.cos((phi+psi)/2) - 0.6575*sp.cos((phi-psi)/2) ) / sp.sin(theta/2) ) - d
	
	sp.pprint(expression)
	sp.pprint( sp.solveset( expression, phi ) )
	exit()
	'''
	
	if 0:
		for omega in [0,180]:
			hdiff = []
			for A in range(-180,181,5):
				for B in range(-180,181,5):
					if A != B:
						h1,theta1,d1 = locallib.calculate_handedness_from_theory(-A, B,omega)
						h2,theta2,d2 = locallib.calculate_handedness_from_theory(-B, A,omega)
					
						h1= round(h1,10)
						h2= round(h2,10)
						#h1 = np.sin(np.radians(theta1))
						#h2 = np.sin(np.radians(theta2))
						hdiff.append(h1+h2)
	
			hdiff = np.array(hdiff)
			print np.average(hdiff),"+/-",np.std(hdiff)
		
			from scipy.stats import norm
			import seaborn as sns
			sns.distplot(hdiff)#,fit=norm,kde=False)#,hist=False,kde=True)#,norm_hist=True)
			plt.title(r'$\omega=$'+str(omega))
			
	
	phi_psi_to_h  = {}
	h_to_phi_psis = {}
	d_theta_to_phi_psis = {}
	X=[];Y=[];Z=[];
	for phi in range(-180,181,1):
		for psi in range(-180,181,1):
			h,theta,d    = locallib.calculate_handedness_from_theory(phi,psi,omega)
			h = np.sin(np.radians(theta))*d
			#h = d
			if not np.isnan(h):
				#h = round(h,12)
				phi_psi_to_h[(phi,psi)] = h
				if not h in h_to_phi_psis:
					h_to_phi_psis[h]=[]
				if not -h in h_to_phi_psis:
					h_to_phi_psis[-h]=[]

					
				#theta_d = (theta,d)
				theta_d = (np.sin(np.radians(theta)),d)
				if not theta_d in d_theta_to_phi_psis:
					d_theta_to_phi_psis[theta_d] = []
				
				d_theta_to_phi_psis[theta_d].append([phi,psi])
				h_to_phi_psis[h].append([phi,psi])
				#h_to_phi_psis[-h].append([phi,psi])
				
				X.append(phi)
				Y.append(psi)
				Z.append(h)
	
	
	cmap = plt.get_cmap("chirality_r")
					
	locallib.make2Dfigure(X,Y,Z,
			xscaling=1, cmap=cmap, title=r'$r_\alpha$',
			xtitle="$\phi$",ytitle="$\psi$", 
			show=0,start_fresh=0, colorbar=1)#,zlim=[-1,1])
	
	
	#vals = d_theta_to_phi_psis
	vals = h_to_phi_psis
	
	for h in vals.keys():
		if len(vals[h]) > 1:
			phis = []
			psis = []
			for i in range(len(vals[h])):
				phi1,psi1 = vals[h][i]
				phis.append(phi1)
				psis.append(psi1)
			
			print vals[h]
			
			plt.scatter(phis[1:],psis[1:],c='r',s=200)
			plt.scatter(phis[:1],psis[:1],c='g',s=200)
			# draw vertical line from (70,100) to (70, 250)
			plt.plot([-180, 180], [180, -180], 'k-', lw=2)
			plt.grid(True)
			plt.xticks(np.arange(-180, 181, 90))
			plt.yticks(np.arange(-180, 181, 90))
			plt.gca().set_aspect('equal', adjustable='box')
			plt.axis([-180,180,-180,180])
			
			plt.show()
	exit()
			
	
	print '[round(h1,4), round(h2,4)]',[round(h1,4), round(h2,4)]
	if round(h1,4) == -1.0*round(h2,4):
		print [phi1,psi1,omega1],"and",[phi2,psi2,omega2],"are equal but opposite in handedness (magnitude: "+str(round(abs(h2),4))+")"
	print
	print
	# Same 'test', but for alpha-sheets (made up of alpha and alpha_L states)
	A = 64.0
	B = -41.0
	phi1,psi1,omega1 = [-A, B,180.0]
	phi2,psi2,omega2 = [ A,-B,180.0]
	
	if 0: # plot points
		plt.scatter([phi1],[psi1],c='g',s=200)
		plt.scatter([phi2],[psi2],c='r',s=200)
		plt.grid(True)
		plt.xticks(np.arange(-180, 181, 90))
		plt.yticks(np.arange(-180, 181, 90))
		plt.gca().set_aspect('equal', adjustable='box')
		plt.axis([-180,180,-180,180])
		plt.show()
	
	h1,theta1,d1 = locallib.calculate_handedness_from_theory(phi1,psi1,omega1)
	h2,theta2,d2 = locallib.calculate_handedness_from_theory(phi2,psi2,omega2)
	print '[round(h1,4), round(h2,4)]',[round(h1,4), round(h2,4)]
	if round(h1,4) == -1.0*round(h2,4):
		print [phi1,psi1,omega1],"and",[phi2,psi2,omega2],"are equal but opposite in handedness (magnitude: "+str(round(abs(h2),4))+")"
	




if 1:
	'''A little script that tests to see whether h from the two sigma sheet points
	on the Ramachandran plot are indeed of equal but opposite chirality'''
	A = 120.0
	B = 90.0
	
	phi1,psi1,omega1 = [-A, B,180.0]
	phi2,psi2,omega2 = [ A,-B,180.0]
	
	h1,theta1,d1 = locallib.calculate_handedness_from_theory(phi1,psi1,omega1)
	h2,theta2,d2 = locallib.calculate_handedness_from_theory(phi2,psi2,omega2)
	
	if 0: # plot points
		plt.scatter([phi1],[psi1],c='g',s=200)
		plt.scatter([phi2],[psi2],c='r',s=200)
		plt.grid(True)
		plt.xticks(np.arange(-180, 181, 90))
		plt.yticks(np.arange(-180, 181, 90))
		plt.gca().set_aspect('equal', adjustable='box')
		plt.axis([-180,180,-180,180])
		plt.show()
	
	print '[round(h1,4), round(h2,4)]',[round(h1,4), round(h2,4)]
	if round(h1,4) == -1.0*round(h2,4):
		print [phi1,psi1,omega1],"and",[phi2,psi2,omega2],"are equal but opposite in handedness (magnitude: "+str(round(abs(h2),4))+")"
	print
	print
	# Same 'test', but for alpha-sheets (made up of alpha and alpha_L states)
	A = 64.0
	B = -41.0
	phi1,psi1,omega1 = [-A, B,180.0]
	phi2,psi2,omega2 = [ A,-B,180.0]
	
	if 0: # plot points
		plt.scatter([phi1],[psi1],c='g',s=200)
		plt.scatter([phi2],[psi2],c='r',s=200)
		plt.grid(True)
		plt.xticks(np.arange(-180, 181, 90))
		plt.yticks(np.arange(-180, 181, 90))
		plt.gca().set_aspect('equal', adjustable='box')
		plt.axis([-180,180,-180,180])
		plt.show()
	
	h1,theta1,d1 = locallib.calculate_handedness_from_theory(phi1,psi1,omega1)
	h2,theta2,d2 = locallib.calculate_handedness_from_theory(phi2,psi2,omega2)
	print '[round(h1,4), round(h2,4)]',[round(h1,4), round(h2,4)]
	if round(h1,4) == -1.0*round(h2,4):
		print [phi1,psi1,omega1],"and",[phi2,psi2,omega2],"are equal but opposite in handedness (magnitude: "+str(round(abs(h2),4))+")"
	
	

# -----------------------
# GLOBAL GRAPHING IMPORTS
import seaborn as sns
def cos(a):
	return np.cos(np.radians(a))
def sin(a):
	return np.sin(np.radians(a))

# ===================================================================================
# SETTING UP A CUSTOM COLORMAP
# 
COLORSWITCH = 0.5; bc = [1,1,1] # background (white)
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

# -----------------------------------------------------------
# from http://stackoverflow.com/questions/30145957/plotting-2d-kernel-density-estimation-with-python
# A 2D kernel density estimator that takes in a set of Xs and Ys. A test for this function follows.
def draw_kde(x,y,axis=False,levels=[0.3,0.7],cmap=plt.get_cmap('Blues'),c='k',linestyles='solid',linewidths=0.6,extent=[]):
	x= np.array(x).astype(float)
	y= np.array(y).astype(float)
	
	if len(extent) == 4:
		xmin = extent[0]
		xmax = extent[1]
		ymin = extent[2]
		ymax = extent[3]
	else:
		xstep = float(np.max(x)-np.min(x))*0.02
		ystep = float(np.max(y)-np.min(y))*0.02
		xmin, xmax = np.min(x)-xstep, np.max(x)+xstep
		ymin, ymax = np.min(y)-ystep, np.max(y)+ystep
		extent = [xmin,xmax,ymin,ymax]
	
	xx, yy = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]

	positions = np.vstack([xx.ravel(), yy.ravel()])
	values = np.vstack([x, y])
	print "\tCalculating KDE"
	kernel = st.gaussian_kde(values)
	print "\tObtaining values from KDE"
	f = np.reshape(kernel(positions).T, xx.shape)
	f /= f.sum()
	
	print "\tfractional levels =", levels
	
	try:
		# -------------------------------
		# levels are in percentile values. So, we need to get the actual frequency above which the percentile value is reached
		n = 1000
		t = np.linspace(0, f.max(), n)
		integral = ((f >= t[:, None, None]) * f).sum(axis=(1,2))
		a = interpolate.interp1d(integral, t)
		levels = sorted(a(np.array(levels)))
		levels = levels + [f.max()]
		# -------------------------------
	except:
		print "Failed getting the values for  levels provided. Using min and max values instead."
		levels = [f.min(),f.max()]
	
	print "\tactual levels     =", levels
	
	if axis is False:
		print "AXIS NOT GIVEN, MAKING A NEW FIGURE"
		fig = plt.figure()
		axis = fig.gca()
	#
	axes = []
	if (type(axis) is list) or (type(axis) is tuple):
		axes=axis
	else:
		axes.append(axis)
	
	for ax in axes:
		cfset = ax.contourf(xx, yy, f, cmap=cmap,levels=levels,linestyles=linestyles,extent=extent)
		cset  = ax.contour( xx, yy, f, colors=c,levels=levels,linestyles=linestyles,linewidths=linewidths,extent=extent)
		# Label plot
	# done

'''
# TEST FOR draw_kde():
data = np.random.multivariate_normal((0, 0), [[0.8, 0.05], [0.05, 0.7]], 100)
xtest = data[:, 0]
ytest = data[:, 1]
draw_kde(xtest,ytest,levels=[0.05,0.3,1],cmap=plt.get_cmap('Blues'))
plt.show()
exit()
'''

# -----------------------------------------------------------

# Download SCOP database with 40% redundancy, if not done already
SCOP_download_location = r"./local_database/pdbstyle-sel-gs-bib-40-2.06.tgz"
SCOP_URL = r'http://scop.berkeley.edu/downloads/pdbstyle/pdbstyle-sel-gs-bib-40-2.06.tgz'
if not os.path.isfile(SCOP_download_location):
	print "\n\n# '%s' does not exist... downloading from:\n# %s\n\n" %(SCOP_download_location,SCOP_URL)
	os.system("wget -O %s %s" %(SCOP_download_location,SCOP_URL))
	#
	tar_command = "tar xzf %s -C %s" %(SCOP_download_location, os.path.split(SCOP_download_location)[0]+"/")
	print 'RUNNING:',tar_command
	os.system(tar_command)

# IF YOU WANT TO US STRIDE (binary already exists for Linux distributions)
# MANUAL STEPS:
# 1. Download STRIDE (from http://webclu.bio.wzw.tum.de/stride/install.html)
# 2. DOWNLOAD LINK: http://webclu.bio.wzw.tum.de/stride/stride.tar.gz
# 3. DOWNLOAD TO: ./local_imports/
# Then:
# > cd ./local_imports/
# > tar xvzf stride.tar.gz
# > cd ./stride/
# > make
# ./stride/stride should work as an executable (used GCC compiler)

program_to_use = "dssp" # can be either 'dssp' or 'stride'
ss_predictor_stride = "./local_imports/stride/stride" 
ss_predictor_dssp   = "./local_imports/dssp/dssp-2.0.4-linux-amd64" 
#obtained from: ftp://ftp.cmbi.ru.nl/pub/software/dssp/ (binary already exists for Linux distributions)

program_to_use = program_to_use.lower()

# Getting the various PDB file names:
files = glob.glob(os.path.split(SCOP_download_location)[0]+"/"+"pdbstyle*/*/*.ent")

# Going through each file:
counter   = 0
len_files = len(files)
print "CHECKING IF RESIDUE-LEVEL REPORTS (<pdbfilename>."+program_to_use+".py) EXIST:"
for fn in files:
	counter += 1
	
	pyfilename = fn+"."+program_to_use+".py"
	if not os.path.isfile(pyfilename):
		
		output_filename = 'deme.ss'
		os.system('rm '+output_filename)
		resno_to_data = {}
		# Collecting SS information from one of two software package
		if program_to_use == "dssp":
			ss_assignment_command   = "%s -i %s -o %s" %(ss_predictor_dssp,fn,output_filename)
			os.system(ss_assignment_command)
			if os.path.isfile(output_filename):
				resno_to_data = locallib.return_secondary_structure_dssp(output_filename)
		elif program_to_use == "stride":
			ss_assignment_command = "%s -f%s %s" %(ss_predictor_stride,output_filename,fn)
			os.system(ss_assignment_command)
			if os.path.isfile(output_filename):
				resno_to_data = locallib.return_secondary_structure_stride(output_filename)
		
		
		# Collecting positions for C, CA, N atoms (to calculate phi psi omega)
		residue_to_atom_to_position = {}
		pdb_parser = PDB.PDBParser()
		structure = pdb_parser.get_structure("reference", fn)
		for model in structure:
			for chain in model:
				for residue in chain:
					resno = residue.get_id()[1]
					if not resno in resno_to_data:
						pass
					else:
						if not resno in residue_to_atom_to_position:
							residue_to_atom_to_position[resno] = {}
						for atom in residue:
							atom_id = atom.get_id()
							if atom_id in ["N","CA","C"]: #help(atom)
								residue_to_atom_to_position[resno][atom_id] = atom.get_vector()
	
		# Calculating phi psi and omega:
		resnumbers = sorted(residue_to_atom_to_position.keys())
		for ri in range(len(resnumbers)):
			if resnumbers[ri-1] == resnumbers[ri]-1 and ri + 1 < len(resnumbers):
				if resnumbers[ri+1] == resnumbers[ri]+1:
					rm = residue_to_atom_to_position[resnumbers[ri-1]]
					r  = residue_to_atom_to_position[resnumbers[ri]]
					rp = residue_to_atom_to_position[resnumbers[ri+1]]
					#Following is less stringent but similar to querying the truth value:
					# ('CA' in rm and 'C' in rm and 'N' in r and 'CA' in r and 'C' in r)
					# ... which, if true, allow us to calculate phi, psi and omega
					if len(rm.keys()) ==  len(r.keys()) == len(rp.keys()) == 3: 
						# then we have a continuous region for the calculation of phi, psi and omega
						v1 = rm['C']
						v2 = r['N']
						v3 = r['CA']
						v4 = r['C']
						phi = Bio.PDB.calc_dihedral(v1, v2, v3, v4)
						v1 = r['N']
						v2 = r['CA']
						v3 = r['C']
						v4 = rp['N']
						psi = Bio.PDB.calc_dihedral(v1, v2, v3, v4)
						v1 = r['CA']
						v2 = r['C']
						v3 = rp['N']
						v4 = rp['CA']
						omega = Bio.PDB.calc_dihedral(v1, v2, v3, v4)
						resno = int(resnumbers[ri])
						resno_to_data[resno]['phi']   = np.degrees(phi)
						resno_to_data[resno]['psi']   = np.degrees(psi)
						resno_to_data[resno]['omega'] = np.degrees(omega)
						
						if resno_to_data[resno]['ss'] == 'H':
							# There are two types of helices (left and right). We check if phi-psi > 0, 
							# in which case we have a (rare) left handed helix.
							if phi+psi > 0.0:
								# reassigning the helix to its left  form
								resno_to_data[resno]['ss'] = 'leftH'
		
		f = open(pyfilename,'w')
		f.write('resno_to_data = '+str(resno_to_data).replace("},","},\n"))
		f.close()
	
	if counter % 10 == 0.0 or counter == len_files:
		sys.stdout.write("\r%d \tof \t%d \t(%0.2f \tpercent)               " %(counter,len_files,float(counter*100.0)/len_files))
		sys.stdout.flush()
		time.sleep(0.05)
sys.stdout.write("\n"); sys.stdout.flush();

#ss_counts = {"all":0}
ss_to_data = {}
counter = 0

print "DIGESTING RESIDUE-LEVEL REPORTS (<pdbfilename>."+program_to_use+".py):"
for fn in files:#[100:200]: #['local_database/pdbstyle-2.06/zz/d1zzwa_.ent']:#files:
	counter += 1
	pyfilename = fn+"."+program_to_use+".py"
	if os.path.isfile(pyfilename):
		# The execfile() command below will reload a fresh 'resno_to_data', but to make sure 
		# that we are not using an old 'resno_to_data', we erase its contents
		resno_to_data = {}
		# Loading the new 'resno_to_data'
		execfile(os.path.abspath(pyfilename))
		
		for r in resno_to_data.keys():
			if 'phi' in resno_to_data[r]:
				aa    = resno_to_data[r]['type']
				ss    = resno_to_data[r]['ss']
				omega = resno_to_data[r]['omega']
				phi   = resno_to_data[r]['phi']
				psi   = resno_to_data[r]['psi']
				
				#if abs(target_omega - omega) > 180:
				#	omega = 360.0 + omega
				
				# omega wrap (Eqn 9 in Mannige, PeerJ, 2017)
				Delta = -90.0
				omega = ( omega - Delta ) % 360.0 + Delta
					
					# checking if our omega lies in the range of the target omega 
				# (which is likely either 0 or 180)
				if (target_omega -50.0 < omega) and (omega < target_omega + 50.0):
					
					if not ss in ss_to_data:
						ss_to_data[ss] = {'phi':[],'psi':[],'omega':[],'theta':[],'d':[]}
					
					ss_to_data[ss]['phi'].append(phi)
					ss_to_data[ss]['psi'].append(psi)
					
					chi, theta, d = locallib.calculate_handedness_from_theory(phi,psi,omega)
					
					ss_to_data[ss]['omega'].append(omega)
					ss_to_data[ss]['theta'].append(theta)
					ss_to_data[ss]['d'].append(d)
		
	
	if counter % 10 == 0.0 or counter == len_files:
		sys.stdout.write("\r%d \tof \t%d \t(%0.2f \tpercent)               " %(counter,len_files,float(counter*100.0)/len_files))
		sys.stdout.flush()
sys.stdout.write("\n" )
sys.stdout.flush()

'''
sns.jointplot(x=np.array(ss_to_data['leftH']['phi']), y=np.array(ss_to_data['leftH']['psi']))#, data=df)
#plt.plot([omega_min, omega_min], [0, 0.2], linewidth=2)
#plt.plot([omega_max, omega_max], [0, 0.2], linewidth=2)
plt.show()
'''

# Combining all elements of 
alldict = {'phi':[],'psi':[],'omega':[],'theta':[],'d':[]}
overflow_phis = []
overflow_psis = []
print "CREATING A COMBINED RECORD FOR ALL RESIDUES"
for ss in ss_to_data.keys():
	for key in alldict.keys():
		alldict[key] += ss_to_data[ss][key]
	
	# overflowing the boundaries so that boundary density is not ignored by the kernel density estimator (for Ramachandran contour plots)
	if 1:
		'''
		KEY: ' | ' = periodic boundary in phi
		     '___' = periodic boundary in psi
		     ' : ' = periodic boundary in phi
		   
			.--------------------------------------band
			|
			|                       .-----periodic band
			|                       |   
		     ___|___________________ ___|___
		-180|   |   :            180|   |   :
		    |   v   :               |   v   :
		    |       :               |       :
		    | <---> :               | <---> :
		    | allow :               | allow :
		    |       :               |       :
		    |       :               |       :
		    |   x   :               |   x'  :
		    |   |   :               |   |   :
		    |___|___:_______________|___|___:
			|                       | 
		   move from -----------------> to
		'''
	
		allow = 10.0
	
		for i in range(len(ss_to_data[ss]['phi'])):
			x = ss_to_data[ss]['phi'][i]
			y = ss_to_data[ss]['psi'][i]
			
			new_xs = []
			new_ys = []
			if   x < -180+allow: # x band 1
				new_xs.append(x+360)
			elif 180-allow < x:  # x band 2
				new_xs.append(x-360)
			if   y < -180+allow: # y band 1
				new_ys.append(y+360)
			elif 180-allow < y:  # y band 2
				new_ys.append(y-360)
		
			if len(new_xs):
				for nx in new_xs:
					# translate along x
					overflow_phis.append(nx)
					overflow_psis.append(y)
			if len(new_ys):
				for ny in new_ys:
					# translate along y
					overflow_phis.append(x)
					overflow_psis.append(ny)
			if len(new_xs) and len(new_ys):
				for nx in new_xs:
					for ny in new_ys:
						overflow_phis.append(nx)
						overflow_psis.append(ny)
alldict['phi'] += overflow_phis
alldict['psi'] += overflow_psis	

# COLLECTING THE DISTRIBUTION STATISTICS FOR OMEGA:
trans_omega_average =  np.average(alldict['omega'])
trans_omega_std     =  np.std(alldict['omega'])
print "omega =",trans_omega_average,"+/-",trans_omega_std

trans_omega     = 180.0
trans_omega_min = trans_omega - 2.0*trans_omega_std
trans_omega_max = trans_omega + 2.0*trans_omega_std

cis_omega     = 0.0
cis_omega_min = cis_omega - 2.0*trans_omega_std
cis_omega_max = cis_omega + 2.0*trans_omega_std

'''
# DRAW THE OMEGA DISTRIBUTION
sns.distplot(alldict['omega'])
plt.plot([omega_min, omega_min], [0, 0.2], linewidth=2)
plt.plot([omega_max, omega_max], [0, 0.2], linewidth=2)
plt.show()
exit()
'''

# CREATING ANOTHER RECORD THAT STORES ALL POSSIBLE VALUES WITHIN A RAMACHANDRAN PLOTS
possible_dict_trans = {'phi':[],'psi':[],'omega':[],'theta':[],'d':[]}
possible_dict_cis   = {'phi':[],'psi':[],'omega':[],'theta':[],'d':[]}
if 1:
	angle_step = 1
	omega = 180.0 # trans backbones only
	for phi in np.arange(-180,180+angle_step,angle_step):
		for psi in np.arange(-180,180+angle_step,angle_step):
			# trans
			for o in [trans_omega, trans_omega_min, trans_omega_max]:
				chi, theta, d = locallib.calculate_handedness_from_theory(phi,psi,o)
				
				possible_dict_trans['phi'].append(phi)
				possible_dict_trans['psi'].append(psi)
				possible_dict_trans['omega'].append(o)
				possible_dict_trans['theta'].append(theta)
				possible_dict_trans['d'].append(d)
			
			for o in [cis_omega, cis_omega_min, cis_omega_max]:
				chi, theta, d = locallib.calculate_handedness_from_theory(phi,psi,o)
				
				possible_dict_cis['phi'].append(phi)
				possible_dict_cis['psi'].append(psi)
				possible_dict_cis['omega'].append(o)
				possible_dict_cis['theta'].append(theta)
				possible_dict_cis['d'].append(d)
				
				
# ADDING THAT RECORD AS A 'POSSIBLE' SPACE
ss_to_data['possible_cis']   = possible_dict_cis
ss_to_data['possible_trans'] = possible_dict_trans

# ADDING A RECORD FOR ALL BACKBONE BEHAVIOR
ss_to_data['all'] = alldict

if 1:	
	sns.set_style("ticks")
	
	linewidths = 0.6
	xbins = 150
	ybins = xbins
		
	allX = []
	allY = []
	plt.clf()
	ss_to_data.keys()
	
	# Creating a three-panel graph
	# 1. Cartesian (phi,psi) plot (Ramachandran plot)
	ax1 = plt.subplot(131, adjustable='box', aspect=1)
	# 2. Polar (theta,d) plot (Zacharias & Knapp, Protein Science, 2013)
	ax2 = plt.subplot(132, projection='polar')
	# 2. Cartesian (d,theta) plot (our proposed replacement for the Ramachandran plot)
	ax3 = plt.subplot(133, adjustable='box', aspect=0.58)
	
	#
	to_draw = [['possible_cis','Greys',[]],
	           ['possible_trans','Greys',[]],
	           ['all','Greys' ,[0.9]    ], # all
	           ['E'  ,'Blues' ,[0.5,0.8]],#'kde'], # sheet 
	           ['H'  ,'Reds'  ,[0.5,0.8]],#'kde'], # alpha   helix
	           ['all','Reds'  ,[0.76]   ],#'kde'], # alpha_L helix
	           ['G'  ,'Greens',[0.5,0.8]],#'kde'], # 3_10  helix
	           ['G'  ,'Greens',[0.9]    ] #'kde'], # 3_10L helix
	           ]
	
	if target_omega == 0.0:
		to_draw = [['possible_cis','Greys',[]],
			   ['possible_trans','Greys',[]],
			   ['all','Greys' ,[0.9]    ], # all
			   ]
			
	for info in to_draw: #
		ss     = info[0]
		color  = info[1]
		levels = info[2]
		contour_type = "histogram"
		if len(info) == 4:
			contour_type = "kde"
		
		if ss in ss_to_data:
			print "type:",ss,"\tcolor:",color,"\t levels:",levels
			
			phis   = ss_to_data[ss]['phi']
			psis   = ss_to_data[ss]['psi']
			omegas = ss_to_data[ss]['omega']
			thetas = ss_to_data[ss]['theta']
			ds     = ss_to_data[ss]['d']
		
			X = list(np.radians(thetas))
			Y = ds
		
			allX += copy.deepcopy(X)
			allY += copy.deepcopy(Y)
		
			lenX = len(X)
			H, xedges, yedges = np.histogram2d(Y, X, bins=(ybins, xbins), range=[[min(Y)-0.2,max(Y)+0.2], [min(X)- 10./180.,max(X)+10./180.]])
		
			phis = list(np.radians(phis))
			psis = list(np.radians(psis))
			
			H2, xedges2, yedges2 = np.histogram2d(psis, phis, bins=(ybins, xbins), range=[[min(psis)-10./180.,max(psis)+10./180.], [min(phis)-10./180.,max(phis)+10./180.]])
			dy2 = yedges2[1]-yedges2[0]; dx2 = xedges2[1]-xedges2[0];
			extent2 = [yedges2[0]+dy2/2, yedges2[-1]-dy2/2, xedges2[0]+dx2/2, xedges2[-1]-dx2/2]
			
			dy = yedges[1]-yedges[0]; dx = xedges[1]-xedges[0]; #(by their monotonic increasing in linear scale)
			extent = [yedges[0]+dy/2, yedges[-1]-dy/2, xedges[0]+dx/2, xedges[-1]-dx/2]
			
			#plt.hist2d(X,Y,bins=(xbins,ybins), cmap=plt.get_cmap(color), cmin=1, alpha=1)#, norm=LogNorm()) # All bins lower than cmin will not be colored
			#plt.colorbar()
		
			linestyles = 'solid'
			
			c  = 'black'
			'''
			if color == 'Blues':
				c = 'b'
			elif color == 'Reds':
				c = 'r'
			elif color == 'Oranges':
				c = 'darkorange'
			elif color == 'Greens':
				c = 'darkgreen'
			'''
			# Normalizing the values... now we have frequencies
			H  /= H.sum()
			H2 /= H2.sum()
			
			if len(levels) == 0: # mostly for when ss == "possible" ... every region is counted
				linestyles = 'solid'
				if ss == 'possible_cis':
					linestyles = 'dotted'
					
				#ax2.contour(H, [1],linewidths=linewidths,colors='k',extent=extent,linestyles=linestyles)
				#ax3.contour(H, [1],linewidths=linewidths,colors='k',extent=extent,linestyles=linestyles)
				flatH = sorted(set(np.ndarray.flatten(H)))
				ax2.contour(H, [flatH[1]-flatH[1]/2.],linewidths=linewidths,colors='k',extent=extent,linestyles=linestyles)
				ax3.contour(H, [flatH[1]-flatH[1]/2.],linewidths=linewidths,colors='k',extent=extent,linestyles=linestyles)
				#
			else:
				if contour_type.lower() == "kde":
					# Switch 'if 0' to 'if 1' in case you want to use kernel density estimates to create smoother 
					# contours (as was done in the publication). Takes a long time, though.
					draw_kde(phis,psis, [  ax1  ],levels=levels,cmap=plt.get_cmap(color),c=c,linestyles=linestyles,linewidths=linewidths,extent=[-180.,180.-180.,180.])
					draw_kde(X   ,Y   , [ax2,ax3],levels=levels,cmap=plt.get_cmap(color),c=c,linestyles=linestyles,linewidths=linewidths,extent=[0,2.0*np.pi,-4.,4.])
				else:
					#H  = scipy.ndimage.zoom(H,  6, order=1) # makes for smoother curves (polar   coordinates)
					#H2 = scipy.ndimage.zoom(H2, 6, order=1) # makes for smoother curves (phi-psi coordinates)
					
					levels1 = [0]
					levels2 = [0]
					try:
						# -------------------------------
						# levels are in percentile values. So, we need to get the actual frequency above which the percentile value is reached
						# neat trick learnt from: http://stackoverflow.com/questions/37890550/python-plotting-percentile-contour-lines-of-a-probability-distribution
						n = 1000
						f = copy.deepcopy(H)
						t = np.linspace(0, f.max(), n)
						integral = ((f >= t[:, None, None]) * f).sum(axis=(1,2))
						a = interpolate.interp1d(integral, t)
						levels1 = sorted(a(np.array(levels)))
						levels1 = levels1 + [f.max()]
						# ---
						f = H2
						t = np.linspace(0, f.max(), n)
						integral = ((f >= t[:, None, None]) * f).sum(axis=(1,2))
						a = interpolate.interp1d(integral, t)
						levels2 = sorted(a(np.array(levels)))
						levels2 = levels2 + [f.max()]
						# -------------------------------
					except:
						print "levels",levels,"do not work (possible due to sparce data)",
					#print "---------------"
					#print current_levels
					#print sorted(set(np.ndarray.flatten(H)))
					#print "---------------"
					# (phi,psi) cartesian plot
					if len(levels2) > 1:
						ax1.contourf(H2,levels=levels2,cmap=plt.get_cmap(color),extent=extent2,linestyles=linestyles)
					ax1.contour( H2,levels=levels2,linewidths=linewidths,colors=c,extent=extent2,linestyles=linestyles)
					# (d,theta) polar plot
					if len(levels1) > 1:
						ax2.contourf(H,levels=levels1,cmap=plt.get_cmap(color),extent=extent,linestyles=linestyles)
					ax2.contour( H,levels=levels1,linewidths=linewidths,colors=c,extent=extent,linestyles=linestyles)
					# (theta,d) cartesian plot
					if len(levels1) > 1:
						ax3.contourf(H,levels=levels1,cmap=plt.get_cmap(color),extent=extent,linestyles=linestyles)
					ax3.contour( H,levels=levels1,linewidths=linewidths,colors=c,extent=extent,linestyles=linestyles)
	X=allX
	Y=allY
	ypadding = float(max(Y)-min(Y))/20.
	# for ax2,ax3
	xticks = np.array([0,1,2]) 
	x_label = [r"$0\pi$", r"$\pi$",   r"$2\pi$"]
	# for ax1
	xticks2  = np.array([-1,0,1])
	x_label2 = [r"$-\pi$", r"$0$",   r"$\pi$"]
	
	# -------------------------------------------------
	# Instructions for the Ramachandran (phi,psi) plot
	ax1.axis([-np.pi,np.pi,-np.pi,np.pi])
	# Prettyfying the ax1 axis
	# X
	ax1.set_xlabel("$\phi$")
	ax1.set_xticks(xticks2*np.pi)
	ax1.set_xticklabels(x_label2)#, fontsize=20)
	# Y
	ax1.set_ylabel("$\psi$")
	ax1.set_yticks(xticks2*np.pi)
	ax1.set_yticklabels(x_label2)#, fontsize=20)
	
	# -------------------------------------------------
	# Instructions for the polar (theta,d) plot
	ax2.set_theta_zero_location('S')
	ax2.set_theta_direction(-1)
	#ax2.set_rticklabels(['-4','','-2','','0','','2','','4'])#, fontsize=20)	
	ax2.set_rticks([-4,-3,-2,-1,0,1,2,3,4])
	ax2.axis([0,2*np.pi,0, 4.035898560121968]) # to see the whole version (including negative values),
	                                           # set to [0,2*np.pi,-4.035898560121968, 4.035898560121968]
	
	# -------------------------------------------------
	# Instructions for the cartesian (theta,d) plot
	ax3.axis([0,2*np.pi, -4.035898560121968, 4.035898560121968])
	ax3.grid(True, which='both', linewidth=linewidths*1.2)
	# set the x-spine (see below for more info on `set_position`)
	ax3.spines['left'].set_position('zero')
	# turn off the right spine/ticks
	ax3.spines['right'].set_color('none')
	ax3.yaxis.tick_left()
	# set the y-spine
	ax3.spines['bottom'].set_position('zero')
	# turn off the top spine/ticks
	ax3.spines['top'].set_color('none')
	ax3.xaxis.tick_bottom()
	# Prettyfying the ax3 axis
	ax3.axis([0,2*np.pi,min(Y)-ypadding,max(Y)+ypadding])
	ax3.set_ylabel(r"$d$")
	ax3.set_xlabel(r"$\theta$")
	#
	ax3.set_xticklabels(x_label)#, fontsize=20)	
	ax3.set_xticks(xticks*np.pi)
	#
	ax3.set_yticklabels(['-4','','-2','','0','','2','','4'])#, fontsize=20)	
	ax3.set_yticks([-4,-3,-2,-1,0,1,2,3,4])
	
	#ax.set_rmin(0)
	ax1.tick_params(length=3, width=0.5)
	ax2.tick_params(length=3, width=0.5)
	ax3.tick_params(length=3, width=0.5)
	
	plt.setp(ax1.spines.values(), linewidth=linewidths*1.2)
	plt.setp(ax2.spines.values(), linewidth=linewidths*1.2)
	plt.setp(ax3.spines.values(), linewidth=linewidths*1.2)
	
	# ---------------------------------------------------
	# WRITING TO FILE
	plt.tight_layout()
	outfn = "graphs/various_2d_distributions_omega%d.svg" %(int(target_omega))
	plt.savefig(outfn,bbox_inches="tight")#dpi=280,
	
	output_file.write("A version of Fig 9 is available at '"+outfn+"'\n")
	output_file.write("Fig 4 contains the solid and dashed contours in Panel C in '"+outfn+"' \n")
	output_file.write("Fig 1b contains the secondary contours in Panel A in '"+outfn+"' \n")
	
	# UNCOMMENT TO SHOW FIGURE
	#plt.show()
	
	
	
	
	
	