from Tkinter import *
import matplotlib
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from itertools import product, combinations
import networkx as nx
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure 

def viewComponentGeo(G):
	componentgeo = Toplevel()
	componentgeo.title('Component Geometry')
		
	fig = Figure()
	canvas = FigureCanvasTkAgg(fig, master=componentgeo)
	ax = fig.add_subplot(111, projection='3d')
	xs = []
	ys = []
	zs = []

	for node in G.nodes():
		if 'Type' in G.node[node]:
			if G.node[node]['Type'] == 'Component':
				try: 
					int(G.node[node]['x'])
					xs.append(G.node[node]['x'])
					ys.append(G.node[node]['y'])
					zs.append(G.node[node]['z'])
				except TypeError:
					pass

	ax.scatter(xs, ys, zs, c='r', marker='o')
	ax.set_xlabel('X')
	ax.set_ylabel('Y')
	ax.set_zlabel('Z')

	#fig.savefig("componentgeo.png", bbox_inches='tight')
	
	canvas.show()
	canvas.get_tk_widget().configure(borderwidth=0, highlightbackground='gray', highlightcolor='gray', selectbackground='gray')
	canvas.get_tk_widget().pack()
	toolbar = NavigationToolbar2TkAgg(canvas, componentgeo)
	toolbar.update()
	#canvas._tkcanvas.pack()

def viewCompartmentGeo(G):
	
	compartmentgeo = Toplevel()
	compartmentgeo.title("Compartment Geometry")
	fig = Figure()

	canvas = FigureCanvasTkAgg(fig, master=compartmentgeo)
	
	ax = fig.gca(projection='3d')
	ax.set_aspect("equal")

	for node in G.nodes():
		if 'Type' in G.node[node]:
			if G.node[node]['Type'] == 'Compartment':
				try: 
					int(G.node[node]['x'])
					a = G.node[node]['EdgeLength']
					x = G.node[node]['x']
					y = G.node[node]['y']
					z = G.node[node]['z']
					hSL = float(a/2)
					r = [-hSL, hSL]
					rX = [-hSL + x, hSL + x]
					rY = [-hSL + y, hSL + y]
					rZ = [-hSL + z, hSL + z]
					for s, e in combinations(np.array(list(product(rX,rY,rZ))), 2):
						if not np.sum(np.abs(s-e)) > a+0.0000001:
							ax.plot3D(*zip(s,e), color="b")
				except TypeError:
					for i in range(0, len(G.node[node]['x'])):	
						a = G.node[node]['EdgeLength'][i]
						x = G.node[node]['x'][i]
						y = G.node[node]['y'][i]
						z = G.node[node]['z'][i]
						hSL = float(a/2)
						r = [-hSL, hSL]
						rX = [-hSL + x, hSL + x]
						rY = [-hSL + y, hSL + y]
						rZ = [-hSL + z, hSL + z]
						for s, e in combinations(np.array(list(product(rX,rY,rZ))), 2):
							if not np.sum(np.abs(s-e)) > a+0.0000001:
								ax.plot3D(*zip(s,e), color="b")

	scaling = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
	ax.auto_scale_xyz(*[[np.min(scaling), np.max(scaling)]]*3)

	canvas.show()
	canvas.get_tk_widget().configure(borderwidth=0, highlightbackground='gray', highlightcolor='gray', selectbackground='gray')
	canvas.get_tk_widget().pack()
	toolbar = NavigationToolbar2TkAgg(canvas, compartmentgeo)
	toolbar.update()
	


