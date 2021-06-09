import tkinter as tk
import math


class NodePlacementError(Exception):
    pass


class Node:
    MOVEMENT_COST = 1

    def __init__(self, canvas, x1, y1, x2, y2, row, col):
        # visual data
        self.rect = canvas.create_rectangle(
            x1, y1, x2, y2, fill="blue", tags="node")
        # positional data
        self.position = [row, col]
        # data related to algorithm
        self.f_cost = 0
        self.g_cost = 0
        self.h_cost = 0
        self.parentNode = None
        self.traversable = True

    def setColour(self, colour, canvas):
        canvas.itemconfig(self.rect, fill=colour)

    def getPosition(self):
        return self.position

    def getGCost(self):
        return self.g_cost

    def getHCost(self):
        return self.h_cost

    def getFCost(self):
        return self.f_cost

    def getParent(self):
        return self.parentNode

    def isTraversable(self):
        return self.traversable

    def setTraversability(self, t):
        self.traversable = t

    def setParent(self, p):
        self.parentNode = p

    def setHCost(self, endNode):
        row_diff = abs(endNode.getPosition()[0]-self.getPosition()[0])
        col_diff = abs(endNode.getPosition()[1]-self.getPosition()[1])
        if row_diff <= col_diff:
            self.h_cost = self.MOVEMENT_COST*row_diff + \
                self.MOVEMENT_COST*(col_diff-row_diff)
        else:
            self.h_cost = self.MOVEMENT_COST*col_diff + \
                self.MOVEMENT_COST*(row_diff-col_diff)

    def setGCost(self):
        self.g_cost += self.MOVEMENT_COST

    def checkGCost(self, neighborNode):
        if not(neighborNode.getPosition()[0] == self.getPosition()[0] or neighborNode.getPosition()[1] == self.getPosition()[1]):
            return self.g_cost + self.MOVEMENT_COST
        else:
            return self.g_cost + self.MOVEMENT_COST

    def setFCost(self, endNode):
        self.setGCost()
        self.setHCost(endNode)
        self.f_cost = self.g_cost + self.h_cost


class UserConfigWindow(object):
    def __init__(self, master):
        top = self.top = tk.Toplevel(master)
        top.geometry("320x230")
        # Add styles
        top.title('Path Finder Visualiser')
        self.gridSize = 0
        self.startX = 0
        self.startY = 35
        self.endX = 0
        self.endY = 0
        self.l1 = tk.Label(
            top, text=" Select Building Location From The Options Below: ")
        self.l1.place(x=0, y=0)
        self.l2 = tk.Label(top, text="Choose Start Location")
        self.l2.place(x=40, y=50)

        # initialize data
        self.places = ('MARRIOT HOTEL', 'BARNES HALL', 'IC1 (INNOVATION CENTRE)',
                       'LINDSAY HALL', 'STUDENTS UNION', 'TAWNEY', 'CENTRE (CICC)', 'VET SCHOOL', 'THE COVERT', 'JACK ASHLEY')
        # set up variable for 1st option
        self.option_var = tk.StringVar(top, self.places[0])
        self.e2 = tk.OptionMenu(
            self.top,
            self.option_var,
            *self.places)
        self.e2.pack()
        self.e2.place(x=50, y=75)
        self.l3 = tk.Label(top, text="Choose End Location")
        self.l3.place(x=40, y=105)
        # set up variable for 2nd option
        self.option_var2 = tk.StringVar(top, self.places[2])
        self.e4 = tk.OptionMenu(
            self.top,
            self.option_var2,
            *self.places)
        self.e4.pack()
        self.e4.place(x=50, y=125)
        self.b = tk.Button(top, text='Enter', command=self.setVals)
        self.b.place(x=75, y=160)
        self.c = tk.Button(top, text='Exit', command=self.endProgam)
        self.c.place(x=150, y=160)
        self.errorMsg = tk.StringVar()
        self.l4 = tk.Label(top, textvariable=self.errorMsg)
        self.l4.place(x=0, y=175)

    def endProgam(self):
        self.top.destroy()

    def setVals(self):
        try:
            self.gridSize = 20
            # set path nodes for each place (see self.places on line 102)
            self.pathlibrary = {
                0: [20, 20],
                1: [20, 13],
                2: [10, 15],
                3: [1, 4],
                4: [6, 11],
                5: [8, 9],
                6: [3, 20],
                7: [10, 19],
                8: [20, 5],
                9: [13, 7]
            }
            # loop through nodes and set start index with end index
            for p in range(10):
                if (self.option_var.get() == self.places[p]):
                    self.startX = self.pathlibrary[p][0] - 1
                    self.startY = self.pathlibrary[p][1] - 1
                if (self.option_var2.get() == self.places[p]):
                    self.endX = self.pathlibrary[p][0] - 1
                    self.endY = self.pathlibrary[p][1] - 1

            # make sure chosen values are not the same
            if (self.option_var.get() == self.option_var2.get()):
                raise NodePlacementError
            self.top.destroy()
        # error handling
        except NodePlacementError:
            # except Exception:
            self.errorMsg.set(
                "Start Location Cannot Be Equel To End Location!")

    def getVals(self):
        return [self.gridSize, self.startX, self.startY, self.endX, self.endY]


class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        userConfig = self.openUserConfigWindow()
        self.startX = userConfig[1]
        self.startY = userConfig[2]
        self.endX = userConfig[3]
        self.endY = userConfig[4]

        # set dimensions of window
        self.gridSize = 20
        self.cellwidth = 25
        self.cellheight = 25
        self.width = self.gridSize*self.cellwidth
        self.height = (self.gridSize*self.cellheight) + 50
        self.canvas = tk.Canvas(
            self, width=self.width, height=self.height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")

        # create grid of Nodes with user dimensions
        self.node = [[0 for x in range(self.gridSize)]
                     for y in range(self.gridSize)]
        for column in range(self.gridSize):
            for row in range(self.gridSize):
                x1 = column*self.cellwidth
                y1 = row * self.cellheight
                x2 = x1 + self.cellwidth
                y2 = y1 + self.cellheight
                self.node[row][column] = Node(
                    self.canvas, x1, y1, x2, y2, row, column)

        # highlight start and end points
        self.node[self.startY][self.startX].setColour('yellow', self.canvas)
        self.node[self.endY][self.endX].setColour('yellow', self.canvas)

        # set blocked paths
        # set path nodes for each blocked cell on map load
        self.blockedpath = {0: [[0, 20]], 2: [[1, 19]], 4: [[
            1, 19]], 7: [[1, 7], [8, 12], [13, 19]], 8: [[1, 7]],
            9: [[1, 7], [8, 12], [13, 19]], 10: [[13, 19]], 12: [[13, 19]],
            12: [[1, 7], [8, 12]], 13: [[1, 7], [8, 12]], 14: [[13, 19]],
            15: [[1, 3], [4, 7], [8, 12], [13, 19]], 16: [[1, 3], [4, 7], [8, 12], [13, 19]],
            17: [[1, 3], [4, 7], [8, 12], [13, 19]], 18: [[1, 3]]}
        for k, v in self.blockedpath.items():
            for l in range(len(v)):
                for p in range(v[l][0], v[l][1]):
                    self.node[k][p].setColour('grey', self.canvas)
                    self.node[k][p].setTraversability(False)

        # create buttons to start algorithm or reset
        self.b1 = tk.Button(self, text='Start', command=lambda: self.aStar(
            self.node, self.node[self.startY][self.startX], self.node[self.endY][self.endX]))
        self.b1.place(x=10, y=self.height-40)
        self.b2 = tk.Button(self, text='Reset', command=self.reset)
        self.b2.place(x=65, y=self.height-40)
        self.b3 = tk.Button(self, text='Exit Program', command=self.endProgam)
        self.b3.place(x=125, y=self.height-40)
        self.canvas.tag_bind('node', '<Button-1>', self.setNodeTrav)

    def reset(self):
        self.destroy()
        self.__init__()

    def endProgam(self):
        self.destroy()

    # refresh the grid
    def refreshGrid(self):
        for column in range(self.gridSize):
            for row in range(self.gridSize):
                if (column == self.startX and row == self.startY) or (column == self.endX and row == self.startY):
                    self.node[row][column].setColour('red', self.canvas)
                if self.node[row][column].isTraversable() == True:
                    self.node[row][column].setColour('blue', self.canvas)
                if self.node[row][column].isTraversable() == False:
                    self.node[row][column].setColour('grey', self.canvas)

    def openUserConfigWindow(self):
        # minimize main window on load
        self.iconify()
        # popup window to initialize user configuration
        config = UserConfigWindow(self.master)
        self.wait_window(config.top)
        self.deiconify()
        return config.getVals()

    def setNodeTrav(self, event):
        col = math.floor(event.x/self.cellwidth)
        row = math.floor(event.y/self.cellheight)
        if not((col == self.startX and row == self.startY) or (col == self.endX and row == self.endY)):
            if self.node[row][col].isTraversable() == True:
                self.node[row][col].setTraversability(False)
                self.node[row][col].setColour('grey', self.canvas)
            else:
                self.node[row][col].setTraversability(True)
                self.node[row][col].setColour('blue', self.canvas)

    def aStar(self, nodes, startNode, endNode):
        # refresh grid
        self.refreshGrid()

        open = [startNode]
        closed = []
        current = None

        while not(current == endNode):
            current = self.getLowestFCost(open)
            open.remove(current)
            closed.append(current)

            neighborLocs = self.getNodeNeighbors(current)
            for coord in neighborLocs:
                # neighbor g cost vs updated neighbor g cost
                oldPath = nodes[coord[0]][coord[1]].getGCost()
                newPath = nodes[coord[0]][coord[1]].checkGCost(current)
                if nodes[coord[0]][coord[1]].isTraversable() == False or nodes[coord[0]][coord[1]] in closed:
                    continue
                elif newPath < oldPath or not(nodes[coord[0]][coord[1]] in open):
                    nodes[coord[0]][coord[1]].setColour('green', self.canvas)
                    nodes[coord[0]][coord[1]].setParent(current)
                    nodes[coord[0]][coord[1]].setFCost(endNode)
                    if not(nodes[coord[0]][coord[1]] in open):
                        open.append(nodes[coord[0]][coord[1]])

        # visualize the path
        pathNode = current
        while not(pathNode is None):
            pathNode.setColour('red', self.canvas)
            pathNode = pathNode.getParent()

        return current

    def getNodeNeighbors(self, node):
        row = node.getPosition()[0]
        col = node.getPosition()[1]
        neighborsRough = [[row, col-1], [row-1, col-1], [row-1, col], [row-1,
                                                                       col+1], [row, col+1], [row+1, col+1], [row+1, col], [row+1, col-1]]
        neighborsNew = []
        for x in range(8):
            if (0 <= neighborsRough[x][0] < self.gridSize and 0 <= neighborsRough[x][1] < self.gridSize):
                neighborsNew.append(neighborsRough[x])
        return neighborsNew

    def getLowestFCost(self, nodes):
        def fCostofIndex(elem):
            return elem.getFCost()

        nodes.sort(key=fCostofIndex)
        # check for empty nodes, stop tkinter and raise an error if no possible path
        if(len(nodes) == 0):
            self.destroy()
            raise ValueError('No Possible Route To Take! Rerun Application!')
        return nodes[0]


if __name__ == "__main__":
    app = App()
    app.mainloop()
