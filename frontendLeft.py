from Tkinter import *
from frontendRight import *
import tkSimpleDialog
import networkx as nx

class FrontendLeft(Frame):
	def __init__(self, parent, rightFrame, G):
		Frame.__init__(self, parent)

		self.parent = parent
		self.rightFrame = rightFrame
		self.G = G
		self.color = "light blue"
		self.initUI()

	#toolbar button click events:
	#ALL: first unbinds the old mouse click events 

	#binds mouse clicks to the createNode function when the 'create node' button is pressed 
	def createNodeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.createNode)
	
	# binds mouse clicks to the startEdge function and binds mouse click releases to the createEdge
	# function when the 'create edge' button is pressed  
	def createEdgeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.bind('<ButtonPress-1>', self.edgeStart)
		self.systemsCanvas.bind('<ButtonRelease-1>', self.createEdge)
	
	# binds mouse clicks to the selectNode function when the 'select node' button is pressed 
	def selectNodeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.selectNode)
	
	# binds mouse clicks to the selectEdge function when the 'select edge' button is pressed 
	def selectEdgeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.selectEdge)
	
	# binds mouse clicks to the deleteNode function when the 'delete node' button is pressed 
	def deleteNodeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.deleteNode)
	
	# binds mouse clicks to the deleteEdge function when the 'delete edge' button is pressed 
	def deleteEdgeButtonClick(self):
		self.systemsCanvas.unbind('<Button-1>')
		self.systemsCanvas.unbind('<ButtonRelease-1>')
		self.systemsCanvas.bind('<Button-1>', self.deleteEdge)


	
	#creation, selection, and deletion of nodes/edges events:

	#creates a red circular node of radius r at the location of the mouse click and initilizes node propoerties
	def createNode(self, event):
		r = 8
		item=self.systemsCanvas.create_oval(event.x-r, event.y-r, event.x+r, event.y+r, fill='red', tag='node') 
		self.G.add_node(item, x=0, y=0, z=0, Name=None, x_coord=event.x, y_coord=event.y)

	#determines the x and y coordinates of where the edge will start, checks that starting coords are from a node
	def edgeStart(self, event):
		r = 24
		self.startNode = ()
		self.startNode = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)
		if len(self.startNode)>0:
			self.startNodeCoords=self.systemsCanvas.coords(self.startNode[0])
			self.startNodeX=(self.startNodeCoords[0]+self.startNodeCoords[2])/2
			self.startNodeY=(self.startNodeCoords[1]+self.startNodeCoords[3])/2
	
	# determines the x and y coordinates of where the edge will terminate, and then creates a line from startNode to endNode
	# will only allow the creation of an edge to happen between two nodes 
	def createEdge(self, event):
		r = 24
		self.endNode = ()
		self.endNode = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)
		if (len(self.startNode)>0) and (len(self.endNode)>0):
			self.endNodeCoords=self.systemsCanvas.coords(self.endNode[0])
			self.endNodeX=(self.endNodeCoords[0]+self.endNodeCoords[2])/2
			self.endNodeY=(self.endNodeCoords[1]+self.endNodeCoords[3])/2 	
			item=self.systemsCanvas.create_line(self.startNodeX, self.startNodeY, self.endNodeX, self.endNodeY, tag='edge')
			self.G.add_edge(self.startNode[0], self.endNode[0])
			self.systemsCanvas.addtag_withtag(str(self.startNode[0]), item)
			self.systemsCanvas.addtag_withtag(str(self.endNode[0]), item)
			
	# finds node enclosed by mouse click with a radius of r and displays node information
	def selectNode(self, event):
		r = 24
		selected = self.systemsCanvas.find_enclosed(event.x-r, event.y-r, event.x+r, event.y+r)

		if (len(selected) > 0):
			for widget in self.rightFrame.winfo_children():
				widget.destroy()

			self.systemInfo = FrontendRight(self.rightFrame, selected[0], self.G, self.optionList)

	# finds edge overlapping mouse click with a radius of r 
	def selectEdge(self, event):
		r = 4
		selected = self.systemsCanvas.find_overlapping(event.x-r, event.y-r, event.x+r, event.y+r)
		if len(selected) > 0:
			selected_tag = self.systemsCanvas.gettags(selected[0])[0]
			if selected_tag == 'edge':
				print "edge %s" % (selected[0])
	
	def deleteNode(self, event):
		pass

	def deleteEdge(self, event):
		pass
	
	# deletes last object created on the canvas
	def undo(self, event=None):
		itemList = self.systemsCanvas.find_all()
		if len(itemList) > 0:
			lastItemIndex = len(itemList)-1
			lastItemTag = self.systemsCanvas.gettags(itemList[lastItemIndex])[0]
			if lastItemTag == 'node':
				self.G.remove_node(itemList[lastItemIndex])
			elif lastItemTag == 'edge':
				self.G.remove_edge(int(self.systemsCanvas.gettags(itemList[lastItemIndex])[1]), int(self.systemsCanvas.gettags(itemList[lastItemIndex])[2]))
			self.systemsCanvas.delete(itemList[lastItemIndex])




	# creates new system in option menu and only displays nodes with specific system demands
	def newOptionMenu(self, event):
		if self.v.get() == "Create New":
			typeLabel = tkSimpleDialog.askstring(title="New System", prompt="Enter a new system")
			if typeLabel != None:
				self.optionList.insert(len(self.optionList)-2, typeLabel)
				self.v.set(self.optionList[len(self.optionList)-3])
				self.dropdown.destroy()
				self.dropdown = OptionMenu(self.toolbar, self.v, *self.optionList, command=self.newOptionMenu)
				self.dropdown.configure(bg="light blue")
				self.dropdown.pack(side='left')

				for nodeitem in self.systemsCanvas.find_withtag('node'):
					self.G.node[nodeitem][typeLabel] = 0
					self.systemsCanvas.itemconfig(nodeitem, state='hidden')
				for edgeitem in self.systemsCanvas.find_withtag('edge'):
					self.systemsCanvas.itemconfig(edgeitem, state='hidden')

				# refresh right panel to include new Demand
				self.systemInfo.createNewDemand(typeLabel)
				self.systemInfo.systemDict[typeLabel] = None
				self.systemInfo.saveAttributes()

			
		elif self.v.get() == 'All':
			for nodeitem in self.systemsCanvas.find_withtag('node'):
				self.systemsCanvas.itemconfig(nodeitem, state='normal')
			for edgeitem in self.systemsCanvas.find_withtag('edge'):
				self.systemsCanvas.itemconfig(edgeitem, state='normal')
			
		else:
			for nodeitem in self.systemsCanvas.find_withtag('node'):
				if int(self.G.node[nodeitem][self.v.get()])==0:
					self.systemsCanvas.itemconfig(nodeitem, state='hidden')
				else:
					self.systemsCanvas.itemconfig(nodeitem, state='normal')

			for edgeitem in self.systemsCanvas.find_withtag('edge'):
				if (self.systemsCanvas.itemcget(int(self.systemsCanvas.gettags(edgeitem)[1]), 'state')=='normal') and (self.systemsCanvas.itemcget(int(self.systemsCanvas.gettags(edgeitem)[2]), 'state')=='normal'):
					self.systemsCanvas.itemconfig(edgeitem, state='normal')
				else:
					self.systemsCanvas.itemconfig(edgeitem, state='hidden')
				

			


	def initUI(self):
		# creates toolbar: implemented using a frame with dropdown/buttons placed on it
		#          referenced from http://zetcode.com/gui/tkinter/menustoolbars/
		self.toolbar = Frame(self.parent, bg=self.color)
		self.toolbar.pack()

		#creates systems dropdown menu
		self.optionList = ['All', 'Create New']
		self.v = StringVar()
		self.v.set(self.optionList[len(self.optionList) - 2])

		self.dropdown = OptionMenu(self.toolbar, self.v, *self.optionList, command=self.newOptionMenu)
		self.dropdown.configure(bg=self.color)
		self.dropdown.pack(side='left')

		#creates toolbar buttons, with functionality and binds them to their repsective button click function
		self.createNodeButton = Button(self.toolbar, text="create node", command=self.createNodeButtonClick,
                        highlightbackground=self.color)
		self.createEdgeButton = Button(self.toolbar, text="create edge", command=self.createEdgeButtonClick,
                        highlightbackground=self.color)
		self.selectNodeButton = Button(self.toolbar, text="node select", command=self.selectNodeButtonClick,
                          highlightbackground=self.color)
		self.selectEdgeButton = Button(self.toolbar, text="edge select", command=self.selectEdgeButtonClick, highlightbackground=self.color)
		self.deleteNodeButton = Button(self.toolbar, text='delete node', command=self.deleteNodeButtonClick, highlightbackground=self.color)
		self.deleteEdgeButton = Button(self.toolbar, text='delete edge', command=self.deleteEdgeButtonClick, highlightbackground=self.color)

		self.deleteEdgeButton.pack(side='right')
		self.deleteNodeButton.pack(side='right')
		self.selectEdgeButton.pack(side='right')
		self.selectNodeButton.pack(side='right')
		self.createEdgeButton.pack(side='right')
		self.createNodeButton.pack(side='right')

		#creates canvas 
		self.systemsCanvas = Canvas(self.parent, height=570, width=700, bg='white')
		self.systemsCanvas.pack(fill="both", expand=1)

