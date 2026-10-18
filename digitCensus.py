# digitCensus.py

def digit_census(n):
    if n == 0:
        print("Digit 0 occurs:1 time(s)")
        return
    if n <0:
         n=-n   
        
    counts =[0,0,0,0,0,0,0,0,0,0]
    while n>0:
        dd= n%10
        counts[dd] +=1
        n =n//10   
    i = 0
    while i<10:
        if counts[i]>0:
            print("Digit",i,":",counts[i])
        i  +=1
print("Enter a Number : 3232 ")
digit_census(3232)        
