# Requirements/Setup
* requires: Python 2.7
* install external modules: networkX, matplotlib, Pillow
* clone github.com/mjsyp/ancr-gui in your preferred working directory
* run main.py from command line/terminal


# System Dropdown
* All: view all nodes and edges created 
* Geometry: view only nodes of type Compartment and the edges that connect them
* Other System: 
* view only nodes that have a value for the demand of this system and the edges that connect them
* edges are shown as directed
* nodes change size based on the magnitude of the value for the demand of this system
* if a node is created while you are in another system, the demand corresponding to the current system will be initialized to 0
* Create New: create a new system, which will also be added as a demand of component nodes with no initialized value


# Toolbar Buttons
* to create a node: press the ‘create node’ button on the toolbar and left-click on the white canvas below the toolbar
* to create an edge: two nodes must have already been created on the canvas and in order to create an edge between them, first press the ‘create edge’ Button and left click on the start node and release at the end node. An edge will only be created between two distinct nodes.
* in order to view and edit the properties of a node or edge, press the ‘select’ button and hover over your desired canvas object. The selected object will be highlighted as green and display its current properties.
* to delete a node or edge press the ‘delete’ button on the toolbar, and hover over the desired canvas object. To delete the object highlighted in green, left click on the object. Deleting a node will removed all associated edges. 
* to drag a node and its associated edges to another location on the canvas, press the ‘drag node’ button on the toolbar and left click and hold on the desired node, which will highlight to green. To drag it to a new location hold down the left key and move the cursor to the node’s new position and release.  


# Menu Bar

### File
* _Open:_ in order to open a previously saved file created through the gui, select open in the menu bar or use the shortcut command (ctrl-O) and a file explorer window will pop up. Select the desired file to open, and the previously saved network will appear on the canvas. 
* _Save:_ pressing save through the menu bar or using shortcut key (ctrl-S) will update the file contents if it was previously named. If a filename was not already established, a file explorer window will pop up and prompt you to save the file’s name and the directory it will be saved in. 
* _Save As:_ pressing save through the menu bar or using shortcut key (ctrl-shift-S) will prompt a file explorer window to pop up, where you will name the file and select where it will be saved. 
* _Exit:_ pressing exit on the menu bar will exit out of the gui. Note: it will not automatically save your file, all contents not previously saved will be lost.  

### Edit
* _Undo:_ Undoes last canvas item action (node/edge creation or deletion)
* _Redo:_ Redoes last undo action
	
### View
	*Show Labels: Will display name labels of nodes above them 
	*Hide Labels: Will hide name labels of nodes
	
### Window
* _Log Window:_ Will create a docked window of gui log actions if it had been exited
* _Component Geometry:_ will display a pop up window with an interactive 3d scatterplot of the component node geometries. 
* _Compartment Geometry:_ will display a pop up window with an interactive 3D plot of compartment node geometries (x, y, z, edge-length), made up of voxels. In this window you can toggle between seeing each individual voxel that makes up each compartment by selecting show intersection lines or you can remove these lines by unchecking show intersection lines. 


### Analysis
* _Node Degrees:_ will create a docked window of a histogram plot of the node degrees (frequency vs degree)



# Node Properties
* when you select a node, you can edit its attributes on the right frame of the GUI
* you must click Save before selecting another node/edge or the user input will be lost

	### All Nodes
	* _Name_
	* _Type_ (either Component or Compartment)
	* _Notes_

	### Component Nodes
	* Demands:
		* _Create New_ Button: new demands can be added to each node with this button. The demand will also be added to the dropdown of systems in the canvas toolbar
		* _Geometry_ (x, y, z)

	### Compartment Nodes
	* _Geometry_ (x, y, z, edge length):
		* _Add Row_ Button: multiple rows can be added in order to create a more complex compartment shape
		* _Show Geometry_ Button: the shape of the compartment and the components within it can be viewed in a 3-D matplotlib plot
		* _Delete:_ rows can be deleted by clicking on the number label for the row


# Edge Properties
* when you select a node, you can edit some of its attributes on the right frame of the GUI
* you must click Save before selecting another node/edge or the user input will be lost

	### All Edges:
	* _Name_
	* _Type:_
		* automatically changes based on node connections
		* Adjacency for compartment-compartment
		* Residency for compartment-component
		* Supply/Demand for component-component
	* _Notes_


# Docked Windows
Windows that can be docked include: log window, node degrees, sub-network
* Log window is initialized as already being docked. However if it is exited you can view it again through menu bar>windows>log window. 
* Node degrees can be docked by going to menu bar>analysis>node degrees. Pressing node degrees again will update the docked window if more objects were created on the canvas. 
* Sub-Network is automatically docked whenever you select a compartment node. It represents a network of the multiple voxels making up that compartment. Edges represent adjacency. 
Each docked window will originally be placed in the frame underneath the canvas. Each includes exit, minimize, and maximize buttons. Exit will destroy the current window. Maximize will destroy the docked window and create a larger pop up window instead which can be resized and moved. Minimizing while the window is docked will configure it into just its toolbar. Minimizing while the window is a pop up will destroy the pop up and dock the window like it originally was. 