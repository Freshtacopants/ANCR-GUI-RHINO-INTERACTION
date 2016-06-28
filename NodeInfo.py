from Tkinter import *
import tkSimpleDialog
import networkx as nx

class NodeInfo(Frame):
	def __init__(self, parent, leftFrame, index, G, systemList):
		Frame.__init__(self, parent)

		self.parent = parent
		self.leftFrame = leftFrame
		self.index = index
		self.G = G
		self.systemDict = {}
		for x in systemList:
			self.systemDict[x] = 0
		for x in self.G.node[self.index]:
			if x not in self.systemDict.keys():
				self.systemDict[x] = 0

		# delete unwanted keys that result from syncing main optionList with Demand
		for x in ['x', 'y', 'z', 'Create New', 'All', 'x_coord', 'y_coord', 'Name', 'Type', 'Notes']:
			try:
				del self.systemDict[x]
 			except KeyError:
 				pass

 		self.color = "dark gray"
		self.initUI()

	def createTypeLabel(self):
		self.typeLabel = Label(self.parent, text="Type:", bg=self.color)
		self.typeLabel.grid(row=2, column=0, padx=5, sticky=E)

		self.typeMenu = Frame(self.parent, highlightbackground=self.color)
		self.typeMenu.grid(row=2, column=1, padx=10)
		self.optionList = ['Hello', 'World']
		self.v = StringVar()
		self.v.set(self.optionList[0])
		self.dropdown = OptionMenu(self.typeMenu, self.v, *self.optionList)
		self.dropdown.config(bg=self.color)
		self.dropdown.grid(row=2, column=1)

		self.createTypeBtn = Button(self.parent, text="Create New", 
			command=self.createNewType, highlightbackground=self.color)
		self.createTypeBtn.grid(row=2, column=2)

	def createNewType(self):
		typeLabel = tkSimpleDialog.askstring(title="New Type", prompt="Enter a new type")

		if typeLabel != None:
			self.optionList.append(typeLabel)
			self.v.set(self.optionList[len(self.optionList)-1])
			self.dropdown.grid_forget()
			self.dropdown = OptionMenu(self.typeMenu, self.v, *self.optionList)
			self.dropdown.configure(bg=self.color)
			self.dropdown.grid(row=2, column=1)

	def createDemandLabel(self):
		# Demand
 		self.demandLabel = Label(self.parent, text="Demand:", bg=self.color)
 		self.demandLabel.grid(row=3, column=0, padx=5, sticky=E)

		self.createDemandBtn = Button(self.parent, text="Create New", 
			command=self.createNewDemand, highlightbackground=self.color)
		self.createDemandBtn.grid(row=3, column=1)

		self.numDemands = 0

		for x in self.systemDict.keys():
			self.createNewDemand(x)

	def createNewDemand(self, label=None):
		# If no label was provided as a parameter, prompt for a label
		if label == None:
			label = tkSimpleDialog.askstring(title="Label", prompt="Enter a Label Name") # Prompt for label
			# If user didn't hit Cancel dialog window, add new key to systemDict
			if label != None: 
				self.systemDict[label] = None

		# If user didn't hit Cancel in dialog window, continue
		if label != None:
			# Create new label and corresponding entry
			self.newDemandLabel = Label(self.parent, text=label, bg=self.color)
			self.newDemandLabel.grid(row=3+self.numDemands, column=1)
			newEntry = Entry(self.parent, highlightbackground=self.color, width=9)
			newEntry.grid(row=3+self.numDemands, column=2, padx=10)
			
			# add the label to NetworkX and initialize its value to None
			for node in self.leftFrame.systemsCanvas.find_withtag('node'):
				if label not in self.G.node[node]:
					self.G.node[node][label] = None
			self.systemDict[label] = newEntry

			# move widgets down to make room for new demand label
			self.createDemandBtn.grid(row=4+self.numDemands, column=1)

			for item in self.parent.grid_slaves():
				if int(item.grid_info()["row"]) > (4 + self.numDemands):
					newRow = int(item.grid_info()["row"]) + self.numDemands + 1
					item.grid_configure(row=newRow)

			self.numDemands += 1

			if label not in self.leftFrame.optionList:
				self.leftFrame.optionList.insert(len(self.leftFrame.optionList)-2, label)
				self.leftFrame.dropdown.destroy()
				self.leftFrame.dropdown = OptionMenu(self.leftFrame.toolbar, self.leftFrame.v, 
					*self.leftFrame.optionList, command=self.leftFrame.newOptionMenu)
				self.leftFrame.dropdown.configure(bg="light blue")
				self.leftFrame.dropdown.pack(side='left')

	def createGeometryLabel(self):
		self.geometryLabel = Label(self.parent, text="Geometry:", bg=self.color)
		self.geometryLabel.grid(row=5, column=0, padx=5, sticky=E)

		self.xLabel = Label(self.parent, text="x", bg=self.color)
		self.xLabel.grid(row=5, column=1, padx=1, pady=1)
		self.xEntry = Entry(self.parent, highlightbackground=self.color, width=9)
		self.xEntry.grid(row=5, column=2)

		self.yLabel = Label(self.parent, text="y", bg=self.color)
		self.yLabel.grid(row=6, column=1, padx=1, pady=1)
		self.yEntry = Entry(self.parent, highlightbackground=self.color, width=9)
		self.yEntry.grid(row=6, column=2)

		self.zLabel = Label(self.parent, text="z", bg=self.color)
		self.zLabel.grid(row=7, column=1, padx=1, pady=1)
		self.zEntry = Entry(self.parent, highlightbackground=self.color, width=9)
		self.zEntry.grid(row=7, column=2)

	def repopulateData(self):
		if 'Name' in self.G.node[self.index] and self.G.node[self.index]['Name'] != None:
			self.nameEntry.delete(0, END)
			self.nameEntry.insert(0, self.G.node[self.index]['Name'])
		if 'Type' in self.G.node[self.index] and self.G.node[self.index]['Type'] != None:
			self.v.set(self.G.node[self.index]['Type'])
		if 'x' in self.G.node[self.index]:
			self.xEntry.delete(0, END)
			self.xEntry.insert(0, self.G.node[self.index]['x'])
		if 'y' in self.G.node[self.index]:
			self.yEntry.delete(0, END)
			self.yEntry.insert(0, self.G.node[self.index]['y'])
		if 'z' in self.G.node[self.index]:
			self.zEntry.delete(0, END)
			self.zEntry.insert(0, self.G.node[self.index]['z'])
		if 'Notes' in self.G.node[self.index]:
			self.notes.delete('0.0', END)
			self.notes.insert('0.0', self.G.node[self.index]['Notes'])
        
		for x in self.systemDict.keys():
			if self.G.node[self.index][x] != None:
				self.systemDict[x].delete(0, END)
				self.systemDict[x].insert(0, self.G.node[self.index][x])

	def updateNodeSizes(self):
		for node in self.leftFrame.systemsCanvas.find_withtag('node'):
			if self.leftFrame.systemsCanvas.itemcget(node, 'state') == 'normal':
				# change sizes of nodes back to normal
				coords = self.leftFrame.systemsCanvas.coords(nodeitem)
				midpointX = (coords[0] + coords[2]) / 2
				midpointY = (coords[1] + coords[3]) / 2
				r = 8
				self.leftFrame.systemsCanvas.coords(nodeitem, midpointX-8, midpointY-8, midpointX+8, midpointY+8)

				# update size of nodes to reflect magnitude of value for this demand
				coords = self.leftFrame.systemsCanvas.coords(node)
				offset = self.G.node[nodeitem][self.leftFrame.v.get()] - self.leftFrame.minDemand
				self.leftFrame.systemsCanvas.coords(node, coords[0]-offset, coords[1]-offset, 
					coords[2]+offset, coords[3]+offset)



	def saveAttributes(self):
		self.G.node[self.index]['Name'] = self.nameEntry.get()
		self.G.node[self.index]['Type'] = self.v.get()
		self.G.node[self.index]['x'] = int(self.xEntry.get())
		self.G.node[self.index]['y'] = int(self.yEntry.get())
		self.G.node[self.index]['z'] = int(self.zEntry.get())
		self.G.node[self.index]['Notes'] = self.notes.get('0.0', END)

		if self.leftFrame.labels == 1:
			self.leftFrame.hideLabels()
			self.leftFrame.showLabels()

		self.updateNodeSizes

		# Demands
		for x in self.systemDict.keys():
			try:
				self.G.node[self.index][x] = int(self.systemDict[x].get())
			except AttributeError:
				pass
			except ValueError:
				pass

	def initUI(self):
		# Name
		self.nameLabel = Label(self.parent, text="Name:", bg=self.color)
		self.nameLabel.grid(row=1, column=0, padx=5, pady=10, sticky=E)

		self.nameEntry = Entry(self.parent, highlightbackground=self.color)
		self.nameEntry.grid(row=1, column=1, columnspan=2, sticky=E+W, padx=10)

		# Notes
		self.notesLabel = Label(self.parent, text="Notes:", bg=self.color)
		self.notesLabel.grid(row=8, column=0, padx=5, sticky=E)
		self.notes = Text(self.parent, height=8, width=23, font='TkDefaultFont')
		self.notes.grid(row=8, column=1, columnspan=2, rowspan=8, pady=5, padx=10)
		
		# save button
		self.saveBtn = Button(self.parent, text="Save", command=self.saveAttributes, 
			highlightbackground=self.color)
		self.saveBtn.grid(row=16, columnspan=3, padx=5)


		# save button
		self.saveBtn = Button(self.parent, text="Save", command=self.saveAttributes, 
			highlightbackground=self.color)
		self.saveBtn.grid(row=16, columnspan=3, padx=5)

		# Type, Demand, Geometry
		self.createTypeLabel()
		self.createGeometryLabel()
		self.createDemandLabel() # create demand last bc placement relies on type and geometry labels

		# if node attributes have been set previously, populate right pane using the existing data
		self.repopulateData()


