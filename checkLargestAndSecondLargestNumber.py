largest  =float('-inf')
second_largest = float ('-inf')

print("Enter one by one, type 'stop' to finish")

while True:
    user_input = input("Enter a Number :")
    if user_input.lower()  ==  'stop':
        break
    num = int(user_input)  
    if num >largest :
        second_largest = largest
        largest  = num
    elif num > second_largest and num!= largest:
        second_largest= num
print(f"Largest : {largest}")   
print(f"Second_Largest:{second_largest}")     
    