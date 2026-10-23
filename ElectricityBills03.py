#  setup hardcoded credentials

USER_DATABASE={
 "abc" : "123",
 "you" : "1234"
}

#CORRECT_USERNAME  =  "abc"
#CORRECT_PASSWORD  =  "123"

print("--- System Login---")
username = input("Enter username:")
password = input("Enter password:")

if username in USER_DATABASE and USER_DATABASE [username] == password :
#if username == CORRECT_USERNAME and password == CORRECT_PASSWORD :
    print("\nLogin successful!\n")
    print("---  Electricity Bill Calculator---")
  
    units = int(input(" Enter Your Units Consumed:"))
    # check conditions based on units
    if units <0 :

        print("Invalid  units etered.")
    else:
        slab1_units,bill1_amount = 0,0
        slab2_units,bill2_amount = 0,0
        slab3_units,bill3_amount = 0,0
        
        # Slab -1: first 100 units at Rs. 5 per unit
        if units <=100:
            slab1_units = units
            bill1_amount = slab1_units *5

            
        #Slab-2: next 100 units at  Rs 7  per  unit  
        elif units <=200 :
              slab1_units = 100
              slab2_units  = units -100

              bill1_amount = slab1_units*5
              bill2_amount = slab2_units*7  

        # slab-3 :  Above 200 units at Rs.10 per unit
        else:
           slab1_units = 100
           slab2_units = 100
           slab3_units = units -200
            
           bill1_amount = slab1_units *5
           bill2_amount = slab2_units *7 
           bill3_amount = slab3_units *10
        total_bill_amount  = bill1_amount + bill2_amount + bill3_amount
        print("\n --- Detailed Electricity Bills Breakdown--- ")
        print(f" slab-1(First 100 units @ Rs. 5):{slab1_units} Units, Rs.{bill1_amount:.2f}")
        print(f" slab-2(Next 100 units @ Rs. 7):{slab2_units} Units, Rs.{bill2_amount:.2f}")
        print(f" slab-3(Above 200units @ Rs. 10):{slab3_units} Units, Rs.{bill3_amount:.2f}")
        print(f" Total Electricity units consumed  : {units} Units")
        print(f" Total Electricity bills Rs.{total_bill_amount:.2f}")     
    
else :
    print("\n Acceess Denied : Incorrect username or password.") 
  