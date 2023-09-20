








import multiprocessing
from multiprocessing import Queue,Process
import time

class Printer:
   def __init__(self, name):
      print("HELLO from "+name)

      
class Multiplier:
    resultList={}  #NOT SHARED 
    def __init__(self, key , n, m, map):
        Multiplier.resultList[key]+=1
        
        if(not key in map.keys()):
            map[key]=0
        map[key]+=n*m
        
      


class Processor(multiprocessing.Process):
    def __init__(self, queue, idx, map):
        super(Processor, self).__init__()
        self.queue = queue
        self.idx = idx
        self.map=map
        
    
    def run(self):
   
        for i in range(0,1000):
            Multiplier(self.idx, i, i, self.map)
        #self.queue.put(result)
        print("idx"+str(self.map))
        print("mlist"+str(multiplierResultList[key]))
        
        
        
if __name__ == '__main__':  
    
 #####################################      
    NUMBER_OF_PROCESSES = 2

    ## Create a list to hold running Processor object instances...
    processes = list()
                
    q = Queue()  # Build a single queue to send to all process objects
    
    start = time.time() 
    
    Multiplier.resultList={0,0,1,0}
    
    bo={}
    
    for i in range(0, NUMBER_OF_PROCESSES):
            p=Processor(queue=q, idx=i, map = bo)
            p.start()
            processes.append(p)            

                
                
    [proc.join() for proc in processes]
    print("ALL PROC TERMINATED")
    #pResult4=0
    #hile not q.empty():
        #pResult4+= q.get()
    print(Multiplier.resultList)
    
x=0  
def sum(x):
    return x+1
    
sum(x)
print(x)