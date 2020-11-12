  
def f(x):
    
    return x**2
def ducu(x):
    
    print("hello ducu")
    print("hello can")
def vector(x):
    
    return "hello vector"
def foo(x,y,z):
    
    print(5+3)
    
    print(7**2)
    print("ERRORRRRR")
    return x**y**z

def fibonacci5(x):
    

    if x<=1:
        
        return x
    return fibonacci5(x-1)+ fibonacci5(x-2)
  
def bubble(x):
    
    l = [i for i in range(x,0,-1)]
    for p in range(len(l)-1):
        for i in range(len(l)-1):
            for j in range(len(l)-1):
                if l[j]>l[j+1]:
                    temp = l[j]
                    l[j]=l[j+1]
                    l[j+1]=temp
    return l
def factorial(x):
  global factorial
  if x<=1:
    return 1
  return factorial(x-1)*x

