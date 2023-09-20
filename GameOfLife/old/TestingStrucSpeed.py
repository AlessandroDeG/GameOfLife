####test dict performance
import time
import random


        
        
        
def existH1(hashMap,x,y):
    try:
        hashMap[x,y]
        return True
    except:
        return False
        

def existH2(hashMap,x,y):
    if (x,y) in hashMap:      
        return True
    else:
        return False
        
        
def existH3(hashMap,x,y):
    if (x,y) in hashMap.keys():     
        return True
    else:
        return False
  
"""
  start = time.time()
  
  end = time.time()-start
  print(""+str(end))
  
"""






n=100000
hashMap = {}
list = []       #actually a dynamic array of pointers


##########sillyArrow###########
sillyArrow=False
    
size=n*n                         
if(size>=100):
    sillyArrow=True
        
if(sillyArrow):
      
    percent= size//100
    rest = size%100
    arrow=[]
    for t in range(0,100):
        arrow.append("-")
    i=0
    ##########################


##all keys 
totalfilling=0
for x in range(0,n):
    for y in range(0,n):
        start = time.time()
        hashMap[(x,y)]=(x,y)
        totalfilling += time.time()-start
        
    ###silly arrow :D
        if(sillyArrow):
        
            if(i%percent==0 and not (size-i <= rest)):
                if(i//percent != 0 ):    arrow[(i//percent)-1]="-"
                arrow[i//percent]=">"
                print(str(i//percent)+"%" , end = "")
                for s in arrow:
                    print(s, end=""), 
                print("100%\r", end=""), 
            i+=1
        
       
print("")       
print("filled hashmap, size : "+str(n)  +  "time : "+ str(totalfilling))
        
#random access
totalH1 = 0
totalH2 = 0
totalH3 = 0

##########sillyArrow###########
sillyArrow=False

print("")
    
size=n                           
if(size>=100):
    sillyArrow=True
        
if(sillyArrow):
      
    percent= size//100
    rest = size%100
    arrow=[]
    for t in range(0,100):
        arrow.append("-")
    i=0
    ##########################

for i in range(0,n):
    
 
    randomT= (random.randint(0,n),random.randint(0,n))
    
    start = time.time()
    exist = existH1(randomT[0],randomT[1],hashMap)
    totalH1 += time.time()-start
    
    start = time.time()
    exist = existH1(randomT[0],randomT[1],hashMap)
    totalH2 += time.time()-start
    
    start = time.time()
    exist = existH1(randomT[0],randomT[1],hashMap)
    totalH3 += time.time()-start
    
    
    ###silly arrow :D
    if(sillyArrow):
        
        if(i%percent==0 and not (size-i <= rest)):
            if(i//percent != 0 ):    arrow[(i//percent)-1]="-"
            arrow[i//percent]=">"
            print(str(i//percent)+"%" , end = "")
            for s in arrow:
                print(s, end=""), 
            print("100%\r", end=""), 
        #i+=1

                
    

print("H1: "+str(totalH1*1000))
print("H2: "+str(totalH2*1000))
print("H3: "+str(totalH3*1000))
        

 
    

            
 

"""
for x in range(0,n)
    for y in range(0,n)
        list.append=(x,y)
"""





        