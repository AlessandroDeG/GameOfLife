import multiprocessing
from multiprocessing import Queue,Process
import time

class Printer:
   def __init__(self, name):
      print("HELLO from "+name)

      
class Multiplier:
    def __init__(self, n,m):
        self.result=n*m
        
      


class Processor(multiprocessing.Process):
    def __init__(self, queue, idx):
        super(Processor, self).__init__()
        self.queue = queue
        self.idx = idx
        
    
    def run(self):
        result=0
        for i in range(0,10000000):
            result+= Multiplier(i,self.idx).result
        self.queue.put(result)
            
 
#print("whatdefuk"+__name__)

if __name__ == '__main__':  
    
 #####################################      
    NUMBER_OF_PROCESSES = 24

    ## Create a list to hold running Processor object instances...
    processes = list()
                
    q = Queue()  # Build a single queue to send to all process objects
    
    start = time.time() 
    
    for i in range(0, NUMBER_OF_PROCESSES):
            p=Processor(queue=q, idx=i)
            p.start()
            processes.append(p)            

                
                
    [proc.join() for proc in processes]
    print("ALL PROC TERMINATED")
    pResult4=0
    while not q.empty():
        pResult4+= q.get()
    
    endProc4 = time.time()-start    
    #######################################
    NUMBER_OF_PROCESSES = 8

    ## Create a list to hold running Processor object instances...
    processes = list()
                
    q = Queue()  # Build a single queue to send to all process objects
    
    start = time.time() 
    
    for i in range(0, NUMBER_OF_PROCESSES):
            p=Processor(queue=q, idx=i)
            p.start()
            processes.append(p)            

                
                
    [proc.join() for proc in processes]
    print("ALL PROC TERMINATED")
    pResult8=0
    while not q.empty():
        pResult8+= q.get()
    
    endProc8 = time.time()-start
    
    
    
    
    
    
    
    ######################################
    start = time.time() 
     
    mResult8=0 
    for i in range(0, NUMBER_OF_PROCESSES):
        for j in range(0,10000000):
            #Printer(str(i))
            mResult8+=Multiplier(i,j).result
     
        
    endMain8 = time.time()-start 
    
    print("tP4=" + str(endProc4*1000))
    print("P4 result =" + str(pResult4))
    print("tP8=" + str(endProc8*1000))
    print("P8 result =" + str(pResult8))
    print("tM8=" + str(endMain8*1000))
    print("M8 result =" + str(mResult8))
    print("tM8/tp8  "+ str((endMain8/endProc8)))   
    
    class X:
        def __init__(self):    
            self.x=0  
    
    def sum(ox):
        ox.x+=1
        return ox.x
    
    ox=X()
    sum(ox)
    print(ox.x)
    
    
    
    
    
    
        
        
    