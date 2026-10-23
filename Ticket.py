#  setup hardcoded credentials
CORRECT_USERNAME  =  "abc"
CORRECT_PASSWORD  =  "123"


print("--- System Login---")
username = input("Enter username:")
password = input("Enter password:")

if username == CORRECT_USERNAME and password == CORRECT_PASSWORD :
    print("\nLogin successful!\n")
    print("---  Ticket Calculator---")
    base_price = float(input("Enter the base full ticket price:"))  
    age = int(input(" Enter Your age:"))
    #  check conditions based on age
    if age < 0 :

        print("Inalid age entered.")
    elif age <5 :
        final_price = 0.0
        print("Your Ticket is free.")
    elif age <=17 :
        final_price = base_price * 0.50
        print(f"Your Ticket is half :{final_price}")  
    elif age <=59 :
        final_price = base_price 
        print(f"Your Ticket  price is full price :{final_price}")
        
    # concession 10% on base_price for having age 60 or  more than 60 yrs  
    else:
        final_price = base_price * 0.90
        print(f"Your Ticket with  10% concession is :{final_price}")     
    
else :
    print("\n Acceess  Denied : Incorrect username or password.") 
    