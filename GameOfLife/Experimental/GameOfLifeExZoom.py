import pygame
import random
import os.path
import inspect
import threading
import time
import sys
from collections import deque #C based Queue


########################### RULES ##################################################################
# 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.             #
# 2. Any live cell with two or three live neighbours lives on to the next generation.              #
# 3. Any live cell with more than three live neighbours dies, as if by overpopulation.             #
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.  #
####################################################################################################

#5. Age of Cells :
    #The oldest cells in every 10th generation die and split into the same amout of cells as the number of neighbours they have
    #


####################################################################################################
class Cell:
   
    allCellsMap={}    #(x,y) ->self
    generationsQueue = deque()
    #currentGeneration=0
    currentGenerationList=[]
    lifeExpectancy=10
    
    size=3    #zoom
    scale=1   #for later use in zooming.. maybe
    
    ADJACENCY_DISTANCE=1  #maybe increment it for fun  ,   = cell field of view
    
    #####COOL:
    #-ADJACENCY_DISTANCE=3   - start with a line of 4 cells   
    ####
    
    aliveCount=0
    deadCount=0
    
    CURRENT_EPOCH_COLOR=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    
    def __init__(self, posX, posY, alive):
              
        self.alive=alive
        self.posX=posX
        self.posY=posY
        self.color = Cell.CURRENT_EPOCH_COLOR
        self.age=0
        
        Cell.allCellsMap[(self.posX,self.posY)]= self
                       
        if(self.alive):
            Cell.aliveCount+=1
        else:
            Cell.deadCount+=1
            
        self.status=0  #number of alive neighbours     
        self.checkStatus()
               
    def delete(self):
        Cell.allCellsMap.pop((self.posX,self.posY))
        del self

    @classmethod    
    def exist(Cell, x , y):
       
        existence={"exist" : False,
                   "alive" : False,
                   "self" : None                   
                   }
              
        if (x,y) in Cell.allCellsMap.keys():     
            existence["exist"] = True
            existence["alive"]=Cell.allCellsMap[(x,y)].alive
            existence["self"]= Cell.allCellsMap[x,y]
                   
        return existence
             
    def checkStatus(self):
       
        aliveNumber=0
        for dx in range(-Cell.ADJACENCY_DISTANCE*Cell.size, (Cell.ADJACENCY_DISTANCE+1)*Cell.size, Cell.size):
            for dy in range(-Cell.ADJACENCY_DISTANCE*Cell.size, (Cell.ADJACENCY_DISTANCE+1)*Cell.size, Cell.size):
               
                if(dx != 0 or dy!=0):
                    exist = Cell.exist(self.posX+dx,self.posY+dy)
                                     
                    if(self.alive and not exist["exist"]):  #adj cell not exist (and is alive or not alive)
                        Cell(self.posX+dx,self.posY+dy, False)  
                                               
                    if(exist["exist"] and exist["alive"]):  #adj exist and is alive                         
                        aliveNumber+=1 
        
        self.status=aliveNumber
    
    @classmethod 
    def lifeCycle(Cell):
            #print("-lifecycle-")
            generation=[]
            spawned=[]
            split=[]
            aliveInGeneration=0
            genAge=0
            while(aliveInGeneration==0):
                if(Cell.generationsQueue):
                    genAge= len(Cell.generationsQueue)
                    
                    generation = Cell.generationsQueue.popleft()
                    
                    #print(generation)
                    for cell in generation:
                        if(cell.alive):
                            #print(str(cell.age), end="")
                            if(cell.age>=genAge):# and cell.age>=Cell.lifeExpectancy):
                                #print(": split", end="")
                                aliveInGeneration+=1
                                spawned.extend(cell.split()) 
                                split.append(cell)
                            #print()                                
                else:
                    break
            if(spawned):
                Cell.currentGenerationList.extend(spawned)
                
            for cell in split:
                cell.alive=False
                cell.age=0
                Cell.aliveCount-=1
                Cell.deadCount+=1
            
               
    def split(self):
        dead=[]
        for dx in range(-Cell.ADJACENCY_DISTANCE*Cell.size, (Cell.ADJACENCY_DISTANCE+1)*Cell.size, Cell.size):
            for dy in range(-Cell.ADJACENCY_DISTANCE*Cell.size, (Cell.ADJACENCY_DISTANCE+1)*Cell.size, Cell.size):               
                if(dx != 0 or dy!=0):
                    exist = Cell.exist(self.posX+dx,self.posY+dy)
                    if(exist["exist"] and not exist["alive"]):
                        dead.append(exist["self"])
                         
        spawned=[]        
        for deadCell in dead:
            deadCell.alive = True
            deadCell.age=0
            Cell.aliveCount+=1
            Cell.deadCount-=1
            spawned.append(deadCell)
   
      
        return spawned
            
             
def zoom0(newSize, focusX, focusY):
    if(newSize>0 and newSize<=15):
        #print("NEWSIZE: "+str(newSize))
            
        newMap = {}  ###preallocate size = Cell.allCellsMap size ???

        for key in Cell.allCellsMap.keys():
            cell=Cell.allCellsMap[key]
           
            
            cell.posX= (cell.posX//Cell.size)*newSize +((focusX)//Cell.size)*newSize        
            cell.posY= (cell.posY//Cell.size)*newSize +((focusY)//Cell.size)*newSize
       
        
            newMap[cell.posX,cell.posY]= cell  #remap (x,y)->cell
            
        Cell.allCellsMap=newMap
        
        Cell.size= newSize


def zoom(newSize, focusX , focusY):
    if(newSize>0 and newSize<=15):
        #print("NEWSIZE: "+str(newSize))
            
        newMap = {}  ###preallocate size = Cell.allCellsMap size ???

        for key in Cell.allCellsMap.keys():
            cell=Cell.allCellsMap[key]
            
            dfx=((cell.posX//Cell.size)-(focusX//Cell.size) )
            dfy=((cell.posY//Cell.size)-(focusY//Cell.size))
                    
            cell.posX= focusX+dfx*newSize
            cell.posY= focusY+dfy*newSize
                
            newMap[cell.posX,cell.posY]= cell  #remap (x,y)->cell
            
        Cell.allCellsMap=newMap
        
        Cell.size= newSize                     
                             
def moveView(mousePositions):

    if(len(mousePositions)>1):
        #first=mousePositions[0]
        first = (screenSizeX//2,screenSizeY//2)
        last= mousePositions[len(mousePositions)-1]
        
        dx =  -(last[0]-first[0])//Cell.size
        dy = -(last[1]-first[1])//Cell.size
        
        newMap = {}  ###preallocate size = Cell.allCellsMap size ???

        for key in Cell.allCellsMap.keys():
            cell=Cell.allCellsMap[key]
            
            cell.posX+=dx*Cell.size
            cell.posY+=dy*Cell.size       
            newMap[cell.posX,cell.posY]= cell  #remap (x,y)->cell
            
        Cell.allCellsMap=newMap
            
 
 
##############################################################
pygame.init()
pygame.font.init()

screenSizeX=1600
screenSizeY=1000

##Camera
viewFocusX=screenSizeX/2
viewFocusY=screenSizeY/2

maxCellsX=screenSizeX/Cell.size
maxCellsY=screenSizeY/Cell.size

epochTime=1000
epochIncrement=50
currentTime=0
EPOCH_TIME_MIN=50
EPOCH_TIME_MAX=60000
delay=15

screen = pygame.display.set_mode((screenSizeX, screenSizeY), 0)
WHITE = (255,255,255)
mouseDrawingPositions=[]

playerSpawns=False
drawing = False

epochCounter=0

maxExecTime =0
lastGenBorn=0
genDiffs=0
genDiff=0

zoomingMode=False
movingMode=False
drawingMode=False

    
while(True):
                
    screen.fill(0)
    
    epochStart = time.time()
    if(currentTime>=epochTime):
        if(epochCounter>0):
            epochCounter+=1
        
        
        currentTime=0
        print("*** EPOCH:"+str(epochCounter)+" ***   ", end="")
        
        
        Cell.CURRENT_EPOCH_COLOR=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
        
        #player spawning   
        if(playerSpawns):
            if(epochCounter==0):  #first generation
                epochCounter+=1
             
            for position in mouseDrawingPositions: 
                exist = Cell.exist(position[0],position[1])
                if(exist["exist"] and not exist["alive"]):
                    Cell.deadCount-=1
                    exist["self"].delete()
                exist = Cell.exist(position[0],position[1])                    
                if(not(exist["alive"])):
                    Cell.currentGenerationList.append(Cell(position[0],position[1],True))
                
                    
            mouseDrawingPositions.clear()
            playerSpawns=False
    
    
        flippingCells = []
        uselessCells = []
        
        totalStatusTime=0
        
        ##check status
        for key in list(Cell.allCellsMap.keys()):
            cell=Cell.allCellsMap[key]
            start = time.time()
            cell.checkStatus()
            end = (time.time() - start)*1000
            totalStatusTime+=end
        
        #apply status changes        
        for key in (Cell.allCellsMap.keys()):
            cell=Cell.allCellsMap[key]   
            
            #alive->dead            
            if(cell.alive and (cell.status<2 or cell.status>3)):
                cell.alive=False
                Cell.aliveCount-=1
                Cell.deadCount+=1
                cell.age=0
        
            ##dead->alive
            elif((not cell.alive) and cell.status==3):
                cell.alive=True
                Cell.aliveCount+=1
                Cell.deadCount-=1
                Cell.currentGenerationList.append(cell)
                cell.age=0
           
            
            #dead->useless        
            elif((not cell.alive) and cell.status==0):
                Cell.deadCount-=1
                uselessCells.append(cell)
             
            #survived             
            elif(cell.alive):
                #Cell.currentGenerationList.append(cell)
                cell.age+=1
                     
                     
         #useless-->cancelled
        for useless in uselessCells:
            useless.delete()       
                
        uselessCells.clear()
        
        #Life Cycle
        if(epochCounter!=0 and epochCounter%Cell.lifeExpectancy==0):
            Cell.lifeCycle()
            genDiff=genDiffs
            genDiffs=0
            
      
        print("BORN="+str(len(Cell.currentGenerationList)), end="")
        bornDiff= len(Cell.currentGenerationList)-lastGenBorn
        genDiffs+=bornDiff
        print(" BORN-DIFF"+str(Cell.lifeExpectancy)+"="+str(genDiff), end="")
        
        
        #save generation state
        lastGenBorn=len(Cell.currentGenerationList)      
        if(Cell.currentGenerationList):
            Cell.generationsQueue.append(Cell.currentGenerationList.copy())
            Cell.currentGenerationList.clear()
        
        nGenerationsAlive=0
        for gen in Cell.generationsQueue:
            if(gen):
                nGenerationsAlive+=1
       
         
        epochEnd = (time.time() - epochStart)*1000  

                          
        print(" ALIVE=%d " % Cell.aliveCount, end="")      
        print(" DEAD=%d " % Cell.deadCount, end="")
        print(" AGE="+str(nGenerationsAlive), end="")
        print(" CHECK: %.2f ms " % totalStatusTime, end="")
        print(" <=> EPOCH: %.2f ms " % epochEnd, end="\r\r")   
        
         
    #draw Cells
    for key in Cell.allCellsMap.keys():
        cell=Cell.allCellsMap[key]
        if(cell.alive):                 
            pygame.draw.rect(screen,cell.color,(cell.posX, cell.posY, Cell.size, Cell.size))
        #else:
            #pygame.draw.rect(screen,(255,255,255),(cell.posX, cell.posY, Cell.size, Cell.size))
        
            
    #draw player spawning cells       
    ###draw.rect will not draw alpha .. so :
    if(not movingMode):
        for showDrawingRect in mouseDrawingPositions:  
            s = pygame.Surface((Cell.size,Cell.size))  # size of rect
            s.set_alpha(50)                # alpha level
            s.fill((255,255,255))           # fills entire surface
            screen.blit(s, (showDrawingRect[0],showDrawingRect[1]))
    
    
    #events
    for event in pygame.event.get():
    
        if(event.type == pygame.QUIT):
             pygame.display.quit()
             pygame.quit()
             sys.exit()
        
        if(event.type == pygame.MOUSEBUTTONDOWN):
            if(not movingMode):
                drawing=True
            else:            
                moveView(mouseDrawingPositions)
                mouseDrawingPositions.clear()
        
        if(event.type == pygame.MOUSEBUTTONUP):
            drawing=False
            
            
            
         
        if(event.type == pygame.MOUSEMOTION):
            mousePos= (pygame.mouse.get_pos()[0]- (pygame.mouse.get_pos()[0]%Cell.size)  ,  pygame.mouse.get_pos()[1]- (pygame.mouse.get_pos()[1]%Cell.size)    )               
            if(drawing or movingMode):
                if(mousePos not in mouseDrawingPositions):
                    mouseDrawingPositions.append(mousePos)          
       
        if(event.type == pygame.KEYDOWN):
             
            if(event.key == pygame.K_z):         ###zoom
                zoomingMode = not zoomingMode
                mouseDrawingPositions.clear()
                
            if(event.key == pygame.K_m):
                movingMode=not movingMode
                mouseDrawingPositions.clear()
                
                          
            if(zoomingMode):
                if(event.key == pygame.K_KP_PLUS):
                    zoom(Cell.size+1, mousePos[0], mousePos[1])
                    mouseDrawingPositions.clear()
                                     
                if(event.key == pygame.K_KP_MINUS):
                    zoom(Cell.size-1, mousePos[0], mousePos[1])
                    mouseDrawingPositions.clear()                    
                   
                      
            else:  #gameSpeed
        
                if(event.key == pygame.K_KP_PLUS):
                    if(epochTime >= EPOCH_TIME_MIN-epochIncrement):
                        print("\nEpochTime: "+str(epochTime)+"ms")
                        epochTime -= epochIncrement
                        
                if(event.key == pygame.K_KP_MINUS):            
                    if(epochTime <= EPOCH_TIME_MAX+epochIncrement):
                        print("\nEpochTime: "+str(epochTime)+"ms")
                        epochTime += epochIncrement
                        
                        
            if(event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                playerSpawns=True
                
            if(event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE or event.key == pygame.K_CLEAR  ):
                if(len(mouseDrawingPositions)>0):
                    mouseDrawingPositions.pop()
                    
    pygame.display.update()     
    pygame.time.delay(delay)
      
    currentTime+=delay
    
    
    
    
    
    
        
        
        
        
        
        
        
        