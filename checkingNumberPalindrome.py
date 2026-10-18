
def check_palidrome(original_num):
    sign= -1 if original_num <0 else 1
        #return False
    #num  = abs(num)
    num  = abs(original_num)
    reversed_num = 0
    
    while num >0 :
        #  Grab  the last  digit
       remainder = num % 10

        # Build the  new  number
       reversed_num = (reversed_num * 10)  + remainder
        # shrink  the  Original  
       num  = num //10 
    
    return original_num,reversed_num*sign,original_num == reversed_num
aa = int(input("Enter Number:"))
print ("Original_num,Reversed_num,Checking palidrome respectfully:",(check_palidrome(aa)))
#aa = int(input())
#print (check_palidrome(aa))