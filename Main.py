import pygame
from roughColorSupport import WHITE, GREY, BLACK, ORANGE, GREEN, TURQUOISE, RED, YELLOW, PINK
import pprint

pygame.init()

WIDTH = 800 # total width of our screen
ROWS = 50 #Rows = Cols, Total number of rows in our grid
screen = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("A* PathFinder")

icon = pygame.image.load("A.png")
pygame.display.set_icon(icon)

running = True

class Node: # this class will contain all the information required for each node
    def __init__(self, NodeRow, NodeCol, NodeWidth, ROWS, WIDTH): # NodeRow means which row the node is located, and col is which NodeCol the node is located, NodeWidth is the width of an individual node
        self.NodeRow = NodeRow
        self.NodeCol = NodeCol
        self.NodeWidth = NodeWidth
        self.color = WHITE # what color is each node
        self.ROWS = ROWS
        self.WIDTH = WIDTH
        self.neighbors = []
        self.Mark = False
        self.GScore = float("inf")
        self.FScore = float("inf")

    def IsBarrier(self): #Checking if the node is a barrier
        return self.color == BLACK

    def IsOpen(self): #Checking if the node is empty
        return self.color == WHITE
    
    def IsStart(self): #Checking if it is the starting node
        return self.color == ORANGE

    def IsCheck(self): #Checking if the node is checked(all neighbors of the checked node will be checked)
        return self.color == GREEN
    
    def IsEnd(self): #Checking if it is the ending node
        return self.color == TURQUOISE

    def IsFocus(self): #Checking if a path can be formed by this node
        return self.color == RED

    def IsPath(self):
        return self.color == YELLOW

    def drawNode(self, screen): #Drawing the nodes in the grid
        pygame.draw.rect(screen, self.color, (self.NodeCol*NodeWidth, self.NodeRow*NodeWidth, self.NodeWidth, self.NodeWidth))

    def EmptyNode(self): #This function is to empty the node, i.e making the color of the node white
        self.color = WHITE

    def StartNode(self): # This function is to make this particular node the start node, i.e, making it orange
        self.color = ORANGE

    def EndNode(self): # this function is to make this particular node the end node, i.e, making it turquoise
        self.color = TURQUOISE

    def CheckNode(self): #Make the nodes scores(G, H, F) checked
        self.color = GREEN

    def BarrierNode(self): # Make this node a barrier
        self.color = BLACK

    def FocusNode(self):
        self.color = RED

    def PathNode(self): #This is the path node
        self.color = YELLOW

    def UpdateNeighbours(self, grid):
        self.neighbors = []
        if self.NodeRow < self.ROWS - 1 and not grid[self.NodeRow + 1][self.NodeCol].IsBarrier() and not grid[self.NodeRow + 1][self.NodeCol].IsStart(): #Checking the down neighbour
            self.neighbors.append(grid[self.NodeRow + 1][self.NodeCol])
        
        if self.NodeRow > 0 and not grid[self.NodeRow - 1][self.NodeCol].IsBarrier() and not grid[self.NodeRow - 1][self.NodeCol].IsStart(): #Checking the up neighbour
            self.neighbors.append(grid[self.NodeRow - 1][self.NodeCol])

        if self.NodeCol < self.ROWS - 1 and not grid[self.NodeRow][self.NodeCol + 1].IsBarrier() and not grid[self.NodeRow][self.NodeCol + 1].IsStart(): #Checking the right neighbour
            self.neighbors.append(grid[self.NodeRow][self.NodeCol + 1])
        
        if self.NodeCol > 0 and not grid[self.NodeRow][self.NodeCol - 1].IsBarrier() and not grid[self.NodeRow][self.NodeCol - 1].IsStart(): #Checking the left neighbour
            self.neighbors.append(grid[self.NodeRow][self.NodeCol - 1])


    def RowPos_ColPos(self): # This function is to print the row and col position of a node
        print("RowPos: ", self.NodeRow)
        print("ColPos:", self.NodeCol)

    def Pos(self): # This function returns the row and col of the node as a list
        return [self.NodeRow, self.NodeCol]

    def ReturnNeighbors(self): # Returns a list of neighbors
        return self.neighbors

    def SetGScore(self, val):
        self.GScore = val

    def SetFScore(self, HScore):
        self.FScore = self.GScore + HScore

    def ReceiveGScore(self):
        return self.GScore
    
    def ReceiveFScore(self):
        return self.FScore

    def heuristic(self, pos1, pos2):
        x, y = pos1
        a, b = pos2
        return abs(x-a) + abs(y-b)


def FinalPath(grid, PathFinder): #Draws the final path
    for FinalNode in PathFinder:
        x, y = FinalNode
        grid[x][y].PathNode()


def algorithm(grid, start, end):
    start.SetGScore(0) # distance to the start node
    start.SetFScore(start.heuristic(start.Pos(), end.Pos())) #Approximate distance to the end node
    Path = [] #the nodes which turned green
    FocusNodeList = {start:True}
    FocusNode = start
    shortList = []
    cameFrom = {}
    count = 0
    LeaveTheLoop = False #This will be true if the neighbor node is the end node 
    exit = False
    while not exit:
        print("neigh:", FocusNode.Pos(), "F:", FocusNode.ReceiveFScore(), "G:", FocusNode.ReceiveGScore())
        MiniLoop = 0
        for neighbor in FocusNode.ReturnNeighbors():
            if neighbor.IsFocus():
                continue
            if MiniLoop == 0:
                RawFScore = neighbor
            if neighbor.IsEnd():
                LeaveTheLoop = True
            if neighbor.ReceiveGScore() > FocusNode.ReceiveGScore()+1:
                neighbor.SetGScore(FocusNode.ReceiveGScore()+1)
                neighbor.SetFScore(neighbor.heuristic(neighbor.Pos(), end.Pos()))
            # if RawFScore.ReceiveFScore()
            if RawFScore.ReceiveFScore() >= neighbor.ReceiveFScore():
                RawFScore = neighbor
            # print ("-->")
            # print(neighbor.Pos(), "F:", neighbor.ReceiveFScore(), "G:", neighbor.ReceiveGScore())
            MiniLoop += 1
            if not neighbor.FocusNode():
                neighbor.CheckNode()
            # List = list(filter(lambda x: x.ReceiveFScore() == neighbor.Pos(), Path))
            # if len(List) == 0:
            if neighbor.Pos() not in shortList:
                Path.append(neighbor)
                shortList.append(neighbor.Pos())
                cameFrom[str(neighbor.Pos())] = FocusNode.Pos()

        MinVal = min(Path, key=lambda x: x.ReceiveFScore()) 
        MinFList = list(filter(lambda x: x.ReceiveFScore() == MinVal.ReceiveFScore(), Path)) #MinFList is a list with the lowest F-scores
        MinVal = min(MinFList, key=lambda x: x.heuristic(x.Pos(), end.Pos())) 
        MinHList = list(filter(lambda x: x.heuristic(x.Pos(), end.Pos()) == MinVal.heuristic(MinVal.Pos(), end.Pos()), MinFList))
        FocusNode = MinHList[0]
        print("FocusNode:", FocusNode.Pos(), "FScore:", FocusNode.ReceiveFScore(), "HScore:", FocusNode.heuristic(FocusNode.Pos(), end.Pos()))
        Path.remove(FocusNode)
        shortList.remove(FocusNode.Pos())
        FocusNode.FocusNode()

        print ("-->")
        for i in Path:
            print(i.Pos(), "FScore:", i.ReceiveFScore(), "HScore:", i.heuristic(i.Pos(), end.Pos()))
        
        
        count += 1
        print("Count:", count)
        if end in FocusNode.ReturnNeighbors():
            cameFrom[str(end.Pos())] = FocusNode.Pos()
            exit = True
            break
        
    # for i in cameFrom:
    #     print(i)
    pprint.pprint(cameFrom)
    print("Start:", start.Pos())
    print("End:", end.Pos())

    PathFinder = []

    x = end.Pos()
    while x != start.Pos():
        if x != end.Pos():
            PathFinder.append(x)
        print(x,"->")
        x = cameFrom.get(str(x))

    FinalPath(grid, PathFinder)


def get_clicked_pos(pos, rows, width):
    # print(pos) # This prints the position of the mouse clicked on the game screen
    x, y = pos # x = x-axis of pos, y = y-axis of pos
    NodeRow = y // 16 # NodeRow is the row number of the clicked node
    NodeCol = x // 16 # NodeCol is the col number of the clicked node
    # print("NodeRow:", NodeRow, "  NodeCol:", NodeCol)

    return NodeRow, NodeCol

def MakingGrid():
    Grid = []
    NodeWidth = WIDTH // ROWS # NodeWidth is the width of an individual node
    for i in range(ROWS):
        Grid.append([]) # grid is basically a list of lists, where each list consists information of each row of nodes
        for j in range(ROWS):
            spot = Node(i, j, NodeWidth, ROWS, WIDTH)
            Grid[i].append(spot)

    # DrawingGrid(NodeWidth, Grid)
    return Grid


def DrawingGrid(NodeWidth): #Drawing the entire grid
    #Each square is considered as a node
    for i in range(ROWS):
        pygame.draw.line(screen, GREY, (0, i * NodeWidth), (WIDTH, i * NodeWidth)) 
        for j in range(ROWS):
            pygame.draw.line(screen, GREY, (j * NodeWidth, 0), (j *  NodeWidth, WIDTH))


def Draw(NodeWidth):
    for row in grid: 
        for spot in row:
            spot.drawNode(screen)

    # pygame.draw.rect(screen, TURQUOISE, (0, 0, NodeWidth, NodeWidth))
            
    DrawingGrid(NodeWidth)
    pygame.display.update()

grid = None
start = None   # Start node before the game started
end = None     # End node before the game started

grid = MakingGrid()

while running:
    NodeWidth = WIDTH // ROWS
    Draw(NodeWidth)
    screen.fill(WHITE) # this gives a background of the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # Click the X button to exit the game
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN: # If there is a mouse input 
            if pygame.mouse.get_pressed()[0]: # single finger click
                pos = pygame.mouse.get_pos() # pos contains x-axis and y-axis of the mouse clicked on the game screen
                NodeRow, NodeCol = get_clicked_pos(pos, ROWS, WIDTH)
            
                spot = grid[NodeRow][NodeCol]

                if spot.IsOpen():

                    if not start: # If there is no start node
                        start = spot
                        start.StartNode()

                    elif not end: # If there is no end node
                        end = spot
                        end.EndNode()

                    else:
                        spot.BarrierNode()


            elif pygame.mouse.get_pressed()[2]: # double finger click
                pos = pygame.mouse.get_pos() # pos contains x-axis and y-axis of the mouse clicked on the game screen
                NodeRow, NodeCol = get_clicked_pos(pos, ROWS, WIDTH)
                spot = grid[NodeRow][NodeCol]

                if spot.IsStart():
                    start = None
                if spot.IsEnd():
                    end = None
                spot.EmptyNode()
            

        if event.type==pygame.KEYDOWN: # Detecting keyboard 
            if event.key==pygame.K_RETURN: # checks if return/enter is clicked
                for row in grid: 
                    for spot in row:
                        spot.EmptyNode() # Empties out all the nodes in the screen (i.e, Clears the enitre board)
                start = None
                end = None

            if event.key == pygame.K_SPACE and start and end: #If space is pressed, and there is a start and end, THE algorithm will take place
                for row in grid: 
                    for spot in row:
                        spot.UpdateNeighbours(grid)  
                
                algorithm(grid, start, end)

    # pygame.display.update() # Update the info, to display on the screen