# gcd.py
def get_greatestCommonDivider(a,b):
     #a,b=  abs(a),abs(b)
    if a<0:
        a  =-a
    if b<0:
        b=-b
       
    while b!=0: 
        rem = a%b
        a=b
        b=rem
    return  a 
print(get_greatestCommonDivider(8,12))
    