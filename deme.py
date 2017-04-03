from mpl_toolkits.mplot3d import Axes3D
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os
#sns.set_style("whitegrid")
sns.set_style("white")

for constant in [-90,-10,0,10,90]:
	X=[]
	Y=[]
	for phi in range(-180,180):
		psi = constant - phi
		X.append(phi)
		Y.append(psi)
	plt.scatter(X,Y)
plt.show()
exit()
	


X=[]
Y=[]
Z=[]

Xatom = []
Yatom = []
Zatom = []



#atomic_theta = 70.0
#theta_offset_from_origin = 180

atomic_theta = 180.0
theta_offset_from_origin = 0
steps = 3.501
d = .005
#d = .001
#d = 0

z = 0.0
for theta in np.arange(0,360*steps):
	x = np.cos(np.radians(theta))
	y = np.sin(np.radians(theta))
	z += d
	
	X.append(x)
	Y.append(y)
	Z.append(z)
	
	# X,Y,Z depicts a continuous curve.
	# We also want to depict atoms at the right positions
	if ( theta - theta_offset_from_origin ) % atomic_theta == 0:
		Xatom.append(x)
		Yatom.append(y)
		Zatom.append(z)

X=np.array(X)
Y=np.array(Y)
Z=np.array(Z)

fig = plt.figure()#figsize=(10,35))
ax = fig.gca(projection='3d')
ax._axis3don = False

#ax.pbaspect = [1000.0, 1.0, 0.25]
ax.scatter(Xatom, Yatom, Zatom, alpha=1.0, s=10, c='w', linewidth=2.0/2.7) # s: sccale, alpha=1:opaque, c:color

ax.plot(X, Y, Z, 
        color = 'k',      # colour of the curve
        linewidth = 2.0/2.5,            # thickness of the line
        linestyle = '-'            # available styles - -- -. :
        )




'''
rcParams['legend.fontsize'] = 11    # legend font size
ax.legend()                         # adds the legend
ax.set_xlabel('')
ax.set_xlim(-5, 5)
ax.set_ylabel('')
ax.set_ylim(-10, 10)
ax.set_zlabel('')
ax.set_zlim(-9*np.pi, 9*np.pi)

ax.set_title('3D line plot,\n parametric curve', va='bottom')
'''

print ax.get_xlim3d()
print ax.get_ylim3d()
print ax.get_zlim3d()
#ax.set_autoscale_on(False)
#ax.set_autoscalez_on(False)

max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max() / 2.0

mid_x = (X.max()+X.min()) * 0.5
mid_y = (Y.max()+Y.min()) * 0.5
mid_z = (Z.max()+Z.min()) * 0.5
ax.set_xlim(mid_x - max_range, mid_x + max_range)
ax.set_ylim(mid_y - max_range, mid_y + max_range)
ax.set_zlim(mid_z - max_range, mid_z + max_range)

#ax.view_init(elev=38., azim=-90.)
ax.view_init(elev=43., azim=-77.)

plt.savefig("deme.svg", format="svg", transparent=True, bbox_inches='tight')
        
plt.show()
exit()
	
# rotate the axes and update
for angle in np.arange(0, 360):
	#ax.view_init(elev=45., azim=angle)
	plt.draw()
	#plt.show()
	#raw_input()
	plt.pause(.001)
#plt.show()                                  # display the plot
