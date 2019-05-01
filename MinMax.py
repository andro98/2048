from main import *
# score l kol node
  nodescores=[0 for x in range (50000)]


 childlist=[[0 for x in range (0)]for y in range (50000)]

 nodeNumber = 1
 directions=[100,101,102,103]
 #check if move is possible


 def createMiniMaxT(depth):
     global nodescores
     global childlist
     global alphaBetaScore
     global nodeNumber
     nodeScores = [0 for x in range(50000)]
     childList = [[0 for x in range(0)] for y in range(50000)]
     nodeNumber = 1


    alphaBetaPruning(1, currentGrid, 0, depth, -math.inf, math.inf)

def alphaBetaPruning(node,grid,parent,depth,alpha,beta):
    global nodeScores
    global childList
    global nodeNumber
    #l state l hy2of 3ndaha
    if depth==0 :
      nodescores[node]=getScore(grid)
      return nodescores[node]
    #making new node for every possible node
    if depth%2==0:
        for i in range(4):
            nodeNumber+=1
            childlist[node].append(nodeNumber)
            if(movepossible(grid,directions[i]))==true:
                alpha=


