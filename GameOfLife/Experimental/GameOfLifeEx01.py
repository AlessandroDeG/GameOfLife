
import random

"""
import pycuda.driver as cuda
import pycuda.autoinit
from pycuda.compiler import SourceModule
import pygame
import random
import os.path
import inspect
import threading
import time
import sys
"""

#from numba import njit, prange

import multiprocessing 
from multiprocessing import Queue,Process


########################### RULES ##################################################################
# 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.             #
# 2. Any live cell with two or three live neighbours lives on to the next generation.              #
# 3. Any live cell with more than three live neighbours dies, as if by overpopulation.             #
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.  #
####################################################################################################


####################################################################################################
class Cell:
   
    allCellsMap={}    #(x,y) ->self
    size=10   #zoom
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
    
    #@njit(parallel=True)    
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
        
#########################MULTIPROCESSING

class Processor(multiprocessing.Process):
    def __init__(self, queue, allCellsMap, cell):
        super(Processor, self).__init__()
        self.queue = queue
        self.allCellsMap=allCellsMap
        self.cell=cell
        
    def exists(self, x , y):
       
        existence={"exist" : False,
                   "alive" : False,
                   "self" : None                   
                   }
              
        if (x,y) in self.allCellsMap.keys():     
            existence["exist"] = True
            existence["alive"]=self.allCellsMap[(x,y)].alive
            existence["self"]= self.allCellsMap[x,y]
                   
        return existence
    
    def run(self):
        aliveNumber=0
        newCells=[]
        for dx in range(-Cell.ADJACENCY_DISTANCE*Cell.size, (Cell.ADJACENCY_DISTANCE+1)*Cell.size, Cell.size):
            for dy in range(-Cell.ADJACENCY_DISTANCE*Cell.size, (Cell.ADJACENCY_DISTANCE+1)*Cell.size, Cell.size):
               
                if(dx != 0 or dy!=0):
                    exist = self.exists(self.cell.posX+dx,self.cell.posY+dy)
                                     
                    if(self.cell.alive and not exist["exist"]):  #adj cell not exist (and is alive or not alive)
                        newCells.append(Cell(self.cell.posX+dx,self.cell.posY+dy,False))  
                                               
                    if(exist["exist"] and exist["alive"]):  #adj exist and is alive                         
                        aliveNumber+=1 
        
        self.queue.put(((self.cell.posX,self.cell.posY),aliveNumber,newCells))
    
    
    
   
        
    
        
        
#################################  ONLY FOR MAIN PROCESS  #####################
if __name__ == '__main__':     
                 
    ##############################################################ZOOM
    def zoom0(newSize, focusX, focusY):
        if(newSize>0 and newSize<=15):
            print("NEWSIZE: "+str(newSize))
                
            newMap = {}  ###preallocate size = Cell.allCellsMap size ???

            for key in Cell.allCellsMap.keys():
                cell=Cell.allCellsMap[key]
               
                
                cell.posX= (cell.posX//Cell.size)*newSize +((focusX)//Cell.size)*newSize        
                cell.posY= (cell.posY//Cell.size)*newSize +((focusY)//Cell.size)*newSize
           
            
                newMap[cell.posX,cell.posY]= cell  #remap (x,y)->cell
                
            Cell.allCellsMap=newMap
            
            Cell.size= newSize


    def zoom(newSize, a , b):
        if(newSize>0 and newSize<=15):
            print("NEWSIZE: "+str(newSize))
                
            newMap = {}  ###preallocate size = Cell.allCellsMap size ???

            for key in Cell.allCellsMap.keys():
                cell=Cell.allCellsMap[key]
               
                cell.posX= (cell.posX//Cell.size)*newSize 
                cell.posY= (cell.posY//Cell.size)*newSize
            
                newMap[cell.posX,cell.posY]= cell  #remap (x,y)->cell
                
            Cell.allCellsMap=newMap
            
            Cell.size= newSize
        







    ############################################################à

    print("Number of processors: ", multiprocessing.cpu_count())
    
    
    import pygame
    import random
    import os.path
    import inspect
    import threading
    import time
    import sys


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
    EPOCH_TIME_MAX=1000
    delay=1

    screen = pygame.display.set_mode((screenSizeX, screenSizeY), 0)
    WHITE = (255,255,255)
    mouseDrawingPositions=[]

    playerSpawns=False

    zoomingMode=False
    #playerZoom=False

    drawing = False

    epochCounter=0

    maxExecTime =0

    mousePos=0

        
    while(True):
                    
        screen.fill(0)
        
        #if(playerZoom):
            
        
        
        
        
        epochStart = time.time()
        if(currentTime>=epochTime):
            
            currentTime=0
            #print("*** EPOCH:"+str(epochCounter)+" ***   ", end="")
            epochCounter+=1
            
            Cell.CURRENT_EPOCH_COLOR=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
            
            #player spawning   
            if(playerSpawns):
                for position in mouseDrawingPositions: 
                    exist = Cell.exist(position[0],position[1])
                    if(exist["exist"] and not exist["alive"]):
                        exist["self"].delete()
                    exist = Cell.exist(position[0],position[1])                    
                    if(not(exist["alive"])):
                        Cell(position[0],position[1],True)
                    
                        
                mouseDrawingPositions.clear()
                playerSpawns=False
        
        
            flippingCells = []
            uselessCells = []
            
            totalStatusTime=0
            
            #
              #####################################      
            #NUMBER_OF_PROCESSES = 16

            ## Create a list to hold running Processor object instances...
            processes = list()
                        
            q = Queue()  # Build a single queue to send to all process objects
        
        
            ############
           
            for key in list(Cell.allCellsMap.keys()):
                cell=Cell.allCellsMap[key]

                p=Processor(queue=q,allCellsMap=Cell.allCellsMap, cell=cell)
                p.start()
                processes.append(p)            

                            
                            
            [proc.join() for proc in processes]
            print("ALL PROC TERMINATED")
             
            # queue.put(((cell.x,cell.y),aliveNumber,newCells))
            start = time.time()
            
            newCellsList=[]
            
            while not q.empty():
                (key,aliveNumber,newCells) = q.get()
                Cell.allCellsMap[key].status=aliveNumber
                newCellsList.extend(newCells)
                
            for cell in newCellsList:
                if(not (Cell.exist(cell.posX,cell.posY)["exist"])):
                    Cell.allCellsMap[cell.posX,cell.posY]=cell
                    
            q1 = Queue()
            processes = list()
            for cell in newCellsList:                                        
                    p=Processor(queue=q1,allCellsMap=Cell.allCellsMap, cell=cell)
                    p.start()
                    processes.append(p) 
            
            [proc.join() for proc in processes]
            print("ALL PROC TERMINATED")
            
            while not q1.empty():
                (key,aliveNumber,newCells) = q1.get()
                Cell.allCellsMap[key].status=aliveNumber
                    
                
                
                
                
                
            #####################################################
            end = (time.time() - start)*1000
            totalStatusTime+=end
              
            for key in (Cell.allCellsMap.keys()):
                cell=Cell.allCellsMap[key] 
                ##alive->dead            
                if(cell.alive and (cell.status<2 or cell.status>3)):
                    cell.alive=False
                    Cell.aliveCount-=1
                    Cell.deadCount+=1
            
                ##dead->alive
                elif((not cell.alive) and cell.status==3):
                    cell.alive=True
                    Cell.aliveCount+=1
                    Cell.deadCount-=1
               
                
                #dead->useless        
                elif((not cell.alive) and cell.status==0):
                    Cell.deadCount-=1
                    uselessCells.append(cell)
                         
                         
             #useless-->cancelled
            for useless in uselessCells:
                useless.delete()       
                    
            uselessCells.clear()
           
                 
            epochEnd = (time.time() - epochStart)*1000  

            print(" CHECK: %.2f ms " % totalStatusTime, end="")       
            print(" = EPOCH: %.2f ms " % epochEnd, end="")       
            print(" ALIVE: %d " % Cell.aliveCount, end="")      
            print(" DEAD: %d" % Cell.deadCount, end="\r")
            
             
        #draw Cells
        for key in Cell.allCellsMap.keys():
            cell=Cell.allCellsMap[key]
            if(cell.alive):                 
                pygame.draw.rect(screen,cell.color,(cell.posX, cell.posY, Cell.size, Cell.size))
            
                
        #draw player spawning cells       
        ###draw.rect will not draw alpha .. so :
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
                drawing=True
            
            if(event.type == pygame.MOUSEBUTTONUP):
                drawing=False  
             
            if(event.type == pygame.MOUSEMOTION and drawing):
                mousePos= (pygame.mouse.get_pos()[0]- (pygame.mouse.get_pos()[0]%Cell.size)  ,  pygame.mouse.get_pos()[1]- (pygame.mouse.get_pos()[1]%Cell.size)    )     
                if(mousePos not in mouseDrawingPositions):
                    mouseDrawingPositions.append(mousePos)          
           
            if(event.type == pygame.KEYDOWN):
                
                if(event.key == pygame.K_z): 
                    zoomingMode = not zoomingMode
            
                          
                if(zoomingMode):
                    if(event.key == pygame.K_KP_PLUS):
                        zoom(Cell.size+1, mousePos[0], mousePos[1])
                                         
                    if(event.key == pygame.K_KP_MINUS):
                        zoom(Cell.size-1, mousePos[0], mousePos[1])                
                       
                          
                else:  #gameSpeed
                          
                    if(event.key == pygame.K_KP_PLUS):
                        if(epochTime >= EPOCH_TIME_MIN-epochIncrement):
                            print("\nEpochTime: "+str(epochTime))
                            epochTime -= epochIncrement
                            
                    if(event.key == pygame.K_KP_MINUS):            
                        if(epochTime <= EPOCH_TIME_MAX+epochIncrement):
                            print("\nEpochTime: "+str(epochTime))
                            epochTime += epochIncrement
                    



                
                if(event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN):
                    playerSpawns=True
                    
                if(event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE or event.key == pygame.K_CLEAR  ):
                    if(len(mouseDrawingPositions)>0):
                        mouseDrawingPositions.pop()
                        
                
                        
        pygame.display.update()     
        pygame.time.delay(delay)
          
        currentTime+=delay
        
        
    
    
    
    
        
        
        
        
        
        
        
        