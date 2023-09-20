import pygame
import random
import os.path
import inspect
import threading
import time
import sys





########################### RULES ##################################################################
# 1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.             #
# 2. Any live cell with two or three live neighbours lives on to the next generation.              #
# 3. Any live cell with more than three live neighbours dies, as if by overpopulation.             #
# 4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.  #
####################################################################################################


####################################################################################################
class Cell:
    #allCellsList=[] turned into hasmap
    allCellsMap={}    #(x,y) ->self
    #allCellsList=[]   #self
    size=5    #zoom
    scale=1   #for later use in zooming.. maybe
    
    ADJACENCY_DISTANCE=3  #maybe increment it for fun  ,   = cell field of view
    
    aliveCount=0
    deadCount=0
    
    CURRENT_EPOCH_COLOR=(random.randint(0,255),random.randint(0,255),random.randint(0,255))
    
    def __init__(self, posX, posY, alive):
              
        self.alive=alive
        
        self.posX=posX
        self.posY=posY
        
        Cell.allCellsMap[(self.posX,self.posY)]= self
        #Cell.allCellsList.append(self)
              
        self.color = Cell.CURRENT_EPOCH_COLOR
        
        if(self.alive):
            Cell.aliveCount+=1
        else:
            Cell.deadCount+=1
            
        self.status=0  #number of alive neighbours
       
        self.checkStatus()
        
        
    def delete(self):
        #Cell.allCellsList.remove(self)
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
           
    @classmethod    
    def spawn(Cell, x , y, alive):
        newCell = Cell(x,y, alive)
        return newCell
        
        
    def checkStatus(self):
       
        aliveNumber=0
        for dx in range(-Cell.ADJACENCY_DISTANCE*Cell.size, (Cell.ADJACENCY_DISTANCE+1)*Cell.size, Cell.size):
            for dy in range(-Cell.ADJACENCY_DISTANCE*Cell.size, (Cell.ADJACENCY_DISTANCE+1)*Cell.size, Cell.size):
               
                if(dx != 0 or dy!=0):
                    exist = Cell.exist(self.posX+dx,self.posY+dy)
                                     
                    if(self.alive and not exist["exist"]):  #adj cell not exist (and is alive or not alive)
                        Cell.spawn(self.posX+dx,self.posY+dy, False)  
                                               
                    if(exist["exist"] and exist["alive"]):  #adj exist and is alive                         
                        aliveNumber+=1 
        
        #if(aliveNumber==2):                 
        #print("ALIVE!")
        self.status=aliveNumber
                
              
    
        
        
   
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
EPOCH_TIME_MAX=1000
delay=15

screen = pygame.display.set_mode((screenSizeX, screenSizeY), 0)
WHITE = (255,255,255)
mouseDrawingPositions=[]

playerSpawns=False
drawing = False



epochCounter=0

maxExecTime =0

    
while(True):
    
            
    screen.fill(0)
    
    epochStart = time.time()
    if(currentTime>=epochTime):
        
        currentTime=0
        print("*** EPOCH:"+str(epochCounter)+" ***   ", end="")
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
    
    
        #gameEvents
        
        flippingCells = []
        uselessCells = []
        
        totalStatusTime=0
        #print(Cell.allCellsList)
        
        #print("\n**DEAD BEFORE: "+str( Cell.deadCount)+"****")
        for key in list(Cell.allCellsMap.keys()):
            cell=Cell.allCellsMap[key]
            #print(Cell.deadCount)
            start = time.time()
            cell.checkStatus()
            end = (time.time() - start)*1000
            totalStatusTime+=end
        #print("**DEAD AFTER: "+str( Cell.deadCount)+"****")   
            
        
        #for key in Cell.allCellsMap:
            #cell=Cell.allCellsMap[key]    
            #alive --> dead   
            #if(status["alive"] and (status["aliveNumber"]<2 or status["aliveNumber"]>3)):
            if(cell.alive and (cell.status<2 or cell.status>3)):
                #print(str(status["aliveNumber"])+":  <2 or >3 : alive ->dead")
                #flippingCells.append(cell)
                cell.alive=False
                Cell.aliveCount-=1
                Cell.deadCount+=1
        
            ##dead->alive
            elif((not cell.alive) and cell.status==3):
                #print(str(status["aliveNumber"])+"==3 : dead ->alive")
                #flippingCells.append(cell)
                cell.alive=True
                Cell.aliveCount+=1
                Cell.deadCount-=1
           
            
            #dead->useless        
            elif((not cell.alive) and cell.status==0):
                #print(str(status["aliveNumber"])+"==0 : dead ->useless")
                Cell.deadCount-=1
                uselessCells.append(cell)
                     
        #startFlipTime = time.time()     
        #for flipping in flippingCells:
            #print("FLIP"+str(flipping.alive))
            #flipping.alive= (not flipping.alive)
            #print("FLIP"+str(flipping.alive))
        #endFlipping = (time.time() - startFlipTime)*1000
        
        #lf=len(flippingCells)
        
        
        
         #useless-->cancelled
        startGarbage=time.time()
        for useless in uselessCells:
            useless.delete()       
        endGarbage = (time.time() - startGarbage)*1000
        
        #startClear=time.time()
        uselessCells.clear()
        #flippingCells.clear()
        #endClear = (time.time() - startClear)*1000
             
        epochEnd = (time.time() - epochStart)*1000  

        print(" CHECK: %.2f ms " % totalStatusTime, end="")       
        
        #print("+ GARB: %.2f ms " % endGarbage, end="") 
        
        #print("+ CLEAR: %.2f ms " % endClear, end="")        
          
        print(" = EPOCH: %.2f ms " % epochEnd, end="")
        
        print(" ALIVE: %d " % Cell.aliveCount, end="")
        
        print(" DEAD: %d" % Cell.deadCount, end="\r")
        
        #print(" FLIP: %d" % lf, end="\r")
        
        
        
   
    #draw
    for key in Cell.allCellsMap.keys():
        cell=Cell.allCellsMap[key]
        if(cell.alive):       
            #print("ALIVE: "+str(cell)+" posX="+str(cell.posX)+"posY"+str(cell.posY))
            pygame.draw.rect(screen,cell.color,(cell.posX, cell.posY, Cell.size, Cell.size))
        #else:
            #pygame.draw.rect(screen,cell.color,(cell.posX, cell.posY, Cell.size, Cell.size))
            
        
    
    
    
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
                #print(mousePos)
        
        if(event.type == pygame.KEYDOWN):
        
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
                
    
    #pygame.display.flip()     
    pygame.display.update()     
    pygame.time.delay(delay)
    
    
    currentTime+=delay
    
    
    
    
    
    
        
        
        
        
        
        
        
        